from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    "FAQ.md",
    "FREE_DEMO_AUDIT.md",
    "HOW_IT_WORKS.md",
    "SAMPLE_AUDIT.md",
    "SECURITY.md",
    "CASE_STUDY_QUANT_SYSTEM.md",
]

FORBIDDEN_PUBLIC_PATTERNS = [
    r"AI-Trading-bot",
    r"icecolor78-dev/AI-Trading-bot",
]

MARKDOWN_FILES = list(ROOT.glob("*.md"))


def fail(message: str) -> None:
    print(f"ERROR: {message}")
    raise SystemExit(1)


for rel in REQUIRED_FILES:
    if not (ROOT / rel).is_file():
        fail(f"required public file missing: {rel}")

for path in MARKDOWN_FILES:
    text = path.read_text(encoding="utf-8")
    for pattern in FORBIDDEN_PUBLIC_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            fail(f"private-system identifier found in {path.name}: {pattern}")

# Validate repository-relative Markdown links to local .md files.
link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
for path in MARKDOWN_FILES:
    text = path.read_text(encoding="utf-8")
    for target in link_pattern.findall(text):
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        clean = target.split("#", 1)[0]
        if not clean:
            continue
        candidate = (path.parent / clean).resolve()
        try:
            candidate.relative_to(ROOT)
        except ValueError:
            fail(f"link escapes repository in {path.name}: {target}")
        if not candidate.exists():
            fail(f"broken local link in {path.name}: {target}")

print("public repository checks passed")
