from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

from exact_subject import bind_exact_subject, exact_tree_snapshot


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
    (root / ".gitignore").write_text("ignored.yml\n", encoding="utf-8")
    git(root, "add", "README.md", ".gitignore")
    git(root, "commit", "-m", "fixture")
    sha = git(root, "rev-parse", "HEAD")

    exact = bind_exact_subject(root, "example/fixture", sha)
    assert exact["exact"] is True
    assert exact["observed_revision"] == sha
    assert str(exact["content_manifest"]).startswith("sha256:")

    (root / "ignored.yml").write_text("not in committed subject\n", encoding="utf-8")
    still_exact = bind_exact_subject(root, "example/fixture", sha)
    assert still_exact["exact"] is True
    assert still_exact["content_manifest"] == exact["content_manifest"]
    with exact_tree_snapshot(root, sha) as snapshot:
        assert (snapshot / "README.md").read_text(encoding="utf-8") == "fixture\n"
        assert not (snapshot / "ignored.yml").exists()

    wrong_repo = bind_exact_subject(root, "unrelated/project", sha)
    assert wrong_repo["exact"] is False
    assert any("origin" in reason for reason in wrong_repo["reasons"])

    wrong_sha = bind_exact_subject(root, "example/fixture", "a" * 40)
    assert wrong_sha["exact"] is False
    assert any("revision" in reason or "unavailable" in reason for reason in wrong_sha["reasons"])

with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    git(root, "init")
    git(root, "config", "user.email", "audit@example.invalid")
    git(root, "config", "user.name", "Audit Test")
    git(root, "remote", "add", "origin", "https://github.com/example/fixture.git")
    (root / "target.txt").write_text("target\n", encoding="utf-8")
    (root / "link.txt").symlink_to("target.txt")
    git(root, "add", "target.txt", "link.txt")
    git(root, "commit", "-m", "symlink fixture")
    sha = git(root, "rev-parse", "HEAD")
    symlink_subject = bind_exact_subject(root, "example/fixture", sha)
    assert symlink_subject["exact"] is False
    assert any("unavailable" in reason for reason in symlink_subject["reasons"])

with tempfile.TemporaryDirectory() as tmp:
    unavailable = bind_exact_subject(Path(tmp), "example/fixture", "a" * 40)
    assert unavailable["exact"] is False

print("Exact subject binding tests passed")
