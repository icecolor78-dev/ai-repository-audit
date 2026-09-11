from __future__ import annotations

from copy import deepcopy

from platform_enforcement import PlatformEnforcementError, apply_platform_state, validate_platform_state

REPO = "example/repo"
BASE = {
    "subject": {"repository": REPO, "revision": "a" * 40},
    "ci": {
        "workflows": [".github/workflows/ci.yml", ".github/workflows/release.yml"],
        "confidence": "PARTIAL",
    },
    "overall_portrait": {"verdict": "BOUNDED_REVIEW"},
}

BUNDLE = {
    "version": "audit-evidence/v1",
    "subject": {"repository": REPO, "revision": "a" * 40},
    "branch_enforcement": [
        {
            "branch": "main",
            "observed_at": "2026-09-11T19:25:00Z",
            "pull_request_required": True,
            "required_status_checks": [],
            "conversation_resolution_required": True,
            "force_push_allowed": False,
            "deletion_allowed": False,
            "source": "https://github.com/example/repo/settings/rules",
        }
    ],
}

rows = validate_platform_state(BUNDLE, REPO)
assert rows[0]["branch"] == "main"
assert rows[0]["required_status_checks"] == []
result = apply_platform_state(BASE, BUNDLE)
assert result["overall_portrait"]["verdict"] == "BOUNDED_REVIEW"
assert result["ci"]["confidence"] == "PARTIAL"
assert result["platform_enforcement_evidence"]["trust"] == "SUPPLIED_PLATFORM_STATE"
assert result["platform_enforcement_evidence"]["confidence"] == "PARTIAL"
obs = result["platform_enforcement_evidence"]["observations"][0]
assert obs["missing_required_status_gate"] is True
assert obs["configured_workflows"] == [".github/workflows/ci.yml", ".github/workflows/release.yml"]
assert "time-bound platform evidence" in result["platform_enforcement_evidence"]["unknowns"][0]

with_gate = deepcopy(BUNDLE)
with_gate["branch_enforcement"][0]["required_status_checks"] = ["Public repository checks", "lint"]
obs2 = apply_platform_state(BASE, with_gate)["platform_enforcement_evidence"]["observations"][0]
assert obs2["missing_required_status_gate"] is False
assert obs2["required_status_checks"] == ["Public repository checks", "lint"]

for mutation in ("repo", "source", "cross_repo", "checks", "boolean", "branch", "observed"):
    broken = deepcopy(BUNDLE)
    if mutation == "repo":
        broken["subject"]["repository"] = "other/repo"
    elif mutation == "source":
        broken["branch_enforcement"][0]["source"] = "https://example.com/rules"
    elif mutation == "cross_repo":
        broken["branch_enforcement"][0]["source"] = "https://github.com/other/repo/settings/rules"
    elif mutation == "checks":
        broken["branch_enforcement"][0]["required_status_checks"] = "ci"
    elif mutation == "boolean":
        broken["branch_enforcement"][0]["pull_request_required"] = "true"
    elif mutation == "branch":
        broken["branch_enforcement"][0]["branch"] = ""
    else:
        broken["branch_enforcement"][0]["observed_at"] = ""
    try:
        validate_platform_state(broken, REPO)
    except PlatformEnforcementError:
        pass
    else:
        raise AssertionError(f"invalid platform enforcement evidence accepted: {mutation}")

empty = apply_platform_state(BASE, {"version": "audit-evidence/v1", "subject": {"repository": REPO, "revision": "a" * 40}})
assert "platform_enforcement_evidence" not in empty
assert empty["overall_portrait"]["verdict"] == "BOUNDED_REVIEW"

print("Platform enforcement evidence tests passed")
