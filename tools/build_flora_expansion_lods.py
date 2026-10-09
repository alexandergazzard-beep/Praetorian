"""Create four conventional LODs per plant, preserving base editable sources."""
import bpy,json,bmesh
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
specs=json.loads((ROOT/'reports/flora_expansion71_specs.json').read_text());report={}
for asset in specs:
 base=ROOT/'assets/models/forest_wreck'/asset
 bpy.ops.wm.open_mainfile(filepath=str(base/'blender/prepared.blend'))
 src=next(o for o in bpy.context.scene.objects if o.type=='MESH')
 counts=[]
 for i,ratio in enumerate([1,.5,.22,.08]):
  bpy.ops.object.select_all(action='DESELECT')
  obj=src if i==0 else src.copy()
  if i:
   obj.data=src.data.copy();bpy.context.collection.objects.link(obj)
  obj.select_set(True);bpy.context.view_layer.objects.active=obj
  if i:
   bm=bmesh.new();bm.from_mesh(obj.data)
   distance=max(src.dimensions)*[0,.004,.012,.03][i]
   bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=distance)
   bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=distance*.05)
   bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
   bm.to_mesh(obj.data);bm.free();obj.data.update();bpy.context.view_layer.update()
   mod=obj.modifiers.new('DistanceReduction','DECIMATE');mod.ratio=ratio;mod.use_collapse_triangulate=True
   bpy.ops.object.modifier_apply(modifier=mod.name)
  bm=bmesh.new();bm.from_mesh(obj.data)
  bmesh.ops.triangulate(bm,faces=list(bm.faces))
  bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=.000001)
  bad=[f for f in bm.faces if f.calc_area()<1e-12]
  if bad:bmesh.ops.delete(bm,geom=bad,context='FACES')
  bm.to_mesh(obj.data);bm.free();obj.data.update()
  obj.data.calc_loop_triangles();counts.append(len(obj.data.loop_triangles))
  bpy.ops.export_scene.fbx(filepath=str(base/'export'/('SM_'+asset+'_LOD'+str(i)+'.fbx')),use_selection=True,object_types={'MESH'},apply_unit_scale=True,axis_forward='-Y',axis_up='Z',add_leaf_bones=False,bake_anim=False,path_mode='AUTO',mesh_smooth_type='FACE')
  if i:bpy.data.objects.remove(obj,do_unlink=True)
 report[asset]={'triangles':counts,'ratios':[1,.5,.22,.08],'simplification':'distance-based vertex welding before collapse to reduce nonmanifold thin foliage; UV loops retained','engine_screen_thresholds':'unassigned; visual distance testing required'}
 print('LOD_EXPORT',asset,counts,flush=True)
 assert all(counts[i]>counts[i+1]>0 for i in range(3))
(ROOT/'reports/flora_expansion71_lods.json').write_text(json.dumps(report,indent=2))
