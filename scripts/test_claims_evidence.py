from __future__ import annotations
import tempfile
from pathlib import Path
from claims_evidence import analyze

REV = '1' * 40
with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    (root/'.github/workflows').mkdir(parents=True)
    (root/'tests').mkdir()
    (root/'README.md').write_text('CI is enabled.\nThe project is tested.\nProduction is secure.\n', encoding='utf-8')
    (root/'.github/workflows/ci.yml').write_text('name: CI\non: [push]\n', encoding='utf-8')
    (root/'tests/test_app.py').write_text('def test_ok(): assert True\n', encoding='utf-8')
    data = analyze(root, REV)
    assert data['schema_version'] == 'claims-evidence/v1'
    assert data['subject_revision'] == REV
    assert data['scoring'] == 'NONE'
    by_kind = {row['claim_kind']: row for row in data['items']}
    assert by_kind['ci']['state'] == 'PARTIAL'
    assert by_kind['tests']['state'] == 'PARTIAL'
    assert by_kind['security']['state'] == 'UNVERIFIED'
    assert all(row['subject_revision'] == REV for row in data['items'])
print('claims evidence tests passed')
