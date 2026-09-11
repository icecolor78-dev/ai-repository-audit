from __future__ import annotations
import tempfile
from pathlib import Path
from supply_chain_health import analyze

REV = '6' * 40
with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp); (root/'.github').mkdir()
    (root/'package.json').write_text('{"dependencies":{"x":"1.0.0"}}', encoding='utf-8')
    data = analyze(root, REV)
    assert data['dependency_inventory']['state'] == 'PARTIAL'
    assert any(f['kind'] == 'missing_lock_evidence' for f in data['findings'])
    (root/'package-lock.json').write_text('{"packages":{},"integrity":"sha512-demo"}', encoding='utf-8')
    data = analyze(root, REV)
    assert data['lockfiles'] == ['package-lock.json']
    assert data['integrity_signals'] == ['package-lock.json']
print('supply-chain health tests passed')
