# /// script
# requires-python = ">=3.12"
# dependencies = ["mcp==2.3.0"]
# ///
import asyncio,base64,json
from pathlib import Path
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
async def main():
 async with streamable_http_client('http://127.0.0.1:8000/mcp') as (r,w):
  async with ClientSession(r,w) as session:
   await session.initialize()
   async def call(ts,tool,**args):
    result=await session.call_tool('call_tool',{'toolset_name':ts,'tool_name':tool,'arguments':args})
    if result.is_error:raise RuntimeError(str(result.content))
    return json.loads(result.content[0].text).get('returnValue')
   ed='EditorToolset.EditorAppToolset';scene='editor_toolset.toolsets.scene.SceneTools';obj='editor_toolset.toolsets.object.ObjectTools'
   if await call(ed,'IsPIERunning'):await call(ed,'StopPIE')
   await call(scene,'load_level',level_path='/Game/WreckagePrototype/Maps/L_Wreckage_Opening')
   level=await call(scene,'get_current_level');print('LIVE_LEVEL',level,flush=True)
   await call(ed,'StartPIE',options={'bSimulate':False,'playMode':'PlayMode_InViewPort','warmupSeconds':.5})
   p=(await call(scene,'find_actors',name='',tag='',collision_channels=[],actor_type={'refPath':'/Game/WreckagePrototype/Blueprints/BP_WreckagePlayer_Runtime.BP_WreckagePlayer_Runtime_C'}))[0]
   await asyncio.sleep(4)
   first=json.loads(await call(obj,'get_properties',instance=p,properties=['Step','Health','HasWeapon','Objective']))
   shot=await call(ed,'CaptureEditorImage');Path('reports/opening_before_debris.png').write_bytes(base64.b64decode(shot['data']))
   await call(obj,'set_properties',instance=p,values=json.dumps({'RequestInteract':True}))
   await asyncio.sleep(3)
   state=json.loads(await call(obj,'get_properties',instance=p,properties=['Step','Health','HasWeapon','Objective']))
   tr=await call('editor_toolset.toolsets.actor.ActorTools','get_actor_transform',actor=p)
   shot=await call(ed,'CaptureEditorImage');Path('reports/opening_starting_view_play.png').write_bytes(base64.b64decode(shot['data']))
   Path('reports/opening_live_preview.json').write_text(json.dumps({'level':level,'fresh':first,'after_debris':state,'transform':tr},indent=2))
   await call(ed,'StopPIE')
   # A clean editor capture at the recorded first-person pose supplements the
   # actual Play-In-Editor screenshot above. Restore the debris before saving.
   actor_ts='editor_toolset.toolsets.actor.ActorTools'
   debris=(await call(scene,'find_actors',name='',tag='LV_Debris',collision_channels=[]))[0]
   original=await call(actor_ts,'get_actor_transform',actor=debris)
   moved=json.loads(json.dumps(original));moved['location']['z']=-1500
   camera=json.loads(json.dumps(tr));camera['location']['z']+=64
   await call(actor_ts,'set_actor_transform',actor=debris,xform=moved,worldspace=True)
   editor_icons=[]
   try:
    for cls in ['Light','SkyLight','ExponentialHeightFog','PlayerStart']:
     fixtures=await call(scene,'find_actors',name='',tag='',collision_channels=[],actor_type={'refPath':'/Script/Engine.'+cls})
     for fixture in fixtures:
      for component in await call(actor_ts,'get_components',actor=fixture,component_type={'refPath':'/Script/Engine.BillboardComponent'}):
       old=json.loads(await call(obj,'get_properties',instance=component,properties=['bVisible']))
       editor_icons.append((component,old))
       await call(obj,'set_properties',instance=component,values=json.dumps({'bVisible':False}))
    annotations={'gridSpacing':0,'gridExtent':0,'gridHeight':0,'maxLabelDistance':0,'classFilter':{'refPath':'/Script/Engine.Actor'},'maxLabels':0}
    shot=await call(ed,'CaptureViewport',captureTransform=camera,annotations=annotations,bShowUI=False)
    Path('reports/opening_starting_view.png').write_bytes(base64.b64decode(shot['image']['data']))
    await asyncio.sleep(3)
    later=await call(ed,'CaptureViewport',captureTransform=camera,annotations=annotations,bShowUI=False)
    Path('reports/opening_starting_view_smoke_later.png').write_bytes(base64.b64decode(later['image']['data']))
    Path('reports/opening_comparison_camera.json').write_text(json.dumps({'camera':camera,'fov':shot['cameraFOV'],'note':'Clean editor capture at the observed player pose after freeing debris; see opening_starting_view_play.png for actual gameplay.'},indent=2))
   finally:
    for component,old in editor_icons:await call(obj,'set_properties',instance=component,values=json.dumps(old))
    await call(actor_ts,'set_actor_transform',actor=debris,xform=original,worldspace=True)
    await call('editor_toolset.toolsets.asset.AssetTools','save_assets',asset_paths=['/Game/WreckagePrototype/Maps/L_Wreckage_Opening'])
   print('PREVIEW_CAPTURED',flush=True)
asyncio.run(main())
