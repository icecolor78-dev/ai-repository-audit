from __future__ import annotations
import tempfile
from pathlib import Path
from v2_wave_b import extract_wave_b

with tempfile.TemporaryDirectory() as tmp:
    r=Path(tmp); (r/"src").mkdir(); (r/"docs").mkdir()
    (r/"src/service.py").write_text('''
def call_provider(client, request_id):
    for attempt in range(3):
        try:
            return client.get(timeout=2)
        except RateLimit429:
            backoff(attempt)
    return fallback()

def consume(event_id):
    if idempotent(event_id):
        audit_log(actor_id="worker", event_id=event_id, correlation_id=event_id)
''',encoding="utf-8")
    (r/"docs/incident-runbook.md").write_text('''Backup restore rollback kill switch incident runbook. RTO and RPO are claims that require restore evidence. Failure injection exercises retry storm and partial dependency outage.''',encoding="utf-8")
    a=extract_wave_b(r); b=extract_wave_b(r)
    assert a==b
    for section in ("resilience","incident_readiness","external_dependency_failure","auditability_forensics"):
        assert a[section]["signals"]
        assert a[section]["unknowns"]
        assert a[section]["confidence"]=="PARTIAL"
    assert any(x["kind"]=="failure_injection" for x in a["resilience"]["signals"])
    assert any(x["kind"]=="auditability" for x in a["auditability_forensics"]["signals"])
print("Wave B tests passed")
