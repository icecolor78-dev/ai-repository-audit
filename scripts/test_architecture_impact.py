from __future__ import annotations
import tempfile
from pathlib import Path
from architecture_impact import analyze

REV = '7' * 40
with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp); (root/'app').mkdir(); (root/'core').mkdir()
    (root/'app/main.py').write_text('import core\n', encoding='utf-8')
    (root/'core/__init__.py').write_text('VALUE=1\n', encoding='utf-8')
    data = analyze(root, REV)
    assert data['top_level_boundaries'] == ['app', 'core']
    assert any(e['from'] == 'app/main.py' and e['to'] == 'core' for e in data['dependency_edges'])
    assert data['hotspots'][0]['boundary'] == 'core'
    assert data['change_impact']['state'] == 'PARTIAL'
print('architecture impact tests passed')
