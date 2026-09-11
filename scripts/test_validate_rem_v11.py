from __future__ import annotations

import copy
import subprocess
import tempfile
from pathlib import Path

from rem_extract_exact import extract_exact
from validate_rem_v11 import EvidenceContractError, validate_document

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
    (root / "README.md").write_text("CI tests security release\n", encoding="utf-8")
    git(root, "add", "README.md")
    git(root, "commit", "-m", "fixture")
    sha = git(root, "rev-parse", "HEAD")

    portrait = extract_exact(root, "example/fixture", sha, "main", OBSERVED)
    assert portrait["schema_version"] == "rem/v1.1"
    validate_document(portrait)

    forged = copy.deepcopy(portrait)
    forged["claims"]["items"][0]["state"] = "VERIFIED"
    forged["claims"]["items"][0]["supporting_refs"] = []
    try:
        validate_document(forged)
    except EvidenceContractError:
        pass
    else:
        raise AssertionError("unsupported VERIFIED claim was accepted")

    wrong_subject = copy.deepcopy(portrait)
    wrong_subject["sources"][0]["subject_revision"] = "a" * 40
    try:
        validate_document(wrong_subject)
    except EvidenceContractError:
        pass
    else:
        raise AssertionError("wrong-subject evidence was accepted")

    no_binding = copy.deepcopy(portrait)
    no_binding["sources"] = [s for s in no_binding["sources"] if s["id"] != "subject-binding"]
    try:
        validate_document(no_binding)
    except EvidenceContractError:
        pass
    else:
        raise AssertionError("exact freshness without subject binding was accepted")

print("REM v1.1 evidence contract tests passed")
