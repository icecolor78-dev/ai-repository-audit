from __future__ import annotations

import re
from pathlib import Path

KINDS = {
    "unit": "unit", "integration": "integration", "e2e": "end-to-end",
    "end_to_end": "end-to-end", "smoke": "smoke", "contract": "contract",
    "schema": "contract", "property": "property-based", "fuzz": "fuzz",
    "security": "security", "compat": "compatibility", "migration": "migration",
    "benchmark": "performance", "performance": "performance", "release": "release-artifact",
}
TEST_FILE = re.compile(r"(?:^|/)(?:test[s]?|spec[s]?|__tests__)(?:/|$)|(?:^|/)(?:test_|.*[._-](?:test|spec)\.)", re.I)
TEST_CONFIG_NAMES = {
    "pytest.ini", "tox.ini", "noxfile.py", "jest.config.js", "jest.config.ts",
    "vitest.config.js", "vitest.config.ts", "playwright.config.js", "playwright.config.ts",
    "cypress.config.js", "cypress.config.ts",
}


def _is_test_evidence(path: Path, rp: str) -> bool:
    if path.name.casefold() in TEST_CONFIG_NAMES:
        return True
    if not TEST_FILE.search(rp):
        return False
    # Avoid classifying arbitrary documentation/data files such as tests/spec.txt as executable suites.
    return path.suffix.casefold() in {
        ".py", ".js", ".jsx", ".ts", ".tsx", ".rs", ".go", ".java", ".kt",
        ".rb", ".php", ".cs", ".cpp", ".cc", ".c", ".swift", ".scala", ".sh",
        ".yaml", ".yml", ".toml", ".json",
    } or path.name.casefold() in TEST_CONFIG_NAMES


def profile_tests(root: Path) -> dict:
    suites: list[str] = []
    kinds: set[str] = set()
    subsystem: list[str] = []
    for path in sorted(p for p in root.rglob("*") if p.is_file() and ".git" not in p.parts):
        rp = path.relative_to(root).as_posix()
        low = rp.casefold()
        if not _is_test_evidence(path, rp):
            continue
        suites.append(rp)
        found = False
        for token, kind in KINDS.items():
            if token in low:
                kinds.add(kind)
                found = True
        if not found:
            kinds.add("unspecified")
        parts = Path(rp).parts
        if parts and parts[0] in {"tests", "test", "spec", "specs", "__tests__"}:
            area = parts[1] if len(parts) > 2 else "repository"
        else:
            area = "repository"
        subsystem.append(f"{area}: {rp}")
    return {
        "suites": suites,
        "types": sorted(kinds),
        "subsystem_map": subsystem,
        "exact_subject_execution": [],
        "confidence": "PARTIAL" if suites else "UNVERIFIED",
        "unknowns": [
            "repository-visible test/config discovery does not prove execution, suite membership, matrix coverage, assertions, or semantic completeness"
        ],
    }
