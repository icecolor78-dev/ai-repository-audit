from __future__ import annotations

import re
from pathlib import Path


def _rel(root: Path, p: Path) -> str:
    return p.relative_to(root).as_posix()


def finding(kind: str, locator: str, detail: str, severity: str, confidence: str = 'HIGH') -> dict:
    return {'kind': kind, 'locator': locator, 'detail': detail, 'severity': severity, 'confidence': confidence}


def analyze(root: Path, revision: str) -> dict:
    findings, positives = [], []
    workflows = sorted(p for p in root.glob('.github/workflows/*') if p.suffix in {'.yml', '.yaml'})
    for path in workflows:
        rp = _rel(root, path)
        text = path.read_text(encoding='utf-8', errors='replace')
        if re.search(r'(?m)^\s*pull_request_target\s*:', text):
            findings.append(finding('pull_request_target', rp, 'Privileged pull_request_target trigger requires explicit trust-boundary review.', 'HIGH'))
        if re.search(r'run\s*:\s*[^\n]*\$\{\{\s*github\.event\.', text, re.I):
            findings.append(finding('untrusted_expression_shell', rp, 'Event-derived expression appears directly in a shell command.', 'HIGH'))
        if 'actions/checkout@' in text:
            if re.search(r'persist-credentials\s*:\s*false', text, re.I):
                positives.append({'kind': 'credential_persistence_disabled', 'locator': rp})
            else:
                findings.append(finding('credential_persistence', rp, 'Checkout is present without observed persist-credentials:false.', 'LOW', 'MEDIUM'))
        for ref in re.findall(r'(?m)^\s*uses:\s*([^\s#]+)', text):
            if ref.startswith('./'):
                continue
            if not re.search(r'@[0-9a-f]{40}$', ref):
                findings.append(finding('mutable_action_ref', rp, ref, 'LOW'))
        if re.search(r'permissions\s*:\s*write-all', text, re.I):
            findings.append(finding('broad_permissions', rp, 'write-all permission observed.', 'HIGH'))
        if re.search(r'(?m)^\s*permissions\s*:\s*read-all\s*$', text, re.I) or re.search(r'(?m)^\s*contents\s*:\s*read\s*$', text, re.I):
            positives.append({'kind': 'scoped_permissions_signal', 'locator': rp})
        if re.search(r'actions/(?:upload|download)-artifact@', text, re.I):
            positives.append({'kind': 'artifact_boundary_observed', 'locator': rp})
        if re.search(r'cache|actions/cache@', text, re.I):
            positives.append({'kind': 'cache_boundary_observed', 'locator': rp})
        if re.search(r'secrets\.[A-Za-z0-9_]+', text):
            positives.append({'kind': 'secret_reference_observed', 'locator': rp})
    severity_rank = {'HIGH': 3, 'MEDIUM': 2, 'LOW': 1}
    max_rank = max((severity_rank.get(f['severity'], 0) for f in findings), default=0)
    return {
        'schema_version': 'workflow-security/v1',
        'subject_revision': revision,
        'findings': findings,
        'positive_controls': positives,
        'risk': {0: 'UNVERIFIED', 1: 'LOW', 2: 'MEDIUM', 3: 'HIGH'}[max_rank],
        'confidence': 'PARTIAL' if workflows else 'UNVERIFIED',
        'scope': 'static workflow evidence only',
        'unknowns': ['Static patterns do not prove exploitability, secret exposure, cache/artifact poisoning, or vulnerability absence.'],
    }
