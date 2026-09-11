from __future__ import annotations

import re
from pathlib import Path

MANIFESTS = {'pyproject.toml','requirements.txt','package.json','Cargo.toml','go.mod','pom.xml','Gemfile','composer.json'}
LOCKFILES = {'uv.lock','poetry.lock','pdm.lock','package-lock.json','pnpm-lock.yaml','yarn.lock','Cargo.lock','go.sum','Gemfile.lock','composer.lock'}
LICENSES = {'license','license.md','license.txt','copying','notice','notice.md'}


def _rel(root: Path, p: Path) -> str:
    return p.relative_to(root).as_posix()


def analyze(root: Path, revision: str) -> dict:
    files = sorted(p for p in root.rglob('*') if p.is_file() and '.git' not in p.parts)
    paths = [_rel(root, p) for p in files]
    manifests = sorted(p for p in paths if Path(p).name in MANIFESTS)
    lockfiles = sorted(p for p in paths if Path(p).name in LOCKFILES)
    updates = sorted(p for p in paths if re.search(r'dependabot|renovate', p, re.I))
    sbom = sorted(p for p in paths if re.search(r'sbom|cyclonedx|spdx', p, re.I))
    licenses = sorted(p for p in paths if Path(p).name.lower() in LICENSES)
    integrity = []
    for p in files:
        rp = _rel(root, p)
        if Path(rp).name in LOCKFILES:
            text = p.read_text(encoding='utf-8', errors='replace')[:20000]
            if re.search(r'integrity|checksum|resolved|hash|h1:', text, re.I):
                integrity.append(rp)
    findings = []
    if manifests and not lockfiles:
        findings.append({'kind':'missing_lock_evidence','locator':manifests[0],'severity':'LOW','confidence':'MEDIUM','detail':'Manifest observed without a recognized lockfile; ecosystem-specific alternatives may exist.'})
    return {
        'schema_version':'supply-chain-health/v1',
        'subject_revision':revision,
        'manifests':manifests,
        'lockfiles':lockfiles,
        'update_automation':updates,
        'sbom_evidence':sbom,
        'license_evidence':licenses,
        'integrity_signals':integrity,
        'findings':findings,
        'dependency_inventory':{'state':'PARTIAL' if manifests or lockfiles else 'UNVERIFIED'},
        'provenance':{'state':'PARTIAL' if sbom else 'UNVERIFIED'},
        'confidence':'PARTIAL' if manifests or lockfiles or updates or sbom or licenses else 'UNVERIFIED',
        'unknowns':['Static repository evidence does not prove vulnerability absence, transitive dependency completeness, license compatibility, provenance freshness, or package authenticity.'],
    }
