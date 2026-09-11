from __future__ import annotations
import tempfile
from pathlib import Path
from audit_v2 import compose_v2

REV='c'*40
with tempfile.TemporaryDirectory() as tmp:
    r=Path(tmp); (r/'src').mkdir(); (r/'migrations').mkdir(); (r/'api').mkdir(); (r/'docs').mkdir(); (r/'evals').mkdir()
    (r/'src/app.py').write_text('''OAuth RBAC tenant webhook database retry backoff idempotency audit_log correlation_id tool confirmation untrusted content max_steps max_tokens transaction lock environment config retention delete TLS backup restore rollback kill switch''',encoding='utf-8')
    (r/'migrations/001.sql').write_text('ALTER TABLE users ADD COLUMN handle TEXT; rollback backward compatible',encoding='utf-8')
    (r/'api/openapi.yaml').write_text('openapi: 3.1.0\n',encoding='utf-8')
    (r/'docs/NOTICE.md').write_text('SPDX-License-Identifier: MIT\nThird-party attribution source origin',encoding='utf-8')
    (r/'evals/frozen.md').write_text('frozen holdout evaluation grader leakage hallucination regression model version',encoding='utf-8')
    d=compose_v2(r,'example/repo',REV,'main','2026-09-11T00:00:00Z')
    assert d['overall_portrait']['version']=='2.0'
    assert d['assurance_v2']['domain_count']==15
    assert d['assurance_v2']['complete_contract'] is True
    assert d['assurance_v2']['scoring']=='NONE'
    assert d['overall_portrait']['assurance_contract_complete'] is True
    assert 'not a claim that every domain passed' in d['overall_portrait']['statement']
    assert 'global_score' not in d
print('Integrated Audit v2 tests passed')
