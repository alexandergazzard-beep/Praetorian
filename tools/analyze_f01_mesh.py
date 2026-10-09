import bpy,bmesh,json
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'assets/models/forest_wreck/F01_MeshyCanopy/blender/prepared.blend'))
o=next(o for o in bpy.context.scene.objects if o.type=='MESH')
bm=bmesh.new();bm.from_mesh(o.data);seen=set();parts=[]
for v in bm.verts:
 if v in seen:continue
 todo=[v];seen.add(v);group=[]
 while todo:
  u=todo.pop();group.append(u)
  for e in u.link_edges:
   n=e.other_vert(u)
   if n not in seen:seen.add(n);todo.append(n)
 faces={f for u in group for f in u.link_faces}
 if len(group)==5 and not any(p.get('example') for p in parts):
  print('FIVE_VERTEX_LEAF',json.dumps({'coords':[list(u.co) for u in group],'faces':[[group.index(u) for u in f.verts] for f in faces],'edges':[[group.index(u) for u in e.verts] for e in {e for u in group for e in u.link_edges}]}))
 parts.append({'verts':len(group),'faces':len(faces),'z_min':min(u.co.z for u in group),'z_max':max(u.co.z for u in group),'example':len(group)==5})
print(json.dumps({'components':len(parts),'sizes':Counter(p['verts'] for p in parts),'largest':sorted(parts,key=lambda p:p['verts'],reverse=True)[:10],'dimensions':list(o.dimensions)},indent=2))
