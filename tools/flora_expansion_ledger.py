"""Record native connector generation steps without credentials or signed URLs."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
LEDGER=ROOT/'reports/forest_wreck_spending.json'
def save(d):
 ops=d['operations'];terminal={'SUCCEEDED','FAILED','CANCELED','CANCELLED'}
 d['actual_spending']=sum(x.get('actual_charge') or 0 for x in ops)
 d['pending_jobs']=sum(bool(x.get('task_id')) and x['outcome'] not in terminal for x in ops)
 d['reserved_or_spent']=sum(x['actual_charge'] if x.get('actual_charge') is not None else x['maximum_charge'] for x in ops)
 d['remaining_authorized_budget']=d['authorized_budget']-d['reserved_or_spent']
 LEDGER.write_text(json.dumps(d,indent=2),encoding='utf-8')
asset,action=sys.argv[1:3]
d=json.loads(LEDGER.read_text())
spec=json.loads((ROOT/'reports/flora_expansion71_specs.json').read_text())[asset]
item=next((x for x in d['operations'] if x['asset']==asset),None)
if action=='reserve':
 assert item is None and d['reserved_or_spent']+35<=d['authorized_budget']
 item=dict(asset=asset,operation='image-to-3d',ai_model='meshy-7.1',model_type='standard',geometry_resolution='4k',texture_resolution='4k',target_triangles=spec['target'],preferred_lod0_range=spec['range'],estimated_charge=35,maximum_charge=35,actual_charge=None,outcome='submission_started',task_id=None,authorization='User directly requests new flora models using best Meshy model; five specimens cost 175 within existing 600 cap, disclosed in chat.',balance_before=int(sys.argv[3]))
 d['operations'].append(item)
elif action=='submitted':
 assert item and not item['task_id']
 item.update(task_id=sys.argv[3],outcome='PENDING')
elif action=='charge':
 after=int(sys.argv[3]);charge=item['balance_before']-after
 assert charge==35,(charge,after)
 item.update(actual_charge=charge,charge_evidence='Immediate native connector account balance difference before next submission.')
 d['account_balance']=after
elif action=='status':
 assert item and item['task_id']
 item.update(outcome=sys.argv[3],progress=int(sys.argv[4]))
elif action=='download':
 path=Path(sys.argv[3]);assert path.is_file()
 item['local_paths']=[str(path)]
save(d)
print(json.dumps(dict(asset=asset,status=item['outcome'],task_id=item['task_id'],spent=d['actual_spending'],reserved=d['reserved_or_spent'],remaining=d['remaining_authorized_budget'])))
