from __future__ import annotations

import re
from copy import deepcopy
from typing import Any
from urllib.parse import urlparse

SHA_RE = re.compile(r"^[0-9a-f]{40}$")
DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
PREDICATE_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/+-]{0,255}$")


class ProvenanceEvidenceError(ValueError):
    pass


def _same_repo_public_github_url(value: Any, field: str, repository: str) -> str:
    if not isinstance(value, str) or not value:
        raise ProvenanceEvidenceError(f"{field} requires a source URL")
    parsed = urlparse(value)
    if parsed.scheme != "https" or parsed.hostname not in {"github.com", "api.github.com"}:
        raise ProvenanceEvidenceError(f"{field} must use a public GitHub HTTPS source")
    owner, name = repository.split("/", 1)
    parts = [part for part in parsed.path.split("/") if part]
    if parsed.hostname == "github.com":
        matches = len(parts) >= 2 and parts[0].casefold() == owner.casefold() and parts[1].casefold() == name.casefold()
    else:
        matches = len(parts) >= 3 and parts[0] == "repos" and parts[1].casefold() == owner.casefold() and parts[2].casefold() == name.casefold()
    if not matches:
        raise ProvenanceEvidenceError(f"{field} does not belong to the audited GitHub repository")
    return value


def _exact_revision(value: Any, expected: str, field: str) -> str:
    if not isinstance(value, str) or not SHA_RE.fullmatch(value):
        raise ProvenanceEvidenceError(f"{field} must be a full lowercase SHA")
    if value != expected:
        raise ProvenanceEvidenceError(f"{field} does not match the audited revision")
    return value


def _digest(value: Any, field: str) -> str:
    if not isinstance(value, str) or not DIGEST_RE.fullmatch(value):
        raise ProvenanceEvidenceError(f"{field} must be sha256:<64 lowercase hex>")
    return value


def _token(value: Any, field: str) -> str:
    if not isinstance(value, str) or not PREDICATE_RE.fullmatch(value.strip()):
        raise ProvenanceEvidenceError(f"{field} must be a bounded non-empty identifier")
    return value.strip()


def validate_provenance(bundle: Any, repository: str, revision: str) -> list[dict]:
    if not isinstance(bundle, dict):
        raise ProvenanceEvidenceError("evidence bundle must be an object")
    if bundle.get("version") != "audit-evidence/v1":
        raise ProvenanceEvidenceError("unsupported evidence bundle version")
    subject = bundle.get("subject")
    if not isinstance(subject, dict) or subject.get("repository") != repository:
        raise ProvenanceEvidenceError("evidence bundle repository does not match audited repository")
    _exact_revision(subject.get("revision"), revision, "subject.revision")

    result: list[dict] = []
    for index, item in enumerate(bundle.get("artifact_provenance", [])):
        if not isinstance(item, dict):
            raise ProvenanceEvidenceError(f"artifact_provenance[{index}] must be an object")
        result.append({
            "revision": _exact_revision(item.get("revision"), revision, f"artifact_provenance[{index}].revision"),
            "artifact_digest": _digest(item.get("artifact_digest"), f"artifact_provenance[{index}].artifact_digest"),
            "predicate_type": _token(item.get("predicate_type"), f"artifact_provenance[{index}].predicate_type"),
            "builder_identity": _token(item.get("builder_identity"), f"artifact_provenance[{index}].builder_identity"),
            "source": _same_repo_public_github_url(item.get("source"), f"artifact_provenance[{index}].source", repository),
        })
    return result


def apply_provenance(portrait: dict, bundle: Any) -> dict:
    repository = portrait["subject"]["repository"]
    revision = portrait["subject"]["revision"]
    rows = validate_provenance(bundle, repository, revision)
    result = deepcopy(portrait)
    if not rows:
        return result

    rendered = [
        "SUPPLIED_EXACT "
        f"revision={row['revision']} artifact={row['artifact_digest']} "
        f"predicate={row['predicate_type']} builder={row['builder_identity']} source={row['source']}"
        for row in rows
    ]
    release = result.setdefault("release", {})
    release["source_artifact_binding"] = sorted(set(release.get("source_artifact_binding", []) + rendered))
    result["artifact_provenance_evidence"] = {
        "trust": "SUPPLIED_EXACT",
        "records": rows,
        "confidence": "PARTIAL",
        "unknowns": [
            "caller-supplied provenance metadata does not prove signature validity, trusted builder identity, reproducible build, deployment success, vulnerability absence, or release authorization"
        ],
    }
    return result
