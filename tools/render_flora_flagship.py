import bpy,json,math
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
specs=json.loads((ROOT/'reports/flora_flagship71_specs.json').read_text())
bpy.ops.wm.read_factory_settings(use_empty=True)
labels={'F01':'Layered canopy','F02':'Split-trunk tree','F08':'Leaning fan tree','F03':'Spreading shrub','F05':'Arched fern','F06':'Blade clump','F10':'Ground cover'}
for i,asset in enumerate(specs):
 with bpy.data.libraries.load(str(ROOT/'assets/models/forest_wreck'/asset/'blender/prepared.blend'),link=False) as (src,dst):dst.objects=[n for n in src.objects if n=='SM_'+asset]
 o=dst.objects[0];bpy.context.collection.objects.link(o);bpy.context.view_layer.update()
 size=max(o.dimensions);factor=(4 if i<3 else 2.4)/size
 o.scale=Vector((factor,)*3)
 x=(-5+i*5) if i<3 else (-6+(i-3)*4)
 o.location=Vector((x,2 if i<3 else -3,0))
 bpy.ops.object.text_add(location=(x,-.3 if i<3 else -4.5,.015),rotation=(0,0,0))
 text=bpy.context.object;text.data.body=asset[:3]+'  '+labels[asset[:3]];text.data.align_x='CENTER';text.data.size=.23;text.rotation_euler=(0,0,0)
 mat=bpy.data.materials.get('Label') or bpy.data.materials.new('Label');mat.use_nodes=True;shader=next(n for n in mat.node_tree.nodes if n.type=='BSDF_PRINCIPLED');shader.inputs['Base Color'].default_value=(.015,.02,.025,1);shader.inputs['Roughness'].default_value=.9;text.data.materials.append(mat)
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=32;scene.render.resolution_x=1920;scene.render.resolution_y=1080;scene.render.resolution_percentage=100
scene.view_settings.view_transform='AgX';scene.view_settings.exposure=-1.3;scene.world=bpy.data.worlds.new('NeutralWorld');scene.world.color=(.4,.4,.4)
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.02));ground=bpy.context.object;mat=bpy.data.materials.new('NeutralGround');mat.diffuse_color=(.3,.32,.34,1);ground.data.materials.append(mat)
target=Vector((0,0,1.3))
for location,energy,size in [((-6,-8,12),4500,8),((8,-2,8),3000,7),((0,8,10),5000,9)]:
 bpy.ops.object.light_add(type='AREA',location=location);o=bpy.context.object;o.data.energy=energy;o.data.size=size;o.rotation_euler=(target-o.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add(location=(0,-21,18));cam=bpy.context.object;scene.camera=cam;cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=18
for image in bpy.data.images:
 if image.type=='IMAGE':image.pack()
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'assets/models/forest_wreck/Flora_Flagship71_Presentation.blend'))
scene.render.filepath=str(ROOT/'reports/flora_flagship71_overview.png');bpy.ops.render.render(write_still=True)
print('FLORA_ACTUAL_MODEL_OVERVIEW_COMPLETE',flush=True)
