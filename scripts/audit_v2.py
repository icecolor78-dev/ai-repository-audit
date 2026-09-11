from __future__ import annotations

import argparse, json
from datetime import datetime, timezone
from pathlib import Path
from audit_portrait import compose
from v2_assurance_summary import summarize


def compose_v2(root:Path,repository:str,revision:str,default_branch:str,observed_at:str)->dict:
    portrait=compose(root,repository,revision,default_branch,observed_at)
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
