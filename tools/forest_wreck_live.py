# /// script
# requires-python = ">=3.12"
# dependencies = ["mcp==2.3.0"]
# ///
"""Sequential native editor inspection/capture; no binary filesystem edits."""
import asyncio,base64,json,sys
from pathlib import Path
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
ROOT=Path(__file__).resolve().parents[1]
SC='editor_toolset.toolsets.scene.SceneTools';AT='editor_toolset.toolsets.actor.ActorTools';AS='editor_toolset.toolsets.asset.AssetTools';OB='editor_toolset.toolsets.object.ObjectTools';ED='EditorToolset.EditorAppToolset'
REVIEW='/Game/LostVanguard/Environment/OpeningReview/Maps/L_ForestWreck_Review'
async def main():
 async with streamable_http_client('http://127.0.0.1:8000/mcp') as (r,w):
  async with ClientSession(r,w) as s:
   await s.initialize()
   async def call(ts,tool,**args):
    result=await asyncio.wait_for(s.call_tool('call_tool',{'toolset_name':ts,'tool_name':tool,'arguments':args}),60)
    if result.is_error:raise RuntimeError(str(result.content))
    return json.loads(result.content[0].text).get('returnValue')
   mode=sys.argv[1] if len(sys.argv)>1 else 'baseline'
   if mode=='describe':
    for ts in [ED,AS,'editor_toolset.toolsets.static_mesh.StaticMeshTools']:
     result=await s.call_tool('describe_toolset',{'toolset_name':ts})
     (ROOT/'reports'/('forest_'+ts.split('.')[-1]+'.json')).write_text(result.model_dump_json(indent=2))
    return
   if mode=='samples':
    SM='editor_toolset.toolsets.static_mesh.StaticMeshTools'
    assets=json.loads((ROOT/'reports/forest_wreck_unreal_import.json').read_text())['assets']
    for item in assets:
     ref={'refPath':item['mesh']};await call(AS,'load_asset',asset_path=item['mesh'])
     await call(SM,'remove_lods',mesh=ref)
     await call(SM,'generate_lods',mesh=ref,triangle_percents=[.5,.22])
     await call(SM,'set_lod_thresholds',mesh=ref,thresholds=[1,.35,.14])
     await call(SM,'set_nanite_enabled',mesh=ref,enabled=False)
     if item['id']=='Hull_ArmoredSection':
      assert await call(SM,'generate_convex_collisions',mesh=ref,hull_count=1,max_hull_verts=16,hull_precision=25000)
     item['lod_triangles']=[await call(SM,'get_triangle_count',mesh=ref,lod_index=i) for i in range(await call(SM,'get_lod_count',mesh=ref))]
     item['material_slots']=await call(SM,'get_material_slots',mesh=ref)
     item['bounds']=await call(SM,'get_bounds',mesh=ref)
     item['nanite']=await call(SM,'is_nanite_enabled',mesh=ref)
     body=json.loads(await call(OB,'get_properties',instance=ref,properties=['BodySetup']))
     item['body_setup']=body
     body_state=json.loads(await call(OB,'get_properties',instance=body['BodySetup'],properties=['AggGeom','CollisionTraceFlag']))
     item['collision_geometry']=body_state
     print(json.dumps({'id':item['id'],'simple_boxes':len(body_state['AggGeom']['boxElems']),'simple_convexes':len(body_state['AggGeom']['convexElems']),'trace_mode':body_state['CollisionTraceFlag']}),flush=True)
     assert await call(AS,'save_assets',asset_paths=[item['mesh'].split('.')[0]])
    inspection='/Game/LostVanguard/Environment/OpeningReview/Maps/L_ForestWreck_Inspection'
    if await call(SC,'get_current_level')!=inspection:await call(SC,'load_level',level_path=inspection)
    for actor in await call(SC,'find_actors',name='FWR_F01',tag='',collision_channels=[]):
     comp=(await call(AT,'get_components',actor=actor,component_type={'refPath':'/Script/Engine.StaticMeshComponent'}))[0]
     assert await call(OB,'set_properties',instance=comp,values=json.dumps({'BodyInstance':{'CollisionEnabled':'NoCollision'}}))
     boxes=await call(AT,'get_components',actor=actor,component_type={'refPath':'/Script/Engine.BoxComponent'})
     box=boxes[0] if boxes else await call(AT,'add_component',owner=comp,component_type={'refPath':'/Script/Engine.BoxComponent'},name='TrunkCollision')
     assert await call(OB,'set_properties',instance=box,values=json.dumps({'BoxExtent':{'x':43,'y':43,'z':205},'RelativeLocation':{'x':0,'y':0,'z':205},'bVisible':False,'BodyInstance':{'CollisionProfileName':'BlockAll','CollisionEnabled':'QueryAndPhysics'}}))
    for actor in await call(SC,'find_actors',name='Inspection_',tag='',collision_channels=[]):
     for comp in await call(AT,'get_components',actor=actor,component_type={'refPath':'/Script/Engine.BillboardComponent'}):await call(OB,'set_properties',instance=comp,values=json.dumps({'bVisible':False}))
     label=await call(AT,'get_label',actor=actor)
     if label=='Inspection_Sun':
      comp=(await call(AT,'get_components',actor=actor,component_type={'refPath':'/Script/Engine.LightComponent'}))[0]
      await call(OB,'set_properties',instance=comp,values=json.dumps({'Intensity':6,'LightColor':{'r':200,'g':225,'b':255,'a':255}}))
    rects=await call(SC,'find_actors',name='Inspection_SoftFill',tag='',collision_channels=[])
    rect=rects[0] if rects else await call(SC,'add_to_scene_from_class',actor_type={'refPath':'/Script/Engine.RectLight'},name='Inspection_SoftFill',xform={'location':{'x':-900,'y':-1700,'z':1000},'rotation':{'pitch':-20,'yaw':55,'roll':0}})
    comp=(await call(AT,'get_components',actor=rect,component_type={'refPath':'/Script/Engine.LightComponent'}))[0]
    await call(OB,'set_properties',instance=comp,values=json.dumps({'Intensity':700,'AttenuationRadius':5000,'SourceWidth':1800,'SourceHeight':1800}))
    traces=[]
    for title,start,end in [('trunk',(-700,-350,160),(-400,-350,160)),('canopy',(-900,-350,650),(-200,-350,650)),('hull',(600,-500,160),(600,1000,160))]:
     distance=await call(SC,'trace_world',start=dict(zip('xyz',start)),end=dict(zip('xyz',end)))
     traces.append({'check':title,'hit_distance_cm':distance})
    assert traces[0]['hit_distance_cm'] is not None,'Trunk collision missing'
    assert traces[1]['hit_distance_cm'] is None,'Tree canopy blocks trace with simple-as-complex collision'
    assert traces[2]['hit_distance_cm'] is not None,'Hull collision missing'
    poses=[{'location':{'x':-1100,'y':-1600,'z':164},'rotation':{'pitch':8,'yaw':60,'roll':0}}, {'location':{'x':-1400,'y':-1800,'z':700},'rotation':{'pitch':-5,'yaw':52,'roll':0}}, {'location':{'x':-2200,'y':-3500,'z':164},'rotation':{'pitch':7,'yaw':58,'roll':0}}]
    for i,pose in enumerate(poses):
     await call(ED,'SetCameraTransform',transform=pose);await asyncio.sleep(5)
     shot=await call(ED,'CaptureViewport',captureTransform=pose,bShowUI=False,annotations={'gridSpacing':0,'gridExtent':0,'gridHeight':0,'maxLabelDistance':0,'classFilter':{'refPath':'/Script/Engine.Actor'},'maxLabels':0})
     (ROOT/'reports'/f'forest_wreck_samples_{i}.png').write_bytes(base64.b64decode(shot['image']['data']))
    assert await call(AS,'save_assets',asset_paths=[inspection])
    (ROOT/'reports/forest_wreck_sample_qa.json').write_text(json.dumps({'assets':assets,'collision_traces':traces,'cameras':poses,'performance':'unverified','visual_acceptance':'pending image inspection','simple_collision':'body shapes and trunk/canopy/hull traces checked; movement regression pending','batch_expansion':'not yet authorized by sample gate'},indent=2))
    print('SAMPLE_TECHNICAL_CHECKS_COMPLETE',flush=True)
    return
   if await call(ED,'IsPIERunning'):raise RuntimeError('PIE active; stop before authoring')
   level=await call(SC,'get_current_level')
   if mode=='baseline':
    assert level=='/Game/WreckagePrototype/Maps/L_Wreckage_Opening',level
    rows=[]
    for actor in await call(SC,'find_actors',name='',tag='',collision_channels=[]):
     rows.append({'actor':actor,'label':await call(AT,'get_label',actor=actor),'transform':await call(AT,'get_actor_transform',actor=actor)})
    (ROOT/'reports/forest_wreck_baseline_actors.json').write_text(json.dumps({'level':level,'actors':rows},indent=2))
   else:
    if await call(SC,'get_current_level')!=REVIEW:await call(SC,'load_level',level_path=REVIEW)
    if mode=='checkpoint':
     tree=(await call(SC,'find_actors',name='FWR_F01',tag='',collision_channels=[]))[0]
     comp=(await call(AT,'get_components',actor=tree,component_type={'refPath':'/Script/Engine.StaticMeshComponent'}))[0]
     await call(OB,'set_properties',instance=comp,values=json.dumps({'BodyInstance':{'CollisionEnabled':'NoCollision'}}))
     boxes=await call(AT,'get_components',actor=tree,component_type={'refPath':'/Script/Engine.BoxComponent'})
     box=boxes[0] if boxes else await call(AT,'add_component',owner=comp,component_type={'refPath':'/Script/Engine.BoxComponent'},name='TrunkCollision')
     await call(OB,'set_properties',instance=box,values=json.dumps({'BoxExtent':{'x':43,'y':43,'z':205},'RelativeLocation':{'x':0,'y':0,'z':205},'bVisible':False,'BodyInstance':{'CollisionProfileName':'BlockAll','CollisionEnabled':'QueryAndPhysics'}}))
   debris=(await call(SC,'find_actors',name='',tag='LV_Debris',collision_channels=[]))[0]
   original=await call(AT,'get_actor_transform',actor=debris)
   moved=json.loads(json.dumps(original));moved['location']['z']=-1500
   await call(AT,'set_actor_transform',actor=debris,xform=moved,worldspace=True)
   poses=[{'location':{'x':-390,'y':0,'z':154.15},'rotation':{'pitch':0,'yaw':0,'roll':0}}, {'location':{'x':650,'y':0,'z':164},'rotation':{'pitch':0,'yaw':15,'roll':0}}, {'location':{'x':1800,'y':80,'z':164},'rotation':{'pitch':-2,'yaw':25,'roll':0}}]
   try:
    await call(ED,'SelectActors',actors=[])
    for i,pose in enumerate(poses):
     await call(ED,'SetCameraTransform',transform=pose)
     await asyncio.sleep(5)
     shot=await call(ED,'CaptureViewport',captureTransform=pose,bShowUI=False,annotations={'gridSpacing':0,'gridExtent':0,'gridHeight':0,'maxLabelDistance':0,'classFilter':{'refPath':'/Script/Engine.Actor'},'maxLabels':0})
     (ROOT/'reports'/f'forest_wreck_{mode}_{i}.png').write_bytes(base64.b64decode(shot['image']['data']))
   finally:await call(AT,'set_actor_transform',actor=debris,xform=original,worldspace=True)
   (ROOT/'reports/forest_wreck_cameras.json').write_text(json.dumps({'poses':poses,'mode':mode,'performance':'unverified'},indent=2))
   if mode=='baseline':
    assert not await call(AS,'exists',path=REVIEW),'Review map already exists; preserve it'
    assert await call(AS,'duplicate',path=level,new_path=REVIEW)
    assert await call(AS,'save_assets',asset_paths=[REVIEW])
   else:assert await call(AS,'save_assets',asset_paths=[REVIEW])
   print('FOREST_WRECK_'+mode.upper()+'_COMPLETE',flush=True)
asyncio.run(main())
