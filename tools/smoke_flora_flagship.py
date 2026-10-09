# /// script
# requires-python = ">=3.12"
# dependencies = ["mcp==2.3.0"]
# ///
"""Inspect loaded trio and verify actual PIE map startup without changing gameplay."""
import asyncio,json,base64
from pathlib import Path
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
ROOT=Path(__file__).resolve().parents[1]
SC='editor_toolset.toolsets.scene.SceneTools';AT='editor_toolset.toolsets.actor.ActorTools';OB='editor_toolset.toolsets.object.ObjectTools';ED='EditorToolset.EditorAppToolset';AS='editor_toolset.toolsets.asset.AssetTools'
async def main():
 data=json.loads((ROOT/'reports/flora_flagship71_unreal_qa.json').read_text());checks=[]
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
   await call(SC,'load_level',level_path=data['map'])
   all_actors=await call(SC,'find_actors',name='FloraFlagship_',tag='',collision_channels=[])
   for actor in all_actors:
    label=await call(AT,'get_label',actor=actor)
    for billboard in await call(AT,'get_components',actor=actor,component_type={'refPath':'/Script/Engine.BillboardComponent'}):await call(OB,'set_properties',instance=billboard,values=json.dumps({'bVisible':False}))
    if label=='FloraFlagship_Fill':
     comp=(await call(AT,'get_components',actor=actor,component_type={'refPath':'/Script/Engine.LightComponent'}))[0]
     await call(OB,'set_properties',instance=comp,values=json.dumps({'Intensity':100000}))
   assert await call(AS,'save_assets',asset_paths=[data['map']])
   try:
    await call(ED,'StartPIE',options={'bSimulate':False,'playMode':'PlayMode_InViewPort','warmupSeconds':0})
    await asyncio.sleep(2);assert await call(ED,'IsPIERunning');checks.append({'name':'inspection PIE runs','passed':True})
    for item in data['assets']:
     found=await call(SC,'find_actors',name='FloraFlagship_'+item['id'],tag='',collision_channels=[]);assert len(found)==1
     comp=(await call(AT,'get_components',actor=found[0],component_type={'refPath':'/Script/Engine.StaticMeshComponent'}))[0]
     props=json.loads(await call(OB,'get_properties',instance=comp,properties=['StaticMesh','BodyInstance']))
     assert item['id'] in str(props['StaticMesh']),props
     collision=props['BodyInstance'].get('collisionEnabled',props['BodyInstance'].get('CollisionEnabled'))
     assert collision=='NoCollision',props['BodyInstance']
     checks.append({'name':item['id']+' mesh/nonblocking foliage in PIE','passed':True})
     if item['kind']=='tree':
      trunks=await call(SC,'find_actors',name='FloraTrunk_'+item['id'],tag='',collision_channels=[]);assert len(trunks)==1
      tc=(await call(AT,'get_components',actor=trunks[0],component_type={'refPath':'/Script/Engine.StaticMeshComponent'}))[0]
      tp=json.loads(await call(OB,'get_properties',instance=tc,properties=['BodyInstance']))
      state=tp['BodyInstance'].get('collisionEnabled',tp['BodyInstance'].get('CollisionEnabled'));assert state=='QueryAndPhysics'
      checks.append({'name':item['id']+' trunk-only blocker in PIE','passed':True})

   finally:
    if await call(ED,'IsPIERunning'):await call(ED,'StopPIE')
   pose={'location':{'x':-2500,'y':-3700,'z':1000},'rotation':{'pitch':-6,'yaw':57,'roll':0}}
   await call(ED,'SetCameraTransform',transform=pose);await asyncio.sleep(4)
   shot=await call(ED,'CaptureViewport',captureTransform=pose,bShowUI=False,annotations={'gridSpacing':0,'gridExtent':0,'gridHeight':0,'maxLabelDistance':0,'classFilter':{'refPath':'/Script/Engine.Actor'},'maxLabels':0})
   (ROOT/'reports/flora_flagship71_unreal_final.png').write_bytes(base64.b64decode(shot['image']['data']))
 data.update(pie_smoke_checks=checks,lods_collision='four LODs, trunk-only blocking proxies, nonblocking foliage; saved reload/traces and PIE state checked',visual_acceptance='candidate flora, not accepted final art; wind/instancing/performance unverified')
 (ROOT/'reports/flora_flagship71_unreal_qa.json').write_text(json.dumps(data,indent=2))
 print('WRECK_TRIO_SMOKE_COMPLETE',json.dumps(checks),flush=True)
asyncio.run(main())
