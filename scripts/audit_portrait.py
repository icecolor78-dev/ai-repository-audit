from __future__ import annotations

import argparse, json, re, sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rem_extract import extract
from v2_wave_a import extract_wave_a
from v2_wave_b import extract_wave_b

LICENSE_NAMES={"LICENSE","LICENSE.md","LICENSE.txt","COPYING","COPYING.md","NOTICE","NOTICE.md"}
UPDATE_FILES={"dependabot.yml","dependabot.yaml","renovate.json","renovate.json5","renovate-config.js"}
API_HINTS=("openapi","swagger","schema","graphql","proto","api")
OPS_HINTS=("dockerfile","compose.yml","compose.yaml","helm","k8s","kubernetes","health","readiness","runbook","deploy")
GOV_HINTS=("codeowners","security.md","contributing.md","governance.md")

def rp(root,p): return p.relative_to(root).as_posix()
def rows(root): return sorted(p for p in root.rglob("*") if p.is_file() and ".git" not in p.parts)
def sig(kind, locator, detail, confidence="MEDIUM", severity="INFO"): return {"kind":kind,"locator":locator,"detail":detail,"confidence":confidence,"severity":severity}

def static_layers(root:Path, all_files:list[Path]):
    paths=[rp(root,p) for p in all_files]
    licenses=[x for x in paths if Path(x).name.upper() in LICENSE_NAMES]
    updates=[x for x in paths if Path(x).name.lower() in UPDATE_FILES or ".github/dependabot" in x.lower()]
    sbom=[x for x in paths if re.search(r"(?:sbom|cyclonedx|spdx)",x,re.I)]
    api=[x for x in paths if any(h in x.lower() for h in API_HINTS)][:100]
    ops=[x for x in paths if any(h in x.lower() for h in OPS_HINTS)][:100]
    gov=[x for x in paths if Path(x).name.lower() in GOV_HINTS or x.lower().endswith("/.github/codeowners")]
    top={p.parts[0] for p in map(Path,paths) if len(p.parts)>1 and not p.parts[0].startswith(".")}
    architecture={"top_level_boundaries":sorted(top),"api_contract_signals":api,"change_impact":"PARTIAL" if top else "UNVERIFIED","cycles":[],"coupling":[],"confidence":"PARTIAL" if top or api else "UNVERIFIED","unknowns":["static path inventory does not prove runtime dependency direction, blast radius or API compatibility"]}
    operability={"signals":ops,"confidence":"PARTIAL" if ops else "UNVERIFIED","unknowns":["files and configuration do not prove deployed health, observability, rollback or recovery behavior"]}
    governance={"signals":gov,"confidence":"PARTIAL" if gov else "UNVERIFIED","unknowns":["repository files do not prove branch/ruleset enforcement or organizational process execution"]}
    supply={"update_automation":updates,"sbom":sbom,"license_evidence":licenses,"confidence":"PARTIAL" if updates or sbom or licenses else "UNVERIFIED","unknowns":["static dependency/license files do not prove vulnerability absence, license compatibility, provenance or freshness"]}
    maintain={"large_files":[rp(root,p) for p in all_files if p.stat().st_size>250000][:50],"generated_or_vendor_signals":[x for x in paths if re.search(r"(^|/)(vendor|generated|dist|build|node_modules)(/|$)",x,re.I)][:50],"confidence":"PARTIAL","unknowns":["file size/path heuristics do not establish complexity, ownership quality or defect probability"]}
    return supply,architecture,operability,governance,maintain

def bind_claims(rem):
    for item in rem["claims"]["items"]:
        c=item["claim"].lower(); refs=[]
        if "ci" in c and rem["ci"]["workflows"]: refs=["workflow definitions"]
        elif "tests" in c and rem["tests"]["suites"]: refs=["test files/configuration"]
        elif "release" in c and rem["release"]["workflows"]: refs=["release workflow definitions"]
        elif "security" in c and rem["security"]["signals"]: refs=["workflow-security static signals"]
        if refs:
            item["state"]="PARTIAL"; item["supporting_refs"]=refs; item["notes"]="Repository evidence supports part of the claim, but runtime/external proof remains required."
    return rem

