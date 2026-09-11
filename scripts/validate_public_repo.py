from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "AGENTS.md", "README.md", "FAQ.md", "FREE_DEMO_AUDIT.md", "HOW_IT_WORKS.md", "SAMPLE_AUDIT.md", "SECURITY.md",
    "CASE_STUDY_QUANT_SYSTEM.md", "CASE_STUDY_LANGUAGE_LEARNING.md", "docs/EVIDENCE_MAPPER_V1.md",
    "schemas/rem-v1.schema.json", "schemas/rem-v1.1.schema.json", "requirements-ci.txt",
    "scripts/validate_rem.py", "scripts/validate_rem_v11.py", "scripts/rem_extract.py", "scripts/rem_extract_exact.py",
    "scripts/exact_subject.py", "scripts/test_rem_extract.py", "scripts/test_rem_extract_exact.py",
    "scripts/test_exact_subject.py", "scripts/test_validate_rem_v11.py",
]

SECRET_PATTERNS = {
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"),
    "GitHub token": re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,})\b"),
    "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "Slack token": re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"),
}
INTERNAL_MARKERS = ("private://", "internal://")
TEXT_SUFFIXES = {".md", ".py", ".yml", ".yaml", ".txt", ".json", ".toml"}
TEXT_FILES = [
    p for p in ROOT.rglob("*")
    if p.is_file() and p.suffix.lower() in TEXT_SUFFIXES and ".git" not in p.parts
]
MARKDOWN_FILES = [p for p in TEXT_FILES if p.suffix.lower() == ".md"]


def fail(message: str) -> None:
    print(f"ERROR: {message}")
    raise SystemExit(1)


for required in REQUIRED_FILES:
    if not (ROOT / required).is_file():
        fail(f"required public file missing: {required}")

for path in TEXT_FILES:
    text = path.read_text(encoding="utf-8")
    low = text.casefold()
    for marker in INTERNAL_MARKERS:
        if marker in low:
            fail(f"internal-only marker found in {path.relative_to(ROOT)}")
    for label, pattern in SECRET_PATTERNS.items():
        if pattern.search(text):
            fail(f"possible {label} found in {path.relative_to(ROOT)}")

link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
for path in MARKDOWN_FILES:
    for target in link_pattern.findall(path.read_text(encoding="utf-8")):
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

subprocess.run([sys.executable, str(ROOT / "scripts" / "validate_rem.py")], cwd=ROOT, check=True)
subprocess.run([sys.executable, str(ROOT / "scripts" / "test_rem_extract.py")], cwd=ROOT, check=True)
subprocess.run([sys.executable, str(ROOT / "scripts" / "test_exact_subject.py")], cwd=ROOT, check=True)
subprocess.run([sys.executable, str(ROOT / "scripts" / "test_rem_extract_exact.py")], cwd=ROOT, check=True)
subprocess.run([sys.executable, str(ROOT / "scripts" / "test_validate_rem_v11.py")], cwd=ROOT, check=True)
print("public repository checks passed")
