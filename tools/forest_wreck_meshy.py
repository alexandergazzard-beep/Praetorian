# /// script
# requires-python = ">=3.12"
# dependencies = ["mcp==2.3.0"]
# ///
"""Budget-limited Meshy candidate generation; resume existing jobs, never retry blindly."""
import asyncio,json,tempfile,sys,re
from pathlib import Path
from mcp import ClientSession,StdioServerParameters
from mcp.client.stdio import stdio_client
ROOT=Path(__file__).resolve().parents[1];LEDGER=ROOT/'reports/forest_wreck_spending.json'
SPECS={'F01_MeshyCanopy':('F01_isolated_v1.png',15000,'Realistic natural woody alien tree, dark rough gnarled bark, layered blue-green leathery foliage and muted violet undersides. No glowing colors, soil base or stones; separate visible trunk and branching.'),'Engine_MeshyNacelle':('D5_nacelle_isolated_v1.png',14000,'Gray painted military armor, muted olive green stripe, matte weathered metal, localized scorch and shallow exposed electronics. Retain exterior panels. No hidden rooms, decks or interior furniture.')}
SPECS.update({
 'Large_WreckModule':('Large_wreck_isolated_v1.png',15000,'Weathered gray military armor with muted olive stripe, dark recessed pipework, rigid exposed rectangular frame and localized broken edges. Preserve the horizontal bulky exterior machinery and hull fragment from the selected Large reference, with thick armor edges and short left equipment housing. No stacked decks, hidden rooms, furniture, ground or loose rubble.'),
 'Medium_WreckPanel':('Medium_wreck_isolated_v1.png',18000,'Weathered gray military armor with muted olive stripe, dark recessed pipework, thick rigid structural frame and localized broken edges. Retain the pictured upright armored equipment wall and shallow right-side fittings. No new rooms, floors, furniture, ground or loose rubble.'),
 'VeryLarge_HullFace':('VeryLarge_wreck_isolated_v1.png',45000,'Battered gray and muted olive military ship armor. Preserve the two visible shallow deck faces, railings and door/wall panels from this specific selected reference. No deeper hidden rooms, additional floors, furniture or complete interiors. Thick exterior plates, robust frame, restrained scorch; readable broken edges and simplified pipes. No ground or loose rubble.')
})
def extract(r):
 if r.is_error:raise RuntimeError('Connector operation rejected')
 if r.structured_content:return r.structured_content
 for b in r.content:
  if b.type=='text':
   try:return json.loads(b.text)
   except json.JSONDecodeError:pass
 return {}
def save(d):
 ops=d['operations'];terminal={'SUCCEEDED','FAILED','CANCELED','CANCELLED'}
 d['actual_spending']=sum(x.get('actual_charge') or 0 for x in ops)
 d['pending_jobs']=sum(bool(x.get('task_id')) and x['outcome'] not in terminal for x in ops)
 d['reserved_or_spent']=sum(x['actual_charge'] if x.get('actual_charge') is not None else x['maximum_charge'] for x in ops)
 d['remaining_authorized_budget']=d['authorized_budget']-d['reserved_or_spent']
 if d.get('authorized_next_operation'):
  op=next((x for x in ops if x['asset']==d['authorized_next_operation']['asset']),None)
  if op:d['authorized_next_operation'].update(task_id=op.get('task_id'),outcome=op['outcome'])
 LEDGER.write_text(json.dumps(d,indent=2),encoding='utf-8')
