from __future__ import annotations

import re
from copy import deepcopy
from typing import Any
from urllib.parse import urlparse

SHA_RE = re.compile(r"^[0-9a-f]{40}$")
DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
WORKFLOW_STATUS = {"queued", "in_progress", "completed"}
CONCLUSIONS = {"success", "failure", "cancelled", "skipped", "timed_out", "action_required", "neutral", "stale", "startup_failure", None}


class ExternalEvidenceError(ValueError):
    pass


def _public_github_url(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value:
        raise ExternalEvidenceError(f"{field} requires a source URL")
    parsed = urlparse(value)
    if parsed.scheme != "https" or parsed.hostname not in {"github.com", "api.github.com"}:
        raise ExternalEvidenceError(f"{field} must use a public GitHub HTTPS source")
    return value


def _exact_revision(value: Any, expected: str, field: str) -> str:
    if not isinstance(value, str) or not SHA_RE.fullmatch(value):
        raise ExternalEvidenceError(f"{field} must be a full lowercase SHA")
    if value != expected:
        raise ExternalEvidenceError(f"{field} does not match the audited revision")
    return value


def _nonnegative_int(value: Any, field: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise ExternalEvidenceError(f"{field} must be a non-negative integer")
    return value


def validate_bundle(bundle: Any, repository: str, revision: str) -> dict:
    if not isinstance(bundle, dict):
        raise ExternalEvidenceError("evidence bundle must be an object")
    if bundle.get("version") != "audit-evidence/v1":
        raise ExternalEvidenceError("unsupported evidence bundle version")
    subject = bundle.get("subject")
    if not isinstance(subject, dict):
        raise ExternalEvidenceError("evidence bundle requires subject")
    if subject.get("repository") != repository:
        raise ExternalEvidenceError("evidence bundle repository does not match audited repository")
    _exact_revision(subject.get("revision"), revision, "subject.revision")
    observed_at = bundle.get("observed_at")
    if not isinstance(observed_at, str) or not observed_at.strip():
        raise ExternalEvidenceError("evidence bundle requires observed_at")

    normalized = {
        "version": "audit-evidence/v1",
        "subject": {"repository": repository, "revision": revision},
        "observed_at": observed_at,
        "workflow_runs": [],
        "test_runs": [],
        "release_runs": [],
    }

    for index, item in enumerate(bundle.get("workflow_runs", [])):
        if not isinstance(item, dict):
            raise ExternalEvidenceError(f"workflow_runs[{index}] must be an object")
        name = item.get("name")
        if not isinstance(name, str) or not name.strip():
            raise ExternalEvidenceError(f"workflow_runs[{index}].name is required")
        status = item.get("status")
        conclusion = item.get("conclusion")
        if status not in WORKFLOW_STATUS:
            raise ExternalEvidenceError(f"workflow_runs[{index}].status is unsupported")
        if conclusion not in CONCLUSIONS:
            raise ExternalEvidenceError(f"workflow_runs[{index}].conclusion is unsupported")
        if status != "completed" and conclusion is not None:
            raise ExternalEvidenceError(f"workflow_runs[{index}] cannot have a conclusion before completion")
        normalized["workflow_runs"].append({
            "name": name.strip(),
            "revision": _exact_revision(item.get("revision"), revision, f"workflow_runs[{index}].revision"),
            "status": status,
            "conclusion": conclusion,
            "source": _public_github_url(item.get("source"), f"workflow_runs[{index}].source"),
        })

    for index, item in enumerate(bundle.get("test_runs", [])):
        if not isinstance(item, dict):
            raise ExternalEvidenceError(f"test_runs[{index}] must be an object")
        suite = item.get("suite")
        if not isinstance(suite, str) or not suite.strip():
            raise ExternalEvidenceError(f"test_runs[{index}].suite is required")
        status = item.get("status")
        if status != "completed":
            raise ExternalEvidenceError(f"test_runs[{index}] must be completed to supply result counts")
        normalized["test_runs"].append({
            "suite": suite.strip(),
            "revision": _exact_revision(item.get("revision"), revision, f"test_runs[{index}].revision"),
            "status": status,
            "passed": _nonnegative_int(item.get("passed"), f"test_runs[{index}].passed"),
            "failed": _nonnegative_int(item.get("failed"), f"test_runs[{index}].failed"),
            "skipped": _nonnegative_int(item.get("skipped"), f"test_runs[{index}].skipped"),
            "source": _public_github_url(item.get("source"), f"test_runs[{index}].source"),
        })

    for index, item in enumerate(bundle.get("release_runs", [])):
        if not isinstance(item, dict):
            raise ExternalEvidenceError(f"release_runs[{index}] must be an object")
        name = item.get("name")
        if not isinstance(name, str) or not name.strip():
            raise ExternalEvidenceError(f"release_runs[{index}].name is required")
        conclusion = item.get("conclusion")
        if conclusion not in CONCLUSIONS - {None}:
            raise ExternalEvidenceError(f"release_runs[{index}].conclusion is unsupported")
        row = {
            "name": name.strip(),
            "revision": _exact_revision(item.get("revision"), revision, f"release_runs[{index}].revision"),
            "conclusion": conclusion,
            "source": _public_github_url(item.get("source"), f"release_runs[{index}].source"),
        }
        digest = item.get("artifact_digest")
        if digest is not None:
            if not isinstance(digest, str) or not DIGEST_RE.fullmatch(digest):
                raise ExternalEvidenceError(f"release_runs[{index}].artifact_digest must be sha256:<64 lowercase hex>")
            row["artifact_digest"] = digest
        normalized["release_runs"].append(row)

    return normalized


def apply_bundle(portrait: dict, bundle: Any) -> dict:
    repository = portrait["subject"]["repository"]
    revision = portrait["subject"]["revision"]
    data = validate_bundle(bundle, repository, revision)
    result = deepcopy(portrait)

    workflow_rows = [
        f"SUPPLIED_EXACT name={row['name']} status={row['status']} conclusion={row['conclusion']} source={row['source']}"
        for row in data["workflow_runs"]
    ]
    test_rows = [
        f"SUPPLIED_EXACT suite={row['suite']} passed={row['passed']} failed={row['failed']} skipped={row['skipped']} source={row['source']}"
        for row in data["test_runs"]
    ]
    release_rows = []
    for row in data["release_runs"]:
        if "artifact_digest" in row:
            release_rows.append(
                f"SUPPLIED_EXACT revision={revision} artifact={row['artifact_digest']} source={row['source']}"
            )

    result["ci"]["exact_subject_runs"] = sorted(set(result["ci"].get("exact_subject_runs", []) + workflow_rows))
    result["tests"]["exact_subject_execution"] = sorted(set(result["tests"].get("exact_subject_execution", []) + test_rows))
    result["release"]["source_artifact_binding"] = sorted(set(result["release"].get("source_artifact_binding", []) + release_rows))
    result["external_execution_evidence"] = {
        "trust": "SUPPLIED_EXACT",
        "subject": data["subject"],
        "observed_at": data["observed_at"],
        "workflow_runs": data["workflow_runs"],
        "test_runs": data["test_runs"],
        "release_runs": data["release_runs"],
        "statement": "Evidence is caller-supplied and exact-subject validated. It is not independently fetched or cryptographically authenticated by this audit path and cannot create VERIFIED or global PASS by presence alone.",
    }
    return result
