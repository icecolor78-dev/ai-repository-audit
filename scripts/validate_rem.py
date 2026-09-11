from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "examples" / "rem-v1"
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
EVIDENCE_STATES = {"VERIFIED", "PARTIAL", "UNVERIFIED", "CONTRADICTED", "NOT_APPLICABLE"}
FRESHNESS_STATES = {"exact", "current-but-not-exact", "historical", "unknown"}
ACCESS_STATES = {"accessible", "partial", "inaccessible"}
DIMENSIONS = ("ci", "tests", "security", "release", "supply_chain", "provenance")


def fail(path: Path, message: str) -> None:
    raise SystemExit(f"ERROR: {path.relative_to(ROOT)}: {message}")


def require_keys(path: Path, obj: dict, keys: tuple[str, ...], where: str) -> None:
    missing = [key for key in keys if key not in obj]
    if missing:
        fail(path, f"{where} missing keys: {', '.join(missing)}")


def validate(path: Path) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    require_keys(path, data, ("schema_version", "subject", "inventory", "ci", "tests", "security", "release", "supply_chain", "claims", "provenance", "coverage", "sources"), "portrait")
    if data["schema_version"] != "rem/v1":
        fail(path, "schema_version must be rem/v1")
    if "score" in data or "global_score" in data:
        fail(path, "opaque global score is forbidden in REM v1")

    subject = data["subject"]
    require_keys(path, subject, ("provider", "repository", "revision", "default_branch", "observed_at", "visibility"), "subject")
    revision = subject["revision"]
    if not isinstance(revision, str) or not SHA_RE.fullmatch(revision):
        fail(path, "subject.revision must be a full lowercase 40-hex SHA")
    if subject["provider"] != "github":
        fail(path, "v1 fixtures currently require github provider")

    for name in DIMENSIONS:
        dimension = data[name]
        require_keys(path, dimension, ("confidence", "unknowns"), name)
        if dimension["confidence"] not in EVIDENCE_STATES:
            fail(path, f"{name}.confidence is invalid")
        if not isinstance(dimension["unknowns"], list):
            fail(path, f"{name}.unknowns must be a list")

    ci = data["ci"]
    for key in ("pr_confidence", "main_confidence", "release_confidence", "security_evidence_freshness"):
        if ci.get(key) not in EVIDENCE_STATES:
            fail(path, f"ci.{key} is missing or invalid")

    sources = data["sources"]
    if not isinstance(sources, list) or not sources:
        fail(path, "sources must contain at least one evidence reference")
    source_ids: set[str] = set()
    for source in sources:
        require_keys(path, source, ("id", "kind", "subject_revision", "locator", "observed_at", "freshness", "access", "supports", "limits"), "source")
        sid = source["id"]
        if sid in source_ids:
            fail(path, f"duplicate source id: {sid}")
        source_ids.add(sid)
        source_revision = source["subject_revision"]
        if source["kind"] != "external":
            if source_revision != revision:
                fail(path, f"repository-bound source {sid} is not bound to subject revision")
        elif source_revision is not None and (not isinstance(source_revision, str) or not SHA_RE.fullmatch(source_revision)):
            fail(path, f"external source {sid} has malformed subject_revision")
        if source["freshness"].get("state") not in FRESHNESS_STATES:
            fail(path, f"source {sid} has invalid freshness state")
        if source["access"].get("state") not in ACCESS_STATES:
            fail(path, f"source {sid} has invalid access state")
        if source["kind"] == "external" and source["access"]["state"] != "accessible" and not source["limits"]:
            fail(path, f"inaccessible/partial external source {sid} must state limits")

    for claim in data["claims"].get("items", []):
        require_keys(path, claim, ("claim", "source_ref", "state", "supporting_refs", "contradicting_refs", "notes"), "claim")
        if claim["state"] not in EVIDENCE_STATES:
            fail(path, "claim has invalid evidence state")
        for ref in [claim["source_ref"], *claim["supporting_refs"], *claim["contradicting_refs"]]:
            if ref and ref not in source_ids:
                fail(path, f"claim references unknown source id: {ref}")

    unknowns = data["coverage"].get("explicit_unknowns", [])
    if not isinstance(unknowns, list):
        fail(path, "coverage.explicit_unknowns must be a list")
    if any(data[name]["confidence"] == "UNVERIFIED" for name in DIMENSIONS) and not unknowns:
        fail(path, "UNVERIFIED dimensions require coverage.explicit_unknowns")


files = sorted(FIXTURES.glob("*.json"))
if not files:
    raise SystemExit("ERROR: no REM v1 fixtures found")
for fixture in files:
    validate(fixture)
print(f"REM v1 validation passed: {len(files)} fixture(s)")
