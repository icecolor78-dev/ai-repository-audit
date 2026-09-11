from __future__ import annotations
import tempfile
from pathlib import Path
from v2_wave_a import extract_wave_a

with tempfile.TemporaryDirectory() as tmp:
    r=Path(tmp); (r/"src").mkdir(); (r/"docs").mkdir()
    (r/"src/app.py").write_text('''
def webhook(request):
    user_id=request.user_id
    logger.info("user request", extra={"user": user_id})
    authorize(scope="repo:write")
    confirm("publish change")
    run_tool(max_steps=8)
    return database.save(user_id)
''',encoding="utf-8")
    (r/"docs/security.md").write_text('''OAuth authentication and RBAC authorization. Tenant boundary uses organization_id. External web content is untrusted and must be allowlisted before tool execution. Data deletion and retention are documented. TLS is required in transit.''',encoding="utf-8")
    a=extract_wave_a(r); b=extract_wave_a(r)
    assert a==b
    assert a["threat_model"]["signals"] and a["threat_model"]["stride_hypotheses"]
    assert a["data_privacy"]["signals"]
    assert a["agent_safety"]["signals"]
    assert a["identity_access"]["signals"]
    assert all(x["state"] in {"PARTIAL","UNVERIFIED"} for section in a.values() for x in section.get("signals",[]))
    assert all(x["state"]=="UNVERIFIED" for x in a["threat_model"]["stride_hypotheses"])
    assert "compliance" in a["data_privacy"]["unknowns"][0]
    assert "prompt injection" in a["agent_safety"]["unknowns"][0]
print("Wave A tests passed")
