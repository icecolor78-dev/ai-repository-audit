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


def rejected(data: dict) -> None:
    try:
        validate_document(data)
    except EvidenceContractError:
        return
    raise AssertionError("invalid evidence contract was accepted")


with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    git(root, "init")
    git(root, "config", "user.email", "audit@example.invalid")
    git(root, "config", "user.name", "Audit Test")
    git(root, "remote", "add", "origin", "https://github.com/example/fixture.git")
    (root / "README.md").write_text("CI tests security release\n", encoding="utf-8")
    (root / ".github/workflows").mkdir(parents=True)
    (root / ".github/workflows/ci.yml").write_text("on: [push]\njobs: {}\n", encoding="utf-8")
    git(root, "add", ".")
    git(root, "commit", "-m", "fixture")
    sha = git(root, "rev-parse", "HEAD")

    portrait = extract_exact(root, "example/fixture", sha, "main", OBSERVED)
    assert portrait["schema_version"] == "rem/v1.1"
    validate_document(portrait)

    unsupported = copy.deepcopy(portrait)
    unsupported["claims"]["items"][0]["state"] = "VERIFIED"
    unsupported["claims"]["items"][0]["supporting_refs"] = []
    rejected(unsupported)

    self_supported = copy.deepcopy(portrait)
    claim = self_supported["claims"]["items"][0]
    claim["state"] = "VERIFIED"
    claim["supporting_refs"] = [claim["source_ref"]]
    rejected(self_supported)

    contradicted_verified = copy.deepcopy(portrait)
    claim = contradicted_verified["claims"]["items"][0]
    claim["state"] = "VERIFIED"
    claim["supporting_refs"] = ["workflow-1"]
    claim["contradicting_refs"] = ["workflow-1"]
    rejected(contradicted_verified)

    non_probative = copy.deepcopy(portrait)
    claim = non_probative["claims"]["items"][0]
    claim["state"] = "VERIFIED"
    claim["supporting_refs"] = ["subject-binding"]
    rejected(non_probative)

    contradicted_without_ref = copy.deepcopy(portrait)
    claim = contradicted_without_ref["claims"]["items"][0]
    claim["state"] = "CONTRADICTED"
    claim["contradicting_refs"] = []
    rejected(contradicted_without_ref)

    wrong_subject = copy.deepcopy(portrait)
    wrong_subject["sources"][0]["subject_revision"] = "a" * 40
    rejected(wrong_subject)

    no_binding = copy.deepcopy(portrait)
    no_binding["sources"] = [s for s in no_binding["sources"] if s["id"] != "subject-binding"]
    rejected(no_binding)

print("REM v1.1 evidence contract tests passed")
