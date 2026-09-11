from __future__ import annotations
import tempfile
from pathlib import Path
from v2_wave_c import extract_wave_c

with tempfile.TemporaryDirectory() as tmp:
    r=Path(tmp); (r/'src').mkdir(); (r/'evals').mkdir()
    (r/'src/app.py').write_text('''
MAX_STEPS=12
DEFAULT_ENV='staging'
# configuration environment default fallback feature flag
def worker(job):
    with transaction():
        lock(job.id)
        retry_with_backoff(job)
        meter_tokens(max_tokens=400)
''',encoding='utf-8')
    (r/'evals/frozen_eval.md').write_text('Frozen holdout evaluation set. Check leakage, grader reliability, hallucination taxonomy, regression and model version drift.',encoding='utf-8')
    a=extract_wave_c(r); b=extract_wave_c(r)
    assert a==b
    for section in ('model_eval','finops','configuration','concurrency'):
        assert a[section]['signals']
        assert a[section]['unknowns']
        assert a[section]['confidence']=='PARTIAL'
    assert all(s['state']=='PARTIAL' for section in a.values() for s in section['signals'])
print('Wave C tests passed')
