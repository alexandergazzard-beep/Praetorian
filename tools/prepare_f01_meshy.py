"""Preserve generated tree source, prepare scaled export and render inspection views."""
import bpy,bmesh,json,math
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'assets/models/forest_wreck/F01_MeshyCanopy'
bpy.ops.wm.read_factory_settings(use_empty=True)
for folder in ('blender','export','textures'):(BASE/folder).mkdir(exist_ok=True)
bpy.ops.import_scene.gltf(filepath=str(BASE/'source/meshy_original.glb'))
for image in bpy.data.images:
 if image.type=='IMAGE':image.pack()
bpy.ops.wm.save_as_mainfile(filepath=str(BASE/'blender/meshy_source.blend'))
meshes=[o for o in bpy.context.scene.objects if o.type=='MESH']
assert meshes,'No mesh in source'
bpy.ops.object.select_all(action='DESELECT')
for o in meshes:o.select_set(True)
bpy.context.view_layer.objects.active=meshes[0]
bpy.ops.object.join();o=bpy.context.object;o.name='SM_F01_MeshyCanopy'
world=o.matrix_world.copy();points=[world@Vector(c) for c in o.bound_box]
low=Vector([min(p[i] for p in points) for i in range(3)])
high=Vector([max(p[i] for p in points) for i in range(3)])
factor=8.3/(high.z-low.z);pivot=Vector(((low.x+high.x)/2,(low.y+high.y)/2,low.z))
for v in o.data.vertices:v.co=(world@v.co-pivot)*factor
o.matrix_world.identity()
bm=bmesh.new();bm.from_mesh(o.data)
before=len(bm.verts)
bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.000001)
bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=.000001)
nonmanifold=sum(not e.is_manifold for e in bm.edges)
bm.to_mesh(o.data);bm.free();o.data.update()
bpy.context.view_layer.update()
bpy.context.scene.unit_settings.system='METRIC';bpy.context.scene.unit_settings.scale_length=1
o.data.calc_loop_triangles()
textures=[]
for image in bpy.data.images:
 if image.type!='IMAGE':continue
 name=image.name.replace('/','_').replace('\\','_')
 image.filepath_raw=str(BASE/'textures'/f'{name}.png');image.file_format='PNG';image.save();image.pack()
 textures.append({'name':image.name,'path':image.filepath_raw,'size':list(image.size)})
materials=[]
for mat in o.data.materials:
 info={'name':mat.name,'images':[]}
 if mat.node_tree:
  for node in mat.node_tree.nodes:
   if node.type=='TEX_IMAGE' and node.image:info['images'].append({'node':node.name,'image':node.image.name})
 materials.append(info)
report={'id':'F01_MeshyCanopy','triangles':len(o.data.loop_triangles),'vertices':len(o.data.vertices),'vertices_removed':before-len(o.data.vertices),'nonmanifold_edges':nonmanifold,'uv_layers':len(o.data.uv_layers),'material_slots':len(o.data.materials),'materials':materials,'textures':textures,'dimensions_m':list(o.dimensions),'pivot':'centered bottom','source_preserved':True,'visual_acceptance':'pending render inspection','scale':'provisional 8.3m tree height; species scale not canon'}
bpy.ops.wm.save_as_mainfile(filepath=str(BASE/'blender/prepared.blend'))
bpy.ops.export_scene.fbx(filepath=str(BASE/'export/SM_F01_MeshyCanopy.fbx'),use_selection=True,object_types={'MESH'},apply_unit_scale=True,axis_forward='-Y',axis_up='Z',add_leaf_bones=False,bake_anim=False,path_mode='AUTO',mesh_smooth_type='FACE')
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=32
scene.render.resolution_x=1200;scene.render.resolution_y=1000;scene.render.resolution_percentage=100
if scene.world is None:scene.world=bpy.data.worlds.new('InspectionWorld')
scene.world.color=(.18,.18,.18)
scene.view_settings.view_transform='AgX'
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.04));ground=bpy.context.object
m=bpy.data.materials.new('InspectionGround');m.diffuse_color=(.12,.14,.13,1);ground.data.materials.append(m)
for name,loc,power,size in [('Key',(-7,-8,14),2600,7),('Fill',(7,-2,10),1700,6),('Rim',(0,8,12),3000,5)]:
 bpy.ops.object.light_add(type='AREA',location=loc);lamp=bpy.context.object;lamp.name=name;lamp.data.energy=power;lamp.data.shape='DISK';lamp.data.size=size;lamp.rotation_euler=(Vector((0,0,4))-lamp.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add();cam=bpy.context.object;scene.camera=cam;cam.data.lens=48
for i,loc in enumerate([(13,-18,7),(-14,17,6),(9,-13,1.7)]):
 cam.location=loc;cam.rotation_euler=(Vector((0,0,4.2))-cam.location).to_track_quat('-Z','Y').to_euler()
 scene.render.filepath=str(ROOT/'reports'/f'f01_meshy_blender_{i}.png');bpy.ops.render.render(write_still=True)
(ROOT/'reports/f01_meshy_blender.json').write_text(json.dumps(report,indent=2))
print('F01_PREPARATION_COMPLETE',json.dumps(report))
