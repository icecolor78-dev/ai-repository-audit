from __future__ import annotations

import re
from pathlib import Path

import yaml

SHA_ACTION = re.compile(r"@[0-9a-f]{40}$")
UNTRUSTED_EXPR = re.compile(r"\$\{\{\s*github\.event\.(?:pull_request|issue|comment|head_commit)", re.I)
PR_HEAD_EXPR = re.compile(r"github\.event\.pull_request\.head\.(?:sha|ref|repo\.full_name)", re.I)
NEGATED_PUBLISH = re.compile(r"\b(?:do\s+not|don't|never|no)\s+(?:publish|upload|push)\b", re.I)
PUBLISH_COMMAND = re.compile(r"\b(?:npm\s+publish|twine\s+upload|docker\s+push|gh\s+release|cargo\s+publish|gem\s+push|mvn\s+deploy)\b", re.I)
PUBLISH_ACTION = re.compile(r"(?:publish|release|deploy)", re.I)


def signal(kind: str, locator: str, detail: str, confidence: str = "HIGH", severity: str = "INFO") -> dict:
    return {"kind": kind, "locator": locator, "detail": detail, "confidence": confidence, "severity": severity}


def _events(doc: dict) -> set[str]:
    value = doc.get("on", doc.get(True))
    if isinstance(value, str): return {value}
    if isinstance(value, list): return {str(item) for item in value}
    if isinstance(value, dict): return {str(item) for item in value}
    return set()


def _permission_rows(value) -> list[str]:
    if isinstance(value, str): return [value]
    if isinstance(value, dict): return [f"{key}:{val}" for key, val in sorted(value.items())]
    return []


def _uses_ref(locator: str, uses: str, security: list[dict], action_refs: list[str], kind: str) -> None:
    if uses.startswith("./"):
        return
    pinned = bool(SHA_ACTION.search(uses))
    action_refs.append(f"{locator}: {uses}" + (" [full-sha]" if pinned else " [mutable-ref-signal]"))
    if not pinned:
        security.append(signal(kind, locator, uses, "HIGH", "LOW"))


