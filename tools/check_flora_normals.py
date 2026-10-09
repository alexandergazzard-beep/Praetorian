import bpy,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'assets/models/forest_wreck/F02_Flagship71/blender/prepared.blend'))
o=next(o for o in bpy.context.scene.objects if o.type=='MESH')
print('FLORA_NORMALS',json.dumps({'faces':len(o.data.polygons),'smooth_faces':sum(p.use_smooth for p in o.data.polygons)}))
