from __future__ import annotations

import re
from pathlib import Path

STATES = {"VERIFIED", "PARTIAL", "UNVERIFIED", "CONTRADICTED", "NOT_APPLICABLE"}
CLAIMS = [
    ("ci", re.compile(r"\b(?:CI|continuous integration|build status)\b", re.I)),
    ("tests", re.compile(r"\b(?:tests?|tested|test suite)\b", re.I)),
    ("security", re.compile(r"\b(?:secure|security|vulnerabilit(?:y|ies)|hardened)\b", re.I)),
    ("release", re.compile(r"\b(?:release|publish|published|package|artifact)\b", re.I)),
    ("compatibility", re.compile(r"\b(?:supports?|compatible|compatibility)\b", re.I)),
]


def _rel(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def _files(root: Path):
    return sorted(p for p in root.rglob("*") if p.is_file() and ".git" not in p.parts)


def _claim_sources(root: Path):
    for path in _files(root):
        rp = _rel(root, path)
        low = rp.lower()
        if path.suffix.lower() not in {".md", ".rst", ".txt"}:
            continue
        if not (low.startswith("readme") or low.startswith("docs/") or "release" in low):
            continue
        yield path


def _evidence(root: Path):
    files = [_rel(root, p) for p in _files(root)]
    workflow = [p for p in files if p.startswith(".github/workflows/") and p.endswith((".yml", ".yaml"))]
    tests = [p for p in files if re.search(r"(^|/)(tests?|specs?|__tests__)(/|$)|(^|/)(test_|.*_test\.)", p, re.I)]
    security = [p for p in files if re.search(r"security\.md$|codeql|dependabot|gitleaks|semgrep|zizmor|trivy|sast", p, re.I)]
    release = [p for p in workflow if re.search(r"release|publish|deploy", p, re.I)]
    contracts = [p for p in files if re.search(r"openapi|swagger|schema|\.proto$|graphql|pyproject\.toml|package\.json|go\.mod|cargo\.toml", p, re.I)]
    return {"ci": workflow, "tests": tests, "security": security, "release": release, "compatibility": contracts}


def analyze(root: Path, revision: str) -> dict:
    evidence = _evidence(root)
    items = []
    for source in _claim_sources(root):
        text = source.read_text(encoding="utf-8", errors="replace")
        for line_no, line in enumerate(text.splitlines(), 1):
            stripped = line.strip()
            if not stripped or len(stripped) > 500:
                continue
            matched = [kind for kind, pattern in CLAIMS if pattern.search(stripped)]
            for kind in matched:
                refs = evidence[kind][:20]
                state = "PARTIAL" if refs else "UNVERIFIED"
                items.append({
                    "claim_kind": kind,
                    "claim": stripped,
                    "state": state,
                    "claim_ref": f"{_rel(root, source)}:{line_no}",
                    "supporting_refs": refs,
                    "contradicting_refs": [],
                    "subject_revision": revision,
                    "confidence": "MEDIUM" if refs else "LOW",
                    "reason": "Repository-visible evidence supports part of the claim; execution/runtime truth is not inferred." if refs else "No repository-visible evidence class matched this claim.",
                })
    return {
        "schema_version": "claims-evidence/v1",
        "subject_revision": revision,
        "items": items,
        "states": sorted(STATES),
        "scoring": "NONE",
        "unknowns": ["Static repository evidence cannot prove production/runtime claims without exact-subject execution evidence."],
    }
