from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXTRACTOR = ROOT / "scripts" / "rem_extract.py"
REVISION = "a" * 40


def run_fixture() -> dict:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / ".github/workflows").mkdir(parents=True)
        (root / "tests").mkdir()
        (root / "src").mkdir()
        (root / "README.md").write_text("CI and tests are used before release. Security matters.\n", encoding="utf-8")
        (root / "pyproject.toml").write_text("[project]\nname='fixture'\n", encoding="utf-8")
        (root / "uv.lock").write_text("version = 1\n", encoding="utf-8")
        (root / "src/app.py").write_text("print('ok')\n", encoding="utf-8")
        (root / "tests/test_app.py").write_text("def test_ok(): assert True\n", encoding="utf-8")
        (root / ".github/workflows/ci.yml").write_text("""name: CI
on:
  pull_request:
    paths-ignore:
      - 'docs/**'
permissions:
  contents: read
jobs:
  test:
    if: github.event_name == 'pull_request'
    strategy:
      matrix:
        python: ['3.11', '3.12']
    steps:
      - uses: actions/checkout@v4
      - run: pytest
  all-green:
    needs: [test]
    runs-on: ubuntu-latest
    steps:
      - run: echo ok
""", encoding="utf-8")
        proc = subprocess.run([sys.executable, str(EXTRACTOR), str(root), "--repository", "example/fixture", "--revision", REVISION, "--observed-at", "2026-09-11T00:00:00Z"], check=True, capture_output=True, text=True)
        return json.loads(proc.stdout)


data = run_fixture()
assert data["schema_version"] == "rem/v1"
assert data["subject"]["revision"] == REVISION
assert "Python" in data["inventory"]["languages"]
assert "pyproject.toml" in data["inventory"]["manifests"]
assert "uv.lock" in data["inventory"]["lockfiles"]
assert data["ci"]["confidence"] == "PARTIAL"
assert data["ci"]["exact_subject_runs"] == []
assert data["ci"]["release_confidence"] == "UNVERIFIED"
assert any("mutable-ref-signal" in value for value in data["security"]["action_pinning"])
assert data["tests"]["confidence"] == "PARTIAL"
assert data["claims"]["items"] and all(item["state"] == "UNVERIFIED" for item in data["claims"]["items"])
assert "workflow executions" in data["coverage"]["explicit_unknowns"]
assert "score" not in data and "global_score" not in data
print("REM extractor tests passed")
