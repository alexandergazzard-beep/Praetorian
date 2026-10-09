"""Render the actual flagship Large mesh closely in neutral studio lighting."""
import bpy,json
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'assets/models/forest_wreck/Large_Flagship71/blender/prepared.blend'))
o=next(o for o in bpy.context.scene.objects if o.type=='MESH');size=max(o.dimensions);target=Vector((0,0,o.dimensions.z*.48))
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=32;scene.cycles.use_denoising=True
scene.render.resolution_x=1400;scene.render.resolution_y=1000;scene.render.resolution_percentage=100
scene.world=bpy.data.worlds.new('NeutralFlagshipWorld');scene.world.color=(.25,.25,.25);scene.view_settings.view_transform='AgX'
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.03));ground=bpy.context.object;m=bpy.data.materials.new('StudioGround');m.diffuse_color=(.18,.18,.18,1);ground.data.materials.append(m)
for loc,power in [((-.7,-.8,1.4),45),((.7,-.2,1),30),((0,.8,1.2),50)]:
 bpy.ops.object.light_add(type='AREA',location=Vector(loc)*size);lamp=bpy.context.object;lamp.data.energy=power*size*size;lamp.data.shape='DISK';lamp.data.size=size*.6;lamp.rotation_euler=(target-lamp.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add(location=Vector((-1.2,1.75,.78))*size);cam=bpy.context.object;cam.data.lens=60;cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();scene.camera=cam
scene.render.filepath=str(ROOT/'reports/Large_Flagship71_close.png');bpy.ops.render.render(write_still=True);print('FLAGSHIP_CLOSE_RENDER_COMPLETE',flush=True)
