"""Author an isolated textured wreck presentation level with native Unreal editor APIs."""
import unreal,json,math,random
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DEST='/Game/LostVanguard/Environment/WreckShowcase'
MAP=DEST+'/Maps/L_LargeWreck_Showcase'
tools=unreal.AssetToolsHelpers.get_asset_tools();lib=unreal.MaterialEditingLibrary
levels=unreal.get_editor_subsystem(unreal.LevelEditorSubsystem);actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
# This script owns only the new showcase folder and actors labelled Showcase_.
random.seed(91)
def node(mat,cls,x=0,y=0):return lib.create_material_expression(mat,cls,x,y)
def connect(a,out,b,inp):
 connected=lib.connect_material_expressions(a,out,b,inp)
 if not connected:
  names=list(lib.get_material_expression_input_names(b));print('SHOWCASE_INPUT_NAMES',b.get_class().get_name(),names)
  for name in names:
   if inp.lower() in str(name).replace(' ','').lower():connected=lib.connect_material_expressions(a,out,b,str(name));break
 assert connected,str((a.get_class().get_name(),out,b.get_class().get_name(),inp))
def scalar(mat,value):
 n=node(mat,unreal.MaterialExpressionConstant);n.set_editor_property('r',value);return n
def color(mat,value):
 n=node(mat,unreal.MaterialExpressionConstant3Vector);n.set_editor_property('constant',unreal.LinearColor(*value,1));return n
def surface(name,a,b,rough):
 m=unreal.load_asset(DEST+'/Materials/'+name) or tools.create_asset(name,DEST+'/Materials',unreal.Material,unreal.MaterialFactoryNew())
 lib.delete_all_material_expressions(m)
 pos=node(m,unreal.MaterialExpressionWorldPosition,-1000,0);freq=node(m,unreal.MaterialExpressionMultiply,-850,0);freq.set_editor_property('const_b',.018);connect(pos,'',freq,'A')
 noise=node(m,unreal.MaterialExpressionNoise,-650,0);noise.set_editor_property('quality',1);noise.set_editor_property('levels',3);noise.set_editor_property('scale',1);noise.set_editor_property('output_min',0);noise.set_editor_property('output_max',1);connect(freq,'',noise,'Position')
 blend=node(m,unreal.MaterialExpressionLinearInterpolate,-250,0);connect(color(m,a),'',blend,'A');connect(color(m,b),'',blend,'B');connect(noise,'',blend,'Alpha');assert lib.connect_material_property(blend,'',unreal.MaterialProperty.MP_BASE_COLOR)
 assert lib.connect_material_property(scalar(m,rough),'',unreal.MaterialProperty.MP_ROUGHNESS)
 lib.recompile_material(m);assert unreal.EditorAssetLibrary.save_loaded_asset(m);return m
groundmat=surface('M_DampAlienSoil',(.025,.033,.029),(.10,.12,.085),.82)
rockmat=surface('M_FracturedStone',(.045,.055,.052),(.19,.21,.17),.94)
glow=unreal.load_asset(DEST+'/Materials/M_AmberFault') or tools.create_asset('M_AmberFault',DEST+'/Materials',unreal.Material,unreal.MaterialFactoryNew());lib.delete_all_material_expressions(glow)
n=color(glow,(4,.65,.035));assert lib.connect_material_property(n,'',unreal.MaterialProperty.MP_EMISSIVE_COLOR);lib.recompile_material(glow);assert unreal.EditorAssetLibrary.save_loaded_asset(glow)
meshes={}
large=unreal.load_asset('/Game/LostVanguard/Environment/OpeningReview/Assets/WreckTrio/Large_WreckModule/SM_Large_WreckModule')
engine=unreal.load_asset('/Game/LostVanguard/Environment/OpeningReview/Assets/WreckTrio/Engine_MeshyNacelle/SM_Engine_MeshyNacelle')
medium=unreal.load_asset('/Game/LostVanguard/Environment/OpeningReview/Assets/WreckTrio/Medium_WreckPanel/SM_Medium_WreckPanel')
tree=unreal.load_asset('/Game/LostVanguard/Environment/OpeningReview/Assets/F01_HybridCanopy/SM_F01_HybridCanopy')
crate=unreal.load_asset('/Game/LostVanguard/Art/Debris/FirstPair/M17_supply_trunk/SM_M17_supply_trunk')
assert all([large,engine,medium,tree,crate])
metal=unreal.load_asset('/Game/LostVanguard/Environment/OpeningReview/Assets/WreckTrio/Large_WreckModule/MI_Large_WreckModule')
for item in json.loads((ROOT/'reports/wreck_showcase_dressing.json').read_text()):
 name=item['name'];opt=unreal.FbxImportUI();opt.import_mesh=True;opt.import_materials=False;opt.import_textures=False;opt.import_as_skeletal=False;opt.static_mesh_import_data.combine_meshes=True;opt.static_mesh_import_data.auto_generate_collision=False
 task=unreal.AssetImportTask();task.filename=str(ROOT/'assets/models/wreck_showcase/export'/(name+'.fbx'));task.destination_path=DEST+'/Assets';task.destination_name=name;task.automated=True;task.save=True;task.replace_existing=False;task.options=opt
 mesh=unreal.load_asset(DEST+'/Assets/'+name)
 if not mesh:
  tools.import_asset_tasks([task]);assert task.imported_object_paths;mesh=unreal.load_asset(task.imported_object_paths[0])
 mesh.set_material(0,groundmat if 'Terrain' in name else rockmat if 'Rock' in name else metal)
 if 'Terrain' in name:mesh.get_editor_property('body_setup').set_editor_property('collision_trace_flag',unreal.CollisionTraceFlag.CTF_USE_COMPLEX_AS_SIMPLE)
 assert unreal.EditorAssetLibrary.save_loaded_asset(mesh);meshes[name]=mesh
