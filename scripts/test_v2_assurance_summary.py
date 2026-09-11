from v2_assurance_summary import DOMAINS, summarize

portrait={name:{'signals':[{'kind':'x'}],'confidence':'PARTIAL','unknowns':['runtime proof missing']} for name in DOMAINS}
s=summarize(portrait)
assert s['domain_count']==15
assert s['complete_contract'] is True
assert not s['missing_domains']
assert s['scoring']=='NONE'
assert all(x['state']=='PARTIAL' for x in s['domains'])
assert all('not a PASS score' in x['statement'] for x in s['domains'])

portrait['threat_model']['confidence']='CONTRADICTED'
contradicted=summarize(portrait)
state={x['domain']:x['state'] for x in contradicted['domains']}
assert state['threat_model']=='CONTRADICTED'

empty=summarize({})
assert empty['complete_contract'] is False
assert len(empty['missing_domains'])==15
assert all(x['state']=='UNVERIFIED' for x in empty['domains'])
print('V2 assurance summary tests passed')
