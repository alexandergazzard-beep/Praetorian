"""Create a fully editable, textured Blender showcase using the actual selected 3D meshes."""
import bpy,json,math,random
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'assets/models/wreck_showcase';random.seed(91)
bpy.ops.wm.read_factory_settings(use_empty=True)
def append(file,objname=None):
 with bpy.data.libraries.load(str(file),link=False) as (source,target):target.objects=[n for n in source.objects if objname is None or n==objname]
 objects=[o for o in target.objects if o is not None and o.type=='MESH']
 for o in objects:bpy.context.collection.objects.link(o)
 assert objects,str(file);return objects
terrainparts=append(BASE/'blender/ShowcaseDressing.blend')
meshbank={o.name:o for o in terrainparts}
large=append(ROOT/'assets/models/forest_wreck/Large_WreckModule/blender/prepared.blend')[0]
engine=append(ROOT/'assets/models/forest_wreck/Engine_MeshyNacelle/blender/prepared.blend')[0]
medium=append(ROOT/'assets/models/forest_wreck/Medium_WreckPanel/blender/prepared.blend')[0]
tree=append(ROOT/'assets/models/forest_wreck/F01_HybridCanopy/blender/F01_HybridCanopy.blend')[0]
crate=append(ROOT/'assets/models/debris/M17_supply_trunk/blender/game_ready.blend')[0]
def mat(name,a,b,rough):
 m=bpy.data.materials.new(name);m.use_nodes=True;n=m.node_tree.nodes;l=m.node_tree.links;bs=n.get('Principled BSDF');noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=2.8;noise.inputs['Detail'].default_value=4
 tex=n.new('ShaderNodeTexCoord');l.new(tex.outputs['Object'],noise.inputs['Vector']);ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].color=(*a,1);ramp.color_ramp.elements[1].color=(*b,1);l.new(noise.outputs['Fac'],ramp.inputs['Fac']);l.new(ramp.outputs['Color'],bs.inputs['Base Color']);bs.inputs['Roughness'].default_value=rough
 bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.3;bump.inputs['Distance'].default_value=.08;l.new(noise.outputs['Fac'],bump.inputs['Height']);l.new(bump.outputs['Normal'],bs.inputs['Normal']);return m
soil=mat('Showcase_Damp_Soil',(.018,.025,.022),(.10,.12,.08),.66);stone=mat('Showcase_Stone',(.025,.038,.04),(.16,.18,.14),.92)
for o in terrainparts:
 o.data.materials.clear();o.data.materials.append(soil if 'Terrain' in o.name else stone if 'Rock' in o.name else large.data.materials[0])
 if 'Terrain' not in o.name:o.hide_render=True;o.hide_viewport=True
def h(x,y):return -.6*math.exp(-((x/17)**2+(y/22)**2))+.20*math.sin(x*.31)*math.cos(y*.24)+.12*math.sin(x*.95+y*.51)+max(0,(math.sqrt((x/1.2)**2+y*y)-25)/12)**2*1.7
def place(o,name,location,rot=(0,0,0),scale=1,copy=False):
 if copy:
  o=o.copy();bpy.context.collection.objects.link(o)
 o.hide_render=False;o.hide_viewport=False;o.name=name;o.location=location;o.rotation_euler=[math.radians(v) for v in rot];o.scale=(scale,scale,scale);return o
place(large,'Hero_Large',(0,2,h(0,2)-.45),(0,5,-12),1.25)
place(large,'Broken_Rear',(4.5,14.5,h(4.5,14.5)+.8),(0,-19,158),.95,True)
place(engine,'Engine',(-11.5,4,h(-11.5,4)-1.1),(0,-8,28),.78)
place(medium,'Detached_Armor',(10.5,-1.8,h(10.5,-1.8)-.25),(0,-21,-43),.75)
place(crate,'Supply_Trunk',(-3.9,-7.5,h(-3.9,-7.5)+.05),(0,0,-18))
tree.hide_render=True;tree.hide_viewport=True
for i in range(42):
 angle=random.uniform(0,math.tau);r=random.uniform(17,43);x=math.cos(angle)*r;y=math.sin(angle)*r
 if y<-11 and abs(x)<21:continue
 if y<8:y+=43
 place(tree,f'BackgroundTree_{i}',(x,y,h(x,y)-.5),(random.uniform(-4,4),random.uniform(-5,5),random.uniform(-180,180)),random.uniform(.85,1.65),True)
for i in range(90):
 x=random.uniform(-26,24);y=random.uniform(-17,26);s=random.uniform(.18,.7)*(2 if i<8 else 1)
 place(meshbank[f'SM_ShowcaseRock_{i%3}'],f'GroundStone_{i}',(x,y,h(x,y)-s*.32),(random.uniform(-20,20),random.uniform(-25,25),random.uniform(-180,180)),s,True)
