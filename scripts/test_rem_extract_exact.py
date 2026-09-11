from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

from rem_extract_exact import extract_exact
from validate_rem_v11 import EvidenceContractError

OBSERVED = "2026-09-11T00:00:00Z"


def git(root: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(root), *args], check=True, capture_output=True, text=True
    ).stdout.strip()


with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    git(root, "init")
    git(root, "config", "user.email", "audit@example.invalid")
    git(root, "config", "user.name", "Audit Test")
    git(root, "remote", "add", "origin", "https://github.com/example/fixture.git")
    (root / "README.md").write_text("CI tests\n", encoding="utf-8")
    (root / "requirements.txt").write_text("demo==1.2.3 --hash=sha256:abcdef\n", encoding="utf-8")
    git(root, "add", "README.md", "requirements.txt")
    git(root, "commit", "-m", "fixture")
    sha = git(root, "rev-parse", "HEAD")

    exact = extract_exact(root, "example/fixture", sha, "main", OBSERVED)
    assert any(source["id"] == "subject-binding" for source in exact["sources"])
    assert all(source["freshness"]["state"] == "exact" for source in exact["sources"])
    assert any(item.startswith("python:demo==1.2.3") for item in exact["supply_chain"]["dependencies"])
    assert any(item.startswith("python-integrity:demo sha256:abcdef") for item in exact["supply_chain"]["provenance"])
    assert exact["supply_chain"]["confidence"] == "PARTIAL"

    try:
        extract_exact(root, "other/repo", sha, "main", OBSERVED)
    except EvidenceContractError as exc:
        assert "exact subject binding failed" in str(exc)
    else:
        raise AssertionError("wrong-repository exact audit did not fail closed")

with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    git(root, "init")
    git(root, "config", "user.email", "audit@example.invalid")
    git(root, "config", "user.name", "Audit Test")
    git(root, "remote", "add", "origin", "https://github.com/example/rst-fixture.git")
    (root / "README.rst").write_text("Security tests are documented.\n", encoding="utf-8")
    git(root, "add", "README.rst")
    git(root, "commit", "-m", "fixture")
    sha = git(root, "rev-parse", "HEAD")
    exact = extract_exact(root, "example/rst-fixture", sha, "main", OBSERVED)
    readme_source = next(source for source in exact["sources"] if source["id"] == "readme")
    assert readme_source["locator"] == "README.rst"
    assert readme_source["supports"] == ["claim-source"]
    assert exact["claims"]["items"][0]["source_ref"] == "readme"
    assert exact["claims"]["items"][0]["state"] == "UNVERIFIED"

print("Exact-bound REM extraction tests passed")
