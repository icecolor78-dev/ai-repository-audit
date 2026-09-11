from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


STATE_ORDER = {"CONTRADICTED": 0, "UNVERIFIED": 1, "PARTIAL": 2, "VERIFIED": 3, "NOT_APPLICABLE": 4}


def _text(value: Any) -> str:
    return str(value).replace("\n", " ").strip()


def _rows(items: list[dict], keys: tuple[str, ...]) -> list[dict]:
    return sorted(items, key=lambda item: tuple(_text(item.get(key, "")) for key in keys))


def render_customer_report(portrait: dict) -> str:
    subject = portrait.get("subject", {})
    overall = portrait.get("overall_portrait", {})
    verdict = _text(overall.get("verdict", "UNVERIFIED")) or "UNVERIFIED"
    lines = [
        "# AI Repository Audit Report",
        "",
        "## Exact subject",
        f"- Repository: `{_text(subject.get('repository', 'UNVERIFIED'))}`",
        f"- Revision: `{_text(subject.get('revision', 'UNVERIFIED'))}`",
        f"- Observed at: `{_text(subject.get('observed_at', 'UNVERIFIED'))}`",
        "",
        "## Executive verdict",
        f"**{verdict}**",
        "",
        _text(overall.get("statement", "No broader assurance statement is available.")),
        "",
    ]

    assurance = portrait.get("assurance_v2", {})
    domains = assurance.get("domains", {}) if isinstance(assurance, dict) else {}
    if isinstance(domains, dict) and domains:
        lines += ["## Evidence-state summary", "", "| Domain | State |", "|---|---|"]
        rows = sorted(domains.items(), key=lambda kv: (STATE_ORDER.get(_text(kv[1].get('state', kv[1].get('confidence', 'UNVERIFIED'))) if isinstance(kv[1], dict) else 'UNVERIFIED', 99), kv[0]))
        for name, value in rows:
            if isinstance(value, dict):
                state = value.get("state", value.get("confidence", "UNVERIFIED"))
            else:
                state = "UNVERIFIED"
            lines.append(f"| {_text(name)} | {_text(state)} |")
        lines.append("")

    findings = overall.get("findings", [])
    lines += ["## Material findings", ""]
    if findings:
        for item in _rows(findings, ("severity", "kind", "locator", "detail")):
            lines.append(f"### {_text(item.get('severity', 'INFO'))} — {_text(item.get('kind', 'finding'))}")
            if item.get("locator"):
                lines.append(f"- Evidence: `{_text(item['locator'])}`")
            if item.get("confidence"):
                lines.append(f"- Confidence: {_text(item['confidence'])}")
            if item.get("detail"):
                lines.append(f"- Finding: {_text(item['detail'])}")
            lines.append("")
    else:
        lines += ["No material findings are recorded in the supplied portrait. This is not a guarantee of defect or vulnerability absence.", ""]

    unknowns = overall.get("explicit_unknowns", [])
    lines += ["## Explicit unknowns", ""]
    if unknowns:
        for item in _rows(unknowns, ("dimension", "detail")):
            lines.append(f"- **{_text(item.get('dimension', 'unknown'))}:** {_text(item.get('detail', 'UNVERIFIED'))}")
    else:
        lines.append("- No explicit unknowns were supplied. This does not create a PASS state.")
    lines.append("")

    remediation = overall.get("remediation", [])
    lines += ["## Remediation roadmap", ""]
    if remediation:
        for item in _rows(remediation, ("priority", "action", "verification")):
            lines.append(f"- **{_text(item.get('priority', 'P2'))}:** {_text(item.get('action', 'No action recorded.'))}")
            if item.get("verification"):
                lines.append(f"  - Verification: {_text(item['verification'])}")
    else:
        lines.append("- No remediation items are recorded in the supplied portrait.")
    lines.append("")

    external = portrait.get("external_execution_evidence")
    runtime = portrait.get("runtime_evidence")
    provenance = portrait.get("artifact_provenance_evidence")
    platform = portrait.get("platform_enforcement_evidence")
    if external or runtime or provenance or platform:
        lines += ["## Supplied external evidence", ""]
        if external:
            lines.append(f"- Execution evidence trust: **{_text(external.get('trust', 'UNVERIFIED'))}**")
            if external.get("statement"):
                lines.append(f"- Boundary: {_text(external['statement'])}")
        if runtime:
            lines.append(f"- Runtime evidence trust: **{_text(runtime.get('trust', 'UNVERIFIED'))}**")
            lines.append(f"- Runtime evidence confidence: **{_text(runtime.get('confidence', 'UNVERIFIED'))}**")
        if provenance:
            lines.append(f"- Artifact provenance trust: **{_text(provenance.get('trust', 'UNVERIFIED'))}**")
            lines.append(f"- Artifact provenance confidence: **{_text(provenance.get('confidence', 'UNVERIFIED'))}**")
            for item in provenance.get("unknowns", []):
                lines.append(f"- Provenance boundary: {_text(item)}")
        if platform:
            lines.append(f"- Platform enforcement trust: **{_text(platform.get('trust', 'UNVERIFIED'))}**")
            lines.append(f"- Platform enforcement confidence: **{_text(platform.get('confidence', 'UNVERIFIED'))}**")
            for observation in platform.get("observations", []):
                lines.append(f"- Branch `{_text(observation.get('branch', 'UNVERIFIED'))}` required status checks: {_text(observation.get('required_status_checks', []))}")
                lines.append(f"- Missing required-status gate: **{_text(observation.get('missing_required_status_gate', 'UNVERIFIED'))}**")
            for item in platform.get("unknowns", []):
                lines.append(f"- Platform-state boundary: {_text(item)}")
        lines.append("")

    lines += [
        "## Interpretation boundary",
        "",
        "This report is a deterministic rendering of an existing Audit portrait. It does not create new evidence, findings, scores, assurance states, certifications, or release authority.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("portrait", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    portrait = json.loads(args.portrait.read_text(encoding="utf-8"))
    rendered = render_customer_report(portrait)
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
