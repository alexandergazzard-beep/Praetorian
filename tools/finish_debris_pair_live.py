# /// script
# requires-python = ">=3.12"
# dependencies = ["mcp==2.3.0"]
# ///
"""Set mesh detail/collision, place in opening, capture real Unreal results."""
import asyncio,base64,json
from pathlib import Path
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
ROOT=Path(__file__).resolve().parents[1]
SC='editor_toolset.toolsets.scene.SceneTools';SM='editor_toolset.toolsets.static_mesh.StaticMeshTools';AT='editor_toolset.toolsets.actor.ActorTools';OB='editor_toolset.toolsets.object.ObjectTools';ED='EditorToolset.EditorAppToolset';AS='editor_toolset.toolsets.asset.AssetTools'
async def main():
 async with streamable_http_client('http://127.0.0.1:8000/mcp') as (r,w):
  async with ClientSession(r,w) as s:
   await s.initialize()
   async def call(ts,tool,**args):
    result=await s.call_tool('call_tool',{'toolset_name':ts,'tool_name':tool,'arguments':args})
    if result.is_error:raise RuntimeError(str(result.content))
    value=json.loads(result.content[0].text)
    return value.get('returnValue')
   if await call(ED,'IsPIERunning'):await call(ED,'StopPIE')
   data=json.loads((ROOT/'reports/debris_pair_unreal_import.json').read_text())
   for a in data:
    ref={'refPath':a['mesh']}
    await call(AS,'load_asset',asset_path=a['mesh'])
    await call(SM,'remove_lods',mesh=ref)
    await call(SM,'generate_lods',mesh=ref,triangle_percents=[.5,.25])
    await call(SM,'set_lod_thresholds',mesh=ref,thresholds=[1,.3,.12])
    await call(SM,'remove_collisions',mesh=ref)
    if a['id'].startswith('M17'):assert await call(SM,'generate_convex_collisions',mesh=ref,hull_count=1,max_hull_verts=8,hull_precision=10000)
    count=await call(SM,'get_lod_count',mesh=ref)
    a['lod_triangles']=[await call(SM,'get_triangle_count',mesh=ref,lod_index=i) for i in range(count)]
    a['bounds']=await call(SM,'get_bounds',mesh=ref)
    a['collision']='one convex hull' if a['id'].startswith('M17') else 'none'
    await call(AS,'save_assets',asset_paths=[a['mesh'].split('.')[0]])
    shot=await call(ED,'CaptureAssetImage',assetPath=a['mesh'])
    (ROOT/'reports'/('debris_'+a['id']+'_unreal.png')).write_bytes(base64.b64decode(shot['data']))
   level=await call(SC,'get_current_level')
   assert 'L_Wreckage_Opening' in str(level),level
   placements=[(data[0],350,250,0,0,-12),(data[1],100,290,9,90,18)]
   for a,x,y,z,roll,yaw in placements:
    label='LV_Art_'+a['id']
    found=await call(SC,'find_actors',name=label,tag='',collision_channels=[])
    transform={'location':{'x':x,'y':y,'z':z},'rotation':{'pitch':0,'yaw':yaw,'roll':roll},'scale':{'x':1,'y':1,'z':1}}
    if found:
     actor=found[0];await call(AT,'set_actor_transform',actor=actor,xform=transform,worldspace=True)
    else:actor=await call(SC,'add_to_scene_from_asset',asset_path=a['mesh'],name=label,xform=transform)
    await call(SC,'set_actor_folder',actor=actor,folder_path='LostVanguard/GeneratedDebris')
    a['placed_actor']=actor;a['placement']=transform
   await call(AS,'save_assets',asset_paths=['/Game/WreckagePrototype/Maps/L_Wreckage_Opening'])
   camera={'location':{'x':-40,'y':-60,'z':180},'rotation':{'pitch':-15,'yaw':44,'roll':0}}
   await call(ED,'SetCameraTransform',transform=camera)
   await asyncio.sleep(4)
   shot=await call(ED,'CaptureViewport',captureTransform=camera,bShowUI=False,annotations={'gridSpacing':0,'gridExtent':0,'gridHeight':0,'maxLabelDistance':0,'classFilter':{'refPath':'/Script/Engine.Actor'},'maxLabels':0})
   (ROOT/'reports/debris_pair_in_level.png').write_bytes(base64.b64decode(shot['image']['data']))
   (ROOT/'reports/debris_pair_unreal_qa.json').write_text(json.dumps({'level':level,'assets':data,'camera':camera,'performance':'Frame time not yet profiled; mesh budgets alone do not establish FPS.'},indent=2))
   print('DEBRIS_PAIR_LIVE_COMPLETE',json.dumps([{'id':a['id'],'lod_triangles':a['lod_triangles'],'collision':a['collision']} for a in data]),flush=True)
asyncio.run(main())
