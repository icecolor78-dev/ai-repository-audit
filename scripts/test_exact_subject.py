from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

from exact_subject import bind_exact_subject


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
    (root / "README.md").write_text("fixture\n", encoding="utf-8")
    git(root, "add", "README.md")
    git(root, "commit", "-m", "fixture")
    sha = git(root, "rev-parse", "HEAD")

    exact = bind_exact_subject(root, "example/fixture", sha)
    assert exact["exact"] is True
    assert exact["observed_revision"] == sha
    assert str(exact["content_manifest"]).startswith("sha256:")

    wrong_repo = bind_exact_subject(root, "unrelated/project", sha)
    assert wrong_repo["exact"] is False
    assert any("origin" in reason for reason in wrong_repo["reasons"])

    wrong_sha = bind_exact_subject(root, "example/fixture", "a" * 40)
    assert wrong_sha["exact"] is False
    assert any("revision" in reason for reason in wrong_sha["reasons"])

    (root / "untracked.txt").write_text("not in subject\n", encoding="utf-8")
    dirty = bind_exact_subject(root, "example/fixture", sha)
    assert dirty["exact"] is False
    assert any("dirty" in reason for reason in dirty["reasons"])

with tempfile.TemporaryDirectory() as tmp:
    unavailable = bind_exact_subject(Path(tmp), "example/fixture", "a" * 40)
    assert unavailable["exact"] is False

print("Exact subject binding tests passed")
