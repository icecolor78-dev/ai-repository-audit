from __future__ import annotations

import re
from pathlib import Path

import yaml

SHA_ACTION = re.compile(r"@[0-9a-f]{40}$")
UNTRUSTED_EXPR = re.compile(r"\$\{\{\s*github\.event\.(?:pull_request|issue|comment|head_commit)", re.I)
PR_HEAD_EXPR = re.compile(r"github\.event\.pull_request\.head\.(?:sha|ref|repo\.full_name)", re.I)


def signal(kind: str, locator: str, detail: str, confidence: str = "HIGH", severity: str = "INFO") -> dict:
    return {"kind": kind, "locator": locator, "detail": detail, "confidence": confidence, "severity": severity}


def _events(doc: dict) -> set[str]:
    value = doc.get("on", doc.get(True))
    if isinstance(value, str):
        return {value}
    if isinstance(value, list):
        return {str(item) for item in value}
    if isinstance(value, dict):
        return {str(item) for item in value}
    return set()


def _permission_rows(value) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        return [f"{key}:{val}" for key, val in sorted(value.items())]
    return []


def analyze_workflows(root: Path) -> tuple[dict, dict, dict]:
    paths = sorted((root / ".github" / "workflows").glob("*.y*ml")) if (root / ".github" / "workflows").is_dir() else []
    names: list[str] = []
    triggers: list[str] = []
    filters: list[str] = []
    matrices: list[str] = []
    conditionals: list[str] = []
    aggregates: list[str] = []
    permissions: list[str] = []
    action_refs: list[str] = []
    security: list[dict] = []
    release_signals: list[dict] = []
    release_workflows: list[str] = []

    for path in paths:
        rp = path.relative_to(root).as_posix()
        names.append(rp)
        try:
            doc = yaml.safe_load(path.read_text(encoding="utf-8", errors="replace")) or {}
        except yaml.YAMLError:
            security.append(signal("yaml_parse_error", rp, "workflow YAML could not be parsed", "HIGH", "INFO"))
            continue
        if not isinstance(doc, dict):
            continue
        events = _events(doc)
        triggers.extend(f"{rp}: {event}" for event in sorted(events))
        on_value = doc.get("on", doc.get(True))
        if isinstance(on_value, dict) and any(
            isinstance(config, dict) and ("paths" in config or "paths-ignore" in config)
            for config in on_value.values()
        ):
            filters.append(f"{rp}: path filter present")

        privileged = "pull_request_target" in events
        if privileged:
            security.append(signal(
                "privileged_pr_context", rp,
                "pull_request_target observed; event choice alone is not a vulnerability",
                "HIGH", "INFO",
            ))

        workflow_permissions = _permission_rows(doc.get("permissions"))
        permissions.extend(f"{rp}: {row}" for row in workflow_permissions)
        if "write-all" in workflow_permissions:
            security.append(signal("broad_permissions", rp, "workflow declares write-all permissions", "HIGH", "HIGH"))

        jobs = doc.get("jobs", {})
        if not isinstance(jobs, dict):
            jobs = {}
        workflow_release = "release" in events
        for job_name, job in jobs.items():
            if not isinstance(job, dict):
                continue
            if "if" in job:
                conditionals.append(f"{rp}:{job_name}: conditional job present")
            if "needs" in job:
                aggregates.append(f"{rp}:{job_name}: dependency present")
            strategy = job.get("strategy")
            if isinstance(strategy, dict) and "matrix" in strategy:
                matrices.append(f"{rp}:{job_name}: matrix present")
            job_permissions = _permission_rows(job.get("permissions"))
            permissions.extend(f"{rp}:{job_name}: {row}" for row in job_permissions)
            if "write-all" in job_permissions:
                security.append(signal("broad_permissions", f"{rp}:{job_name}", "job declares write-all permissions", "HIGH", "HIGH"))
            effective_permissions = job_permissions or workflow_permissions
            if any(row == "id-token:write" for row in effective_permissions):
                release_signals.append(signal(
                    "oidc_permission", f"{rp}:{job_name}",
                    "id-token:write permission observed; trusted publishing and publication remain unverified",
                ))

            steps = job.get("steps", [])
            if not isinstance(steps, list):
                continue
            for index, step in enumerate(steps, 1):
                if not isinstance(step, dict):
                    continue
                locator = f"{rp}:{job_name}:step-{index}"
                if "if" in step:
                    conditionals.append(f"{locator}: conditional step present")
                uses = step.get("uses")
                if isinstance(uses, str) and not uses.startswith("./"):
                    pinned = bool(SHA_ACTION.search(uses))
                    action_refs.append(f"{locator}: {uses}" + (" [full-sha]" if pinned else " [mutable-ref-signal]"))
                    if not pinned:
                        security.append(signal("mutable_action_ref", locator, uses, "HIGH", "LOW"))
                    if uses.startswith("actions/checkout@"):
                        with_data = step.get("with") if isinstance(step.get("with"), dict) else {}
                        persist = with_data.get("persist-credentials")
                        if persist is not False and str(persist).casefold() != "false":
                            security.append(signal(
                                "checkout_credentials", locator,
                                "checkout does not explicitly disable persisted credentials; effective risk depends on permissions and later steps",
                                "HIGH", "INFO",
                            ))
                        ref_text = " ".join(str(with_data.get(key, "")) for key in ("ref", "repository"))
                        if privileged and PR_HEAD_EXPR.search(ref_text):
                            security.append(signal(
                                "privileged_untrusted_checkout", locator,
                                "pull_request_target checkout references pull-request head content; review whether untrusted code can execute with privileged context",
                                "HIGH", "HIGH",
                            ))
                    if uses.startswith(("actions/upload-artifact@", "actions/download-artifact@")):
                        release_signals.append(signal(
                            "artifact_handoff", locator,
                            "artifact transfer observed; producer/consumer identity and release binding remain unverified",
                        ))
                run = step.get("run")
                if isinstance(run, str):
                    if UNTRUSTED_EXPR.search(run):
                        security.append(signal(
                            "untrusted_expression_shell", locator,
                            "event-derived expression appears in a shell script; review quoting and data flow",
                            "HIGH", "HIGH",
                        ))
                    if "secrets." in run:
                        security.append(signal("secret_reference", locator, "shell step references a secret; exposure is not inferred", "HIGH", "INFO"))
                    if re.search(r"\b(?:publish|upload|push)\b", run, re.I):
                        workflow_release = True
                    if re.search(r"attest|provenance|sigstore|cosign|gpg|signing", run, re.I):
                        release_signals.append(signal("signing_or_attestation", locator, "signing/attestation command signal observed", "MEDIUM"))
                    if re.search(r"smoke|verify|verification", run, re.I):
                        release_signals.append(signal("release_verification", locator, "verification/smoke command signal observed", "MEDIUM"))
                    if re.search(r"rollback|revert|recovery", run, re.I):
                        release_signals.append(signal("rollback_or_recovery", locator, "rollback/recovery command signal observed", "MEDIUM"))
        if workflow_release:
            release_workflows.append(rp)
            release_signals.append(signal("release_workflow", rp, "release event or publication command observed", "HIGH"))

    confidence = "PARTIAL" if names else "UNVERIFIED"
    ci = {
        "workflows": names, "required_checks": [], "trigger_model": sorted(set(triggers)),
        "path_filters": sorted(set(filters)), "runtime_matrix": sorted(set(matrices)), "os_arch_matrix": [],
        "conditional_jobs": sorted(set(conditionals)), "aggregate_checks": sorted(set(aggregates)), "exact_subject_runs": [],
        "confidence": confidence, "unknowns": ["actual jobs/steps, conclusions and required-check enforcement require exact-subject runtime evidence"],
        "pr_confidence": confidence, "main_confidence": confidence, "release_confidence": "UNVERIFIED", "security_evidence_freshness": "UNVERIFIED",
    }
    security_section = {
        "workflow_permissions": sorted(set(permissions)),
        "credential_persistence": [item for item in security if item["kind"] == "checkout_credentials"],
        "action_pinning": sorted(set(action_refs)), "static_analysis": [], "dependency_security": [],
        "secret_scanning_evidence": [], "freshness": [], "signals": security,
        "confidence": "PARTIAL" if security or permissions or action_refs else "UNVERIFIED",
        "unknowns": ["static workflow evidence does not prove exploitability or vulnerability absence"],
    }
    release_section = {
        "workflows": sorted(set(release_workflows)),
        "artifact_handoffs": [item for item in release_signals if item["kind"] == "artifact_handoff"],
        "source_artifact_binding": [], "trusted_publishing": [],
        "signing_or_attestation": [item for item in release_signals if item["kind"] == "signing_or_attestation"],
        "smoke_or_release_tests": [item for item in release_signals if item["kind"] == "release_verification"],
        "rollback_or_recovery": [item for item in release_signals if item["kind"] == "rollback_or_recovery"],
        "signals": release_signals,
        "confidence": "PARTIAL" if release_signals else "UNVERIFIED",
        "unknowns": ["OIDC permission is not trusted-publisher proof; release execution and source/artifact provenance require external evidence"],
    }
    return ci, security_section, release_section