def compose(root:Path, repository:str, revision:str, default_branch:str, observed_at:str):
    rem=bind_claims(extract(root,repository,revision,default_branch,observed_at)); all_files=rows(root); supply,arch,ops,gov,maint=static_layers(root,all_files)
    rem["supply_chain"].update(supply); rem["architecture"]=arch; rem["operability"]=ops; rem["governance"]=gov; rem["maintainability"]=maint
    rem.update(extract_wave_a(root)); rem.update(extract_wave_b(root))
    findings=[]
    for s in rem["security"]["signals"]:
        if s["severity"] in {"HIGH","MEDIUM","LOW"}: findings.append(s)
    if rem["inventory"]["manifests"] and not rem["inventory"]["lockfiles"]: findings.append(sig("dependency_reproducibility",rem["inventory"]["manifests"][0],"manifest observed without a recognized lockfile; ecosystem-specific reproducibility remains to be verified","MEDIUM","LOW"))
    if rem["release"]["workflows"] and not rem["release"]["trusted_publishing"]: findings.append(sig("release_identity",rem["release"]["workflows"][0],"release workflow observed without static OIDC trusted-publishing signal; alternate authentication may exist","LOW","INFO"))
    unknowns=[]
    for section in ("ci","tests","security","release","supply_chain","architecture","operability","governance","maintainability","threat_model","data_privacy","agent_safety","identity_access","resilience","incident_readiness","external_dependency_failure","auditability_forensics"):
        unknowns += [{"dimension":section,"detail":u} for u in rem[section].get("unknowns",[])]
    remediation=[]
    if any(f["kind"]=="mutable_action_ref" for f in findings): remediation.append({"priority":"P1","action":"Pin third-party GitHub Actions to reviewed full commit SHAs where operationally appropriate.","verification":"Re-extract exact subject and verify mutable-ref signals are resolved or explicitly accepted."})
    if any(f["kind"]=="untrusted_expression_shell" for f in findings): remediation.append({"priority":"P0","action":"Move event-derived values out of direct shell interpolation and validate/quote through environment or structured inputs.","verification":"Review exact workflow and run bounded security regression fixtures."})
    if rem["inventory"]["manifests"] and not rem["inventory"]["lockfiles"]: remediation.append({"priority":"P2","action":"Confirm ecosystem reproducibility policy and add/justify lock or equivalent immutable dependency resolution evidence.","verification":"Re-extract dependency evidence and run reproducible install/build check."})
    if rem["threat_model"]["stride_hypotheses"]: remediation.append({"priority":"P1","action":"Review evidence-backed STRIDE hypotheses against real assets, trust boundaries and mitigations; keep unsupported categories UNVERIFIED.","verification":"Bind each accepted threat/mitigation to exact-subject design, test or runtime evidence."})
    if rem["data_privacy"]["signals"]: remediation.append({"priority":"P1","action":"Build an explicit data-flow inventory for observed personal/customer-data signals, including logging, retention, deletion/export and encryption boundaries.","verification":"Trace representative data classes end-to-end and attach execution/policy evidence where static evidence is insufficient."})
    if rem["agent_safety"]["signals"]: remediation.append({"priority":"P1","action":"Verify untrusted-content-to-tool paths, action authority, confirmation gates and loop/budget controls with bounded adversarial tests.","verification":"Attach exact-subject prompt-injection/tool-authority regression evidence; do not infer runtime safety from code presence."})
    if rem["identity_access"]["signals"]: remediation.append({"priority":"P1","action":"Map authentication, authorization, scopes/service identities and tenant boundaries separately.","verification":"Run negative authorization and cross-tenant tests where applicable; static configuration alone remains PARTIAL."})
    if rem["resilience"]["signals"] or rem["external_dependency_failure"]["signals"]: remediation.append({"priority":"P1","action":"Exercise observed retry/timeout/idempotency/dependency-failure paths under bounded fault injection.","verification":"Attach exact-subject failure-injection evidence for timeout, partial outage, duplicate delivery and recovery; static controls alone remain PARTIAL."})
    if rem["incident_readiness"]["signals"]: remediation.append({"priority":"P1","action":"Verify backup restore, rollback, kill-switch and incident-runbook claims with dated operational evidence.","verification":"Perform bounded restore/rollback exercises and bind measured recovery evidence to claimed RTO/RPO where applicable."})
    if rem["auditability_forensics"]["signals"]: remediation.append({"priority":"P1","action":"Verify actor attribution, correlation IDs and forensic event continuity across representative state changes.","verification":"Reconstruct a bounded incident/change from durable evidence and explicitly test tamper-resistance claims where made."})
    verdict="HOLD" if any(f["severity"]=="HIGH" for f in findings) else "BOUNDED_REVIEW"
    rem["overall_portrait"]={"verdict":verdict,"verdict_scope":"static repository evidence only","findings":findings,"claims":rem["claims"]["items"],"explicit_unknowns":unknowns,"remediation":remediation,"confidence":"PARTIAL","statement":"This portrait summarizes exact-subject repository evidence. It is not a penetration test, certification, compliance or legal opinion, production-runtime proof, privacy guarantee, prompt-injection guarantee, tenant-isolation proof, resilience/SLA proof, disaster-recovery attestation, or guarantee of defect/vulnerability absence."}
    rem["coverage"]["dimensions"] += ["supply-chain static evidence","architecture/change-impact signals","operability signals","governance signals","maintainability signals","claims/evidence binding","threat-model evidence","data-privacy evidence","agent-safety evidence","identity/access evidence","resilience evidence","incident-readiness evidence","external-dependency-failure evidence","auditability/forensics evidence","Overall Repository Portrait"]
    return rem

def main():
    p=argparse.ArgumentParser(); p.add_argument("root",type=Path); p.add_argument("--repository",required=True); p.add_argument("--revision",required=True); p.add_argument("--default-branch",default="main"); p.add_argument("--observed-at"); a=p.parse_args(); observed=a.observed_at or datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00","Z"); print(json.dumps(compose(a.root.resolve(),a.repository,a.revision,a.default_branch,observed),indent=2,sort_keys=True))
if __name__=="__main__": main()
