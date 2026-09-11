from __future__ import annotations
import tempfile
from pathlib import Path
from workflow_security import analyze

REV = '5' * 40
with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp); wf = root/'.github/workflows'; wf.mkdir(parents=True)
    (wf/'danger.yml').write_text('''name: danger
on:
  pull_request_target:
permissions: write-all
jobs:
  run:
    steps:
      - uses: actions/checkout@v4
      - run: echo ${{ github.event.pull_request.title }}
''', encoding='utf-8')
    data = analyze(root, REV)
    kinds = {f['kind'] for f in data['findings']}
    assert {'pull_request_target', 'untrusted_expression_shell', 'mutable_action_ref', 'broad_permissions'} <= kinds
    assert data['risk'] == 'HIGH'
    assert data['scope'] == 'static workflow evidence only'
print('workflow security tests passed')