async def main():
 asset=sys.argv[1];mode=sys.argv[2] if len(sys.argv)>2 else 'status'
 d=json.loads(LEDGER.read_text()) if LEDGER.exists() else {'authorized_budget':600,'cost_source':'https://docs.meshy.ai/en/api/pricing','pricing_checked':'2026-10-08','operations':[]}
 params=StdioServerParameters(command='C:/Windows/System32/WindowsPowerShell/v1.0/powershell.exe',args=['-NoProfile','-ExecutionPolicy','Bypass','-File',str(ROOT/'tools/start_meshy_mcp.ps1')])
 with tempfile.TemporaryFile(mode='w+',encoding='utf-8') as err:
  async with stdio_client(params,errlog=err) as (r,w):
   async with ClientSession(r,w) as s:
    await s.initialize()
    specs=await s.list_tools()
    assert 'meshy_image_to_3d' in [t.name for t in specs.tools]
    item=next((x for x in reversed(d['operations']) if x['asset']==asset and x['outcome']!='LOCAL_VALIDATION_REJECTED'),None)
    if item is None:
     assert mode=='submit','No job exists; status mode never submits'
     image,count,prompt=SPECS[asset];count=min(count,15000);file=ROOT/'assets/models/forest_wreck/references'/image;assert file.is_file()
     reserved=sum(x['maximum_charge'] for x in d['operations']);assert reserved+15<=d['authorized_budget']
     balance=await s.call_tool('meshy_check_balance',{});assert not balance.is_error
     item={'asset':asset,'operation':'image-to-3d','ai_model':'meshy-t2','model_type':'smart-topology','texture_resolution':'2k','target_triangles':count,'estimated_charge':15,'maximum_charge':15,'actual_charge':None,'outcome':'submission_started','task_id':None,'balance_before':[b.text for b in balance.content if b.type=='text']}
     d['operations'].append(item);save(d)
     created=extract(await s.call_tool('meshy_image_to_3d',{'file_path':str(file),'ai_model':'meshy-t2','model_type':'smart-topology','target_polycount':count,'should_texture':True,'enable_pbr':True,'texture_resolution':'2k','texture_prompt':prompt,'response_format':'json'}))
     item['task_id']=created['task_id'];item['outcome']=created.get('status','PENDING');save(d)
    assert item['task_id'],'Submission uncertain; reserved charge retained; do not retry'
    status=extract(await s.call_tool('meshy_get_task_status',{'task_id':item['task_id'],'task_type':'image-to-3d','wait':False,'timeout_seconds':40,'response_format':'json'}))
    item['outcome']=status.get('status','UNKNOWN');item['progress']=status.get('progress');save(d)
    if item['outcome']=='SUCCEEDED' and not item.get('local_paths'):
     folder=ROOT/'assets/models/forest_wreck'/asset/'source';folder.mkdir(parents=True,exist_ok=True)
     downloaded=extract(await s.call_tool('meshy_download_model',{'task_id':item['task_id'],'task_type':'image-to-3d','format':'glb','save_to':str(folder/'meshy_original.glb')}))
     item['local_paths']=downloaded.get('local_paths') or ([downloaded['local_path']] if downloaded.get('local_path') else [])
     item['texture_paths']=downloaded.get('texture_paths',[])
     assert item['local_paths'] and all(Path(p).is_file() for p in item['local_paths']),'Download not saved locally'
     balance=await s.call_tool('meshy_check_balance',{});assert not balance.is_error
     item['balance_after']=[b.text for b in balance.content if b.type=='text'];save(d)
    balance=await s.call_tool('meshy_check_balance',{});assert not balance.is_error
    item['latest_balance']=[b.text for b in balance.content if b.type=='text']
    def credits(texts):
     match=re.search(r'Balance\*\*:\s*([\d,]+)', '\n'.join(texts))
     return int(match.group(1).replace(',','')) if match else None
    before=credits(item['balance_before']);after=credits(item['latest_balance'])
    d['account_balance']=after if after is not None else item['latest_balance']
    if before is not None and after is not None:
     item['observed_account_charge']=before-after
     if item.get('actual_charge') is None and before-after==item['estimated_charge']:
      item['actual_charge']=before-after
      item['charge_evidence']='Balance decreased by quoted cost during this operation, before the next assignment submission. Charged pending tasks count toward spending.'
    save(d)
    print(json.dumps({'asset':asset,'task_id':item['task_id'],'outcome':item['outcome'],'progress':item.get('progress'),'local_paths':item.get('local_paths'),'maximum_reserved':sum(x['maximum_charge'] for x in d['operations'])}),flush=True)
if __name__=='__main__':
 try:asyncio.run(main())
 except BaseException as error:
  def names(e):return [type(e).__name__]+[n for child in getattr(e,'exceptions',[]) for n in names(child)]
  print(json.dumps({'failure_types':names(error),'ledger_present':LEDGER.exists(),'generation_outcome':'consult ledger; do not retry uncertain submissions'}),flush=True)
  raise SystemExit(1)
