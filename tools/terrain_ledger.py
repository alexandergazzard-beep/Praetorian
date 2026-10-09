import json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];p=R/'reports/forest_wreck_spending.json'
d=json.loads(p.read_text());asset,action=sys.argv[1:3]
item=next((x for x in d['operations'] if x['asset']==asset),None)
if action=='reserve':
 assert item is None and d['reserved_or_spent']+35<=d['authorized_budget']
 spec=json.loads((R/'reports/orison_terrain_specs.json').read_text())[asset]
 item=dict(asset=asset,operation='image-to-3d',ai_model='meshy-7.1',model_type='standard',geometry_resolution='4k',texture_resolution='4k',target_triangles=spec['target'],maximum_charge=35,estimated_charge=35,actual_charge=None,outcome='submission_started',task_id=None,balance_before=int(sys.argv[3]),authorization='User approves terrain proof and cap900; four models140 disclosed.')
 d['operations'].append(item)
elif action=='submitted':item.update(task_id=sys.argv[3],outcome='PENDING')
elif action=='charge':
 after=int(sys.argv[3]);charge=item['balance_before']-after;assert charge==35,(charge,after)
 item.update(actual_charge=charge,charge_evidence='Immediate account difference before next submission.');d['account_balance']=after
elif action=='status':item.update(outcome=sys.argv[3],progress=int(sys.argv[4]))
elif action=='download':
 path=Path(sys.argv[3]);assert path.is_file();item['local_paths']=[str(path)]
terminal={'SUCCEEDED','FAILED','CANCELED','CANCELLED'}
d['actual_spending']=sum(x.get('actual_charge') or 0 for x in d['operations'])
d['pending_jobs']=sum(bool(x.get('task_id')) and x['outcome'] not in terminal for x in d['operations'])
d['reserved_or_spent']=sum(x['actual_charge'] if x.get('actual_charge') is not None else x['maximum_charge'] for x in d['operations'])
d['remaining_authorized_budget']=d['authorized_budget']-d['reserved_or_spent']
p.write_text(json.dumps(d,indent=2));print(json.dumps(dict(asset=asset,outcome=item['outcome'],spent=d['actual_spending'],reserved=d['reserved_or_spent'],remaining=d['remaining_authorized_budget'])))
