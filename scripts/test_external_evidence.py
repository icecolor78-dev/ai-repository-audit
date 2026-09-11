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
    "runtime_measurements": [
        {"kind": "latency", "value": 125.5, "unit": "ms", "sample_count": 40, "environment": "public-ci-fixture", "revision": REV, "source": SOURCE + "7"},
        {"kind": "memory", "value": 96, "unit": "MiB", "sample_count": 3, "environment": "public-ci-fixture", "revision": REV, "source": SOURCE + "8"},
    ],
    "observability_artifacts": [
        {"kind": "logs", "revision": REV, "source": SOURCE + "9"},
        {"kind": "traces", "revision": REV, "source": SOURCE + "10"},
    ],
}

normalized = validate_bundle(BUNDLE, REPO, REV)
assert normalized["workflow_runs"][1]["conclusion"] == "failure"
assert normalized["runtime_measurements"][0]["unit"] == "ms"
result = apply_bundle(BASE, BUNDLE)
assert result["external_execution_evidence"]["trust"] == "SUPPLIED_EXACT"
assert len(result["ci"]["exact_subject_runs"]) == 2
assert "failed=1" in result["tests"]["exact_subject_execution"][0]
assert "sha256:" in result["release"]["source_artifact_binding"][0]
assert result["runtime_evidence"]["confidence"] == "PARTIAL"
assert len(result["runtime_evidence"]["measurements"]) == 2
assert len(result["runtime_evidence"]["observability_artifacts"]) == 2
assert result["overall_portrait"]["verdict"] == "BOUNDED_REVIEW"
assert result["ci"]["confidence"] == "PARTIAL"
assert "cannot create VERIFIED or global PASS" in result["external_execution_evidence"]["statement"]
assert "do not prove production representativeness" in result["runtime_evidence"]["unknowns"][0]

for mutation in (
    "repo",
    "sha",
    "source",
    "cross_repo_source",
    "count",
    "premature",
    "runtime_negative",
    "runtime_nan",
    "runtime_pos_inf",
    "runtime_neg_inf",
    "runtime_zero_samples",
    "runtime_unit",
    "runtime_repo",
):
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
    elif mutation == "premature":
        broken["workflow_runs"][0]["status"] = "in_progress"
        broken["workflow_runs"][0]["conclusion"] = "success"
    elif mutation == "runtime_negative":
        broken["runtime_measurements"][0]["value"] = -1
    elif mutation == "runtime_nan":
        broken["runtime_measurements"][0]["value"] = float("nan")
    elif mutation == "runtime_pos_inf":
        broken["runtime_measurements"][0]["value"] = float("inf")
    elif mutation == "runtime_neg_inf":
        broken["runtime_measurements"][0]["value"] = float("-inf")
    elif mutation == "runtime_zero_samples":
        broken["runtime_measurements"][0]["sample_count"] = 0
    elif mutation == "runtime_unit":
        broken["runtime_measurements"][0]["unit"] = "fast"
    else:
        broken["runtime_measurements"][0]["source"] = "https://github.com/other/repo/actions/runs/10"
    try:
        validate_bundle(broken, REPO, REV)
    except ExternalEvidenceError:
        pass
    else:
        raise AssertionError(f"invalid supplied evidence accepted: {mutation}")

print("External execution evidence tests passed")
