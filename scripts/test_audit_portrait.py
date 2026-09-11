from __future__ import annotations
import tempfile
from pathlib import Path
from audit_portrait import compose
REV="b"*40
with tempfile.TemporaryDirectory() as tmp:
    r=Path(tmp); (r/".github/workflows").mkdir(parents=True); (r/"src/api").mkdir(parents=True); (r/"tests").mkdir(); (r/".github").mkdir(exist_ok=True)
    (r/"README.md").write_text("CI tests release security\n",encoding="utf-8"); (r/"pyproject.toml").write_text("[project]\nname='x'\n",encoding="utf-8"); (r/"LICENSE").write_text("example license text\n",encoding="utf-8"); (r/".github/dependabot.yml").write_text("version: 2\nupdates: []\n",encoding="utf-8"); (r/"src/api/openapi.yaml").write_text("openapi: 3.0.0\n",encoding="utf-8"); (r/"tests/test_x.py").write_text("def test_x(): assert True\n",encoding="utf-8")
    (r/".github/workflows/release.yml").write_text("""name: release
on:
  release:
permissions:
  contents: read
  id-token: write
jobs:
  publish:
    steps:
      - uses: actions/checkout@v4
      - uses: actions/upload-artifact@v4
      - run: python -m pytest -m smoke
""",encoding="utf-8")
    d=compose(r,"example/repo",REV,"main","2026-09-11T00:00:00Z")
    assert d["subject"]["revision"]==REV
    assert d["supply_chain"]["license_evidence"]==["LICENSE"]
    assert d["supply_chain"]["update_automation"]
    assert d["architecture"]["api_contract_signals"]
    assert d["overall_portrait"]["confidence"]=="PARTIAL"
    assert d["overall_portrait"]["explicit_unknowns"]
    assert d["overall_portrait"]["remediation"]
    assert any(x["state"]=="PARTIAL" for x in d["claims"]["items"])
    assert "global_score" not in d and "score" not in d["overall_portrait"]
    assert "certification" in d["overall_portrait"]["statement"]
print("Overall portrait tests passed")