if unreal.EditorAssetLibrary.does_asset_exist(MAP):
 assert levels.load_level(MAP)
 for existing in actors.get_all_level_actors():
  if existing.get_actor_label().startswith('Showcase_'):actors.destroy_actor(existing)
else:assert levels.new_level(MAP)
def h(x,y):
 x/=100;y/=100
 return 100*(-.6*math.exp(-((x/17)**2+(y/22)**2))+.20*math.sin(x*.31)*math.cos(y*.24)+.12*math.sin(x*.95+y*.51)+max(0,(math.sqrt((x/1.2)**2+y*y)-25)/12)**2*1.7)
def spawn(cls,name,pos,rot=(0,0,0)):
 a=actors.spawn_actor_from_class(cls,unreal.Vector(*pos),unreal.Rotator(*rot));a.set_actor_label(name);a.set_folder_path('LostVanguard/WreckShowcase');return a
def put(mesh,name,pos,rot=(0,0,0),scale=(1,1,1),collision=False):
 a=spawn(unreal.StaticMeshActor,name,pos,rot);a.static_mesh_component.set_static_mesh(mesh);a.set_actor_scale3d(unreal.Vector(*scale));a.static_mesh_component.set_collision_profile_name('BlockAll' if collision else 'NoCollision');a.static_mesh_component.set_collision_enabled(unreal.CollisionEnabled.QUERY_AND_PHYSICS if collision else unreal.CollisionEnabled.NO_COLLISION);return a
put(meshes['SM_ShowcaseTerrain'],'Showcase_Terrain',(0,0,0),collision=True)
put(large,'Showcase_HeroLarge',(0,200,h(0,200)-45),(0,-12,5),(1.25,1.25,1.25),True)
put(large,'Showcase_BrokenRearSection',(450,1450,h(450,1450)+80),(0,158,-19),(.95,.95,.95),True)
put(engine,'Showcase_Engine',(-1150,400,h(-1150,400)-110),(0,28,-8),(.78,.78,.78),True)
put(medium,'Showcase_DetachedArmor',(1050,-180,h(1050,-180)-25),(0,-43,-21),(.75,.75,.75),True)
put(crate,'Showcase_ScaleSupplyTrunk',(-390,-750,h(-390,-750)+5),(0,-18,0),collision=True)
for i in range(42):
 angle=random.uniform(0,math.tau);r=random.uniform(1700,4300);x=math.cos(angle)*r;y=math.sin(angle)*r
 if y < -1100 and abs(x)<2100:continue
 s=random.uniform(.85,1.65)
 if y<800:y+=4300
 put(tree,f'Showcase_BackgroundTree_{i}',(x,y,h(x,y)-50),(random.uniform(-6,6),random.uniform(-180,180),random.uniform(-5,5)),(s,s,s))
for i in range(65):
 x=random.uniform(-2600,2400);y=random.uniform(-1700,2600);s=random.uniform(18,70)
 if i<8:s*=2.3
 put(meshes[f'SM_ShowcaseRock_{i%3}'],f'Showcase_Stone_{i}',(x,y,h(x,y)-s*.32),(random.uniform(-20,20),random.uniform(-180,180),random.uniform(-25,25)),(s/100,s/100,s/100))
for i in range(38):
 x=random.uniform(-1300,1700);y=random.uniform(-1300,1750);s=random.uniform(.2,.85)
 put(meshes[f'SM_ShowcasePlate_{i%3}'],f'Showcase_ArmorScatter_{i}',(x,y,h(x,y)+6),(random.uniform(-10,10),random.uniform(-180,180),random.uniform(-12,12)),(s,s,s))
