from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "rem-v1.1.schema.json"
DIMENSIONS = ("ci", "tests", "security", "release", "supply_chain", "provenance")


class EvidenceContractError(ValueError):
    pass


def validate_document(data: dict) -> None:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(data), key=lambda item: list(item.absolute_path))
    if errors:
        first = errors[0]
        location = ".".join(str(part) for part in first.absolute_path) or "portrait"
        raise EvidenceContractError(f"schema violation at {location}: {first.message}")

    subject_revision = data["subject"]["revision"]
    sources = {source["id"]: source for source in data["sources"]}
    if len(sources) != len(data["sources"]):
        raise EvidenceContractError("duplicate source id")

    exact_binding = sources.get("subject-binding")
    if exact_binding is not None:
        if exact_binding["kind"] != "commit":
            raise EvidenceContractError("subject-binding must be commit evidence")
        if exact_binding["subject_revision"] != subject_revision:
            raise EvidenceContractError("subject-binding revision mismatch")
        if exact_binding["freshness"]["state"] != "exact":
            raise EvidenceContractError("subject-binding must be exact")
        if exact_binding["access"]["state"] != "accessible":
            raise EvidenceContractError("subject-binding must be accessible")
        if not exact_binding.get("content_digest"):
            raise EvidenceContractError("subject-binding requires content digest")

    for source in data["sources"]:
        if source["kind"] != "external" and source["subject_revision"] != subject_revision:
            raise EvidenceContractError(f"wrong-subject source: {source['id']}")
        if source["freshness"]["state"] == "exact" and exact_binding is None:
            raise EvidenceContractError("exact freshness requires verified subject-binding evidence")

    for claim in data["claims"]["items"]:
        refs = [claim["source_ref"], *claim["supporting_refs"], *claim["contradicting_refs"]]
        if any(ref and ref not in sources for ref in refs):
            raise EvidenceContractError("claim contains an unresolved evidence reference")
        if claim["state"] == "VERIFIED":
            if not claim["supporting_refs"]:
                raise EvidenceContractError("VERIFIED claim requires supporting evidence")
            for ref in claim["supporting_refs"]:
                source = sources[ref]
                if source["subject_revision"] != subject_revision:
                    raise EvidenceContractError("VERIFIED claim uses wrong-subject evidence")
                if source["freshness"]["state"] != "exact":
                    raise EvidenceContractError("VERIFIED claim requires exact evidence")
                if source["access"]["state"] != "accessible":
                    raise EvidenceContractError("VERIFIED claim requires accessible evidence")
        if claim["state"] == "NOT_APPLICABLE" and not claim["notes"].strip():
            raise EvidenceContractError("NOT_APPLICABLE claim requires rationale")

    for name in DIMENSIONS:
        if data[name]["confidence"] == "VERIFIED":
            raise EvidenceContractError(
                f"{name}.confidence cannot be VERIFIED in REM v1.1 without dimension-level evidence refs"
            )


def validate_file(path: Path) -> None:
    validate_document(json.loads(path.read_text(encoding="utf-8")))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("portrait", type=Path)
    args = parser.parse_args()
    validate_file(args.portrait)
    print("REM v1.1 schema and evidence validation passed")
