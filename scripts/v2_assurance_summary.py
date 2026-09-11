from __future__ import annotations

DOMAINS=(
 'threat_model','data_privacy','agent_safety','identity_access',
 'resilience','incident_readiness','external_dependency_failure','auditability_forensics',
 'model_eval','finops','configuration','concurrency','migration','interface','license_ip'
)

PRESERVED_STATES={'CONTRADICTED','UNVERIFIED','NOT_APPLICABLE'}

def summarize(portrait:dict)->dict:
    domains=[]
    for name in DOMAINS:
        section=portrait.get(name) or {}
        signals=section.get('signals') or []
        confidence=section.get('confidence','UNVERIFIED')
        unknowns=section.get('unknowns') or []
        if confidence in PRESERVED_STATES:
            state=confidence
        elif not signals:
            state='UNVERIFIED'
        else:
            state='PARTIAL'
        domains.append({
          'domain':name,
          'state':state,
          'signal_count':len(signals),
          'explicit_unknowns':list(unknowns),
          'statement':'Repository evidence is bounded to observed static signals; signal count is not a PASS score.'
        })
    missing=[x['domain'] for x in domains if x['domain'] not in portrait]
    return {
      'version':'2.0',
      'domain_count':len(DOMAINS),
      'domains':domains,
      'missing_domains':missing,
      'complete_contract':not missing,
      'scoring':'NONE',
      'verdict_rule':'No global PASS is manufactured from domain presence, signal count, PARTIAL evidence, or contradicted evidence.',
      'limitations':['Runtime, exploitability, legal/compliance, economic, operational and model-quality claims require corresponding evidence beyond static repository signals.']
    }
