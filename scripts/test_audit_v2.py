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
    (r/'src/app.py').write_text('from src import helper\nOAuth = RBAC = tenant = webhook = database = retry = backoff = idempotency = audit_log = correlation_id = tool = confirmation = untrusted = content = max_steps = max_tokens = transaction = lock = environment = config = retention = delete = TLS = backup = restore = rollback = kill_switch = True\n',encoding='utf-8')
    (r/'src/helper.py').write_text('VALUE = 1\n',encoding='utf-8')
    (r/'migrations/001.sql').write_text('ALTER TABLE users ADD COLUMN handle TEXT; rollback backward compatible',encoding='utf-8')
    (r/'api/openapi.yaml').write_text('openapi: 3.1.0\ncomponents:\n  schemas:\n    User:\n      type: object\n',encoding='utf-8')
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
    assert 'src/app.py -> src/helper.py' in d['architecture']['dependency_edges']
    assert d['contract_drift']['surfaces']==['api/openapi.yaml']
    assert any(x['dimension']=='contract_drift' for x in d['overall_portrait']['explicit_unknowns'])
    assert all('ignored.yml' not in str(value) for value in d.values())

    bundle={
      'version':'audit-evidence/v1',
      'subject':{'repository':'example/repo','revision':rev},
      'observed_at':OBSERVED,
      'workflow_runs':[{'name':'CI','revision':rev,'status':'completed','conclusion':'success','source':'https://github.com/example/repo/actions/runs/1'}],
      'test_runs':[{'suite':'unit','revision':rev,'status':'completed','passed':12,'failed':0,'skipped':1,'source':'https://github.com/example/repo/actions/runs/1'}],
      'release_runs':[]
    }
    with_evidence=compose_v2(r,'example/repo',rev,'main',OBSERVED,bundle)
    assert with_evidence['external_execution_evidence']['trust']=='SUPPLIED_EXACT'
    assert with_evidence['ci']['exact_subject_runs']
    assert with_evidence['tests']['exact_subject_execution']
    assert with_evidence['overall_portrait']['verdict']==d['overall_portrait']['verdict']
    assert any(x['dimension']=='external_execution_evidence' for x in with_evidence['overall_portrait']['explicit_unknowns'])
print('Integrated Audit v2 tests passed')
