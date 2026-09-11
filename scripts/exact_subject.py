from __future__ import annotations

import hashlib
import re
import subprocess
from pathlib import Path

SHA_RE = re.compile(r"^[0-9a-f]{40}$")


def _git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def _canonical_github_repo(remote: str) -> str | None:
    value = remote.strip().removesuffix(".git")
    for prefix in ("https://github.com/", "http://github.com/", "ssh://git@github.com/"):
        if value.startswith(prefix):
            return value[len(prefix):]
    if value.startswith("git@github.com:"):
        return value[len("git@github.com:"):]
    return None


def _tracked_manifest(root: Path) -> str:
    names = _git(root, "ls-files", "-z").split("\0")
    digest = hashlib.sha256()
    for name in sorted(item for item in names if item):
        path = root / name
        if not path.is_file():
            raise ValueError(f"tracked non-file entry cannot be attested: {name}")
        data = path.read_bytes()
        digest.update(name.encode("utf-8"))
        digest.update(b"\0")
        digest.update(hashlib.sha256(data).digest())
    return "sha256:" + digest.hexdigest()


def bind_exact_subject(root: Path, repository: str, revision: str) -> dict[str, str | bool | list[str]]:
    """Bind a requested GitHub repository/SHA to the clean local Git tree being scanned.

    Failure is represented explicitly. Callers must never convert a non-exact result into
    exact freshness merely because the requested revision has a valid SHA shape.
    """
    reasons: list[str] = []
    if not SHA_RE.fullmatch(revision):
        return {"exact": False, "reasons": ["requested revision is not a full lowercase SHA"]}
    try:
        top = Path(_git(root, "rev-parse", "--show-toplevel")).resolve()
        if top != root.resolve():
            reasons.append("scan root is not the Git repository root")
        head = _git(root, "rev-parse", "HEAD")
        tree = _git(root, "rev-parse", "HEAD^{tree}")
        status = _git(root, "status", "--porcelain=v1", "--untracked-files=all")
        remote = _git(root, "remote", "get-url", "origin")
        observed_repo = _canonical_github_repo(remote)
        if head != revision:
            reasons.append("requested revision does not equal local HEAD")
        if observed_repo is None or observed_repo.casefold() != repository.casefold():
            reasons.append("origin does not match requested GitHub repository")
        if status:
            reasons.append("working tree is dirty or contains untracked files")
        manifest = _tracked_manifest(root)
    except (OSError, subprocess.CalledProcessError, ValueError) as exc:
        return {"exact": False, "reasons": [f"Git subject binding unavailable: {type(exc).__name__}"]}

    exact = not reasons
    return {
        "exact": exact,
        "reasons": reasons,
        "observed_repository": observed_repo or "",
        "observed_revision": head,
        "git_tree": tree,
        "content_manifest": manifest,
    }