# Restrained amber fault marks and warm pools frame the damaged machinery.
cube=unreal.load_asset('/Engine/BasicShapes/Cube')
for i,pos in enumerate([(260,-280,235),(-90,-235,100),(600,500,210)]):
 a=put(cube,f'Showcase_FaultStrip_{i}',pos,(0,-12,0),(.025,.35,.025));a.static_mesh_component.set_material(0,glow)
 light=spawn(unreal.PointLight,f'Showcase_FaultGlow_{i}',(pos[0],pos[1]-60,pos[2]+35));c=light.light_component;c.set_editor_property('intensity',90);c.set_editor_property('attenuation_radius',550);c.set_light_color(unreal.LinearColor(1,.21,.025,1));c.set_editor_property('volumetric_scattering_intensity',.45)
spawn(unreal.SkyAtmosphere,'Showcase_Atmosphere',(0,0,0))
sun=spawn(unreal.DirectionalLight,'Showcase_MoonRim',(0,0,2500),(-22,-120,0));c=sun.light_component;c.set_editor_property('intensity',2.2);c.set_light_color(unreal.LinearColor(.38,.64,1,1));c.set_editor_property('atmosphere_sun_light',True);c.set_editor_property('light_source_angle',3);c.set_editor_property('volumetric_scattering_intensity',.7)
sky=spawn(unreal.SkyLight,'Showcase_Sky',(0,0,1500));sky.light_component.set_editor_property('real_time_capture',True);sky.light_component.set_editor_property('intensity',.5)
fill=spawn(unreal.RectLight,'Showcase_SoftKey',(-1500,-1300,1300),(-24,43,0));c=fill.light_component;c.set_editor_property('intensity',6500);c.set_editor_property('attenuation_radius',6000);c.set_editor_property('source_width',1800);c.set_editor_property('source_height',1100);c.set_light_color(unreal.LinearColor(.58,.78,1,1));c.set_editor_property('volumetric_scattering_intensity',0)
rim=spawn(unreal.RectLight,'Showcase_WarmEdge',(900,1100,1200),(-30,-112,0));c=rim.light_component;c.set_editor_property('intensity',8500);c.set_editor_property('attenuation_radius',4000);c.set_editor_property('source_width',900);c.set_editor_property('source_height',1000);c.set_light_color(unreal.LinearColor(1,.47,.19,1));c.set_editor_property('volumetric_scattering_intensity',.3)
fog=spawn(unreal.ExponentialHeightFog,'Showcase_GroundMist',(0,0,-40));c=fog.get_component_by_class(unreal.ExponentialHeightFogComponent);c.set_editor_property('fog_density',.016);c.set_editor_property('fog_height_falloff',.28);c.set_editor_property('fog_inscattering_luminance',unreal.LinearColor(.12,.22,.30,1));c.set_editor_property('enable_volumetric_fog',True);c.set_editor_property('volumetric_fog_scattering_distribution',.45);c.set_editor_property('start_distance',500)
post=spawn(unreal.PostProcessVolume,'Showcase_Exposure',(0,0,0));post.set_editor_property('unbound',True);settings=post.get_editor_property('settings')
for name,value in {'override_auto_exposure_method':True,'auto_exposure_method':unreal.AutoExposureMethod.AEM_MANUAL,'override_auto_exposure_apply_physical_camera_exposure':True,'auto_exposure_apply_physical_camera_exposure':False,'override_auto_exposure_bias':True,'auto_exposure_bias':-1.5,'override_bloom_intensity':True,'bloom_intensity':.22,'override_vignette_intensity':True,'vignette_intensity':.25}.items():settings.set_editor_property(name,value)
post.set_editor_property('settings',settings);post.brush_component.set_visibility(False)
spawn(unreal.PlayerStart,'Showcase_PlayerStart',(-1200,-1700,h(-1200,-1700)+140),(0,56,0))
camera=spawn(unreal.CineCameraActor,'Showcase_HeroCamera',(-1900,-2400,420),(-1,51,0));camera.get_cine_camera_component().set_editor_property('current_focal_length',32)
for a in actors.get_all_level_actors():
 for billboard in a.get_components_by_class(unreal.BillboardComponent):billboard.set_visibility(False)
assert levels.save_current_level()
(ROOT/'reports/wreck_showcase_build.json').write_text(json.dumps({'map':MAP,'project':unreal.Paths.get_project_file_path(),'engine':unreal.SystemLibrary.get_engine_version(),'actor_count':len(actors.get_all_level_actors()),'hero':'selected Large module (two placements); Medium and D5 supporting','new_meshes':list(meshes),'new_paid_generations':0,'original_maps_preserved':True,'lighting':'cool forest rim, warm fault lights, low volumetric mist','verification':'pending live reload/capture/PIE'},indent=2));print('WRECK_SHOWCASE_BUILD_COMPLETE',flush=True)
