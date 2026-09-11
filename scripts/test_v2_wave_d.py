from __future__ import annotations
import tempfile
from pathlib import Path
from v2_wave_d import extract_wave_d

with tempfile.TemporaryDirectory() as tmp:
    r=Path(tmp); (r/'migrations').mkdir(); (r/'api').mkdir(); (r/'docs').mkdir()
    (r/'migrations/001.sql').write_text('ALTER TABLE users ADD COLUMN handle TEXT; -- rollback and backward compatible expand contract',encoding='utf-8')
    (r/'api/openapi.yaml').write_text('openapi: 3.1.0\ninfo:\n  version: 2.0.0\n',encoding='utf-8')
    (r/'docs/NOTICE.md').write_text('SPDX-License-Identifier: MIT\nThird-party attribution and source origin documented.',encoding='utf-8')
    a=extract_wave_d(r); b=extract_wave_d(r)
    assert a==b
    for section in ('migration','interface','license_ip'):
        assert a[section]['signals']
        assert a[section]['unknowns']
        assert a[section]['confidence']=='PARTIAL'
    assert all(s['state']=='PARTIAL' for section in a.values() for s in section['signals'])
print('Wave D tests passed')
