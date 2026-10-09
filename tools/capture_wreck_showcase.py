# /// script
# requires-python = ">=3.12"
# dependencies = ["mcp==2.3.0"]
# ///
"""Capture and verify the real textured showcase level through Unreal's native bridge."""
import asyncio,json,base64,math
from pathlib import Path
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
ROOT=Path(__file__).resolve().parents[1]
SC='editor_toolset.toolsets.scene.SceneTools';AT='editor_toolset.toolsets.actor.ActorTools';OB='editor_toolset.toolsets.object.ObjectTools';ED='EditorToolset.EditorAppToolset';AS='editor_toolset.toolsets.asset.AssetTools'
async def main():
 data=json.loads((ROOT/'reports/wreck_showcase_build.json').read_text());checks=[]
 async with streamable_http_client('http://127.0.0.1:8000/mcp') as (r,w):
  async with ClientSession(r,w) as s:
   await s.initialize()
   async def call(ts,tool,**args):
    result=await asyncio.wait_for(s.call_tool('call_tool',{'toolset_name':ts,'tool_name':tool,'arguments':args}),60)
    if result.is_error:
     if tool=='StartPIE' and 'PIE ended before warmup completed' in str(result.content) and await call(ED,'IsPIERunning'):return True
     raise RuntimeError(str(result.content))
    return json.loads(result.content[0].text).get('returnValue')
   if await call(ED,'IsPIERunning'):await call(ED,'StopPIE')
   await call(SC,'load_level',level_path=data['map']);assert await call(SC,'get_current_level')==data['map']
   found=await call(SC,'find_actors',name='Showcase_',tag='',collision_channels=[]);assert len(found)>100
   checks.append({'name':'saved showcase reload','passed':True,'showcase_actor_count':len(found)})
   distance=await call(SC,'trace_world',start={'x':-1200,'y':-1700,'z':400},end={'x':-1200,'y':-1700,'z':-500});assert distance is not None
   checks.append({'name':'start terrain collision','passed':True,'hit_cm':distance})
   poses=[((-1450,-1900,360),(0,350,350)),((-400,-1800,190),(200,400,280)),((1500,-2100,500),(150,350,320))]
   await call(ED,'SelectActors',actors=[])
   for i,(loc,target) in enumerate(poses):
    dx,dy,dz=[target[j]-loc[j] for j in range(3)];pose={'location':dict(zip('xyz',loc)),'rotation':{'pitch':math.degrees(math.atan2(dz,math.hypot(dx,dy))),'yaw':math.degrees(math.atan2(dy,dx)),'roll':0}}
    await call(ED,'SetCameraTransform',transform=pose);await asyncio.sleep(6)
    shot=await call(ED,'CaptureViewport',captureTransform=pose,bShowUI=False,annotations={'gridSpacing':0,'gridExtent':0,'gridHeight':0,'maxLabelDistance':0,'classFilter':{'refPath':'/Script/Engine.Actor'},'maxLabels':0})
    (ROOT/'reports'/f'wreck_showcase_{i}.png').write_bytes(base64.b64decode(shot['image']['data']))
   try:
    await call(ED,'StartPIE',options={'bSimulate':False,'playMode':'PlayMode_InViewPort','warmupSeconds':0});await asyncio.sleep(2);assert await call(ED,'IsPIERunning')
    hero=await call(SC,'find_actors',name='Showcase_HeroLarge',tag='',collision_channels=[]);assert len(hero)==1
    checks.append({'name':'PIE runs with hero wreck present','passed':True})
   finally:
    if await call(ED,'IsPIERunning'):await call(ED,'StopPIE')
   loc,target=poses[0];dx,dy,dz=[target[j]-loc[j] for j in range(3)];await call(ED,'SetCameraTransform',transform={'location':dict(zip('xyz',loc)),'rotation':{'pitch':math.degrees(math.atan2(dz,math.hypot(dx,dy))),'yaw':math.degrees(math.atan2(dy,dx)),'roll':0}})
 data.update(checks=checks,visual_acceptance='pending capture inspection',performance='unverified',piestopped=True)
 (ROOT/'reports/wreck_showcase_qa.json').write_text(json.dumps(data,indent=2));print('SHOWCASE_CAPTURE_COMPLETE',json.dumps(checks),flush=True)
asyncio.run(main())
