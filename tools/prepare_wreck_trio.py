"""Preserve source meshes and prepare the three user-selected wreck models."""
import bpy,bmesh,json,sys,math
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
SPECS={'Medium_WreckPanel':(4.5,'height'),'Large_WreckModule':(12,'width'),'Engine_MeshyNacelle':(12,'width')}
selected=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else list(SPECS)
report_path=ROOT/'reports/wreck_trio_blender.json'
reports=json.loads(report_path.read_text()) if report_path.exists() else {}
for asset in selected:
 bpy.ops.wm.read_factory_settings(use_empty=True)
 base=ROOT/'assets/models/forest_wreck'/asset
 for sub in ('blender','export'):(base/sub).mkdir(exist_ok=True)
 bpy.ops.import_scene.gltf(filepath=str(base/'source/meshy_original.glb'))
 for im in bpy.data.images:
  if im.type=='IMAGE':im.pack()
 bpy.ops.wm.save_as_mainfile(filepath=str(base/'blender/meshy_source.blend'))
 meshes=[o for o in bpy.context.scene.objects if o.type=='MESH']
 assert meshes
 bpy.ops.object.select_all(action='DESELECT')
 for o in meshes:o.select_set(True)
 bpy.context.view_layer.objects.active=meshes[0];bpy.ops.object.join()
 o=bpy.context.object;o.name='SM_'+asset
 world=o.matrix_world.copy();pts=[world@Vector(c) for c in o.bound_box]
 low=Vector([min(p[i] for p in pts) for i in range(3)]);high=Vector([max(p[i] for p in pts) for i in range(3)])
 extent=high-low;length,axis=SPECS[asset]
 factor=length/(extent.z if axis=='height' else max(extent.x,extent.y))
 pivot=Vector(((low.x+high.x)/2,(low.y+high.y)/2,low.z))
 for v in o.data.vertices:v.co=(world@v.co-pivot)*factor
 o.matrix_world.identity()
 bm=bmesh.new();bm.from_mesh(o.data);before=len(bm.verts)
 bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.000001)
 bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=.000001)
 bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
 nonmanifold=sum(not e.is_manifold for e in bm.edges)
 bm.to_mesh(o.data);bm.free();o.data.update();bpy.context.view_layer.update()
 bpy.context.scene.unit_settings.system='METRIC';bpy.context.scene.unit_settings.scale_length=1
 o.data.calc_loop_triangles()
 reports[asset]={'triangles':len(o.data.loop_triangles),'vertices':len(o.data.vertices),'vertices_removed':before-len(o.data.vertices),'nonmanifold_edges':nonmanifold,'uv_layers':len(o.data.uv_layers),'material_slots':len(o.data.materials),'dimensions_m':list(o.dimensions),'pivot':'centered bottom','scale':'provisional production size; not story canon','source_preserved':True}
 bpy.ops.wm.save_as_mainfile(filepath=str(base/'blender/prepared.blend'))
 bpy.ops.export_scene.fbx(filepath=str(base/'export'/('SM_'+asset+'.fbx')),use_selection=True,object_types={'MESH'},apply_unit_scale=True,axis_forward='-Y',axis_up='Z',add_leaf_bones=False,bake_anim=False,path_mode='AUTO',mesh_smooth_type='FACE')
 scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=16
 scene.render.resolution_x=1000;scene.render.resolution_y=800;scene.render.resolution_percentage=100
 scene.world=bpy.data.worlds.new('WreckInspectionWorld');scene.world.color=(.25,.25,.25)
 scene.view_settings.view_transform='AgX'
 size=max(o.dimensions);target=Vector((0,0,o.dimensions.z*.45))
 bpy.ops.mesh.primitive_plane_add(size=size*20,location=(0,0,-.03));ground=bpy.context.object
 mat=bpy.data.materials.new('InspectionGround');mat.diffuse_color=(.18,.18,.18,1);ground.data.materials.append(mat)
 for name,loc,power in [('Key',(-.7,-.8,1.4),45),('Fill',(.7,-.2,1),30),('Rim',(0,.8,1.2),50)]:
  bpy.ops.object.light_add(type='AREA',location=Vector(loc)*size);lamp=bpy.context.object;lamp.name=name;lamp.data.energy=power*size*size;lamp.data.shape='DISK';lamp.data.size=size*.6;lamp.rotation_euler=(target-lamp.location).to_track_quat('-Z','Y').to_euler()
 bpy.ops.object.camera_add();cam=bpy.context.object;scene.camera=cam;cam.data.lens=48
 for i,loc in enumerate([(1.4,-2,1),(-1.5,2,1)]):
  cam.location=Vector(loc)*size;cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
  scene.render.filepath=str(ROOT/'reports'/f'{asset}_blender_{i}.png');bpy.ops.render.render(write_still=True)
 report_path.write_text(json.dumps(reports,indent=2))
 print('WRECK_PREPARATION_COMPLETE',asset,json.dumps(reports[asset]),flush=True)
