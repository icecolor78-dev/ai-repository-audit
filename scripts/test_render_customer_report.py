from __future__ import annotations

from render_customer_report import render_customer_report

PORTRAIT = {
    "subject": {"repository": "example/public-repo", "revision": "a" * 40, "observed_at": "2026-09-11T00:00:00Z"},
    "overall_portrait": {
        "verdict": "BOUNDED_REVIEW",
        "statement": "Static and supplied evidence are bounded; runtime guarantees are not established.",
        "findings": [
            {"severity": "HIGH", "kind": "example-risk", "locator": ".github/workflows/ci.yml", "confidence": "HIGH", "detail": "A bounded finding."}
        ],
        "explicit_unknowns": [
            {"dimension": "tests", "detail": "Exact execution coverage remains UNVERIFIED."},
            {"dimension": "release", "detail": "Artifact provenance remains UNVERIFIED."},
        ],
        "remediation": [
            {"priority": "P1", "action": "Add exact evidence for the release path.", "verification": "Re-run on the exact revision."}
        ],
    },
    "assurance_v2": {
        "domains": {
            "tests": {"state": "UNVERIFIED"},
            "release": {"state": "CONTRADICTED"},
            "security": {"state": "PARTIAL"},
        }
    },
    "external_execution_evidence": {
        "trust": "SUPPLIED_EXACT",
        "statement": "Caller-supplied exact-subject evidence; not independently authenticated.",
    },
    "runtime_evidence": {"trust": "SUPPLIED_EXACT", "confidence": "PARTIAL"},
    "artifact_provenance_evidence": {
        "trust": "SUPPLIED_EXACT",
        "confidence": "PARTIAL",
        "unknowns": ["Supplied provenance does not establish trusted builder or release authorization."],
    },
}

first = render_customer_report(PORTRAIT)
second = render_customer_report(PORTRAIT)
assert first == second
assert "**BOUNDED_REVIEW**" in first
assert "CONTRADICTED" in first
assert "UNVERIFIED" in first
assert "SUPPLIED_EXACT" in first
assert "Artifact provenance trust" in first
assert "trusted builder or release authorization" in first
assert "global_score" not in first
assert "**PASS**" not in first
assert "Exact execution coverage remains UNVERIFIED." in first
assert "Artifact provenance remains UNVERIFIED." in first
assert "does not create new evidence" in first

empty = render_customer_report({
    "subject": {"repository": "example/public-repo", "revision": "b" * 40},
    "overall_portrait": {"verdict": "HOLD", "findings": [], "explicit_unknowns": [], "remediation": []},
})
assert "**HOLD**" in empty
assert "**PASS**" not in empty
assert "not a guarantee of defect or vulnerability absence" in empty
assert "does not create a PASS state" in empty

print("Customer report renderer tests passed")
