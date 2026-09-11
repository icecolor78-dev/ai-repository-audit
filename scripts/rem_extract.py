from __future__ import annotations

import argparse, json, re
from datetime import datetime, timezone
from pathlib import Path

SHA_RE = re.compile(r"^[0-9a-f]{40}$")
LANGUAGE_SUFFIXES = {".py":"Python",".rs":"Rust",".go":"Go",".ts":"TypeScript",".tsx":"TypeScript",".js":"JavaScript",".jsx":"JavaScript",".java":"Java",".kt":"Kotlin",".rb":"Ruby",".php":"PHP",".cs":"C#",".cpp":"C++",".cc":"C++",".c":"C",".swift":"Swift",".scala":"Scala"}
MANIFESTS={"pyproject.toml","setup.py","setup.cfg","package.json","Cargo.toml","go.mod","pom.xml","build.gradle","build.gradle.kts","Gemfile","composer.json","requirements.txt"}
LOCKFILES={"uv.lock","poetry.lock","pdm.lock","package-lock.json","pnpm-lock.yaml","yarn.lock","bun.lockb","Cargo.lock","go.sum","Gemfile.lock","composer.lock"}
TEST_HINTS={"pytest":"unit/integration","unittest":"unit","playwright":"end-to-end","cypress":"end-to-end","vitest":"unit/integration","jest":"unit/integration","tox":"compatibility","nox":"compatibility","fuzz":"fuzz","benchmark":"performance","contract":"contract","smoke":"smoke","e2e":"end-to-end"}
CLAIM_PATTERNS=[(re.compile(r"\bCI\b|continuous integration",re.I),"CI is present/used"),(re.compile(r"\btests?\b|tested",re.I),"tests are present/used"),(re.compile(r"release|publish|PyPI|npm",re.I),"release or publishing path is described"),(re.compile(r"security|secure|vulnerability",re.I),"security property or process is described")]

def files(root): return sorted(p for p in root.rglob("*") if p.is_file() and ".git" not in p.parts)
def rel(root,p): return p.relative_to(root).as_posix()
def signal(kind, locator, detail, confidence="MEDIUM", severity="INFO"): return {"kind":kind,"locator":locator,"detail":detail,"confidence":confidence,"severity":severity}

