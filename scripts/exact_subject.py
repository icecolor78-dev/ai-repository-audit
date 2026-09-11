from __future__ import annotations

import hashlib
import re
import shutil
import subprocess
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

SHA_RE = re.compile(r"^[0-9a-f]{40}$")
REGULAR_MODES = {"100644", "100755"}


def _git(root: Path, *args: str, text: bool = True):
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        check=True,
        capture_output=True,
        text=text,
    )
    return result.stdout.strip() if text else result.stdout


def _canonical_github_repo(remote: str) -> str | None:
    value = remote.strip().removesuffix(".git")
    for prefix in ("https://github.com/", "http://github.com/", "ssh://git@github.com/"):
        if value.startswith(prefix):
            return value[len(prefix):]
    if value.startswith("git@github.com:"):
        return value[len("git@github.com:"):]
    return None


def _tree_entries(root: Path, revision: str) -> list[tuple[str, str, str]]:
    raw = _git(root, "ls-tree", "-rz", "--full-tree", revision, text=False)
    entries: list[tuple[str, str, str]] = []
    for row in raw.split(b"\0"):
        if not row:
            continue
        meta, raw_name = row.split(b"\t", 1)
        mode, kind, object_sha = meta.decode("ascii").split(" ")
        name = raw_name.decode("utf-8", errors="strict")
        if kind != "blob" or mode not in REGULAR_MODES:
            raise ValueError(f"unsupported exact-scan entry: {mode} {kind} {name}")
        entries.append((name, mode, object_sha))
    return sorted(entries)


def _tree_manifest(root: Path, revision: str) -> str:
    digest = hashlib.sha256()
    for name, mode, object_sha in _tree_entries(root, revision):
        data = _git(root, "cat-file", "blob", object_sha, text=False)
        digest.update(name.encode("utf-8"))
        digest.update(b"\0")
        digest.update(mode.encode("ascii"))
        digest.update(b"\0")
        digest.update(hashlib.sha256(data).digest())
    return "sha256:" + digest.hexdigest()


def bind_exact_subject(root: Path, repository: str, revision: str) -> dict[str, str | bool | list[str]]:
    """Bind a requested GitHub repository/SHA to one immutable Git tree.

    The attested manifest is computed from Git objects, not working-tree bytes. Callers
    must scan a snapshot materialized from the same tree rather than the mutable worktree.
    """
    reasons: list[str] = []
    if not SHA_RE.fullmatch(revision):
        return {"exact": False, "reasons": ["requested revision is not a full lowercase SHA"]}
    try:
        top = Path(_git(root, "rev-parse", "--show-toplevel")).resolve()
        if top != root.resolve():
            reasons.append("scan root is not the Git repository root")
        head = _git(root, "rev-parse", "HEAD")
        tree = _git(root, "rev-parse", f"{revision}^{{tree}}")
        remote = _git(root, "remote", "get-url", "origin")
        observed_repo = _canonical_github_repo(remote)
        if head != revision:
            reasons.append("requested revision does not equal local HEAD")
        if observed_repo is None or observed_repo.casefold() != repository.casefold():
            reasons.append("origin does not match requested GitHub repository")
        manifest = _tree_manifest(root, revision)
    except (OSError, subprocess.CalledProcessError, UnicodeDecodeError, ValueError) as exc:
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


@contextmanager
def exact_tree_snapshot(root: Path, revision: str) -> Iterator[Path]:
    """Materialize exactly the regular-file blobs from one Git tree into a temp root.

    Ignored/untracked working-tree files cannot enter this snapshot. Symlinks, gitlinks
    and other non-regular entries fail closed until an explicit scan policy exists.
    """
    tmp = Path(tempfile.mkdtemp(prefix="audit-exact-tree-"))
    try:
        for name, mode, object_sha in _tree_entries(root, revision):
            target = tmp / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(_git(root, "cat-file", "blob", object_sha, text=False))
            if mode == "100755":
                target.chmod(target.stat().st_mode | 0o100)
        yield tmp
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
