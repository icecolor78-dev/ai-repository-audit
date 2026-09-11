from __future__ import annotations
import tempfile
from pathlib import Path
from ci_evidence_profiler import analyze

REV = '2' * 40
with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp); wf = root/'.github/workflows'; wf.mkdir(parents=True)
    (wf/'ci.yml').write_text('''name: CI
on:
  pull_request:
    paths: ["src/**"]
permissions:
  contents: read
jobs:
  test:
    if: github.event.pull_request.draft == false
    strategy:
      matrix:
        python: ["3.11", "3.12"]
    steps:
      - uses: actions/checkout@v4
''', encoding='utf-8')
    data = analyze(root, REV)
    assert data['subject_revision'] == REV
    assert data['false_green_risk'] == 'MEDIUM'
    profile = data['workflows'][0]
    assert profile['path_filters'] and profile['conditionals'] and profile['matrix']
    assert profile['permissions_declared']
    assert 'actions/checkout@v4' in profile['mutable_action_refs']
    assert data['required_checks']['state'] == 'UNVERIFIED'
print('CI evidence profiler tests passed')