for i in range(38):
 x=random.uniform(-13,17);y=random.uniform(-13,17.5)
 place(meshbank[f'SM_ShowcasePlate_{i%3}'],f'ArmorScatter_{i}',(x,y,h(x,y)+.06),(random.uniform(-8,8),random.uniform(-8,8),random.uniform(-180,180)),random.uniform(.2,.85),True)
# Sparse short grass tufts soften the ground without introducing another paid asset.
grass=mat('Muted_Reed_Grass',(.015,.035,.025),(.10,.16,.09),.8)
for i in range(65):
 x=random.uniform(-23,24);y=random.uniform(-13,24)
 if abs(x)<5 and y<3:continue
 verts=[];faces=[]
 for j in range(6):
  dx=random.uniform(-.12,.12);dy=random.uniform(-.12,.12);height=random.uniform(.16,.42);a=len(verts);verts.extend([(dx-.018,dy,0),(dx+.018,dy,0),(dx+.06,dy+.03,height)]);faces.append((a,a+1,a+2))
 me=bpy.data.meshes.new('GrassTuft');me.from_pydata(verts,[],faces);me.materials.append(grass);o=bpy.data.objects.new(f'Grass_{i}',me);bpy.context.collection.objects.link(o);o.location=(x,y,h(x,y))
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=64;scene.cycles.use_denoising=True
scene.render.resolution_x=1920;scene.render.resolution_y=1080;scene.render.resolution_percentage=100
scene.view_settings.view_transform='AgX';scene.view_settings.look='AgX - Medium High Contrast';scene.view_settings.exposure=0
world=bpy.data.worlds.new('CoolTwilight');world.use_nodes=True;world.node_tree.nodes['Background'].inputs['Color'].default_value=(.065,.115,.20,1);world.node_tree.nodes['Background'].inputs['Strength'].default_value=.35;scene.world=world
def light(name,loc,power,size,color,target=(0,3,3)):
 bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.name=name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;o.data.color=color;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();return o
light('CoolKey',(-13,-13,13),6500,12,(.55,.75,1))
light('AmberRim',(10,13,11),10500,9,(1,.46,.19))
light('ForestBacklight',(-17,23,17),5500,14,(.30,.60,1))
light('GentleFrontFill',(-1,-14,6),1800,10,(.53,.65,.84))
for i,loc in enumerate([(2.6,-2.8,2.35),(-.9,-2.35,1),(6,5,2.1)]):
 bpy.ops.object.light_add(type='POINT',location=loc);o=bpy.context.object;o.name=f'WarmFault_{i}';o.data.energy=65;o.data.color=(1,.18,.018);o.data.shadow_soft_size=.3
# Real volumetric haze in the 3D render, kept light enough to reveal the textured armor.
bpy.ops.mesh.primitive_cube_add(size=1,location=(0,14,9));mist=bpy.context.object;mist.name='AtmosphericMist';mist.scale=(100,105,30)
fog=bpy.data.materials.new('ThinBlueMist');fog.use_nodes=True;nodes=fog.node_tree.nodes;nodes.clear();out=nodes.new('ShaderNodeOutputMaterial');vol=nodes.new('ShaderNodeVolumePrincipled');vol.inputs['Density'].default_value=.006;vol.inputs['Color'].default_value=(.55,.68,.8,1);vol.inputs['Anisotropy'].default_value=.25;fog.node_tree.links.new(vol.outputs['Volume'],out.inputs['Volume']);mist.data.materials.append(fog);mist.display_type='WIRE'
bpy.ops.object.camera_add(location=(-17,-23,5));cam=bpy.context.object;cam.name='ShowcaseCamera';target=Vector((0,4,3.2));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=40;scene.camera=cam
for image in bpy.data.images:
 if image.type=='IMAGE' and image.has_data:image.pack()
bpy.ops.wm.save_as_mainfile(filepath=str(BASE/'blender/LargeWreck_Showcase.blend'))
scene.render.filepath=str(ROOT/'reports/wreck_showcase_beauty.png');bpy.ops.render.render(write_still=True)
(ROOT/'reports/wreck_showcase_blender.json').write_text(json.dumps({'file':str(BASE/'blender/LargeWreck_Showcase.blend'),'render':scene.render.filepath,'actual_3d_render':True,'renderer':'Cycles','samples':64,'resolution':[1920,1080],'paid_generations':0,'objects':len(scene.objects),'materials':'packed existing wreck/wood/foliage PBR and procedural ground/rocks/grass','interpretation':'presentation scene, not story canon or gameplay validation'},indent=2));print('BLENDER_SHOWCASE_COMPLETE',flush=True)
