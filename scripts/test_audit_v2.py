from __future__ import annotations
import subprocess
import tempfile
from pathlib import Path
from audit_v2 import compose_v2

OBSERVED='2026-09-11T00:00:00Z'

def git(root:Path,*args:str)->str:
    return subprocess.run(['git','-C',str(root),*args],check=True,capture_output=True,text=True).stdout.strip()

with tempfile.TemporaryDirectory() as tmp:
    r=Path(tmp)
    git(r,'init')
    git(r,'config','user.email','audit@example.invalid')
    git(r,'config','user.name','Audit Test')
    git(r,'remote','add','origin','https://github.com/example/repo.git')
    (r/'src').mkdir(); (r/'migrations').mkdir(); (r/'api').mkdir(); (r/'docs').mkdir(); (r/'evals').mkdir()
    (r/'src/app.py').write_text('OAuth RBAC tenant webhook database retry backoff idempotency audit_log correlation_id tool confirmation untrusted content max_steps max_tokens transaction lock environment config retention delete TLS backup restore rollback kill switch',encoding='utf-8')
    (r/'migrations/001.sql').write_text('ALTER TABLE users ADD COLUMN handle TEXT; rollback backward compatible',encoding='utf-8')
    (r/'api/openapi.yaml').write_text('openapi: 3.1.0\n',encoding='utf-8')
    (r/'docs/NOTICE.md').write_text('SPDX-License-Identifier: MIT\nThird-party attribution source origin',encoding='utf-8')
    (r/'evals/frozen.md').write_text('frozen holdout evaluation grader leakage hallucination regression model version',encoding='utf-8')
    (r/'README.md').write_text('CI tests security release\n',encoding='utf-8')
    (r/'.gitignore').write_text('ignored.yml\n',encoding='utf-8')
    git(r,'add','.')
    git(r,'commit','-m','fixture')
    rev=git(r,'rev-parse','HEAD')
    (r/'ignored.yml').write_text('on: [push]\njobs: {unsafe: {runs-on: ubuntu-latest}}\n',encoding='utf-8')
    d=compose_v2(r,'example/repo',rev,'main',OBSERVED)
    assert d['schema_version']=='rem/v1.1'
    assert d['overall_portrait']['version']=='2.0'
    assert d['assurance_v2']['domain_count']==15
    assert d['assurance_v2']['complete_contract'] is True
    assert d['assurance_v2']['scoring']=='NONE'
    assert d['overall_portrait']['assurance_contract_complete'] is True
    assert 'not a claim that every domain passed' in d['overall_portrait']['statement']
    assert 'global_score' not in d
    assert all('ignored.yml' not in str(value) for value in d.values())
print('Integrated Audit v2 tests passed')
