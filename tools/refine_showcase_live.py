# /// script
# requires-python = ">=3.12"
# dependencies = ["mcp==2.3.0"]
# ///
"""Iterate only the isolated showcase composition and lighting in the live editor."""
import asyncio,json
from pathlib import Path
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
ROOT=Path(__file__).resolve().parents[1];SC='editor_toolset.toolsets.scene.SceneTools';AT='editor_toolset.toolsets.actor.ActorTools';OB='editor_toolset.toolsets.object.ObjectTools';AS='editor_toolset.toolsets.asset.AssetTools';ED='EditorToolset.EditorAppToolset'
async def main():
 async with streamable_http_client('http://127.0.0.1:8000/mcp') as (r,w):
  async with ClientSession(r,w) as s:
   await s.initialize()
   async def call(ts,tool,**args):
    result=await s.call_tool('call_tool',{'toolset_name':ts,'tool_name':tool,'arguments':args})
    if result.is_error:raise RuntimeError(str(result.content))
    return json.loads(result.content[0].text).get('returnValue')
   assert not await call(ED,'IsPIERunning')
   level='/Game/LostVanguard/Environment/WreckShowcase/Maps/L_LargeWreck_Showcase';assert await call(SC,'get_current_level')==level
   removed=[]
   for actor in await call(SC,'find_actors',name='Showcase_',tag='',collision_channels=[]):
    label=await call(AT,'get_label',actor=actor)
    if label.startswith('Showcase_BackgroundTree_'):
     transform=await call(AT,'get_actor_transform',actor=actor)
     if transform['location']['y']<800:
      transform['location']['y']+=4300;await call(AT,'set_actor_transform',actor=actor,xform=transform,worldspace=True);removed.append(label)
    light=await call(AT,'get_components',actor=actor,component_type={'refPath':'/Script/Engine.LightComponent'})
    if light:
     intensity={'Showcase_SoftKey':6500,'Showcase_WarmEdge':8500,'Showcase_MoonRim':2.2,'Showcase_Sky':.5}.get(label,90 if label.startswith('Showcase_FaultGlow_') else None)
     if intensity is not None:assert await call(OB,'set_properties',instance=light[0],values=json.dumps({'Intensity':intensity}))
    if label=='Showcase_Exposure':
     assert await call(OB,'set_properties',instance=actor,values=json.dumps({'Settings':{'AutoExposureBias':-1.5}}))
   assert await call(AS,'save_assets',asset_paths=[level]);print('SHOWCASE_REFINED',json.dumps({'moved_foreground_trees_to_background':removed}),flush=True)
asyncio.run(main())
