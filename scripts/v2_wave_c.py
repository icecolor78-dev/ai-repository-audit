from __future__ import annotations

import re
from pathlib import Path

TEXT_SUFFIXES={".py",".js",".jsx",".ts",".tsx",".go",".rs",".java",".kt",".rb",".php",".cs",".yml",".yaml",".json",".toml",".md",".ini",".cfg",".env"}

def _rel(root,p): return p.relative_to(root).as_posix()
def _files(root): return sorted(p for p in root.rglob("*") if p.is_file() and ".git" not in p.parts and p.suffix.lower() in TEXT_SUFFIXES)
def _sig(kind,path,detail): return {"kind":kind,"locator":path,"detail":detail,"state":"PARTIAL","confidence":"MEDIUM"}
def _pack(items,unknown):
    seen=set(); out=[]
    for x in items:
        k=(x["kind"],x["locator"],x["detail"])
        if k not in seen: seen.add(k); out.append(x)
    return {"signals":out[:200],"confidence":"PARTIAL" if out else "UNVERIFIED","unknowns":[unknown]}

def extract_wave_c(root:Path)->dict:
    model=[]; cost=[]; config=[]; conc=[]
    for p in _files(root):
        path=_rel(root,p); text=p.read_text(encoding="utf-8",errors="replace"); low=text.lower()
        if re.search(r"\b(eval|evaluation|benchmark|golden set|test set|holdout|grader|judge|hallucination|regression set|model version)\b",low): model.append(_sig("evaluation_signal",path,"model/evaluation or frozen test evidence signal observed"))
        if re.search(r"\b(leakage|contamination|train.*test|holdout|frozen.*eval|blind set)\b",low): model.append(_sig("evaluation_integrity",path,"evaluation leakage/holdout integrity signal observed"))
        if re.search(r"\b(token|tokens|max_tokens|usage|meter|billing|cost|budget|quota|rate limit|storage|log retention)\b",low): cost.append(_sig("cost_driver",path,"compute/API/token/storage/log cost or budget signal observed"))
        if re.search(r"\b(retry|backoff|loop|while true|max_iterations|max_steps)\b",low): cost.append(_sig("amplification_risk",path,"retry/loop amplification signal observed; actual cost impact not proven"))
        if re.search(r"\b(env|environment|config|configuration|feature flag|flag|default|fallback|secret|setting)\b",low): config.append(_sig("configuration_surface",path,"configuration/default/feature-flag/environment signal observed"))
        if re.search(r"\b(prod|production|staging|development|dev|test)\b",low) and re.search(r"\b(env|config|default|fallback|flag)\b",low): config.append(_sig("environment_drift",path,"environment-specific configuration/drift signal observed"))
        if re.search(r"\b(lock|mutex|semaphore|transaction|atomic|race|concurrent|thread|worker|queue|webhook|idempotent|exactly once|exactly-once)\b",low): conc.append(_sig("concurrency_surface",path,"concurrency/transaction/duplicate-work signal observed"))
        if re.search(r"\b(unique constraint|dedup|idempotency key|compare and swap|optimistic lock|select for update)\b",low): conc.append(_sig("concurrency_control",path,"concurrency/deduplication control signal observed"))
    return {
      "model_eval":_pack(model,"static repository evidence does not prove evaluation-set freshness, absence of leakage, grader reliability, model quality or regression resistance"),
      "finops":_pack(cost,"static repository evidence does not prove actual spend, savings, capacity, retry amplification cost or provider billing behavior"),
      "configuration":_pack(config,"static repository evidence does not prove deployed configuration, safe defaults, environment parity or feature-flag state"),
      "concurrency":_pack(conc,"static repository evidence does not prove race freedom, exactly-once behavior, correct locking or transaction isolation under concurrent execution"),
    }
