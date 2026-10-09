"""Deterministic editable environment meshes. Run with background Blender.

Two representative samples only. Batch expansion is held at the quality gate.
Sources, texture originals, exports and QA are kept separately.
"""
import bpy,math,random,json,sys
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'assets/models/forest_wreck'
BASE.mkdir(parents=True,exist_ok=True)
rng=random.Random(81026)
report=[]

def texture(name,kind):
 size=512
 path=BASE/'textures'/f'T_{name}_BaseColor.png';path.parent.mkdir(exist_ok=True)
 im=bpy.data.images.new(name,width=size,height=size)
 pixels=[]
 for y in range(size):
  v=y/(size-1)
  for x in range(size):
   u=x/(size-1)
   grain=rng.uniform(-.018,.018)
   if kind=='leaf':
    vein=math.exp(-abs(u-.5)*150)*.09
    side=.025*max(0,math.cos((v*16+abs(u-.5)*5)*math.tau))**12
    shade=.82+.18*math.sin(v*math.pi)
    c=(.045*shade+vein+side+grain,.23*shade+vein+side+grain,.245*shade+vein+side+grain)
   elif kind=='bark':
    groove=(math.sin(u*math.tau*22+math.sin(v*8)*.5)+math.sin(u*math.tau*67+v*9))*.014
    c=(.095+groove+grain,.105+groove+grain,.09+groove+grain)
   elif kind=='armor':
    base=(.32,.34,.335) if u<.333 else ((.155,.185,.105) if u<.666 else (.047,.053,.057))
    wear=.035*math.sin(x*.22+y*.014)*math.sin(y*.17)
    scratch=.05 if abs(math.sin(x*.031+y*.14))>.997 else 0
    c=tuple(q+grain+wear+scratch for q in base)
   else:
    n=.035*math.sin(x*.071+y*.047)+.025*math.cos(x*.23-y*.13)
    c=(.18+n+grain,.205+n+grain,.20+n+grain)
   pixels.extend((*[max(.008,min(1,q)) for q in c],1))
 im.pixels.foreach_set(pixels);im.filepath_raw=str(path);im.file_format='PNG';im.save()
 return im

def material(name,kind):
 m=bpy.data.materials.new(name);m.use_nodes=True
 p=next(n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED')
 p.inputs['Roughness'].default_value=.78 if kind!='armor' else .72
 p.inputs['Metallic'].default_value=.5 if kind=='armor' else 0
 tex=m.node_tree.nodes.new('ShaderNodeTexImage');tex.image=texture(name,kind)
 m.node_tree.links.new(tex.outputs['Color'],p.inputs['Base Color'])
 noise=m.node_tree.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=34
 bump=m.node_tree.nodes.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.18;bump.inputs['Distance'].default_value=.035
 m.node_tree.links.new(noise.outputs['Fac'],bump.inputs['Height']);m.node_tree.links.new(bump.outputs['Normal'],p.inputs['Normal'])
 return m

def reset():
 bpy.ops.wm.read_factory_settings(use_empty=True)
 bpy.context.scene.unit_settings.system='METRIC';bpy.context.scene.unit_settings.scale_length=1

def uv_smart(o,zone=None):
 bpy.context.view_layer.objects.active=o;o.select_set(True)
 bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.uv.smart_project(island_margin=.02);bpy.ops.object.mode_set(mode='OBJECT')
 if zone is not None:
  for uv in o.data.uv_layers.active.data:uv.uv.x=(uv.uv.x*.90+.05+zone)/3
 o.select_set(False)

def cube(name,loc,size,mat,zone=0,rot=None,bevel=.035):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc)
 o=bpy.context.object;o.name=name;o.dimensions=size
 bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 if bevel:
  mod=o.modifiers.new('Visible armor bevel','BEVEL');mod.width=bevel;mod.segments=2
  bpy.ops.object.modifier_apply(modifier=mod.name)
 o.data.materials.append(mat);uv_smart(o,zone)
 if rot:o.rotation_euler=rot
 return o

