"""Import isolated Meshy rock kit and compose a playable native Landscape test."""
import unreal,json,math,random
from pathlib import Path
import toolset_registry
from editor_toolset.toolsets.blueprint import BlueprintTools as BP
from editor_toolset.toolsets import blueprint_dsl
R=Path(__file__).resolve().parents[1];D='/Game/LostVanguard/Environment/OrisonTerrain';MAP=D+'/Maps/L_OrisonTerrain_Review'
T=unreal.AssetToolsHelpers.get_asset_tools();L=unreal.MaterialEditingLibrary;E=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);S=unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
assert unreal.EditorLevelLibrary.get_editor_world().get_path_name().split('.')[0]==MAP
ctx=toolset_registry.tool_raising_exceptions();ctx.__enter__()
def imp(src,name,folder,opt=None):
 assert not unreal.EditorAssetLibrary.does_asset_exist(folder+'/'+name),'New packages only'
 t=unreal.AssetImportTask();t.filename=str(src);t.destination_name=name;t.destination_path=folder;t.automated=True;t.save=True
 if opt:t.options=opt
 T.import_asset_tasks([t]);assert t.imported_object_paths
 a=unreal.load_asset(t.imported_object_paths[0]);target=folder+'/'+name
 if a.get_path_name().split('.')[0]!=target:
  assert unreal.EditorAssetLibrary.rename_asset(a.get_path_name(),target);a=unreal.load_asset(target)
 return a
master=T.create_asset('M_OrisonRockPBR',D+'/Materials',unreal.Material,unreal.MaterialFactoryNew());assert master
nodes={}
for name,prop,sampler in [('BaseColor',unreal.MaterialProperty.MP_BASE_COLOR,unreal.MaterialSamplerType.SAMPLERTYPE_COLOR),('Normal',unreal.MaterialProperty.MP_NORMAL,unreal.MaterialSamplerType.SAMPLERTYPE_NORMAL),('Roughness',unreal.MaterialProperty.MP_ROUGHNESS,unreal.MaterialSamplerType.SAMPLERTYPE_MASKS)]:
 n=L.create_material_expression(master,unreal.MaterialExpressionTextureSampleParameter2D);n.set_editor_property('parameter_name',name);n.set_editor_property('sampler_type',sampler);nodes[name]=n
 assert L.connect_material_property(n,'R' if name=='Roughness' else 'RGB',prop)
metal=L.create_material_expression(master,unreal.MaterialExpressionConstant);metal.set_editor_property('r',0);L.connect_material_property(metal,'',unreal.MaterialProperty.MP_METALLIC)
assets=[];meshes={}
for asset,spec in json.loads((R/'reports/orison_terrain_specs.json').read_text()).items():
 base=R/'assets/models/orison_terrain'/asset;folder=D+'/Assets/'+asset
 opt=unreal.FbxImportUI();opt.import_mesh=True;opt.import_materials=False;opt.import_textures=False;opt.import_as_skeletal=False
 opt.static_mesh_import_data.combine_meshes=True;opt.static_mesh_import_data.auto_generate_collision=False
 mesh=imp(base/'export'/('SM_'+asset+'.fbx'),'SM_'+asset,folder,opt)
 mat=T.create_asset('MI_'+asset,folder,unreal.MaterialInstanceConstant,unreal.MaterialInstanceConstantFactoryNew());L.set_material_instance_parent(mat,master)
 maps={}
 for name,file in [('BaseColor','base_color'),('Normal','normal'),('Roughness','roughness')]:
  tex=imp(base/'source/meshy_original_textures'/(file+'.png'),'T_'+asset+'_'+name,folder)
  tex.set_editor_property('srgb',name=='BaseColor');tex.set_editor_property('max_texture_size',4096)
  tex.set_editor_property('mip_gen_settings',unreal.TextureMipGenSettings.TMGS_FROM_TEXTURE_GROUP)
  tex.set_editor_property('lod_group',unreal.TextureGroup.TEXTUREGROUP_WORLD_NORMAL_MAP if name=='Normal' else unreal.TextureGroup.TEXTUREGROUP_WORLD)
  if name=='Normal':tex.set_editor_property('compression_settings',unreal.TextureCompressionSettings.TC_NORMALMAP);tex.set_editor_property('flip_green_channel',True)
  elif name=='Roughness':tex.set_editor_property('compression_settings',unreal.TextureCompressionSettings.TC_MASKS)
  else:tex.set_editor_property('compression_settings',unreal.TextureCompressionSettings.TC_DEFAULT)
  L.set_material_instance_texture_parameter_value(mat,name,tex);maps[name]=tex.get_path_name()
  if not assets:nodes[name].set_editor_property('texture',tex)
  assert unreal.EditorAssetLibrary.save_loaded_asset(tex)
 mesh.set_material(0,mat);L.update_material_instance(mat)
 for a in [mat,mesh]:assert unreal.EditorAssetLibrary.save_loaded_asset(a)
 meshes[asset]=mesh;assets.append(dict(id=asset,mesh=mesh.get_path_name(),material=mat.get_path_name(),textures=maps))
