from __future__ import annotations

import argparse, json
from datetime import datetime, timezone
from pathlib import Path
from architecture_exact import analyze_architecture, analyze_contract_drift
from audit_portrait import compose
from exact_subject import bind_exact_subject, exact_tree_snapshot
from external_evidence import apply_bundle
from rem_extract_exact import build_exact_rem
from v2_assurance_summary import summarize


def compose_v2(root:Path,repository:str,revision:str,default_branch:str,observed_at:str,evidence_bundle:dict|None=None)->dict:
    binding=bind_exact_subject(root,repository,revision)
    if binding.get('exact') is not True:
        detail='; '.join(str(x) for x in binding.get('reasons',[]))
        raise ValueError(f'exact subject binding failed: {detail}')
    with exact_tree_snapshot(root,revision) as scan_root:
        rem=build_exact_rem(scan_root,repository,revision,default_branch,observed_at,binding)
        portrait=compose(scan_root,repository,revision,default_branch,observed_at,base_rem=rem)
        portrait['architecture']=analyze_architecture(scan_root)
        portrait['contract_drift']=analyze_contract_drift(scan_root)
    portrait['assurance_v2']=summarize(portrait)
    portrait['overall_portrait']['version']='2.0'
    portrait['overall_portrait']['assurance_contract_complete']=portrait['assurance_v2']['complete_contract']
    for item in portrait['architecture'].get('unknowns',[]):
        row={'dimension':'architecture','detail':item}
        if row not in portrait['overall_portrait']['explicit_unknowns']:
            portrait['overall_portrait']['explicit_unknowns'].append(row)
    for item in portrait['contract_drift'].get('unknowns',[]):
        portrait['overall_portrait']['explicit_unknowns'].append({'dimension':'contract_drift','detail':item})
    if evidence_bundle is not None:
        portrait=apply_bundle(portrait,evidence_bundle)
        portrait['overall_portrait']['explicit_unknowns'].append({
            'dimension':'external_execution_evidence',
            'detail':'SUPPLIED_EXACT evidence is exact-subject validated but caller-supplied; independent provider retrieval/authentication remains unverified.'
        })
    portrait['overall_portrait']['statement'] += ' V2 completeness means the 15-domain evidence contract is present; it is not a claim that every domain passed.'
    return portrait


def main():
    p=argparse.ArgumentParser(); p.add_argument('root',type=Path); p.add_argument('--repository',required=True); p.add_argument('--revision',required=True); p.add_argument('--default-branch',default='main'); p.add_argument('--observed-at'); p.add_argument('--evidence-bundle',type=Path)
    a=p.parse_args(); observed=a.observed_at or datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
    bundle=json.loads(a.evidence_bundle.read_text(encoding='utf-8')) if a.evidence_bundle else None
    print(json.dumps(compose_v2(a.root.resolve(),a.repository,a.revision,a.default_branch,observed,bundle),indent=2,sort_keys=True))
if __name__=='__main__': main()
