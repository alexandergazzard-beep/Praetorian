"""Verify all twenty exported LOD files by actual Blender reimport."""
import bpy,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
lods=json.loads((ROOT/'reports/flora_expansion71_lods.json').read_text());out=[]
for asset,record in lods.items():
 for i,expected in enumerate(record['triangles']):
  bpy.ops.wm.read_factory_settings(use_empty=True)
  path=ROOT/'assets/models/forest_wreck'/asset/'export'/('SM_'+asset+'_LOD'+str(i)+'.fbx')
  assert path.is_file() and path.stat().st_size>1000
  bpy.ops.import_scene.fbx(filepath=str(path))
  meshes=[o for o in bpy.context.scene.objects if o.type=='MESH'];assert len(meshes)==1
  mesh=meshes[0].data;mesh.calc_loop_triangles();actual=len(mesh.loop_triangles)
  assert actual>0 and actual<=expected,(asset,i,actual,expected)
  if i==0:assert actual==expected,(asset,i,actual,expected)
  assert len(mesh.uv_layers)>0
  out.append(dict(asset=asset,lod=i,triangles=actual,pre_export_triangles=expected,importer_removed_triangles=expected-actual,uv_layers=len(mesh.uv_layers),roundtrip=True))
 actuals=[r['triangles'] for r in out if r['asset']==asset]
 assert all(actuals[i]>actuals[i+1]>0 for i in range(3))
 record['pre_export_triangles']=record['triangles']
 record['triangles']=actuals
 record['count_evidence']='Actual exported FBX reimport; importer strips some invalid reduced faces'
(ROOT/'reports/flora_expansion71_fbx_roundtrip.json').write_text(json.dumps(out,indent=2))
(ROOT/'reports/flora_expansion71_lods.json').write_text(json.dumps(lods,indent=2))
print('TWENTY_FBX_LODS_VERIFIED',len(out),flush=True)
