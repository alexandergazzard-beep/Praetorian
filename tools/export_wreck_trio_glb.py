"""Export portable textured meshes from prepared Blender sources, excluding inspection props."""
import bpy,json,struct
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];report=[]
for asset in ['Medium_WreckPanel','Large_WreckModule','Engine_MeshyNacelle']:
 base=ROOT/'assets/models/forest_wreck'/asset
 bpy.ops.wm.open_mainfile(filepath=str(base/'blender/prepared.blend'))
 bpy.ops.object.select_all(action='DESELECT');meshes=[o for o in bpy.context.scene.objects if o.type=='MESH']
 assert len(meshes)==1
 meshes[0].select_set(True);bpy.context.view_layer.objects.active=meshes[0]
 target=base/'export'/('SM_'+asset+'.glb')
 bpy.ops.export_scene.gltf(filepath=str(target),export_format='GLB',use_selection=True,export_yup=True)
 raw=target.read_bytes();assert raw[:4]==b'glTF';length,kind=struct.unpack_from('<II',raw,12);assert kind==0x4e4f534a
 doc=json.loads(raw[20:20+length]);assert len(doc['meshes'])==1 and doc.get('textures') and doc.get('images')
 report.append({'asset':asset,'path':str(target),'bytes':len(raw),'mesh_count':len(doc['meshes']),'embedded_images':len(doc['images']),'prepared_meter_scale':True})
(ROOT/'reports/wreck_trio_glb_exports.json').write_text(json.dumps(report,indent=2))
print('WRECK_TRIO_GLB_COMPLETE',json.dumps(report),flush=True)
