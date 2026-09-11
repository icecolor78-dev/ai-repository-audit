from __future__ import annotations

from pathlib import Path

KINDS = {
    "unit": "unit", "integration": "integration", "e2e": "end-to-end",
    "end_to_end": "end-to-end", "smoke": "smoke", "contract": "contract",
    "schema": "contract", "property": "property-based", "fuzz": "fuzz",
    "security": "security", "compat": "compatibility", "migration": "migration",
    "benchmark": "performance", "performance": "performance", "release": "release-artifact",
}


def profile_tests(root: Path) -> dict:
    suites: list[str] = []
    kinds: set[str] = set()
    subsystem: list[str] = []
    for path in sorted(p for p in root.rglob("*") if p.is_file() and ".git" not in p.parts):
        rp = path.relative_to(root).as_posix()
        low = rp.casefold()
        if not any(token in low for token in ("test", "spec", "__tests__")):
            continue
        suites.append(rp)
        found = False
        for token, kind in KINDS.items():
            if token in low:
                kinds.add(kind)
                found = True
        if not found:
            kinds.add("unit/unspecified")
        parts = Path(rp).parts
        area = parts[1] if len(parts) > 2 and parts[0] in {"tests", "test"} else "repository"
        subsystem.append(f"{area}: {rp}")
    return {
        "suites": suites,
        "types": sorted(kinds),
        "subsystem_map": subsystem,
        "exact_subject_execution": [],
        "confidence": "PARTIAL" if suites else "UNVERIFIED",
        "unknowns": ["test discovery is complete for repository-visible paths but does not prove exact-subject execution or semantic coverage"],
    }