def tube(name,points,radii,mat,sides=9):
 verts=[];faces=[]
 for i,p in enumerate(points):
  p=Vector(p);d=Vector(points[min(i+1,len(points)-1)])-Vector(points[max(i-1,0)])
  d.normalize()
  tangent=d.cross(Vector((0,1,0)))
  if tangent.length<.001:tangent=d.cross(Vector((1,0,0)))
  tangent.normalize();bitangent=d.cross(tangent).normalized()
  for j in range(sides):
   a=j*math.tau/sides
   verts.append(p+(tangent*math.cos(a)+bitangent*math.sin(a))*radii[i])
 for i in range(len(points)-1):
  for j in range(sides):faces.append((i*sides+j,i*sides+(j+1)%sides,(i+1)*sides+(j+1)%sides,(i+1)*sides+j))
 faces.extend([tuple(reversed(range(sides))),tuple((len(points)-1)*sides+j for j in range(sides))])
 mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.update()
 o=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(o);o.data.materials.append(mat)
 for p in mesh.polygons:p.use_smooth=True
 uv_smart(o)
 return o

def leaves(name,items,mat):
 verts=[];faces=[];uvs=[]
 # Forked leaf ends, curved blade and real silhouette instead of alpha cards.
 outline=[(0,0),(.23,-.32),(.62,-.46),(.92,-.17),(1,-.11),(.89,0),(1,.11),(.92,.17),(.62,.46),(.23,.32)]
 for pos,length,width,quat,tilt in items:
  start=len(verts)
  verts.append(Vector(pos)+quat@Vector((length*.5,0,length*.09)))
  for u,v in outline:verts.append(Vector(pos)+quat@Vector((length*u,width*v,length*.13*math.sin(u*math.pi)+tilt*u)))
  local_uv=[(.5,.5)]+[(.5+v,u) for u,v in outline]
  for j in range(len(outline)):
   faces.append((start,start+1+j,start+1+(j+1)%len(outline)))
   uvs.extend([local_uv[0],local_uv[j+1],local_uv[1+(j+1)%len(outline)]])
 mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.update()
 uv=mesh.uv_layers.new(name='UVMap')
 for loop,co in zip(uv.data,uvs):loop.uv=co
 o=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(o);o.data.materials.append(mat)
 for p in mesh.polygons:p.use_smooth=True
 return o

def join(name):
 objs=[o for o in bpy.context.scene.objects if o.type=='MESH']
 bpy.ops.object.select_all(action='DESELECT')
 for o in objs:o.select_set(True)
 bpy.context.view_layer.objects.active=objs[0];bpy.ops.object.join();o=bpy.context.object;o.name='SM_'+name
 bpy.context.scene.cursor.location=(0,0,0);bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
 bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
 # Collapse identical material slots by name after joining procedural pieces.
 unique=[];mapping={}
 for i,m in enumerate(o.data.materials):
  if m not in unique:unique.append(m)
  mapping[i]=unique.index(m)
 ids=[mapping[p.material_index] for p in o.data.polygons]
 o.data.materials.clear()
 for m in unique:o.data.materials.append(m)
 for p,i in zip(o.data.polygons,ids):p.material_index=i
 return o

def tree(name='F01_LayeredCanopy',small=False,lean=False):
 reset();bark=material('Bark','bark');leaf=material('Leaf','leaf');items=[]
 height=7.8 if not small else 4.4
 tube('fluted trunk',[(0,0,0),(.04,0,1),(-.15,.06,2.5),(.25,.06,4.2),(.18,.15,height*.82),(.3,0,height)], [.46,.32,.24,.17,.10,.02],bark,12)
 for j in range(7):
  a=j*math.tau/7
  tube('buttress root',[(math.cos(a)*1.35,math.sin(a)*1.35,.015),(math.cos(a)*.55,math.sin(a)*.55,.22),(0,0,1.2)],[.065,.16,.15],bark,7)
 for tier in range(4):
  z=height*(.48+tier*.15);reach=[3.5,3.15,2.8,1.9][tier]
  for b in range(5):
   a=b*math.tau/5+tier*.69+rng.uniform(-.22,.22);d=Vector((math.cos(a),math.sin(a),0))
   p=Vector((.12,0,z));mid=p+d*reach*.58+Vector((0,0,.25));end=p+d*reach+Vector((0,0,.38))
   tube('main branching limb',[p,mid,end],[.13-tier*.019,.055,.017],bark,8)
   for twig in range(5):
    t=(twig+1)/5;center=p.lerp(end,t);side=Vector((-d.y,d.x,0))*(1 if twig%2 else -1)
    tip=center+side*(.50+(.2 if tier<2 else 0))+d*.20+Vector((0,0,.28))
    tube('leaf bearing twig',[center,tip],[.022,.006],bark,6)
    for k in range(14):
     r=math.sqrt(rng.random())*.70;aa=rng.random()*math.tau
     pos=tip+Vector((math.cos(aa)*r,math.sin(aa)*r,rng.uniform(-.15,.22)))
     direction=Vector((math.cos(aa),math.sin(aa),rng.uniform(-.35,.3)))
     q=direction.to_track_quat('X','Z')
     items.append((pos,rng.uniform(.40,.64),rng.uniform(.34,.48),q,rng.uniform(-.04,.03)))
 leaves('forked teal canopy',items,leaf)
 o=join(name)
 if small:o.scale=(.70,.70,.72);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 if lean:
  for v in o.data.vertices:v.co.x+=v.co.z*.24
 return o

