import subprocess,json,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
UV='C:/Users/alexa/AppData/Local/Programs/Python/Python312/Scripts/uv.exe'
BLENDER='C:/Program Files/Blender Foundation/Blender 5.2/blender.exe'
specs=json.loads((ROOT/'reports/flora_flagship71_specs.json').read_text())
def run(cmd,log=None):
 p=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True,encoding='utf-8',errors='replace')
 if log:(ROOT/'reports'/log).write_text(p.stdout+'\n'+p.stderr)
 if p.returncode:raise RuntimeError('Local step failed: '+str(cmd[1:]))
 return p.stdout
pending=set(specs)
while pending:
 for asset in list(specs):
  if asset not in pending:continue
  print(run([UV,'run','tools/recreate_flora_flagship.py',asset,'status']).strip(),flush=True)
  ledger=json.loads((ROOT/'reports/forest_wreck_spending.json').read_text())
  item=next(x for x in ledger['operations'] if x['asset']==asset)
  if item['outcome'] in ('FAILED','CANCELED','CANCELLED'):raise RuntimeError(asset+' terminal failure; no paid retry')
  if item['outcome']=='SUCCEEDED' and item.get('local_paths'):
   run([BLENDER,'--background','--python','tools/prepare_flora_flagship.py','--',asset],asset+'_prepare.log')
   pending.remove(asset);print('PREPARED '+asset,flush=True)
 if pending:time.sleep(45)
run([BLENDER,'--background','--python','tools/export_flora_flagship.py'],'flora_flagship71_export.log')
print(run(['C:/Users/alexa/AppData/Local/Programs/Python/Python312/python.exe','tools/verify_flora_flagship.py']),flush=True)
print('FLORA_GENERATION_PREPARATION_COMPLETE',flush=True)
