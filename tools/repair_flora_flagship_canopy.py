import bpy,bmesh,json,math,random
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'assets/models/forest_wreck/F01_Flagship71'
bpy.ops.wm.open_mainfile(filepath=str(BASE/'blender/prepared.blend'))
o=next(o for o in bpy.context.scene.objects if o.type=='MESH')
assert len(o.data.materials)==1,'One-time canopy repair; preserve previous output'
rng=random.Random(7101)
# Use actual generated upper branch points; greedily space crown anchors in 3D.
candidates=[v.co.copy() for v in o.data.vertices if v.co.z>3.7 and Vector((v.co.x,v.co.y,0)).length>1.0]
rng.shuffle(candidates);candidates.sort(key=lambda p:p.z,reverse=True)
anchors=[]
for v in candidates:
 if all((v-a).length>.72 for a in anchors):anchors.append(v)
 if len(anchors)==60:break
assert len(anchors)>=45
leaf=bpy.data.materials.new('M_F01_CurvedForkLeaf');leaf.use_nodes=True
nodes=leaf.node_tree.nodes;links=leaf.node_tree.links;p=next(n for n in nodes if n.type=='BSDF_PRINCIPLED');p.inputs['Roughness'].default_value=.72
tex=nodes.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(ROOT/'assets/models/forest_wreck/textures/T_Leaf_BaseColor.png'));tex.image.pack()
geo=nodes.new('ShaderNodeNewGeometry');mix=nodes.new('ShaderNodeMixRGB');mix.inputs[2].default_value=(.055,.018,.09,1)
links.new(geo.outputs['Backfacing'],mix.inputs[0]);links.new(tex.outputs['Color'],mix.inputs[1]);links.new(mix.outputs[0],p.inputs['Base Color'])
verts=[];faces=[];uv=[]
for anchor in anchors:
 for j in range(10):
  angle=j*math.tau/10+rng.uniform(-.3,.3);length=rng.uniform(.5,.9)
  along=Vector((math.cos(angle),math.sin(angle),rng.uniform(-.3,.65))).normalized();across=Vector((-math.sin(angle),math.cos(angle),0));normal=along.cross(across).normalized()
  origin=anchor+Vector((rng.uniform(-.18,.18),rng.uniform(-.18,.18),rng.uniform(-.12,.22)))
  start=len(verts)
  for t,w in [(0,.02),(.2,.16),(.4,.23),(.6,.22),(.72,.17),(.84,.12)]:
   for side in (-1,0,1):
    curve=(.09*math.sin(math.pi*t)+.04*side*side*math.sin(math.pi*t))*length
    verts.append(origin+along*(t*length)+across*(side*w*length)+normal*curve);uv.append((.5+side*w*2,t))
  for k in range(5):
   a=start+k*3;b=a+3
   faces.extend([(a,b,b+1),(a,b+1,a+1),(a+1,b+1,b+2),(a+1,b+2,a+2)])
  # Two separate fork tips and recessed central notch, preserving an open organic outline.
  for x,t in [(-.075,1),(0,.90),(.075,1)]:verts.append(origin+along*(t*length)+across*(x*length)+normal*(.015*length));uv.append((.5+x*2,t))
  a=start+15;tips=start+18
  faces.extend([(a,tips,a+1),(a+1,tips,tips+1),(a+1,tips+1,tips+2),(a+1,tips+2,a+2)])
mesh=bpy.data.meshes.new('CurvedForkCanopy');mesh.from_pydata(verts,[],faces);mesh.update()
leaves=bpy.data.objects.new('CurvedForkLeaves',mesh);bpy.context.collection.objects.link(leaves);mesh.materials.append(leaf)
layer=mesh.uv_layers.new(name='LeafUV')
for loop in mesh.loops:layer.data[loop.index].uv=uv[loop.vertex_index]
for poly in mesh.polygons:poly.use_smooth=True
bpy.ops.object.select_all(action='DESELECT');o.select_set(True);leaves.select_set(True);bpy.context.view_layer.objects.active=o;bpy.ops.object.join();bpy.context.view_layer.update()
# Restore the provisional nine-meter height after adding canopy geometry.
factor=9/o.dimensions.z
for v in o.data.vertices:v.co*=factor
o.data.update();bpy.context.view_layer.update();o.data.calc_loop_triangles()
r=json.loads((ROOT/'reports/flora_flagship71_blender.json').read_text());r[o.name[3:]].update(triangles=len(o.data.loop_triangles),material_slots=len(o.data.materials),dimensions_m=list(o.dimensions),canopy_repair={'reason':'flagship remesh returned bare tree with 11507 triangles; foliage reference not met','method':'retained new generated trunk; 3D branch-anchored curved forked leaf geometry, teal texture/violet reverse','anchors':len(anchors),'leaves':len(anchors)*10,'original_meshy_source_preserved':True,'extra_meshy_credits':0})
bpy.ops.wm.save_as_mainfile(filepath=str(BASE/'blender/prepared.blend'))
bpy.ops.export_scene.fbx(filepath=str(BASE/'export/SM_F01_Flagship71.fbx'),use_selection=True,object_types={'MESH'},apply_unit_scale=True,axis_forward='-Y',axis_up='Z',add_leaf_bones=False,bake_anim=False,path_mode='AUTO',mesh_smooth_type='FACE')
(ROOT/'reports/flora_flagship71_blender.json').write_text(json.dumps(r,indent=2))
print('FLAGSHIP_CANOPY_REPAIRED',json.dumps(r['F01_Flagship71']),flush=True)