def workflow_profile(root, all_files):
    workflows=[p for p in all_files if rel(root,p).startswith(".github/workflows/") and p.suffix in {".yml",".yaml"}]
    names=[]; triggers=[]; filters=[]; matrices=[]; conditionals=[]; aggregates=[]; permissions=[]; action_refs=[]; sources=[]; security=[]; release=[]
    for path in workflows:
        text=path.read_text(encoding="utf-8",errors="replace"); rp=rel(root,path); names.append(rp); low=(rp+"\n"+text).lower()
        for token in ("pull_request","pull_request_target","push","workflow_dispatch","workflow_run","schedule","release"):
            if re.search(rf"(?m)^\s*{token}\s*:",text): triggers.append(f"{rp}: {token}")
        if re.search(r"(?m)^\s*paths(?:-ignore)?\s*:",text): filters.append(f"{rp}: path filter present")
        if re.search(r"(?m)^\s*matrix\s*:",text): matrices.append(f"{rp}: matrix present")
        if re.search(r"(?m)^\s*if\s*:",text): conditionals.append(f"{rp}: conditional job/step present")
        if re.search(r"(?m)^\s*needs\s*:",text): aggregates.append(f"{rp}: dependency/aggregate signal present")
        for m in re.finditer(r"(?m)^\s*permissions\s*:\s*(.*)$",text): permissions.append(f"{rp}: permissions {m.group(1).strip() or 'mapping'}")
        if re.search(r"(?m)^\s*pull_request_target\s*:",text): security.append(signal("pull_request_target",rp,"privileged PR-context trigger present","HIGH","HIGH"))
        if re.search(r"persist-credentials\s*:\s*false",text,re.I): security.append(signal("credential_persistence",rp,"checkout credential persistence explicitly disabled","HIGH"))
        elif "actions/checkout@" in text: security.append(signal("credential_persistence",rp,"checkout present without observed persist-credentials:false","MEDIUM","LOW"))
        if re.search(r"run\s*:\s*[^\n]*\$\{\{\s*github\.event\.(?:pull_request|issue|comment|head_commit)",text,re.I): security.append(signal("untrusted_expression_shell",rp,"event-derived expression appears directly in a run command","MEDIUM","HIGH"))
        if re.search(r"secrets\.[A-Za-z0-9_]+",text): security.append(signal("secret_reference",rp,"workflow references a secret; static inspection does not establish exposure","HIGH","INFO"))
        for m in re.finditer(r"uses:\s*([^\s#]+)",text):
            ref=m.group(1)
            if ref.startswith("./"): continue
            pinned=bool(re.search(r"@[0-9a-f]{40}$",ref)); item=f"{rp}: {ref}"+(" [mutable-ref-signal]" if not pinned else " [full-sha]"); action_refs.append(item)
            if not pinned: security.append(signal("mutable_action_ref",rp,ref,"HIGH","LOW"))
        releaseish=bool(re.search(r"release|publish|pypi|npm|rubygems|crates\.io|docker|ghcr",low))
        if releaseish:
            release.append(signal("release_workflow",rp,"release/publish vocabulary or trigger observed","MEDIUM"))
            if re.search(r"actions/(?:upload|download)-artifact@",text): release.append(signal("artifact_handoff",rp,"GitHub artifact upload/download action observed","HIGH"))
            if re.search(r"id-token\s*:\s*write",text,re.I): release.append(signal("trusted_publishing",rp,"OIDC id-token: write permission observed; publication success remains unverified","HIGH"))
            if re.search(r"attest|provenance|sigstore|cosign|gpg|signing",text,re.I): release.append(signal("signing_or_attestation",rp,"signing/attestation/provenance signal observed","MEDIUM"))
            if re.search(r"smoke|verify|verification",text,re.I): release.append(signal("release_verification",rp,"release verification/smoke signal observed","MEDIUM"))
            if re.search(r"rollback|revert|recovery",text,re.I): release.append(signal("rollback_or_recovery",rp,"rollback/recovery signal observed","MEDIUM"))
        sources.append({"id":f"workflow-{len(sources)+1}","kind":"workflow_definition","locator":rp,"supports":["workflow definition","CI/release/security static signals"],"limits":["definition does not prove execution, exploitability, publication or vulnerability absence"]})
    conf="PARTIAL" if workflows else "UNVERIFIED"
    return {"workflows":names,"required_checks":[],"trigger_model":sorted(set(triggers)),"path_filters":sorted(set(filters)),"runtime_matrix":sorted(set(matrices)),"os_arch_matrix":[],"conditional_jobs":sorted(set(conditionals)),"aggregate_checks":sorted(set(aggregates)),"exact_subject_runs":[],"confidence":conf,"unknowns":["workflow execution and required-check enforcement require external exact-subject evidence"],"pr_confidence":conf,"main_confidence":conf,"release_confidence":"UNVERIFIED","security_evidence_freshness":"UNVERIFIED","_permissions":permissions,"_action_refs":action_refs,"_security_signals":security,"_release_signals":release},sources

def test_profile(root,all_files):
    candidates=[]; types=set()
    for p in all_files:
        rp=rel(root,p); low=rp.lower()
        if any(x in low for x in ("test","spec","__tests__")): candidates.append(rp)
        for hint,kind in TEST_HINTS.items():
            if hint in low: types.add(kind)
    conf="PARTIAL" if candidates else "UNVERIFIED"
    return {"suites":candidates[:100],"types":sorted(types),"subsystem_map":[],"exact_subject_execution":[],"confidence":conf,"unknowns":["file/config discovery does not prove execution or semantic completeness"]}

def claims(root):
    items=[]
    for p in (root/"README.md",root/"README.rst",root/"README.txt"):
        if not p.is_file(): continue
        text=p.read_text(encoding="utf-8",errors="replace")
        for pattern,label in CLAIM_PATTERNS:
            if pattern.search(text): items.append({"claim":label,"source_ref":"readme","state":"UNVERIFIED","supporting_refs":[],"contradicting_refs":[],"notes":"Claim discovered from README text; evidence binding requires a separate matcher."})
    return items

