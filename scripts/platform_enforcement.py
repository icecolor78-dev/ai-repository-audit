from __future__ import annotations

from copy import deepcopy
from typing import Any
from urllib.parse import urlparse


class PlatformEnforcementError(ValueError):
    pass


def _same_repo_public_github_url(value: Any, field: str, repository: str) -> str:
    if not isinstance(value, str) or not value:
        raise PlatformEnforcementError(f"{field} requires a source URL")
    parsed = urlparse(value)
    if parsed.scheme != "https" or parsed.hostname not in {"github.com", "api.github.com"}:
        raise PlatformEnforcementError(f"{field} must use a public GitHub HTTPS source")
    owner, name = repository.split("/", 1)
    parts = [part for part in parsed.path.split("/") if part]
    if parsed.hostname == "github.com":
        matches = len(parts) >= 2 and parts[0].casefold() == owner.casefold() and parts[1].casefold() == name.casefold()
    else:
        matches = len(parts) >= 3 and parts[0] == "repos" and parts[1].casefold() == owner.casefold() and parts[2].casefold() == name.casefold()
    if not matches:
        raise PlatformEnforcementError(f"{field} does not belong to the audited GitHub repository")
    return value


def _bool(value: Any, field: str) -> bool:
    if not isinstance(value, bool):
        raise PlatformEnforcementError(f"{field} must be boolean")
    return value


def _name(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip() or len(value.strip()) > 200:
        raise PlatformEnforcementError(f"{field} must be a bounded non-empty string")
    return value.strip()


def validate_platform_state(bundle: Any, repository: str) -> list[dict]:
    if not isinstance(bundle, dict):
        raise PlatformEnforcementError("evidence bundle must be an object")
    if bundle.get("version") != "audit-evidence/v1":
        raise PlatformEnforcementError("unsupported evidence bundle version")
    subject = bundle.get("subject")
    if not isinstance(subject, dict) or subject.get("repository") != repository:
        raise PlatformEnforcementError("evidence bundle repository does not match audited repository")

    result: list[dict] = []
    for index, item in enumerate(bundle.get("branch_enforcement", [])):
        if not isinstance(item, dict):
            raise PlatformEnforcementError(f"branch_enforcement[{index}] must be an object")
        observed_at = item.get("observed_at")
        if not isinstance(observed_at, str) or not observed_at.strip():
            raise PlatformEnforcementError(f"branch_enforcement[{index}].observed_at is required")
        checks = item.get("required_status_checks")
        if not isinstance(checks, list) or any(not isinstance(x, str) or not x.strip() for x in checks):
            raise PlatformEnforcementError(f"branch_enforcement[{index}].required_status_checks must be a list of non-empty strings")
        normalized_checks = sorted(set(x.strip() for x in checks))
        result.append({
            "branch": _name(item.get("branch"), f"branch_enforcement[{index}].branch"),
            "observed_at": observed_at.strip(),
            "pull_request_required": _bool(item.get("pull_request_required"), f"branch_enforcement[{index}].pull_request_required"),
            "required_status_checks": normalized_checks,
            "conversation_resolution_required": _bool(item.get("conversation_resolution_required"), f"branch_enforcement[{index}].conversation_resolution_required"),
            "force_push_allowed": _bool(item.get("force_push_allowed"), f"branch_enforcement[{index}].force_push_allowed"),
            "deletion_allowed": _bool(item.get("deletion_allowed"), f"branch_enforcement[{index}].deletion_allowed"),
            "source": _same_repo_public_github_url(item.get("source"), f"branch_enforcement[{index}].source", repository),
        })
    return result


def apply_platform_state(portrait: dict, bundle: Any) -> dict:
    repository = portrait["subject"]["repository"]
    rows = validate_platform_state(bundle, repository)
    result = deepcopy(portrait)
    if not rows:
        return result

    configured = set()
    ci = result.get("ci", {})
    for workflow in ci.get("workflows", []):
        configured.add(str(workflow))

    observations = []
    for row in rows:
        missing_gate = not row["required_status_checks"]
        observations.append({
            **row,
            "configured_workflows": sorted(configured),
            "missing_required_status_gate": missing_gate,
        })

    result["platform_enforcement_evidence"] = {
        "trust": "SUPPLIED_PLATFORM_STATE",
        "confidence": "PARTIAL",
        "observations": observations,
        "unknowns": [
            "caller-supplied branch/ruleset state is time-bound platform evidence, not commit-bound proof; provider-authenticated current enforcement remains unverified"
        ],
    }
    return result
