# /// script
# requires-python = ">=3.12"
# dependencies = ["mcp==2.3.0"]
# ///
"""Explicit flagship replacement jobs; preserve previous tasks, sources and spending."""
import asyncio,json,tempfile,sys,re
from pathlib import Path
from mcp import ClientSession,StdioServerParameters
from mcp.client.stdio import stdio_client
sys.path.insert(0,str(Path(__file__).parent))
from forest_wreck_meshy import extract,save,ROOT,LEDGER
SPECS={
 'Medium_Flagship71':('Medium_wreck_isolated_v1.png',30000,(25000,35000),'Gray painted military armor and distinct muted olive painted stripe. Crisp panel boundaries, dark recessed hoses, rigid structural rails, restrained edge wear and scorch. Preserve the selected upright shallow machinery wall, armor coverage and exterior shape. No extra rooms, floors or rubble.'),
 'Large_Flagship71':('Large_wreck_isolated_v1.png',65000,(55000,75000),'Weathered military ship exterior, gray painted armor with a clearly distinct muted olive stripe, exposed dark metallic frame and piping. Crisp readable armor seams, chipped edges, localized scorch. Retain the horizontal Large module silhouette and attached left machinery housing. No stacked decks, rooms, furniture or loose rubble.'),
 'Engine_Flagship71':('D5_nacelle_isolated_v1.png',45000,(35000,55000),'Armored military engine nacelle with gray paint, distinct muted olive armor band, dark exposed metal and pipes, localized chipped edges and soot around the short exhaust. Preserve the reference armored horizontal cylinder and nozzle silhouette. No glowing armor, complete engine internals, rooms, extra engines or ground.')}
def credits(result):
 match=re.search(r'Balance\*\*:\s*([\d,]+)','\n'.join(b.text for b in result.content if b.type=='text'))
 assert match,'Balance unavailable';return int(match.group(1).replace(',',''))
async def main():
 asset=sys.argv[1];mode=sys.argv[2] if len(sys.argv)>2 else 'status';assert asset in SPECS
 d=json.loads(LEDGER.read_text());item=next((x for x in d['operations'] if x['asset']==asset),None)
 params=StdioServerParameters(command='C:/Windows/System32/WindowsPowerShell/v1.0/powershell.exe',args=['-NoProfile','-ExecutionPolicy','Bypass','-File',str(ROOT/'tools/start_meshy_mcp.ps1')])
 with tempfile.TemporaryFile(mode='w+',encoding='utf-8') as err:
  async with stdio_client(params,errlog=err) as (r,w):
   async with ClientSession(r,w) as s:
    await s.initialize()
    if not item:
     assert mode=='submit','Status never submits';file,count,budget,prompt=SPECS[asset]
     assert d['reserved_or_spent']+35<=d['authorized_budget'];before=credits(await s.call_tool('meshy_check_balance',{}));assert before>=35
     request={'file_path':str(ROOT/'assets/models/forest_wreck/references'/file),'ai_model':'meshy-7.1','model_type':'standard','geometry_resolution':'4k','should_remesh':True,'topology':'triangle','target_polycount':count,'should_texture':True,'enable_pbr':True,'texture_resolution':'4k','image_enhancement':False,'texture_prompt':prompt,'save_pre_remeshed_model':True,'target_formats':['glb'],'response_format':'json'}
     item={'asset':asset,'operation':'image-to-3d','ai_model':'meshy-7.1','model_type':'standard','geometry_resolution':'4k','texture_resolution':'4k','target_triangles':count,'preferred_lod0_range':list(budget),'estimated_charge':35,'maximum_charge':35,'actual_charge':None,'outcome':'submission_started','task_id':None,'balance_before':['**Balance**: '+str(before)],'authorization':'Direct user request to recreate selected assets with flagship instead of Smart Topology; existing 600-credit assignment cap.','request':request}
     d['operations'].append(item);save(d)
     created=extract(await s.call_tool('meshy_image_to_3d',request));item['task_id']=created['task_id'];item['outcome']=created.get('status','PENDING');save(d)
     after=credits(await s.call_tool('meshy_check_balance',{}));item['observed_account_charge']=before-after
     if before-after==35:item.update(actual_charge=35,charge_evidence='Immediate account balance difference before next submission.')
     d['account_balance']=after;save(d)
    assert item['task_id'],'Uncertain submission reserved; never retry'
    result=extract(await s.call_tool('meshy_get_task_status',{'task_id':item['task_id'],'task_type':'image-to-3d','wait':False,'timeout_seconds':40,'response_format':'json'}))
    item['outcome']=result.get('status','UNKNOWN');item['progress']=result.get('progress');save(d)
    if item['outcome']=='SUCCEEDED' and not item.get('local_paths'):
     folder=ROOT/'assets/models/forest_wreck'/asset/'source';folder.mkdir(parents=True,exist_ok=True)
     downloaded=extract(await s.call_tool('meshy_download_model',{'task_id':item['task_id'],'task_type':'image-to-3d','format':'glb','save_to':str(folder/'meshy_original.glb')}))
     item['local_paths']=downloaded.get('local_paths') or [downloaded['local_path']];item['texture_paths']=downloaded.get('texture_paths',[]);assert all(Path(p).is_file() for p in item['local_paths'])
     # Preserve the optional high-detail pre-remesh source without logging signed URLs.
     url=(result.get('model_urls') or {}).get('pre_remeshed_glb')
     if url:
      import urllib.request
      urllib.request.urlretrieve(url,folder/'meshy_pre_remeshed.glb');item['pre_remeshed_path']=str(folder/'meshy_pre_remeshed.glb')
     save(d)
    d['account_balance']=credits(await s.call_tool('meshy_check_balance',{}));save(d)
    print(json.dumps({'asset':asset,'task_id':item['task_id'],'outcome':item['outcome'],'progress':item.get('progress'),'local_paths':item.get('local_paths'),'actual_spending':d['actual_spending'],'remaining':d['remaining_authorized_budget']}),flush=True)
try:asyncio.run(main())
except BaseException as error:
 def names(e):return [type(e).__name__]+[n for child in getattr(e,'exceptions',[]) for n in names(child)]
 print(json.dumps({'failure_types':names(error),'instruction':'Consult ledger; uncertain submissions must not be retried.'}),flush=True);raise SystemExit(1)
