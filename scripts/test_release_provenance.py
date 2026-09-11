from __future__ import annotations

from copy import deepcopy

from release_provenance import ProvenanceEvidenceError, apply_provenance, validate_provenance

REV = "a" * 40
REPO = "example/repo"
SOURCE = "https://github.com/example/repo/actions/runs/123"

BASE = {
    "subject": {"repository": REPO, "revision": REV},
    "release": {"source_artifact_binding": [], "confidence": "PARTIAL"},
    "overall_portrait": {"verdict": "BOUNDED_REVIEW"},
}

BUNDLE = {
    "version": "audit-evidence/v1",
    "subject": {"repository": REPO, "revision": REV},
    "artifact_provenance": [
        {
            "revision": REV,
            "artifact_digest": "sha256:" + "b" * 64,
            "predicate_type": "https://slsa.dev/provenance/v1",
            "builder_identity": "github-actions:workflow:release",
            "source": SOURCE,
        }
    ],
}

rows = validate_provenance(BUNDLE, REPO, REV)
assert len(rows) == 1
assert rows[0]["revision"] == REV
assert rows[0]["artifact_digest"].startswith("sha256:")
assert rows[0]["predicate_type"] == "https://slsa.dev/provenance/v1"

result = apply_provenance(BASE, BUNDLE)
assert result["overall_portrait"]["verdict"] == "BOUNDED_REVIEW"
assert result["release"]["confidence"] == "PARTIAL"
assert result["artifact_provenance_evidence"]["trust"] == "SUPPLIED_EXACT"
assert result["artifact_provenance_evidence"]["confidence"] == "PARTIAL"
assert "trusted builder identity" in result["artifact_provenance_evidence"]["unknowns"][0]
assert "artifact=sha256:" in result["release"]["source_artifact_binding"][0]

for mutation in (
    "repo",
    "subject_sha",
    "row_sha",
    "digest",
    "predicate",
    "builder",
    "source",
    "cross_repo_source",
):
    broken = deepcopy(BUNDLE)
    if mutation == "repo":
        broken["subject"]["repository"] = "other/repo"
    elif mutation == "subject_sha":
        broken["subject"]["revision"] = "c" * 40
    elif mutation == "row_sha":
        broken["artifact_provenance"][0]["revision"] = "c" * 40
    elif mutation == "digest":
        broken["artifact_provenance"][0]["artifact_digest"] = "sha256:not-a-digest"
    elif mutation == "predicate":
        broken["artifact_provenance"][0]["predicate_type"] = ""
    elif mutation == "builder":
        broken["artifact_provenance"][0]["builder_identity"] = "builder identity with spaces"
    elif mutation == "source":
        broken["artifact_provenance"][0]["source"] = "https://example.com/provenance"
    else:
        broken["artifact_provenance"][0]["source"] = "https://github.com/other/repo/actions/runs/1"
    try:
        validate_provenance(broken, REPO, REV)
    except ProvenanceEvidenceError:
        pass
    else:
        raise AssertionError(f"invalid provenance evidence accepted: {mutation}")

empty = apply_provenance(BASE, {"version": "audit-evidence/v1", "subject": {"repository": REPO, "revision": REV}})
assert "artifact_provenance_evidence" not in empty
assert empty["overall_portrait"]["verdict"] == "BOUNDED_REVIEW"

print("Release provenance evidence tests passed")
