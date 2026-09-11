from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from claims_exact import extract_readme_claims
from exact_subject import bind_exact_subject
from rem_extract import extract
from workflow_structured import analyze_workflows


def extract_exact(
    root: Path,
    repository: str,
    revision: str,
    default_branch: str,
    observed_at: str,
) -> dict:
    portrait = extract(root, repository, revision, default_branch, observed_at)
    portrait["schema_version"] = "rem/v1.1"
    portrait["claims"]["items"] = extract_readme_claims(root)
    ci, security, release = analyze_workflows(root)
    portrait["ci"] = ci
    portrait["security"] = security
    portrait["release"] = release

    binding = bind_exact_subject(root, repository, revision)
    if binding["exact"] is True:
        reason = (
            "verified clean Git subject; "
            f"tree={binding['git_tree']}; manifest={binding['content_manifest']}"
        )
        for source in portrait["sources"]:
            source["freshness"] = {"state": "exact", "reason": reason}
        portrait["sources"].append({
            "id": "subject-binding",
            "kind": "commit",
            "subject_revision": revision,
            "locator": "git:HEAD",
            "observed_at": observed_at,
            "freshness": {"state": "exact", "reason": reason},
            "access": {"state": "accessible"},
            "content_digest": str(binding["content_manifest"]),
            "supports": ["repository identity", "exact revision", "clean scanned Git tree"],
            "limits": ["does not prove external runtime or hosted CI execution"],
        })
    else:
        detail = "; ".join(str(item) for item in binding["reasons"])
        for source in portrait["sources"]:
            source["freshness"] = {
                "state": "unknown",
                "reason": f"exact subject binding failed: {detail}",
            }
        portrait["coverage"]["explicit_unknowns"].append(
            f"exact subject binding failed: {detail}"
        )
    return portrait


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
