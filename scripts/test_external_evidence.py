from __future__ import annotations

from copy import deepcopy

from external_evidence import ExternalEvidenceError, apply_bundle, validate_bundle

REV = "a" * 40
REPO = "example/repo"
SOURCE = "https://github.com/example/repo/actions/runs/123"

BASE = {
    "subject": {"repository": REPO, "revision": REV},
    "ci": {"exact_subject_runs": [], "confidence": "PARTIAL"},
    "tests": {"exact_subject_execution": [], "confidence": "PARTIAL"},
    "release": {"source_artifact_binding": [], "confidence": "PARTIAL"},
    "overall_portrait": {"verdict": "BOUNDED_REVIEW"},
}

BUNDLE = {
    "version": "audit-evidence/v1",
    "subject": {"repository": REPO, "revision": REV},
    "observed_at": "2026-09-11T18:00:00Z",
    "workflow_runs": [
        {"name": "ci", "revision": REV, "status": "completed", "conclusion": "success", "source": SOURCE},
        {"name": "negative", "revision": REV, "status": "completed", "conclusion": "failure", "source": SOURCE + "4"},
    ],
    "test_runs": [
        {"suite": "unit", "revision": REV, "status": "completed", "passed": 10, "failed": 1, "skipped": 2, "source": SOURCE + "5"},
    ],
    "release_runs": [
        {"name": "release", "revision": REV, "conclusion": "success", "artifact_digest": "sha256:" + "b" * 64, "source": SOURCE + "6"},
    ],
}

normalized = validate_bundle(BUNDLE, REPO, REV)
assert normalized["workflow_runs"][1]["conclusion"] == "failure"
result = apply_bundle(BASE, BUNDLE)
assert result["external_execution_evidence"]["trust"] == "SUPPLIED_EXACT"
assert len(result["ci"]["exact_subject_runs"]) == 2
assert "failed=1" in result["tests"]["exact_subject_execution"][0]
assert "sha256:" in result["release"]["source_artifact_binding"][0]
assert result["overall_portrait"]["verdict"] == "BOUNDED_REVIEW"
assert result["ci"]["confidence"] == "PARTIAL"
assert "cannot create VERIFIED or global PASS" in result["external_execution_evidence"]["statement"]

for mutation in ("repo", "sha", "source", "cross_repo_source", "count", "premature"):
    broken = deepcopy(BUNDLE)
    if mutation == "repo":
        broken["subject"]["repository"] = "other/repo"
    elif mutation == "sha":
        broken["workflow_runs"][0]["revision"] = "c" * 40
    elif mutation == "source":
        broken["workflow_runs"][0]["source"] = "https://example.com/not-github"
    elif mutation == "cross_repo_source":
        broken["workflow_runs"][0]["source"] = "https://github.com/other/repo/actions/runs/9"
    elif mutation == "count":
        broken["test_runs"][0]["failed"] = -1
    else:
        broken["workflow_runs"][0]["status"] = "in_progress"
        broken["workflow_runs"][0]["conclusion"] = "success"
    try:
        validate_bundle(broken, REPO, REV)
    except ExternalEvidenceError:
        pass
    else:
        raise AssertionError(f"invalid supplied evidence accepted: {mutation}")

print("External execution evidence tests passed")