def hull(name='Hull_ArmoredSection',plate=False,engine=False):
 reset();armor=material('ArmorAtlas','armor')
 if engine:
  # Closed shallow nozzle backing avoids invented engine-room interiors.
  for j in range(12):
   a=j*math.tau/12;rot=(a,0,0)
   cube('outer nacelle armor',(0,math.sin(a)*1.9,2.0+math.cos(a)*1.9),(6,.98,.18),armor,1 if j in (2,3) else 0,rot, .045)
   for x in (-2.8,2.8):cube('nozzle rim',(x,math.sin(a)*1.82,2+math.cos(a)*1.82),(.19,.97,.23),armor,2,rot,.025)
  bpy.ops.mesh.primitive_cylinder_add(vertices=32,radius=1.68,depth=.12,location=(2.52,0,2),rotation=(0,math.pi/2,0))
  o=bpy.context.object;o.data.materials.append(armor);uv_smart(o,2)
  for j in range(9):cube('exhaust louver',(2.72,0,.65+j*.33),(.13,2.6,.10),armor,2,bevel=.015)
 elif plate:
  cube('thick plate',(0,0,.10),(2.8,1.7,.20),armor,0,bevel=.045)
  cube('olive identity stripe',(0,0,.211),(.50,1.65,.018),armor,1,bevel=.008)
  for x in (-1.1,1.1):cube('reinforcing edge',(x,0,.25),(.14,1.7,.14),armor,2)
 else:
  cube('simple closed backing',(0,0,1.6),(12,4.8,3.2),armor,2,bevel=.13)
  for row in range(3):
   for col in range(8):
    x=-5.25+col*1.5;y=-1.65+row*1.65
    if (row,col) in [(0,6),(0,7),(1,7)]:continue
    z=3.30-rng.uniform(0,.035)
    cube('upper armor panel',(x,y,z),(1.44,1.58,.18),armor,1 if col in (2,3) else 0,bevel=.032)
    for yy in (-.64,.64):cube('panel clasp',(x,y+yy,z+.12),(.24,.10,.065),armor,2,bevel=.012)
  for side in (-1,1):
   for col in range(8):
    x=-5.25+col*1.5
    cube('retained side armor',(x,side*2.47,1.9),(1.43,.18,2.45),armor,1 if col in (2,3) else 0,bevel=.05)
    cube('lower reinforcing rail',(x,side*2.48,.48),(1.48,.22,.25),armor,2)
   for x in (-5.6,-2.8,0,2.8,5.6):cube('reinforcing vertical rib',(x,side*2.6,1.7),(.17,.17,2.85),armor,2)
  for j in range(5):
   cube('shallow damaged electronics',(4.0+j*.3,-1.7,3.29),(.17,.8,.14),armor,2,bevel=.015)
  for j in range(8):
   x=4.3+rng.random()*1.6;y=-2+rng.random()*2.5
   cube('torn armor edge',(x,y,3.40),(.55,.40,.12),armor,0,rot=(rng.uniform(-.12,.24),rng.uniform(-.16,.16),rng.uniform(-.3,.3)))
 o=join(name)
 if not engine and not plate:
  # Chamfered armor shoulders and a tapered broken connection give a hull
  # silhouette rather than a rectangular cargo-box mass.
  for v in o.data.vertices:
   if v.co.z>2.25:
    v.co.y*=1-.12*min(1,(v.co.z-2.25)/1.2)
   if v.co.x<-3.8:
    v.co.y*=1-.22*min(1,(-v.co.x-3.8)/2.2)
    v.co.z*=1-.14*min(1,(-v.co.x-3.8)/2.2)
 return o

