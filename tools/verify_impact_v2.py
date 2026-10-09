# /// script
# requires-python = ">=3.12"
# dependencies = ["mcp==2.3.0"]
# ///
import asyncio,json,re,base64,shutil,time
from pathlib import Path
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
R=Path(__file__).resolve().parents[1];UI='SlateInspectorToolset.SlateInspectorToolset';ED='EditorToolset.EditorAppToolset';NS='NiagaraToolsets.NiagaraToolset_System';D='/Game/LostVanguard/Environment/SpaceImpact'
async def main():
 async with streamable_http_client('http://127.0.0.1:8000/mcp') as (r,w):
  async with ClientSession(r,w) as session:
   await session.initialize()
   async def call(ts,name,**args):
    z=await session.call_tool('call_tool',{'toolset_name':ts,'tool_name':name,'arguments':args})
    if z.is_error:raise RuntimeError(str(z.content))
    return json.loads(z.content[0].text)['returnValue']
   async def cmd(text):await call(UI,'Type',ref='tb2',text=text,submit=True)
   await call(UI,'Observe',ref='',maxDepth=70)
   await call('editor_toolset.toolsets.object.ObjectTools','set_properties',instance={'refPath':'/Script/UnrealEd.Default__EditorPerformanceSettings'},values='{"bThrottleCPUWhenNotForeground":false}')
   if await call(ED,'IsPIERunning'):await call(ED,'StopPIE')
   await call(ED,'StartPIE',options={'bSimulate':False,'playMode':'PlayMode_InViewPort','warmupSeconds':2})
   await cmd('r.Editor.Viewport.OverridePIEScreenPercentage 0');await cmd('r.DynamicRes.OperationMode 0');await cmd('r.ScreenPercentage 100');await cmd('r.VSync 0');await cmd('t.MaxFPS 0')
   await asyncio.sleep(8)
   await cmd('HighResShot 1920x1080');await asyncio.sleep(3)
   shots=R/'Unreal/LostVanguard 5.8/Saved/Screenshots/WindowsEditor'
   shutil.copy2(max(shots.glob('*.png'),key=lambda p:p.stat().st_mtime),R/'reports/space_impact_v2_cinematic.png')
   await cmd('csvprofile start')
   await cmd('py "'+str(R/'tools/orbit_impact_runtime.py').replace('\\','/')+'"')
   samples=[]
   for i in range(6):
    shot=await call(UI,'Screenshot',ref='w1');p=R/'reports'/f'space_impact_v2_orbit_{i}.png';p.write_bytes(base64.b64decode(shot['data']));samples.append(str(p));await asyncio.sleep(3)
   await asyncio.sleep(10);await cmd('csvprofile stop');await asyncio.sleep(3)
   await cmd('HighResShot 1920x1080');await asyncio.sleep(2)
   shutil.copy2(max(shots.glob('*.png'),key=lambda p:p.stat().st_mtime),R/'reports/space_impact_v2_alternate.png')
   qa={}
   for name in ['NS_ImpactFireVolume','NS_ImpactEmbers']:
    sys={'refPath':D+'/FX/'+name+'.'+name};qa[name]={'summary':await call(NS,'GetSystemSummary',system=sys),'compile':await call(NS,'GetSystemCompileState',system=sys),'issues':await call(NS,'GetStackIssues',system=sys)}
    assert not qa[name]['compile']['bHasErrors']
   qa.update(actual_pie=True,render_screen_percentage=100,editor_override_disabled=True,dynamic_resolution_disabled=True,camera_motion_evidence=json.loads((R/'reports/space_impact_v2_camera_motion.json').read_text()),orbit_screenshots=samples,visual_acceptance='User rejected original; revised candidate requires user review',historical_live_material_update_crash=True)
   assert await call(ED,'IsPIERunning')
   await call(ED,'StopPIE')
   await cmd('r.Editor.Viewport.OverridePIEScreenPercentage 1');await cmd('r.ScreenPercentage 0')
   await call('editor_toolset.toolsets.object.ObjectTools','set_properties',instance={'refPath':'/Script/UnrealEd.Default__EditorPerformanceSettings'},values='{"bThrottleCPUWhenNotForeground":true}')
   (R/'reports/space_impact_v2_qa.json').write_text(json.dumps(qa,indent=2));print('IMPACT_V2_VERIFIED',flush=True)
asyncio.run(main())
