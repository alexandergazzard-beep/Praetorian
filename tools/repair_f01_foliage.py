"""Hybrid candidate: preserve generated wood, replace blocky leaf islands with tapered fork-tip leaves."""
import bpy,bmesh,json,math,random
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'assets/models/forest_wreck/F01_HybridCanopy'
for folder in ('blender','export'):(BASE/folder).mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'assets/models/forest_wreck/F01_MeshyCanopy/blender/prepared.blend'))
o=next(o for o in bpy.context.scene.objects if o.type=='MESH');o.name='SM_F01_HybridCanopy'
bm=bmesh.new();bm.from_mesh(o.data);seen=set();remove=[];placements=[]
for v in bm.verts:
 if v in seen:continue
 todo=[v];seen.add(v);group=[]
 while todo:
  u=todo.pop();group.append(u)
  for e in u.link_edges:
   n=e.other_vert(u)
   if n not in seen:seen.add(n);todo.append(n)
 if len(group)>9 or min(u.co.z for u in group)<2:continue
 faces={f for u in group for f in u.link_faces}
 if not faces:continue
 center=sum((u.co for u in group),Vector())/len(group)
 face=max(faces,key=lambda f:f.calc_area());normal=face.normal.normalized()
 if normal.z<0:normal=-normal
 a,b=max(((a,b) for a in group for b in group),key=lambda p:(p[0].co-p[1].co).length_squared)
 along=(b.co-a.co);length=along.length;along.normalize()
 across=normal.cross(along).normalized()
 if across.length<.5:continue
 if along.dot(Vector((center.x,center.y,0)))<0:along=-along
 placements.append((center,along,across,normal,length));remove.extend(group)
bmesh.ops.delete(bm,geom=remove,context='VERTS');bm.to_mesh(o.data);bm.free()
leaf=bpy.data.materials.new('M_F01_TaperedLeaf');leaf.use_nodes=True
nodes=leaf.node_tree.nodes;links=leaf.node_tree.links;p=next(n for n in nodes if n.type=='BSDF_PRINCIPLED')
p.inputs['Roughness'].default_value=.78
tex=nodes.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(ROOT/'assets/models/forest_wreck/textures/T_Leaf_BaseColor.png'));tex.image.pack()
geo=nodes.new('ShaderNodeNewGeometry');mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MIX';mix.inputs[2].default_value=(.038,.023,.053,1)
links.new(geo.outputs['Backfacing'],mix.inputs[0]);links.new(tex.outputs['Color'],mix.inputs[1]);links.new(mix.outputs[0],p.inputs['Base Color'])
verts=[];faces=[];uv=[]
outline=[(0,-.5),(.23,-.18),(.18,.20),(.08,.50),(0,.39),(-.08,.50),(-.18,.20),(-.23,-.18)]
for center,along,across,normal,length in placements:
 length=max(.2,min(.9,length*1.15));start=len(verts)
 verts.append(center+normal*.018);uv.append((.5,.5))
 for x,y in outline:verts.append(center+(across*x+along*y)*length);uv.append((x*2+.5,y+.5))
 for j in range(8):faces.append((start,start+1+(j+1)%8,start+1+j))
mesh=bpy.data.meshes.new('ForkTipLeafGeometry');mesh.from_pydata(verts,[],faces);mesh.update()
leaves=bpy.data.objects.new('TaperedLeaves',mesh);bpy.context.collection.objects.link(leaves);mesh.materials.append(leaf)
layer=mesh.uv_layers.new(name='LeafUV')
for loop in mesh.loops:layer.data[loop.index].uv=uv[loop.vertex_index]
bpy.ops.object.select_all(action='DESELECT');o.select_set(True);leaves.select_set(True);bpy.context.view_layer.objects.active=o;bpy.ops.object.join()
bpy.context.view_layer.update();o.data.calc_loop_triangles()
report={'id':'F01_HybridCanopy','replaced_leaf_islands':len(placements),'triangles':len(o.data.loop_triangles),'materials':len(o.data.materials),'dimensions_m':list(o.dimensions),'method':'Meshy wood retained, opaque rectangular foliage replaced by tapered fork-tip geometry and violet undersides','collision':'pending trunk-only setup','visual_acceptance':'pending'}
bpy.ops.wm.save_as_mainfile(filepath=str(BASE/'blender/F01_HybridCanopy.blend'))
bpy.ops.export_scene.fbx(filepath=str(BASE/'export/SM_F01_HybridCanopy.fbx'),use_selection=True,object_types={'MESH'},apply_unit_scale=True,axis_forward='-Y',axis_up='Z',add_leaf_bones=False,bake_anim=False,path_mode='AUTO',mesh_smooth_type='FACE')
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=24
scene.render.resolution_x=1200;scene.render.resolution_y=1000;scene.render.resolution_percentage=100
if scene.world is None:scene.world=bpy.data.worlds.new('InspectionWorld')
scene.world.color=(.18,.18,.18);scene.view_settings.view_transform='AgX'
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.04));ground=bpy.context.object
m=bpy.data.materials.new('InspectionGround');m.diffuse_color=(.12,.14,.13,1);ground.data.materials.append(m)
for name,loc,power,size in [('Key',(-7,-8,14),2600,7),('Fill',(7,-2,10),1700,6),('Rim',(0,8,12),3000,5)]:
 bpy.ops.object.light_add(type='AREA',location=loc);lamp=bpy.context.object;lamp.name=name;lamp.data.energy=power;lamp.data.shape='DISK';lamp.data.size=size;lamp.rotation_euler=(Vector((0,0,4))-lamp.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add();cam=bpy.context.object;scene.camera=cam;cam.data.lens=48
for i,loc in enumerate([(13,-18,7),(-14,17,6),(9,-13,1.7)]):
 cam.location=loc;cam.rotation_euler=(Vector((0,0,4.2))-cam.location).to_track_quat('-Z','Y').to_euler();scene.render.filepath=str(ROOT/'reports'/f'f01_hybrid_blender_{i}.png');bpy.ops.render.render(write_still=True)
(ROOT/'reports/f01_hybrid_blender.json').write_text(json.dumps(report,indent=2));print('HYBRID_TREE_COMPLETE',json.dumps(report))
