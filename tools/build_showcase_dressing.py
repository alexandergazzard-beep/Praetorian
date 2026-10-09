"""Create editable terrain/rock/armor-scatter sources for the isolated wreck showcase."""
import bpy,math,random,json
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'assets/models/wreck_showcase';BASE.mkdir(exist_ok=True)
for sub in ['blender','export']:(BASE/sub).mkdir(exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True);random.seed(43)
def height(x,y):
 return -.6*math.exp(-((x/17)**2+(y/22)**2))+.20*math.sin(x*.31)*math.cos(y*.24)+.12*math.sin(x*.95+y*.51)+max(0,(math.sqrt((x/1.2)**2+y*y)-25)/12)**2*1.7
def mesh(name,verts,faces):
 m=bpy.data.meshes.new(name);m.from_pydata(verts,[],faces);m.update();o=bpy.data.objects.new(name,m);bpy.context.collection.objects.link(o);return o
N=125;verts=[];faces=[]
for iy in range(N):
 for ix in range(N):
  x=(ix/(N-1)-.5)*120;y=(iy/(N-1)-.5)*120;verts.append((x,y,height(x,y)))
for iy in range(N-1):
 for ix in range(N-1):
  a=iy*N+ix;faces.append((a,a+1,a+1+N,a+N))
o=mesh('SM_ShowcaseTerrain',verts,faces)
for p in o.data.polygons:p.use_smooth=True
uv=o.data.uv_layers.new(name='TerrainUV')
for loop in o.data.loops:
 v=o.data.vertices[loop.vertex_index].co;uv.data[loop.index].uv=(v.x/120+.5,v.y/120+.5)
color=o.data.color_attributes.new(name='GroundMask',type='FLOAT_COLOR',domain='POINT')
for i,v in enumerate(o.data.vertices):
 x,y=v.co.x,v.co.y;wet=math.exp(-((x+5)/7)**2)*math.exp(-(y/26)**2);color.data[i].color=(wet,0,0,1)
for variant in range(3):
 bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2,radius=1);o=bpy.context.object;o.name=f'SM_ShowcaseRock_{variant}'
 for v in o.data.vertices:
  n=v.co.normalized();jitter=random.uniform(.8,1.15);v.co*=jitter;v.co.x*=1.5;v.co.y*=1.1;v.co.z*=.8;v.co.z+=.3*math.sin(v.co.x*3+variant)
 for p in o.data.polygons:p.use_smooth=False
 bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.uv.smart_project();bpy.ops.object.mode_set(mode='OBJECT')
 verts=[(-1.2,-.55,.0),(1,-.55,.0),(1.15,.43,.04),(-.85,.65,.03),(-1.2,-.55,.08),(1,-.55,.08),(1.15,.43,.12),(-.85,.65,.11)]
 plate=mesh(f'SM_ShowcasePlate_{variant}',verts,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)])
 bpy.context.view_layer.objects.active=plate;plate.select_set(True)
 bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.uv.smart_project();bpy.ops.object.mode_set(mode='OBJECT');plate.select_set(False)
bpy.context.scene.unit_settings.system='METRIC';bpy.context.scene.unit_settings.scale_length=1
bpy.ops.wm.save_as_mainfile(filepath=str(BASE/'blender/ShowcaseDressing.blend'))
report=[]
for o in list(bpy.context.scene.objects):
 if o.type!='MESH':continue
 bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
 bpy.ops.export_scene.fbx(filepath=str(BASE/'export'/(o.name+'.fbx')),use_selection=True,object_types={'MESH'},apply_unit_scale=True,axis_forward='-Y',axis_up='Z',add_leaf_bones=False,bake_anim=False,mesh_smooth_type='FACE')
 o.data.calc_loop_triangles();report.append({'name':o.name,'triangles':len(o.data.loop_triangles)})
(ROOT/'reports/wreck_showcase_dressing.json').write_text(json.dumps(report,indent=2));print('SHOWCASE_DRESSING_COMPLETE',json.dumps(report))
