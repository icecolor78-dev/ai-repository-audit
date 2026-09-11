from __future__ import annotations

import re
from pathlib import Path

TEXT_SUFFIXES={".py",".js",".jsx",".ts",".tsx",".go",".rs",".java",".kt",".rb",".php",".cs",".yml",".yaml",".json",".toml",".md",".ini",".cfg"}

def _rel(root:Path,p:Path)->str:return p.relative_to(root).as_posix()
def _files(root:Path):return sorted(p for p in root.rglob("*") if p.is_file() and ".git" not in p.parts and p.suffix.lower() in TEXT_SUFFIXES)
def _signal(kind,locator,detail,confidence="MEDIUM"):return {"kind":kind,"locator":locator,"detail":detail,"confidence":confidence,"state":"PARTIAL"}
def _pack(items,unknown):
    seen=set(); out=[]
    for x in items:
        key=(x["kind"],x["locator"],x["detail"])
        if key not in seen: seen.add(key); out.append(x)
    return {"signals":out[:200],"confidence":"PARTIAL" if out else "UNVERIFIED","unknowns":[unknown]}

def extract_wave_b(root:Path)->dict:
    resilience=[]; incident=[]; dependency=[]; forensic=[]
    for p in _files(root):
        path=_rel(root,p); low=p.read_text(encoding="utf-8",errors="replace").lower()
        if re.search(r"\b(timeout|retry|backoff|circuit breaker|circuit_breaker|bulkhead|rate limit|ratelimit|degraded|fallback|idempotent|idempotency|duplicate|dead letter|dlq)\b",low): resilience.append(_signal("failure_control",path,"failure/retry/idempotency/degraded-mode control signal observed"))
        if re.search(r"\b(chaos|fault injection|failure injection|kill -9|network partition|latency injection|retry storm)\b",low): resilience.append(_signal("failure_injection",path,"failure-injection/chaos evidence signal observed","HIGH"))
        if re.search(r"\b(backup|restore|rollback|kill switch|killswitch|runbook|incident|disaster recovery|rto|rpo|point in time recovery|pit recovery)\b",low): incident.append(_signal("recovery_readiness",path,"backup/restore/rollback/runbook/incident-readiness signal observed"))
        if re.search(r"\b(status page|on-call|oncall|pager|postmortem|post-mortem|incident commander)\b",low): incident.append(_signal("incident_process",path,"incident-response process signal observed"))
        if re.search(r"\b(http|https|api|client|provider|stripe|openai|github|s3|redis|postgres|database|queue|broker|webhook)\b",low) and re.search(r"\b(timeout|retry|429|rate limit|5\d\d|partial success|fallback|circuit)\b",low): dependency.append(_signal("external_failure_contract",path,"external dependency plus failure-handling signal observed"))
        if re.search(r"\b(correlation[_ -]?id|request[_ -]?id|trace[_ -]?id|event[_ -]?id|actor[_ -]?id|audit log|audit_log|append-only|immutable log|tamper|forensic)\b",low): forensic.append(_signal("auditability",path,"correlation/actor/audit/forensic evidence signal observed"))
        if re.search(r"\b(hash chain|signed log|signature|merkle|write once|worm)\b",low): forensic.append(_signal("tamper_resistance",path,"tamper-resistance evidence signal observed","HIGH"))
    return {
      "resilience":_pack(resilience,"static evidence does not prove runtime resilience, recovery time, retry-storm safety, idempotency under concurrency, degraded-mode correctness or chaos-test success"),
      "incident_readiness":_pack(incident,"static evidence does not prove backups are restorable, rollback works, kill switches are effective, runbooks are current, or RTO/RPO claims are met"),
      "external_dependency_failure":_pack(dependency,"static evidence does not prove provider/database/storage/rate-limit/partial-success behavior under real failures"),
      "auditability_forensics":_pack(forensic,"static evidence does not prove complete actor attribution, event ordering, log immutability, tamper resistance or successful incident reconstruction"),
    }
