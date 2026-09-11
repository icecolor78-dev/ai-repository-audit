from __future__ import annotations
import tempfile
from pathlib import Path
from test_depth_map import analyze

REV = '3' * 40
with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp); (root/'src').mkdir(); (root/'tests').mkdir()
    (root/'src/app.py').write_text('def f(): return 1\n', encoding='utf-8')
    (root/'tests/test_src.py').write_text('def test_src(): assert True\n', encoding='utf-8')
    partial = analyze(root, REV)
    assert partial['subsystem_map'][0]['state'] == 'PARTIAL'
    verified = analyze(root, REV, ['tests/test_src.py'])
    assert verified['subsystem_map'][0]['state'] == 'VERIFIED'
    assert verified['test_files'][0]['executed_on_subject'] is True
print('test depth map tests passed')
