from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from claims_exact import extract_readme_claims
from exact_subject import bind_exact_subject, exact_tree_snapshot
from rem_extract import extract
from test_depth_exact import profile_tests
from validate_rem_v11 import EvidenceContractError, validate_document
from workflow_structured import analyze_workflows


def build_exact_rem(
    scan_root: Path,
    repository: str,
    revision: str,
    default_branch: str,
    observed_at: str,
    binding: dict,
) -> dict:
    portrait = extract(scan_root, repository, revision, default_branch, observed_at)
    portrait["schema_version"] = "rem/v1.1"
    portrait["claims"]["items"] = extract_readme_claims(scan_root)
    portrait["tests"] = profile_tests(scan_root)
    ci, security, release = analyze_workflows(scan_root)
    portrait["ci"] = ci
    portrait["security"] = security
    portrait["release"] = release

    if binding.get("exact") is not True:
        raise EvidenceContractError("integrated exact audit requires a verified Git subject binding")

    reason = (
        "verified immutable Git-tree subject; "
        f"tree={binding['git_tree']}; manifest={binding['content_manifest']}"
    )
    for source in portrait["sources"]:
        source["freshness"] = {"state": "exact", "reason": reason}
        if source["kind"] == "repository_file":
            source["supports"] = ["claim-source"]
        elif source["kind"] == "workflow_definition":
            source["supports"] = ["ci", "security", "release"]
    portrait["sources"].append({
        "id": "subject-binding",
        "kind": "commit",
        "subject_revision": revision,
        "locator": "git:tree",
        "observed_at": observed_at,
        "freshness": {"state": "exact", "reason": reason},
        "access": {"state": "accessible"},
        "content_digest": str(binding["content_manifest"]),
        "supports": ["subject"],
        "limits": ["does not prove external runtime or hosted CI execution"],
    })
    validate_document(portrait)
    return portrait


def extract_exact(
    root: Path,
    repository: str,
    revision: str,
    default_branch: str,
    observed_at: str,
) -> dict:
    binding = bind_exact_subject(root, repository, revision)
    if binding.get("exact") is not True:
        detail = "; ".join(str(item) for item in binding.get("reasons", []))
        raise EvidenceContractError(f"exact subject binding failed: {detail}")
    with exact_tree_snapshot(root, revision) as scan_root:
        return build_exact_rem(
            scan_root, repository, revision, default_branch, observed_at, binding
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--revision", required=True)
    parser.add_argument("--default-branch", default="main")
    parser.add_argument("--observed-at", default=None)
    args = parser.parse_args()
    observed = args.observed_at or datetime.now(timezone.utc).replace(
        microsecond=0
    ).isoformat().replace("+00:00", "Z")
    portrait = extract_exact(
        args.root.resolve(), args.repository, args.revision, args.default_branch, observed
    )
    print(json.dumps(portrait, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
