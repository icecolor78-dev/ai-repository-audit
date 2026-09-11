from __future__ import annotations
import tempfile
from pathlib import Path
from release_provenance import analyze

REV = '4' * 40
with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp); wf = root/'.github/workflows'; wf.mkdir(parents=True)
    (wf/'release.yml').write_text('''name: release
on:
  release:
    types: [published]
permissions:
  contents: read
  id-token: write
jobs:
  publish:
    steps:
      - uses: actions/checkout@v4
      - uses: actions/upload-artifact@v4
      - run: echo provenance attest verify
''', encoding='utf-8')
    data = analyze(root, REV)
    assert data['trusted_publishing']['state'] == 'PARTIAL'
    assert data['provenance']['state'] == 'PARTIAL'
    assert data['release_workflows'][0]['artifact_handoff'] is True
    assert any(f['kind'] == 'mutable_release_dependency' for f in data['findings'])
print('release provenance tests passed')
