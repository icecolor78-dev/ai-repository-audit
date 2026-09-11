from __future__ import annotations

import re
from pathlib import Path

CLAIM_SIGNAL = re.compile(
    r"\b(?:ci|continuous integration|tests?|tested|release|publish|production|secure|security|vulnerab|reproducib|performance|compatib)\w*\b",
    re.I,
)


def extract_readme_claims(root: Path) -> list[dict]:
    """Preserve bounded README claim text and location without inferring truth."""
    path = root / "README.md"
    if not path.is_file():
        return []
    items: list[dict] = []
    for line_number, raw in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        text = " ".join(raw.strip().split())
        if not text or not CLAIM_SIGNAL.search(text):
            continue
        items.append({
            "claim": text,
            "source_ref": "readme",
            "state": "UNVERIFIED",
            "supporting_refs": [],
            "contradicting_refs": [],
            "notes": f"README.md:{line_number}; exact wording preserved; truth not inferred from documentation",
        })
    return items
