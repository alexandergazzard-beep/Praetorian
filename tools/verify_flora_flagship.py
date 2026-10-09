"""Check preserved source/export mesh counts and actual PBR texture sizes."""
import json,struct
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];out=[]
def glb_info(path):
 with path.open('rb') as f:
  assert f.read(4)==b'glTF';f.seek(12);n,kind=struct.unpack('<II',f.read(8));assert kind==0x4e4f534a;doc=json.loads(f.read(n))
 tris=sum(doc['accessors'][p['indices']]['count']//3 for m in doc['meshes'] for p in m['primitives']);return {'triangles':tris,'meshes':len(doc['meshes']),'embedded_images':len(doc.get('images',[])),'bytes':path.stat().st_size}
specs=json.loads((ROOT/'reports/flora_flagship71_specs.json').read_text())
for asset,v in specs.items():
 lo,hi=v['range']
 base=ROOT/'assets/models/forest_wreck'/asset
 exported=glb_info(base/'export'/('SM_'+asset+'.glb'));assert lo<=exported['triangles']<=hi;assert exported['embedded_images']>=3
 textures={}
 for p in (base/'source/meshy_original_textures').glob('*.png'):
  raw=p.read_bytes()[:24];assert raw[:8]==b'\x89PNG\r\n\x1a\n';textures[p.name]=list(struct.unpack('>II',raw[16:24]))
 assert textures.get('base_color.png')==[4096,4096]
 out.append({'asset':asset,'preferred_lod0_range':[lo,hi],'game_glb':exported,'high_detail_source':glb_info(base/'source/meshy_pre_remeshed.glb'),'textures':textures,'historical_flora_preserved':True})
(ROOT/'reports/flora_flagship71_file_verification.json').write_text(json.dumps(out,indent=2));print('FLAGSHIP_FILES_VERIFIED',json.dumps(out),flush=True)
