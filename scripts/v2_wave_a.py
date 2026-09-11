from __future__ import annotations

import re
from pathlib import Path

STATE_VALUES={"VERIFIED","PARTIAL","UNVERIFIED","CONTRADICTED","NOT_APPLICABLE"}
TEXT_SUFFIXES={".py",".js",".jsx",".ts",".tsx",".go",".rs",".java",".kt",".rb",".php",".cs",".yml",".yaml",".json",".toml",".md",".ini",".cfg",".env"}


def _rel(root:Path,p:Path)->str:return p.relative_to(root).as_posix()
def _files(root:Path):return sorted(p for p in root.rglob("*") if p.is_file() and ".git" not in p.parts and p.suffix.lower() in TEXT_SUFFIXES)
def _signal(kind,locator,detail,confidence="MEDIUM"):return {"kind":kind,"locator":locator,"detail":detail,"confidence":confidence,"state":"PARTIAL"}

def extract_wave_a(root:Path)->dict:
    rows=_files(root); threat=[]; privacy=[]; agent=[]; identity=[]
    for p in rows:
        path=_rel(root,p); low_path=path.lower(); text=p.read_text(encoding="utf-8",errors="replace")
        low=text.lower()
        # Threat-model evidence: observable entry points/assets/trust-boundary transitions only.
        if re.search(r"\b(route|router|endpoint|webhook|callback|listener|handler|socket|grpc|graphql)\b",low): threat.append(_signal("entry_point",path,"network/request entry-point signal observed"))
        if re.search(r"\b(database|postgres|mysql|sqlite|redis|s3|bucket|filesystem|file store|queue|broker|secret|token)\b",low): threat.append(_signal("asset_or_trust_boundary",path,"state/credential/external-resource signal observed"))
        if re.search(r"\b(subprocess|os\.system|exec\(|eval\(|shell=true|child_process|spawn\()",low): threat.append(_signal("execution_boundary",path,"code/process execution boundary signal observed","HIGH"))
        # Privacy: presence/flow indicators; never compliance conclusions.
        if re.search(r"\b(email|phone|address|name|user_id|customer_id|account_id|ip_address|location|recording|audio|transcript|pii|personal data)\b",low): privacy.append(_signal("personal_data_signal",path,"potential personal/customer data field or concept observed"))
        if re.search(r"\b(log|logger|logging|print\()",low) and re.search(r"\b(token|secret|password|email|user|customer|request|payload|body)\b",low): privacy.append(_signal("logging_boundary",path,"logging plus sensitive/request data vocabulary observed; leakage not proven"))
        if re.search(r"\b(delete|erase|purge|retention|ttl|expire|export|download my data|data residency|region)\b",low): privacy.append(_signal("lifecycle_control",path,"data lifecycle/retention/deletion/export/residency signal observed"))
        if re.search(r"\b(encrypt|encryption|kms|tls|https|at rest|in transit)\b",low): privacy.append(_signal("encryption_boundary",path,"encryption/transport-protection signal observed"))
        # Agent safety: tools, untrusted content, confirmation and budgets.
        if re.search(r"\b(tool|tools|function call|function_call|mcp|connector|browser|shell|terminal|execute|action)\b",low): agent.append(_signal("tool_authority",path,"agent/tool/action authority signal observed"))
        if re.search(r"\b(prompt injection|untrusted|user content|external content|web content|instruction hierarchy|sanitize|allowlist|denylist)\b",low): agent.append(_signal("untrusted_content_boundary",path,"untrusted-content or prompt-boundary signal observed"))
        if re.search(r"\b(confirm|approval|authorize|consent|human in the loop|human-in-the-loop)\b",low): agent.append(_signal("confirmation_gate",path,"confirmation/authorization gate signal observed"))
        if re.search(r"\b(max_steps|max_iterations|iteration limit|loop limit|token budget|tool budget|timeout|max_tokens)\b",low): agent.append(_signal("loop_or_budget_control",path,"agent loop/token/tool budget control signal observed"))
        if re.search(r"\b(memory|vector store|retrieval|rag)\b",low) and re.search(r"\b(untrusted|poison|validate|provenance|source)\b",low): agent.append(_signal("memory_provenance_boundary",path,"memory/retrieval provenance or poisoning-control signal observed"))
        # Identity/access: authentication and authorization are separate dimensions.
        if re.search(r"\b(authenticate|authentication|oauth|oidc|jwt|session|login|api key|bearer)\b",low): identity.append(_signal("authentication",path,"authentication/session identity signal observed"))
        if re.search(r"\b(authorize|authorization|rbac|abac|role|permission|scope|policy|access control)\b",low): identity.append(_signal("authorization",path,"authorization/role/scope/policy signal observed"))
        if re.search(r"\b(tenant|workspace|organization_id|org_id|account_id)\b",low): identity.append(_signal("tenant_boundary",path,"tenant/workspace/account boundary signal observed"))
        if re.search(r"\b(service account|service principal|workload identity|machine identity)\b",low): identity.append(_signal("service_identity",path,"service/workload identity signal observed"))
    def pack(items:list[dict],unknowns:list[str])->dict:
        # dedupe identical path/kind pairs to keep output compact and deterministic
        seen=set(); out=[]
        for item in items:
            key=(item["kind"],item["locator"],item["detail"])
            if key not in seen: seen.add(key); out.append(item)
        return {"signals":out[:200],"confidence":"PARTIAL" if out else "UNVERIFIED","unknowns":unknowns}
    result={
      "threat_model":pack(threat,["static repository evidence does not prove exploitability, complete asset inventory, runtime trust boundaries or mitigation effectiveness"]),
      "data_privacy":pack(privacy,["static evidence does not prove privacy-law compliance, actual retention/deletion behavior, residency, encryption effectiveness or absence of data leakage"]),
      "agent_safety":pack(agent,["static evidence does not prove resistance to prompt injection, correct confirmation behavior at runtime, bounded autonomous execution or memory-poisoning resistance"]),
      "identity_access":pack(identity,["static evidence does not prove production authentication strength, authorization correctness, tenant isolation or absence of privilege escalation"]),
    }
    # Evidence-backed STRIDE-style hypotheses are hypotheses, not findings.
    hypotheses=[]
    if any(x["kind"]=="authentication" for x in identity): hypotheses.append({"category":"SPOOFING","state":"UNVERIFIED","reason":"authentication boundary exists; spoofing resistance requires protocol/runtime evidence"})
    if any(x["kind"] in {"asset_or_trust_boundary","execution_boundary"} for x in threat): hypotheses.append({"category":"TAMPERING","state":"UNVERIFIED","reason":"state/execution boundary exists; tamper resistance requires validation/integrity evidence"})
    if any(x["kind"]=="tool_authority" for x in agent): hypotheses.append({"category":"ELEVATION_OF_PRIVILEGE","state":"UNVERIFIED","reason":"tool/action authority exists; escalation resistance requires permission and runtime gate evidence"})
    if any(x["kind"]=="personal_data_signal" for x in privacy): hypotheses.append({"category":"INFORMATION_DISCLOSURE","state":"UNVERIFIED","reason":"personal/customer data signal exists; disclosure requires data-flow/logging/runtime evidence"})
    result["threat_model"]["stride_hypotheses"]=hypotheses
    return result