L.recompile_material(master);assert unreal.EditorAssetLibrary.save_loaded_asset(master)
(R/'reports/orison_terrain_import.json').write_text(json.dumps(dict(assets=assets,map=MAP),indent=2))
def h(x,y):
 z=40+120*math.exp(-((x+1700)/1100)**2-((y-500)/1800)**2)+220*math.exp(-((x-1900)/1000)**2-((y-1500)/1300)**2)+15*math.sin(x*.002)*math.cos(y*.0016)
 center=170*math.sin(y*.0009);return z*(.45+.55*(1-math.exp(-((x-center)/480)**2)))
def spawn(cls,label,loc,rot=(0,0,0)):
 a=E.spawn_actor_from_class(cls,unreal.Vector(*loc),unreal.Rotator(*rot));a.set_actor_label(label);a.set_folder_path('OrisonTerrain');return a
placements=[]
def place(asset,x,y,scale=1,yaw=0,burial=8,label=None):
 mesh=meshes[asset] if asset in meshes else unreal.load_asset(asset);assert mesh
 a=spawn(unreal.StaticMeshActor,label or 'Terrain_'+asset+'_'+str(len(placements)),(x,y,h(x,y)-burial),(0,yaw,0))
 a.static_mesh_component.set_static_mesh(mesh);a.static_mesh_component.set_collision_profile_name('BlockAll');a.set_actor_scale3d(unreal.Vector(scale,scale,scale))
 placements.append(dict(label=a.get_actor_label(),asset=mesh.get_path_name(),location=list(a.get_actor_location().to_tuple()),scale=scale));return a
# Large ledge modules define perimeter landforms and leave the centre path open.
for x,y,scale,yaw in [(1250,800,1.4,0),(-1500,1550,1.1,180),(1700,2200,1.7,20),(-2100,-500,1.3,160)]:place('T02_Terrain71',x,y,scale,yaw,20)
random.seed(709)
for i in range(32):
 y=random.uniform(-2350,2550);side=random.choice([-1,1]);x=side*random.uniform(450,2450)
 place(['R01_Terrain71','R02_Terrain71','R06_Terrain71'][i%3],x,y,random.uniform(.55,1.65),random.uniform(0,360),random.uniform(4,14))
flora='/Game/LostVanguard/Environment/OpeningReview/Assets/FloraFlagship71/'
for i,(x,y) in enumerate([(-900,-1750),(1000,-1500),(-1200,-500),(1350,-100),(-900,700),(1600,1400),(-1450,1900),(750,2450),(-2300,2500),(2400,2400)]):
 name=['F01_Flagship71','F02_Flagship71','F08_Flagship71'][i%3];place(flora+name+'/SM_'+name,x,y,random.uniform(.65,1.1),random.uniform(0,360),0,'Terrain_Tree_'+str(i))
for i in range(34):
 y=random.uniform(-2300,2500);x=random.choice([-1,1])*random.uniform(290,2200)
 name=['F03_Flagship71','F05_Flagship71','F06_Flagship71','F10_Flagship71'][i%4]
 a=place(flora+name+'/SM_'+name,x,y,random.uniform(.5,1.0),random.uniform(0,360),1,'Terrain_Understory_'+str(i));a.static_mesh_component.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)
