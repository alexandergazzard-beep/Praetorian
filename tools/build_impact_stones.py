import bpy,random,json
from pathlib import Path
from mathutils import noise,Vector
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'assets/models/space_impact';(B/'blender').mkdir(parents=True,exist_ok=True);(B/'export').mkdir(exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True);random.seed(812);report=[]
for k in range(3):
 bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=4,radius=1);o=bpy.context.object;o.name='SM_ImpactStone_'+str(k)
 for v in o.data.vertices:
  q=v.co.copy();v.co*=.78+.22*noise.noise_vector(q*3+Vector((k*7,2,9))).x;v.co.x*=1.35;v.co.y*=.9;v.co.z*=.65
  v.co.z=max(v.co.z,-.43)
 for p in o.data.polygons:p.use_smooth=True
 bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.uv.smart_project();bpy.ops.object.mode_set(mode='OBJECT')
 bpy.ops.export_scene.fbx(filepath=str(B/'export'/(o.name+'.fbx')),use_selection=True,object_types={'MESH'},apply_unit_scale=True,axis_forward='-Y',axis_up='Z',add_leaf_bones=False,bake_anim=False)
 o.data.calc_loop_triangles();report.append({'name':o.name,'triangles':len(o.data.loop_triangles)});o.select_set(False)
bpy.ops.wm.save_as_mainfile(filepath=str(B/'blender/ImpactStones.blend'));(ROOT/'reports/space_impact_stones.json').write_text(json.dumps(report,indent=2));print('IMPACT_STONES_COMPLETE',flush=True)
