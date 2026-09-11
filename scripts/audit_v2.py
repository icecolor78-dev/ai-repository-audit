from __future__ import annotations

import argparse, json
from datetime import datetime, timezone
from pathlib import Path
from audit_portrait import compose
from exact_subject import bind_exact_subject, exact_tree_snapshot
from rem_extract_exact import build_exact_rem
from v2_assurance_summary import summarize


def compose_v2(root:Path,repository:str,revision:str,default_branch:str,observed_at:str)->dict:
    binding=bind_exact_subject(root,repository,revision)
    if binding.get('exact') is not True:
        detail='; '.join(str(x) for x in binding.get('reasons',[]))
        raise ValueError(f'exact subject binding failed: {detail}')
    with exact_tree_snapshot(root,revision) as scan_root:
        rem=build_exact_rem(scan_root,repository,revision,default_branch,observed_at,binding)
        portrait=compose(scan_root,repository,revision,default_branch,observed_at,base_rem=rem)
    portrait['assurance_v2']=summarize(portrait)
    portrait['overall_portrait']['version']='2.0'
    portrait['overall_portrait']['assurance_contract_complete']=portrait['assurance_v2']['complete_contract']
    portrait['overall_portrait']['statement'] += ' V2 completeness means the 15-domain evidence contract is present; it is not a claim that every domain passed.'
    return portrait


def main():
    p=argparse.ArgumentParser(); p.add_argument('root',type=Path); p.add_argument('--repository',required=True); p.add_argument('--revision',required=True); p.add_argument('--default-branch',default='main'); p.add_argument('--observed-at')
    a=p.parse_args(); observed=a.observed_at or datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
    print(json.dumps(compose_v2(a.root.resolve(),a.repository,a.revision,a.default_branch,observed),indent=2,sort_keys=True))
if __name__=='__main__': main()
