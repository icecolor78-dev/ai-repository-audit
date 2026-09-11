from __future__ import annotations

import re
from pathlib import Path

CLAIM_SIGNAL = re.compile(
    r"\b(?:ci|continuous integration|tests?|tested|release|publish|production|secure|security|vulnerab|reproducib|performance|compatib)\w*\b",
    re.I,
)
README_CANDIDATES = ("README.md", "README.rst", "README.txt")


def selected_readme(root: Path) -> Path | None:
    for name in README_CANDIDATES:
        path = root / name
        if path.is_file():
            return path
    return None


def extract_readme_claims(root: Path) -> list[dict]:
    """Preserve bounded README claim text and location without inferring truth.

    One canonical README is selected deterministically (Markdown, then RST, then text)
    so claim extraction and evidence source binding remain unambiguous.
    """
    path = selected_readme(root)
    if path is None:
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
            "notes": f"{path.name}:{line_number}; exact wording preserved; truth not inferred from documentation",
        })
    return items