start=spawn(unreal.PlayerStart,'Terrain_PlayerStart',(0,-2300,h(0,-2300)+100),(0,90,0))
# A separate player uses existing camera/components but only walking controls.
player=unreal.EditorAssetLibrary.duplicate_asset('/Game/WreckagePrototype/Blueprints/BP_WreckagePlayer',D+'/Blueprints/BP_TerrainPlayer');assert player
for name,typ,val in [('DebugForward','float',0.0),('DebugRight','float',0.0),('DebugMoveTime','float',0.0),('RequestJump','bool',False)]:
 BP.add_variable(player,name,typ);BP.compile_blueprint(player);BP.get_default_object(player).set_editor_property(name,val)
graph=BP.get_graph(player,'EventGraph')
def create(g,typ,pos):
 editor=unreal.BlueprintGraphEditor.get_graph_editor(g)
 if typ.startswith('Variables|Default|Get'):n=editor.add_get_member_variable_node(typ.split('|')[-1][3:])
 elif typ.startswith('Variables|Default|Set'):n=editor.add_set_member_variable_node(typ.split('|')[-1][3:])
 elif typ=='AddEvent|EventTick':n=BP.add_event(player,'ReceiveTick',pos)
 else:n=BP.create_node(g,typ,pos)
 assert n,typ;n.set_node_pos(pos);return n
code='''(event EventTick (DeltaSeconds)
 (bind pc (Game|GetPlayerController :PlayerIndex 0))
 (bind (dx dy) (Game|Player|GetInputMouseDelta :self pc))
 (Pawn|Input|AddControllerYawInput :Val (* dx 0.6))
 (Pawn|Input|AddControllerPitchInput :Val (* dy -0.6))
 (Variables|Default|SetDebugMoveTime (- (Variables|Default|GetDebugMoveTime) DeltaSeconds))
 (if (<= (Variables|Default|GetDebugMoveTime) 0.0) (Variables|Default|SetDebugForward 0.0) (Variables|Default|SetDebugRight 0.0))
 (Pawn|Input|AddMovementInput :WorldDirection (Transformation|GetActorForwardVector) :ScaleValue (+ (Variables|Default|GetDebugForward) (- (select (Game|Player|IsInputKeyDown :self pc :Key "W") 1.0 0.0) (select (Game|Player|IsInputKeyDown :self pc :Key "S") 1.0 0.0))))
 (Pawn|Input|AddMovementInput :WorldDirection (Transformation|GetActorRightVector) :ScaleValue (+ (Variables|Default|GetDebugRight) (- (select (Game|Player|IsInputKeyDown :self pc :Key "D") 1.0 0.0) (select (Game|Player|IsInputKeyDown :self pc :Key "A") 1.0 0.0))))
 (if (Game|Player|IsInputKeyDown :self pc :Key "C") (Character|Crouch) (else (Character|UnCrouch)))
 (if (or (Variables|Default|GetRequestJump) (Game|Player|WasInputKeyJustPressed :self pc :Key "SpaceBar")) (Variables|Default|SetRequestJump false) (Character|Jump)))'''
blueprint_dsl.Transpiler(graph,create,BP.connect_pins,BP._get_node_info,BP.set_pin_value,lambda g:BP.find_nodes(g),delete_node_fn=BP.delete_node,find_node_types_fn=lambda f:BP.find_node_types(graph,f)).transpile(code)
BP.compile_blueprint(player,True);assert unreal.EditorAssetLibrary.save_loaded_asset(player)
factory=unreal.BlueprintFactory();factory.set_editor_property('parent_class',unreal.GameModeBase)
mode=T.create_asset('BP_TerrainGameMode',D+'/Blueprints',unreal.Blueprint,factory);BP.compile_blueprint(mode,True)
BP.get_default_object(mode).set_editor_property('default_pawn_class',player.generated_class());BP.compile_blueprint(mode,True);assert unreal.EditorAssetLibrary.save_loaded_asset(mode)
world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world();world.get_world_settings().set_editor_property('default_game_mode',mode.generated_class())
assert S.save_current_level()
(R/'reports/orison_terrain_composition.json').write_text(json.dumps(dict(map=MAP,placements=placements,player=player.get_path_name(),game_mode=mode.get_path_name(),landscape=True,gameplay_originals_preserved=True),indent=2))
print('ORISON_TERRAIN_ASSEMBLED',len(placements))
