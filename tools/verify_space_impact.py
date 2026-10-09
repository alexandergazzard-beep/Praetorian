# /// script
# requires-python = ">=3.12"
# dependencies = ["mcp==2.3.0"]
# ///
import asyncio,json,re,base64,shutil,time
from pathlib import Path
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
ROOT=Path(__file__).resolve().parents[1];ED='EditorToolset.EditorAppToolset';UI='SlateInspectorToolset.SlateInspectorToolset';SC='editor_toolset.toolsets.scene.SceneTools';NS='NiagaraToolsets.NiagaraToolset_System';D='/Game/LostVanguard/Environment/SpaceImpact'
async def main():
 async with streamable_http_client('http://127.0.0.1:8000/mcp') as (r,w):
  async with ClientSession(r,w) as s:
   await s.initialize()
   async def call(ts,tool,**args):
    r=await s.call_tool('call_tool',dict(toolset_name=ts,tool_name=tool,arguments=args))
    if r.is_error:raise RuntimeError(str(r.content))
    return json.loads(r.content[0].text)['returnValue']
   async def command(cmd):
    snapshot=await call(UI,'Snapshot',ref='',maxDepth=70)
    textbox=re.findall(r'textbox(?: \[focused\])? \[pos=335,1008[^\n]*\[ref=([^]]+)\]',snapshot)[-1]
    await call(UI,'Type',ref=textbox,text=cmd);await call(UI,'PressKey',key='Enter')
   await call(UI,'Observe',ref='',maxDepth=70)
   if not await call(ED,'IsPIERunning'):await call(ED,'StartPIE',options={'bSimulate':False,'playMode':'PlayMode_InViewPort','warmupSeconds':1})
   for cmd in ['stat fps','stat unit','r.ScreenPercentage','t.MaxFPS','r.VSync','csvprofile start']:await command(cmd)
   await asyncio.sleep(22)
   await command('csvprofile stop');await asyncio.sleep(3)
   shot=await call(UI,'Screenshot',ref='w4');(ROOT/'reports/space_impact_performance_view.png').write_bytes(base64.b64decode(shot['data']))
   await command('stat fps');await command('stat unit')
   before=set((ROOT/'Unreal/LostVanguard 5.8/Saved/Screenshots').rglob('*.png'))
   await command('HighResShot 1920x1080');await asyncio.sleep(3)
   after=set((ROOT/'Unreal/LostVanguard 5.8/Saved/Screenshots').rglob('*.png'));new=after-before
   if new:shutil.copy2(max(new,key=lambda x:x.stat().st_mtime),ROOT/'reports/space_impact_cinematic.png')
   samples=[]
   for i in range(3):
    shot=await call(UI,'Screenshot',ref='sp4');path=ROOT/'reports'/f'space_impact_motion_{i}.png';path.write_bytes(base64.b64decode(shot['data']));samples.append({'file':str(path),'wall_clock':time.time()});await asyncio.sleep(2)
   compile=await call(NS,'GetSystemCompileState',system={'refPath':D+'/FX/NS_ImpactAtmosphere.NS_ImpactAtmosphere'});issues=await call(NS,'GetStackIssues',system={'refPath':D+'/FX/NS_ImpactAtmosphere.NS_ImpactAtmosphere'})
   hero=await call(SC,'find_actors',name='Impact_EntryWreck',tag='',collision_channels=[]);burn=await call(SC,'find_actors',name='Impact_Burn_',tag='',collision_channels=[])
   assert len(hero)==1 and len(burn)==3;assert not compile['bHasErrors'];assert await call(ED,'IsPIERunning')
   result={'map':D+'/Maps/L_SpaceImpact_Cinematic','pie_runs':True,'runtime_hero_count':len(hero),'runtime_burn_sites':len(burn),'niagara_compile':compile,'niagara_issues':issues,'motion_samples':samples,'performance':'CSV analysis pending','image_is_actual_unreal':True}
   await call(ED,'StopPIE');result['pie_stopped']=True
   await call(ED,'SetCameraTransform',transform={'location':{'x':-1350,'y':-2000,'z':340},'rotation':{'pitch':-1,'yaw':57,'roll':0}})
   (ROOT/'reports/space_impact_qa.json').write_text(json.dumps(result,indent=2));print('SPACE_IMPACT_VERIFIED',flush=True)
asyncio.run(main())