def render(o,name):
 scene=bpy.context.scene
 # Blender-supported engine identifier from installed build, no GUI scene touched.
 try:scene.render.engine='CYCLES'
 except TypeError:raise
 scene.cycles.samples=24
 scene.render.resolution_x=1200;scene.render.resolution_y=900;scene.render.resolution_percentage=100
 scene.world=bpy.data.worlds.new('Neutral world');scene.world.use_nodes=True
 bg=next(n for n in scene.world.node_tree.nodes if n.type=='BACKGROUND');bg.inputs[0].default_value=(.30,.33,.35,1);bg.inputs[1].default_value=.6
 center=Vector((0,0,o.dimensions.z*.45));extent=max(o.dimensions)
 for loc,power,size in [((-extent,-extent,extent*1.6),extent*extent*160,extent),((extent,extent,extent),extent*extent*90,extent)]:
  data=bpy.data.lights.new('Soft light','AREA');data.energy=power;data.shape='DISK';data.size=size
  light=bpy.data.objects.new('Soft light',data);scene.collection.objects.link(light);light.location=loc;light.rotation_euler=(center-light.location).to_track_quat('-Z','Y').to_euler()
 data=bpy.data.cameras.new('Asset inspection');cam=bpy.data.objects.new('Asset inspection',data);scene.collection.objects.link(cam)
 cam.location=center+Vector((extent*1.2,-extent*1.5,extent*.65));cam.rotation_euler=(center-cam.location).to_track_quat('-Z','Y').to_euler();data.type='ORTHO';data.ortho_scale=extent*1.82;scene.camera=cam
 scene.render.filepath=str(ROOT/'reports'/f'forest_wreck_blender_{name}.png');scene.render.image_settings.file_format='PNG';bpy.ops.render.render(write_still=True)

def save(o,name,ref):
 dest=BASE/name
 for part in ['blender','export']:(dest/part).mkdir(parents=True,exist_ok=True)
 o.data.calc_loop_triangles()
 result={'id':name,'reference':ref,'source':str(dest/'blender'/f'{name}.blend'),'export':str(dest/'export'/f'SM_{name}.fbx'),'dimensions_m':list(o.dimensions),'triangles':len(o.data.loop_triangles),'materials':[m.name for m in o.data.materials],'uv_layers':len(o.data.uv_layers),'pivot':'ground at origin','produced':True,'imported':False,'integrated':False,'verified':False}
 for m in o.data.materials:
  for n in m.node_tree.nodes:
   if n.type=='TEX_IMAGE':n.image.pack()
 bpy.ops.wm.save_as_mainfile(filepath=result['source'])
 bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
 if name.startswith('F01'):
  bpy.ops.mesh.primitive_cylinder_add(vertices=12,radius=.43,depth=4.1,location=(0,0,2.05))
  collider=bpy.context.object;collider.name='UCX_SM_'+name+'_00';collider.hide_render=True
  bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
  bpy.ops.object.select_all(action='DESELECT');o.select_set(True);collider.select_set(True);bpy.context.view_layer.objects.active=o
  bpy.ops.wm.save_as_mainfile(filepath=result['source'])
 bpy.ops.export_scene.fbx(filepath=result['export'],use_selection=True,object_types={'MESH'},apply_unit_scale=True,axis_forward='-Y',axis_up='Z',add_leaf_bones=False,bake_anim=False,path_mode='AUTO',mesh_smooth_type='FACE')
 render(o,name)
 report.append(result)

save(tree(),'F01_LayeredCanopy','F1/F01')
save(hull(),'Hull_ArmoredSection','A4/D5')
(ROOT/'reports/forest_wreck_blender.json').write_text(json.dumps(report,indent=2))
print('SAMPLES_PRODUCED',json.dumps(report),flush=True)
