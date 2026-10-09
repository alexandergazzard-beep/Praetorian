# /// script
# requires-python = ">=3.12"
# dependencies = ["mcp==2.3.0"]
# ///
"""Configure/reload and inspect only the isolated user-selected wreck trio."""
import asyncio,base64,json,sys
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
    result=await asyncio.wait_for(s.call_tool('call_tool',{'toolset_name':ts,'tool_name':tool,'arguments':args}),60)
    if result.is_error:raise RuntimeError(str(result.content))
    return json.loads(result.content[0].text).get('returnValue')
   if await call(ED,'IsPIERunning'):await call(ED,'StopPIE')
   data=json.loads((ROOT/'reports/flora_flagship71_unreal_import.json').read_text())
   for item in data['assets']:
    ref={'refPath':item['mesh']};await call(AS,'load_asset',asset_path=item['mesh'])
    await call(SM,'remove_lods',mesh=ref);await call(SM,'generate_lods',mesh=ref,triangle_percents=[.5,.22,.08]);await call(SM,'set_lod_thresholds',mesh=ref,thresholds=[1,.4,.18,.07]);await call(SM,'set_nanite_enabled',mesh=ref,enabled=False)
    await call(SM,'remove_collisions',mesh=ref)
    item['lod_triangles']=[await call(SM,'get_triangle_count',mesh=ref,lod_index=i) for i in range(4)]
    item['bounds']=await call(SM,'get_bounds',mesh=ref)
    item['mesh_collision']='disabled; tree trunk uses isolated invisible blocking proxy'
    assert await call(AS,'save_assets',asset_paths=[item['mesh'].split('.')[0]])
   await call(SC,'load_level',level_path=data['map']);assert await call(SC,'get_current_level')==data['map']
   await call(AS,'save_assets',asset_paths=[data['map']])
   await call(SC,'load_level',level_path='/Game/WreckagePrototype/Maps/L_Wreckage_Opening')
   await call(SC,'load_level',level_path=data['map']);assert await call(SC,'get_current_level')==data['map'];data['saved_map_reload']=True
   traces=[]
   for item in data['assets']:
    x,y,z=item['location_cm']
    if item['kind']=='tree':
     distance=await call(SC,'trace_world',start={'x':x,'y':-500,'z':160},end={'x':x,'y':500,'z':160})
     assert distance is not None,item['id']
     canopy=await call(SC,'trace_world',start={'x':x,'y':-500,'z':380},end={'x':x,'y':500,'z':380})
     assert canopy is None,(item['id'],canopy)
     traces.append({'asset':item['id'],'trunk_hit_cm':distance,'canopy_no_collision':True})
    else:
     distance=await call(SC,'trace_world',start={'x':x,'y':y-300,'z':20},end={'x':x,'y':y+300,'z':20})
     assert distance is None,(item['id'],distance)
     traces.append({'asset':item['id'],'understory_no_collision':True})
   poses=[((-2200,-6000,1300),(-5,70,0)),((-2000,-2000,550),(-5,75,0)),((-1100,-2400,900),(-5,66,0)),((2400,-2300,750),(-8,105,0))]
   await call(ED,'SelectActors',actors=[])
   for i,(location,rotation) in enumerate(poses):
    pose={'location':dict(zip('xyz',location)),'rotation':dict(zip(['pitch','yaw','roll'],rotation))}
    await call(ED,'SetCameraTransform',transform=pose);await asyncio.sleep(4)
    shot=await call(ED,'CaptureViewport',captureTransform=pose,bShowUI=False,annotations={'gridSpacing':0,'gridExtent':0,'gridHeight':0,'maxLabelDistance':0,'classFilter':{'refPath':'/Script/Engine.Actor'},'maxLabels':0})
    (ROOT/'reports'/f'flora_flagship71_unreal_{i}.png').write_bytes(base64.b64decode(shot['image']['data']))
   data.update(collision_traces=traces,visual_acceptance='pending captured image inspection',performance='unverified',review_integration=False)
   (ROOT/'reports/flora_flagship71_unreal_qa.json').write_text(json.dumps(data,indent=2))
   print('WRECK_TRIO_LIVE_COMPLETE',json.dumps([{'id':a['id'],'lod_triangles':a['lod_triangles'],'mesh_collision':a['mesh_collision']} for a in data['assets']]),flush=True)
asyncio.run(main())
