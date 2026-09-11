from __future__ import annotations
import json, subprocess, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; EXTRACTOR=ROOT/"scripts"/"rem_extract.py"; REVISION="a"*40

def run_fixture():
    with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp); (root/".github/workflows").mkdir(parents=True); (root/"tests").mkdir(); (root/"src").mkdir()
        (root/"README.md").write_text("CI and tests are used before release. Security matters.\n",encoding="utf-8"); (root/"pyproject.toml").write_text("[project]\nname='fixture'\n",encoding="utf-8"); (root/"uv.lock").write_text("version=1\n",encoding="utf-8"); (root/"src/app.py").write_text("print('ok')\n",encoding="utf-8"); (root/"tests/test_app.py").write_text("def test_ok(): assert True\n",encoding="utf-8")
        (root/".github/workflows/ci.yml").write_text("""name: CI
on:
  pull_request:
permissions:
  contents: read
jobs:
  test:
    steps:
      - uses: actions/checkout@v4
      - run: pytest
""",encoding="utf-8")
        (root/".github/workflows/publish.yml").write_text("""name: Publish release
on:
  release:
    types: [published]
permissions:
  contents: read
  id-token: write
jobs:
  publish:
    steps:
      - uses: actions/checkout@0123456789012345678901234567890123456789
        with:
          persist-credentials: false
      - uses: actions/upload-artifact@v4
      - run: python -m pytest -m smoke
      - run: cosign attest artifact.whl
      - run: echo ${{ secrets.PUBLISH_TOKEN }}
""",encoding="utf-8")
        (root/".github/workflows/risky.yml").write_text("""name: risky
on:
  pull_request_target:
jobs:
  risky:
    steps:
      - uses: thirdparty/example@main
      - run: echo ${{ github.event.pull_request.title }}
""",encoding="utf-8")
        p=subprocess.run([sys.executable,str(EXTRACTOR),str(root),"--repository","example/fixture","--revision",REVISION,"--observed-at","2026-09-11T00:00:00Z"],check=True,capture_output=True,text=True); return json.loads(p.stdout)

data=run_fixture(); assert data["schema_version"]=="rem/v1"; assert data["subject"]["revision"]==REVISION; assert data["ci"]["exact_subject_runs"]==[]; assert data["ci"]["release_confidence"]=="UNVERIFIED"; assert data["release"]["confidence"]=="PARTIAL"; assert data["release"]["trusted_publishing"]; assert data["release"]["artifact_handoffs"]; assert data["release"]["signing_or_attestation"]; assert data["release"]["smoke_or_release_tests"]
kinds={s["kind"] for s in data["security"]["signals"]}; assert "pull_request_target" in kinds; assert "mutable_action_ref" in kinds; assert "untrusted_expression_shell" in kinds; assert "credential_persistence" in kinds; assert "secret_reference" in kinds
assert data["claims"]["items"] and all(x["state"]=="UNVERIFIED" for x in data["claims"]["items"]); assert "exploitability" in data["coverage"]["explicit_unknowns"]; assert "score" not in data and "global_score" not in data
print("REM extractor tests passed")
