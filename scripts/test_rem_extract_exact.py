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
    git(root, "add", "README.md")
    git(root, "commit", "-m", "fixture")
    sha = git(root, "rev-parse", "HEAD")

    exact = extract_exact(root, "example/fixture", sha, "main", OBSERVED)
    assert any(source["id"] == "subject-binding" for source in exact["sources"])
    assert all(source["freshness"]["state"] == "exact" for source in exact["sources"])

    try:
        extract_exact(root, "other/repo", sha, "main", OBSERVED)
    except EvidenceContractError as exc:
        assert "exact subject binding failed" in str(exc)
    else:
        raise AssertionError("wrong-repository exact audit did not fail closed")

print("Exact-bound REM extraction tests passed")