def extract(root,repository,revision,default_branch,observed_at):
    if not SHA_RE.fullmatch(revision): raise SystemExit("revision must be a lowercase full 40-hex SHA")
    all_files=files(root); manifests=sorted(rel(root,p) for p in all_files if p.name in MANIFESTS); lockfiles=sorted(rel(root,p) for p in all_files if p.name in LOCKFILES)
    ci,sources=workflow_profile(root,all_files); permissions=ci.pop("_permissions"); refs=ci.pop("_action_refs"); security_signals=ci.pop("_security_signals"); release_signals=ci.pop("_release_signals")
    source_rows=([{"id":"readme","kind":"repository_file","locator":"README.md","supports":["public claims"],"limits":["claim text does not prove claim"]}] if (root/"README.md").is_file() else [])+sources
    for row in source_rows: row.update({"subject_revision":revision,"observed_at":observed_at,"freshness":{"state":"exact","reason":"local tree supplied for exact subject"},"access":{"state":"accessible"}})
    return {"schema_version":"rem/v1","subject":{"provider":"github","repository":repository,"revision":revision,"default_branch":default_branch,"observed_at":observed_at,"visibility":"public"},"inventory":{"languages":sorted({LANGUAGE_SUFFIXES[p.suffix.lower()] for p in all_files if p.suffix.lower() in LANGUAGE_SUFFIXES}),"manifests":manifests,"lockfiles":lockfiles,"modules":sorted(p.name for p in root.iterdir() if p.is_dir() and not p.name.startswith(".")),"generated_or_vendor_boundaries":[]},"ci":ci,"tests":test_profile(root,all_files),"security":{"workflow_permissions":permissions,"credential_persistence":[s for s in security_signals if s["kind"]=="credential_persistence"],"action_pinning":refs,"static_analysis":[],"dependency_security":[],"secret_scanning_evidence":[],"freshness":[],"signals":security_signals,"confidence":"PARTIAL" if security_signals or permissions or refs else "UNVERIFIED","unknowns":["static signals do not prove exploitability, vulnerability absence or scanner freshness"]},"release":{"workflows":[s["locator"] for s in release_signals if s["kind"]=="release_workflow"],"artifact_handoffs":[s for s in release_signals if s["kind"]=="artifact_handoff"],"source_artifact_binding":[],"trusted_publishing":[s for s in release_signals if s["kind"]=="trusted_publishing"],"signing_or_attestation":[s for s in release_signals if s["kind"]=="signing_or_attestation"],"smoke_or_release_tests":[s for s in release_signals if s["kind"]=="release_verification"],"rollback_or_recovery":[s for s in release_signals if s["kind"]=="rollback_or_recovery"],"signals":release_signals,"confidence":"PARTIAL" if release_signals else "UNVERIFIED","unknowns":["release success and artifact/source provenance require execution evidence"]},"supply_chain":{"dependencies":manifests+lockfiles,"update_automation":[],"sbom":[],"license_evidence":[],"provenance":[],"confidence":"PARTIAL" if manifests or lockfiles else "UNVERIFIED","unknowns":["dependency presence is not a vulnerability, license or provenance audit"]},"claims":{"items":claims(root)},"provenance":{"ai_assisted_changes":[],"generated_code":[],"external_build_or_test_services":[],"confidence":"UNVERIFIED","unknowns":["change authorship/provenance requires explicit evidence"]},"coverage":{"dimensions":["inventory","workflow definitions","test discovery","README claim discovery","release static signals","workflow-security static signals"],"explicit_unknowns":["workflow executions","required-check enforcement","external security freshness","release success","runtime behavior","claim verification","exploitability"],"excluded_scope":["penetration testing","certification","production runtime behavior"]},"sources":source_rows}

def main():
    p=argparse.ArgumentParser(); p.add_argument("root",type=Path); p.add_argument("--repository",required=True); p.add_argument("--revision",required=True); p.add_argument("--default-branch",default="main"); p.add_argument("--observed-at",default=None); a=p.parse_args(); observed=a.observed_at or datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00","Z"); print(json.dumps(extract(a.root.resolve(),a.repository,a.revision,a.default_branch,observed),indent=2,sort_keys=True))
if __name__=="__main__": main()
