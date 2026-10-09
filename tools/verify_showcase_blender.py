"""Reopen the saved showcase and verify its actual meshes and packed texture images."""
import bpy,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];file=ROOT/'assets/models/wreck_showcase/blender/LargeWreck_Showcase.blend'
bpy.ops.wm.open_mainfile(filepath=str(file))
for name in ['Hero_Large','Broken_Rear','Engine','Detached_Armor','Supply_Trunk','ShowcaseCamera']:
 assert bpy.data.objects.get(name),name
for name in ['Hero_Large','Broken_Rear','Engine','Detached_Armor']:
 o=bpy.data.objects[name];assert o.type=='MESH' and len(o.data.materials)>0 and len(o.data.uv_layers)>0,name
images=[i for i in bpy.data.images if i.type=='IMAGE' and i.source in {'FILE','TILED'}]
print('SHOWCASE_IMAGE_DEPENDENCIES',json.dumps([{'name':i.name,'source':i.source,'packed':bool(i.packed_file or len(i.packed_files)>0),'path':i.filepath} for i in images]),flush=True)
assert images and all(i.packed_file or len(i.packed_files)>0 for i in images),'Unpacked texture dependency'
assert (ROOT/'reports/wreck_showcase_beauty.png').is_file()
(ROOT/'reports/wreck_showcase_blender_verification.json').write_text(json.dumps({'saved_source_reopened':True,'hero_and_supporting_meshes_verified':True,'packed_texture_images':len(images),'resolution':[bpy.context.scene.render.resolution_x,bpy.context.scene.render.resolution_y],'camera':bpy.context.scene.camera.name,'render_exists':True,'paid_generations':0},indent=2));print('SHOWCASE_SOURCE_VERIFIED',len(images),flush=True)
