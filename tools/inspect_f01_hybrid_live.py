# /// script
# requires-python = ">=3.12"
# dependencies = ["mcp==2.3.0"]
# ///
"""Native live-editor inspection and isolated sample replacement; original opening preserved."""
import asyncio,base64,json,sys
from pathlib import Path
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
ROOT=Path(__file__).resolve().parents[1]
SC='editor_toolset.toolsets.scene.SceneTools';SM='editor_toolset.toolsets.static_mesh.StaticMeshTools';AT='editor_toolset.toolsets.actor.ActorTools';OB='editor_toolset.toolsets.object.ObjectTools';ED='EditorToolset.EditorAppToolset';AS='editor_toolset.toolsets.asset.AssetTools'
INSPECT='/Game/LostVanguard/Environment/OpeningReview/Maps/L_ForestWreck_Inspection'
REVIEW='/Game/LostVanguard/Environment/OpeningReview/Maps/L_ForestWreck_Review'
async def main():
 async with streamable_http_client('http://127.0.0.1:8000/mcp') as (r,w):
  async with ClientSession(r,w) as s:
   await s.initialize()
   async def call(ts,tool,**args):
    result=await asyncio.wait_for(s.call_tool('call_tool',{'toolset_name':ts,'tool_name':tool,'arguments':args}),60)
    if result.is_error:raise RuntimeError(str(result.content))
    return json.loads(result.content[0].text).get('returnValue')
   assert not await call(ED,'IsPIERunning'),'PIE active; preserve session'
   report=json.loads((ROOT/'reports/f01_hybrid_unreal_import.json').read_text());mesh={'refPath':report['mesh']}
   await call(AS,'load_asset',asset_path=report['mesh'])
   await call(SM,'remove_lods',mesh=mesh);await call(SM,'generate_lods',mesh=mesh,triangle_percents=[.5,.22])
   await call(SM,'set_lod_thresholds',mesh=mesh,thresholds=[1,.35,.14]);await call(SM,'set_nanite_enabled',mesh=mesh,enabled=False)
   await call(SM,'remove_collisions',mesh=mesh)
   report['lod_triangles']=[await call(SM,'get_triangle_count',mesh=mesh,lod_index=i) for i in range(3)]
   report['material_slots']=await call(SM,'get_material_slots',mesh=mesh);report['bounds']=await call(SM,'get_bounds',mesh=mesh)
   assert await call(AS,'save_assets',asset_paths=[report['mesh'].split('.')[0]])
   for level in (INSPECT,REVIEW):
    if await call(SC,'get_current_level')!=level:await call(SC,'load_level',level_path=level)
    assert await call(SC,'get_current_level')==level
    trees=await call(SC,'find_actors',name='FWR_F01',tag='',collision_channels=[]);assert len(trees)==1,trees
    actor=trees[0];comp=(await call(AT,'get_components',actor=actor,component_type={'refPath':'/Script/Engine.StaticMeshComponent'}))[0]
    if '--verify-only' not in sys.argv:
     assert await call(OB,'set_properties',instance=comp,values=json.dumps({'StaticMesh':mesh,'BodyInstance':{'collisionProfileName':'NoCollision','collisionEnabled':'NoCollision'}}))
    boxes=await call(AT,'get_components',actor=actor,component_type={'refPath':'/Script/Engine.BoxComponent'})
    box=boxes[0] if boxes else await call(AT,'add_component',owner=comp,component_type={'refPath':'/Script/Engine.BoxComponent'},name='TrunkCollision')
    if '--verify-only' not in sys.argv:
     assert await call(OB,'set_properties',instance=box,values=json.dumps({'BoxExtent':{'x':43,'y':43,'z':205},'RelativeLocation':{'x':0,'y':0,'z':205},'bVisible':False,'BodyInstance':{'collisionProfileName':'BlockAll','collisionEnabled':'QueryAndPhysics','bAutoWeld':False}}))
    assert await call(AS,'save_assets',asset_paths=[level])
    # Reopen so physics state is rebuilt from saved properties after mesh replacement.
    await call(SC,'load_level',level_path=REVIEW if level==INSPECT else INSPECT)
    await call(SC,'load_level',level_path=level)
    assert await call(SC,'get_current_level')==level
    if level==INSPECT:
     rects=await call(SC,'find_actors',name='Inspection_SoftFill',tag='',collision_channels=[])
     for rect in rects:
      light=(await call(AT,'get_components',actor=rect,component_type={'refPath':'/Script/Engine.LightComponent'}))[0]
      assert await call(OB,'set_properties',instance=light,values=json.dumps({'Intensity':250}))
     traces=[]
     for title,start,end in [('trunk',(-700,-350,160),(-400,-350,160)),('canopy',(-900,-350,650),(-200,-350,650)),('hull',(600,-500,160),(600,1000,160))]:
      distance=await call(SC,'trace_world',start=dict(zip('xyz',start)),end=dict(zip('xyz',end)));traces.append({'check':title,'hit_distance_cm':distance})
     if traces[1]['hit_distance_cm'] is not None:
      tree=(await call(SC,'find_actors',name='FWR_F01',tag='',collision_channels=[]))[0]
      current=(await call(AT,'get_components',actor=tree,component_type={'refPath':'/Script/Engine.StaticMeshComponent'}))[0]
      print('SAVED_COLLISION_STATE',await call(OB,'get_properties',instance=current,properties=['BodyInstance','StaticMesh']),flush=True)
     assert traces[0]['hit_distance_cm'] is not None and traces[1]['hit_distance_cm'] is None and traces[2]['hit_distance_cm'] is not None,traces
     report['collision_traces']=traces
     poses=[{'location':{'x':-1100,'y':-1600,'z':164},'rotation':{'pitch':8,'yaw':60,'roll':0}}, {'location':{'x':-1400,'y':-1800,'z':700},'rotation':{'pitch':-5,'yaw':52,'roll':0}}, {'location':{'x':1200,'y':-1900,'z':164},'rotation':{'pitch':5,'yaw':104,'roll':0}}]
    else:
     poses=[{'location':{'x':-390,'y':0,'z':154.15},'rotation':{'pitch':0,'yaw':0,'roll':0}}, {'location':{'x':650,'y':0,'z':164},'rotation':{'pitch':0,'yaw':15,'roll':0}}]
    await call(ED,'SelectActors',actors=[])
    debris=None
    if level==REVIEW:
     debris=(await call(SC,'find_actors',name='',tag='LV_Debris',collision_channels=[]))[0]
     debris_xform=await call(AT,'get_actor_transform',actor=debris)
     below=json.loads(json.dumps(debris_xform));below['location']['z']=-1500
     await call(AT,'set_actor_transform',actor=debris,xform=below,worldspace=True)
    try:
     for i,pose in enumerate(poses):
      await call(ED,'SetCameraTransform',transform=pose);await asyncio.sleep(5)
      shot=await call(ED,'CaptureViewport',captureTransform=pose,bShowUI=False,annotations={'gridSpacing':0,'gridExtent':0,'gridHeight':0,'maxLabelDistance':0,'classFilter':{'refPath':'/Script/Engine.Actor'},'maxLabels':0})
      (ROOT/'reports'/f'f01_hybrid_{"inspection" if level==INSPECT else "review"}_{i}.png').write_bytes(base64.b64decode(shot['image']['data']))
    finally:
     if debris:await call(AT,'set_actor_transform',actor=debris,xform=debris_xform,worldspace=True)
    assert await call(AS,'save_assets',asset_paths=[level])
   report.update(integrated=True,review_map=REVIEW,inspection_map=INSPECT,performance='unverified',visual_acceptance='pending saved captures',gameplay_regression='rerun pending',reusable_collision='per-actor trunk component; reusable Blueprint pending')
   (ROOT/'reports/f01_hybrid_unreal_qa.json').write_text(json.dumps(report,indent=2));print('F01_HYBRID_NATIVE_CHECKS_COMPLETE',json.dumps({'lods':report['lod_triangles'],'traces':report['collision_traces']}))
asyncio.run(main())
