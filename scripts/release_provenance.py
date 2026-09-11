from __future__ import annotations

import re
from pathlib import Path


def _rel(root: Path, p: Path) -> str:
    return p.relative_to(root).as_posix()


def analyze(root: Path, revision: str) -> dict:
    workflows = sorted(p for p in root.glob('.github/workflows/*') if p.suffix in {'.yml', '.yaml'})
    signals, findings = [], []
    for path in workflows:
        rp = _rel(root, path)
        text = path.read_text(encoding='utf-8', errors='replace')
        low = (rp + '\n' + text).lower()
        if not re.search(r'release|publish|deploy|pypi|npm|crates\.io|ghcr|docker', low):
            continue
        row = {
            'workflow': rp,
            'oidc': bool(re.search(r'id-token\s*:\s*write', text, re.I)),
            'artifact_handoff': bool(re.search(r'actions/(?:upload|download)-artifact@', text, re.I)),
            'attestation_or_signing': bool(re.search(r'attest|provenance|sigstore|cosign|gpg|signing', text, re.I)),
            'release_verification': bool(re.search(r'smoke|verify|verification|checksum', text, re.I)),
            'rollback_or_recovery': bool(re.search(r'rollback|revert|recovery', text, re.I)),
            'checkout_subject_binding': [],
        }
        for m in re.finditer(r'(?m)^\s*(?:ref|sha)\s*:\s*([^\n#]+)', text):
            row['checkout_subject_binding'].append(m.group(1).strip())
        for ref in re.findall(r'(?m)^\s*uses:\s*([^\s#]+)', text):
            if ref.startswith('./'):
                continue
            if not re.search(r'@[0-9a-f]{40}$', ref):
                findings.append({'kind': 'mutable_release_dependency', 'locator': rp, 'detail': ref, 'severity': 'LOW', 'confidence': 'HIGH'})
        signals.append(row)
    state = 'PARTIAL' if signals else 'UNVERIFIED'
    return {
        'schema_version': 'release-provenance/v1',
        'subject_revision': revision,
        'release_workflows': signals,
        'findings': findings,
        'source_to_artifact_binding': {'state': 'PARTIAL' if any(r['checkout_subject_binding'] for r in signals) else 'UNVERIFIED', 'evidence': [r['workflow'] for r in signals if r['checkout_subject_binding']]},
        'provenance': {'state': 'PARTIAL' if any(r['attestation_or_signing'] for r in signals) else 'UNVERIFIED'},
        'trusted_publishing': {'state': 'PARTIAL' if any(r['oidc'] for r in signals) else 'UNVERIFIED'},
        'confidence': state,
        'unknowns': ['Static release configuration does not prove publication success, artifact integrity, rollback effectiveness, or exact source-to-artifact identity.'],
    }
