from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "AGENTS.md",
    "README.md",
    "FAQ.md",
    "FREE_DEMO_AUDIT.md",
    "HOW_IT_WORKS.md",
    "SAMPLE_AUDIT.md",
    "SECURITY.md",
    "CASE_STUDY_QUANT_SYSTEM.md",
    "CASE_STUDY_LANGUAGE_LEARNING.md",
]

FORBIDDEN_PUBLIC_PATTERNS = [
    r"AI-Trading-bot",
    r"icecolor78-dev/AI-Trading-bot",
]

SECRET_PATTERNS = {
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"),
    "GitHub token": re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,})\b"),
    "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "Slack token": re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"),
}

TEXT_SUFFIXES = {".md", ".py", ".yml", ".yaml", ".txt", ".json", ".toml"}
TEXT_FILES = [
    path
    for path in ROOT.rglob("*")
    if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES and ".git" not in path.parts
]
MARKDOWN_FILES = [path for path in TEXT_FILES if path.suffix.lower() == ".md"]


def fail(message: str) -> None:
    print(f"ERROR: {message}")
    raise SystemExit(1)


for rel in REQUIRED_FILES:
    if not (ROOT / rel).is_file():
        fail(f"required public file missing: {rel}")

for path in TEXT_FILES:
    text = path.read_text(encoding="utf-8")
    relative = path.relative_to(ROOT)
    for pattern in FORBIDDEN_PUBLIC_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            fail(f"private-system identifier found in {relative}: {pattern}")
    for label, pattern in SECRET_PATTERNS.items():
        if pattern.search(text):
            fail(f"possible {label} found in {relative}")

# Validate repository-relative Markdown links to local files.
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
            fail(f"link escapes repository in {path.relative_to(ROOT)}: {target}")
        if not candidate.exists():
            fail(f"broken local link in {path.relative_to(ROOT)}: {target}")

print("public repository checks passed")
