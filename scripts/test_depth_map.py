from __future__ import annotations

import re
from pathlib import Path

TYPE_HINTS = {
    'unit': ('unit', 'pytest', 'unittest', 'jest', 'vitest'),
    'integration': ('integration', 'contract'),
    'end_to_end': ('e2e', 'end-to-end', 'playwright', 'cypress'),
    'smoke': ('smoke',),
    'property': ('property', 'hypothesis', 'quickcheck', 'proptest'),
    'fuzz': ('fuzz', 'afl', 'libfuzzer'),
    'security': ('security', 'sast', 'codeql', 'semgrep', 'zizmor', 'trivy'),
    'compatibility': ('compat', 'tox', 'nox', 'matrix'),
    'migration': ('migration', 'upgrade', 'downgrade'),
    'performance': ('benchmark', 'performance', 'loadtest', 'load-test'),
    'release': ('release', 'publish', 'artifact'),
}


def _rel(root: Path, p: Path) -> str:
    return p.relative_to(root).as_posix()


def _test_files(root: Path):
    out = []
    for p in root.rglob('*'):
        if not p.is_file() or '.git' in p.parts:
            continue
        rp = _rel(root, p)
        if re.search(r"(^|/)(tests?|specs?|__tests__)(/|$)|(^|/)(test_|.*_test\.)", rp, re.I):
            out.append(p)
    return sorted(out)


def _subsystems(root: Path):
    ignored = {'tests', 'test', 'spec', 'specs', 'docs', '.github', 'scripts'}
    dirs = sorted(p for p in root.iterdir() if p.is_dir() and not p.name.startswith('.') and p.name not in ignored)
    return [p.name for p in dirs]


def analyze(root: Path, revision: str, executed_refs: list[str] | None = None) -> dict:
    executed = set(executed_refs or [])
    tests = _test_files(root)
    rows = []
    observed_types = set()
    for p in tests:
        rp = _rel(root, p)
        low = rp.lower() + '\n' + p.read_text(encoding='utf-8', errors='replace').lower()[:20000]
        kinds = sorted(kind for kind, hints in TYPE_HINTS.items() if any(h in low for h in hints)) or ['unit']
        observed_types.update(kinds)
        rows.append({'path': rp, 'types': kinds, 'executed_on_subject': rp in executed, 'subject_revision': revision})
    subsystem_map = []
    for subsystem in _subsystems(root):
        matching = [row for row in rows if subsystem.lower() in row['path'].lower() or any(subsystem.lower() in Path(row['path']).stem.lower() for _ in [0])]
        if not matching:
            state = 'UNVERIFIED'
        elif any(r['executed_on_subject'] for r in matching):
            state = 'VERIFIED'
        else:
            state = 'PARTIAL'
        subsystem_map.append({'subsystem': subsystem, 'state': state, 'test_refs': [r['path'] for r in matching]})
    return {
        'schema_version': 'test-depth-map/v1',
        'subject_revision': revision,
        'test_files': rows,
        'types': sorted(observed_types),
        'subsystem_map': subsystem_map,
        'execution_evidence': sorted(executed),
        'confidence': 'PARTIAL' if tests else 'UNVERIFIED',
        'unknowns': ['Test discovery does not prove semantic completeness; VERIFIED requires explicit exact-subject execution evidence supplied to this analyzer.'],
    }