def analyze_workflows(root: Path) -> tuple[dict, dict, dict]:
    paths = sorted((root / ".github" / "workflows").glob("*.y*ml")) if (root / ".github" / "workflows").is_dir() else []
    names=[]; triggers=[]; filters=[]; matrices=[]; conditionals=[]; aggregates=[]; permissions=[]; action_refs=[]; security=[]; release_signals=[]; release_workflows=[]

    for path in paths:
        rp = path.relative_to(root).as_posix(); names.append(rp)
        try:
            doc = yaml.safe_load(path.read_text(encoding="utf-8", errors="replace")) or {}
        except yaml.YAMLError:
            security.append(signal("yaml_parse_error", rp, "workflow YAML could not be parsed", "HIGH", "INFO")); continue
        if not isinstance(doc, dict): continue
        events = _events(doc); triggers.extend(f"{rp}: {event}" for event in sorted(events))
        on_value = doc.get("on", doc.get(True))
        if isinstance(on_value, dict) and any(isinstance(c, dict) and ("paths" in c or "paths-ignore" in c) for c in on_value.values()): filters.append(f"{rp}: path filter present")
        privileged = "pull_request_target" in events
        if privileged: security.append(signal("privileged_pr_context", rp, "pull_request_target observed; event choice alone is not a vulnerability", "HIGH", "INFO"))

        workflow_permissions = _permission_rows(doc.get("permissions")); permissions.extend(f"{rp}: {row}" for row in workflow_permissions)
        if "write-all" in workflow_permissions: security.append(signal("broad_permissions", rp, "workflow declares write-all permissions", "HIGH", "HIGH"))

        jobs = doc.get("jobs", {}) if isinstance(doc.get("jobs", {}), dict) else {}
        workflow_release = "release" in events
        for job_name, job in jobs.items():
            if not isinstance(job, dict): continue
            locator_job = f"{rp}:{job_name}"
            if "if" in job:
                conditionals.append(f"{locator_job}: conditional job present")
                if str(job.get("if")).strip().casefold() in {"false", "${{ false }}"}:
                    security.append(signal("statically_skipped_job", locator_job, "job condition is statically false; green downstream aggregation may not imply this job ran", "HIGH", "MEDIUM"))
            if "needs" in job: aggregates.append(f"{locator_job}: dependency present")
            strategy = job.get("strategy")
            if isinstance(strategy, dict) and "matrix" in strategy: matrices.append(f"{locator_job}: matrix present")

            if "permissions" in job:
                job_permissions = _permission_rows(job.get("permissions"))
                effective_permissions = job_permissions
            else:
                job_permissions = []
                effective_permissions = workflow_permissions
            permissions.extend(f"{locator_job}: {row}" for row in job_permissions)
            if "write-all" in job_permissions: security.append(signal("broad_permissions", locator_job, "job declares write-all permissions", "HIGH", "HIGH"))
            if any(row == "id-token:write" for row in effective_permissions): release_signals.append(signal("oidc_permission", locator_job, "id-token:write permission observed; trusted publishing and publication remain unverified"))

            job_uses = job.get("uses")
            if isinstance(job_uses, str):
                _uses_ref(locator_job, job_uses, security, action_refs, "mutable_reusable_workflow_ref")
                if "secrets" in job:
                    detail = "reusable workflow receives secrets; effective exposure depends on called workflow and ref integrity"
                    if job.get("secrets") == "inherit": detail = "reusable workflow inherits caller secrets; inspect called workflow and ref integrity"
                    security.append(signal("reusable_workflow_secrets", locator_job, detail, "HIGH", "MEDIUM"))
                if PUBLISH_ACTION.search(job_uses): workflow_release = True
                continue

            steps = job.get("steps", [])
            if not isinstance(steps, list): continue
            for index, step in enumerate(steps, 1):
                if not isinstance(step, dict): continue
                locator=f"{locator_job}:step-{index}"
                if "if" in step: conditionals.append(f"{locator}: conditional step present")
                uses=step.get("uses")
                if isinstance(uses, str) and not uses.startswith("./"):
                    _uses_ref(locator, uses, security, action_refs, "mutable_action_ref")
                    if uses.startswith("actions/checkout@"):
                        with_data=step.get("with") if isinstance(step.get("with"), dict) else {}
                        persist=with_data.get("persist-credentials")
                        if persist is not False and str(persist).casefold() != "false": security.append(signal("checkout_credentials", locator, "checkout does not explicitly disable persisted credentials; effective risk depends on permissions and later steps", "HIGH", "INFO"))
                        ref_text=" ".join(str(with_data.get(key, "")) for key in ("ref", "repository"))
                        if privileged and PR_HEAD_EXPR.search(ref_text): security.append(signal("privileged_untrusted_checkout", locator, "pull_request_target checkout references pull-request head content; review whether untrusted code can execute with privileged context", "HIGH", "HIGH"))
                    if uses.startswith(("actions/upload-artifact@", "actions/download-artifact@")): release_signals.append(signal("artifact_handoff", locator, "artifact transfer observed; producer/consumer identity and release binding remain unverified"))
                    if PUBLISH_ACTION.search(uses): workflow_release = True
                run=step.get("run")
                if isinstance(run, str):
                    if UNTRUSTED_EXPR.search(run): security.append(signal("untrusted_expression_shell", locator, "event-derived expression appears in a shell script; review quoting and data flow", "HIGH", "HIGH"))
                    if "secrets." in run: security.append(signal("secret_reference", locator, "shell step references a secret; exposure is not inferred", "HIGH", "INFO"))
                    if not NEGATED_PUBLISH.search(run) and PUBLISH_COMMAND.search(run): workflow_release = True
                    if re.search(r"attest|provenance|sigstore|cosign|gpg|signing", run, re.I): release_signals.append(signal("signing_or_attestation", locator, "signing/attestation command signal observed", "MEDIUM"))
                    if re.search(r"smoke|verify|verification", run, re.I): release_signals.append(signal("release_verification", locator, "verification/smoke command signal observed", "MEDIUM"))
                    if re.search(r"rollback|revert|recovery", run, re.I): release_signals.append(signal("rollback_or_recovery", locator, "rollback/recovery command signal observed", "MEDIUM"))
        if workflow_release:
            release_workflows.append(rp); release_signals.append(signal("release_workflow", rp, "release event, publisher action, or recognized publication command observed", "HIGH"))

    confidence="PARTIAL" if names else "UNVERIFIED"
    ci={"workflows":names,"required_checks":[],"trigger_model":sorted(set(triggers)),"path_filters":sorted(set(filters)),"runtime_matrix":sorted(set(matrices)),"os_arch_matrix":[],"conditional_jobs":sorted(set(conditionals)),"aggregate_checks":sorted(set(aggregates)),"exact_subject_runs":[],"confidence":confidence,"unknowns":["actual jobs/steps, conclusions and required-check enforcement require exact-subject runtime evidence"],"pr_confidence":confidence,"main_confidence":confidence,"release_confidence":"UNVERIFIED","security_evidence_freshness":"UNVERIFIED"}
    security_section={"workflow_permissions":sorted(set(permissions)),"credential_persistence":[x for x in security if x["kind"]=="checkout_credentials"],"action_pinning":sorted(set(action_refs)),"static_analysis":[],"dependency_security":[],"secret_scanning_evidence":[],"freshness":[],"signals":security,"confidence":"PARTIAL" if security or permissions or action_refs else "UNVERIFIED","unknowns":["static workflow evidence does not prove exploitability, vulnerability absence, called-workflow behavior, or runtime enforcement"]}
    release_section={"workflows":sorted(set(release_workflows)),"artifact_handoffs":[x for x in release_signals if x["kind"]=="artifact_handoff"],"source_artifact_binding":[],"trusted_publishing":[],"signing_or_attestation":[x for x in release_signals if x["kind"]=="signing_or_attestation"],"smoke_or_release_tests":[x for x in release_signals if x["kind"]=="release_verification"],"rollback_or_recovery":[x for x in release_signals if x["kind"]=="rollback_or_recovery"],"signals":release_signals,"confidence":"PARTIAL" if release_signals else "UNVERIFIED","unknowns":["OIDC permission is not trusted-publisher proof; release execution and source/artifact provenance require external evidence"]}
    return ci, security_section, release_section
