"""Preserve Meshy sources and prepare separate game exports in background Blender."""
import bpy, bmesh, json
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
report=[]
for asset,length in [('M17_supply_trunk',1.8),('S04_vent_grille',.75)]:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    base=ROOT/'assets/models/debris'/asset
    (base/'blender').mkdir(exist_ok=True)
    (base/'export').mkdir(exist_ok=True)
    bpy.ops.import_scene.gltf(filepath=str(base/'source/meshy_original.glb'))
    bpy.ops.wm.save_as_mainfile(filepath=str(base/'blender/meshy_source.blend'))
    meshes=[o for o in bpy.context.scene.objects if o.type=='MESH']
    bpy.ops.object.select_all(action='DESELECT')
    for o in meshes:o.select_set(True)
    bpy.context.view_layer.objects.active=meshes[0]
    bpy.ops.object.join()
    o=bpy.context.object;o.name=asset
    bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
    bm=bmesh.new();bm.from_mesh(o.data)
    before=len(bm.verts)
    bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.000001)
    bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=.000001)
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
    bm.to_mesh(o.data);bm.free()
    points=[o.matrix_world@Vector(c) for c in o.bound_box]
    low=Vector([min(p[i] for p in points) for i in range(3)])
    high=Vector([max(p[i] for p in points) for i in range(3)])
    extent=high-low;factor=length/max(extent.x,extent.y)
    center=Vector(((low.x+high.x)/2,(low.y+high.y)/2,low.z))
    # Bake world space to mesh, with a centered bottom pivot and true meter scale.
    world=o.matrix_world.copy()
    for v in o.data.vertices:v.co=(world@v.co-center)*factor
    o.matrix_world.identity()
    bpy.context.scene.unit_settings.system='METRIC'
    bpy.context.scene.unit_settings.scale_length=1
    o.data.calc_loop_triangles()
    for m in bpy.data.materials:
        for n in m.node_tree.nodes if m.node_tree else []:
            if n.type=='TEX_IMAGE' and n.image:n.image.pack()
    bpy.ops.wm.save_as_mainfile(filepath=str(base/'blender/game_ready.blend'))
    bpy.ops.export_scene.fbx(filepath=str(base/'export'/('SM_'+asset+'.fbx')),use_selection=True,object_types={'MESH'},apply_unit_scale=True,axis_forward='-Y',axis_up='Z',add_leaf_bones=False,bake_anim=False,path_mode='AUTO')
    report.append({'id':asset,'triangles':len(o.data.loop_triangles),'vertices':len(o.data.vertices),'vertices_removed':before-len(o.data.vertices),'material_slots':len(o.data.materials),'uv_layers':len(o.data.uv_layers),'dimensions_m':list(o.dimensions),'pivot':'centered bottom','source_preserved':True})
(ROOT/'reports/debris_pair_blender.json').write_text(json.dumps(report,indent=2))
print('DEBRIS_CLEANUP_COMPLETE',json.dumps(report))
