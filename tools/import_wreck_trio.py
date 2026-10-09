"""Author new selected wreck packages and an isolated inspection map through Unreal APIs."""
import unreal,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DEST='/Game/LostVanguard/Environment/OpeningReview/Assets/WreckTrio'
MAP='/Game/LostVanguard/Environment/OpeningReview/Maps/L_Wreck_Trio_Inspection'
tools=unreal.AssetToolsHelpers.get_asset_tools();lib=unreal.MaterialEditingLibrary
levels=unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
report=[]
def imp(source,name,folder,options=None):
 assert not unreal.EditorAssetLibrary.does_asset_exist(folder+'/'+name),'New isolated packages only: '+name
 t=unreal.AssetImportTask();t.filename=str(source);t.destination_path=folder;t.destination_name=name;t.automated=True;t.save=True;t.replace_existing=False
 if options:t.options=options
 tools.import_asset_tasks([t]);assert t.imported_object_paths,str(source)
 result=unreal.load_asset(t.imported_object_paths[0]);target=folder+'/'+name
 if result.get_path_name().split('.')[0]!=target:
  assert unreal.EditorAssetLibrary.rename_asset(result.get_path_name(),target);result=unreal.load_asset(target)
 return result
assert not unreal.EditorAssetLibrary.does_asset_exist(MAP),'Do not overwrite existing inspection map'
assert not unreal.EditorAssetLibrary.does_asset_exist(DEST+'/M_WreckTrio_PBR')
master=tools.create_asset('M_WreckTrio_PBR',DEST,unreal.Material,unreal.MaterialFactoryNew());nodes={}
for i,(param,prop,sampler) in enumerate([
 ('BaseColor',unreal.MaterialProperty.MP_BASE_COLOR,unreal.MaterialSamplerType.SAMPLERTYPE_COLOR),
 ('Normal',unreal.MaterialProperty.MP_NORMAL,unreal.MaterialSamplerType.SAMPLERTYPE_NORMAL),
 ('Roughness',unreal.MaterialProperty.MP_ROUGHNESS,unreal.MaterialSamplerType.SAMPLERTYPE_LINEAR_COLOR),
 ('Metallic',unreal.MaterialProperty.MP_METALLIC,unreal.MaterialSamplerType.SAMPLERTYPE_LINEAR_COLOR)]):
 node=lib.create_material_expression(master,unreal.MaterialExpressionTextureSampleParameter2D,-400,i*180)
 node.set_editor_property('parameter_name',param);node.set_editor_property('sampler_type',sampler);nodes[param]=node
 assert lib.connect_material_property(node,'RGB' if i<2 else 'R',prop)
for asset in ['Medium_WreckPanel','Large_WreckModule','Engine_MeshyNacelle']:
 base=ROOT/'assets/models/forest_wreck'/asset;folder=DEST+'/'+asset
 opt=unreal.FbxImportUI();opt.import_mesh=True;opt.import_materials=False;opt.import_textures=False;opt.import_as_skeletal=False
 opt.static_mesh_import_data.combine_meshes=True;opt.static_mesh_import_data.auto_generate_collision=False
 mesh=imp(base/'export'/('SM_'+asset+'.fbx'),'SM_'+asset,folder,opt)
 mat=tools.create_asset('MI_'+asset,folder,unreal.MaterialInstanceConstant,unreal.MaterialInstanceConstantFactoryNew());lib.set_material_instance_parent(mat,master)
 textures={}
 for param,file in [('BaseColor','base_color'),('Normal','normal'),('Roughness','roughness'),('Metallic','metallic')]:
  tex=imp(base/'source/meshy_original_textures'/(file+'.png'),'T_'+asset+'_'+param,folder)
  tex.set_editor_property('srgb',param=='BaseColor');tex.set_editor_property('max_texture_size',2048)
  if param=='Normal':tex.set_editor_property('compression_settings',unreal.TextureCompressionSettings.TC_NORMALMAP);tex.set_editor_property('flip_green_channel',True)
  elif param in ['Roughness','Metallic']:tex.set_editor_property('compression_settings',unreal.TextureCompressionSettings.TC_MASKS)
  lib.set_material_instance_texture_parameter_value(mat,param,tex);textures[param]=tex.get_path_name()
  if asset=='Medium_WreckPanel':nodes[param].set_editor_property('texture',tex)
  assert unreal.EditorAssetLibrary.save_loaded_asset(tex)
 mesh.set_material(0,mat);lib.update_material_instance(mat)
 for item in [mesh,mat]:assert unreal.EditorAssetLibrary.save_loaded_asset(item)
 report.append({'id':asset,'mesh':mesh.get_path_name(),'material':mat.get_path_name(),'textures':textures,'bounds_cm':str(mesh.get_bounding_box())})
lib.recompile_material(master);assert unreal.EditorAssetLibrary.save_loaded_asset(master)
assert levels.new_level(MAP)
def spawn(cls,name,location,rotation=None):
 a=actors.spawn_actor_from_class(cls,unreal.Vector(*location),unreal.Rotator(*(rotation or (0,0,0))));a.set_actor_label(name);return a
floor=spawn(unreal.StaticMeshActor,'WreckTrio_Ground',(0,0,-20));floor.static_mesh_component.set_static_mesh(unreal.load_asset('/Engine/BasicShapes/Cube'));floor.set_actor_scale3d(unreal.Vector(70,80,.4));floor.static_mesh_component.set_collision_profile_name('BlockAll')
for item,pos in zip(report,[(-1500,0,0),(0,0,0),(1800,0,0)]):
 a=spawn(unreal.StaticMeshActor,'WreckTrio_'+item['id'],pos);a.static_mesh_component.set_static_mesh(unreal.load_asset(item['mesh']));a.static_mesh_component.set_collision_profile_name('BlockAll');a.static_mesh_component.set_collision_enabled(unreal.CollisionEnabled.QUERY_AND_PHYSICS)
 item['actor']=a.get_path_name();item['location_cm']=list(pos)
spawn(unreal.SkyAtmosphere,'WreckTrio_Atmosphere',(0,0,0))
sun=spawn(unreal.DirectionalLight,'WreckTrio_Sun',(0,0,1800),(-45,-50,0));sun.light_component.set_editor_property('intensity',4);sun.light_component.set_editor_property('atmosphere_sun_light',True)
sky=spawn(unreal.SkyLight,'WreckTrio_Sky',(0,0,1500));sky.light_component.set_editor_property('real_time_capture',True);sky.light_component.set_editor_property('intensity',1.5)
fill=spawn(unreal.RectLight,'WreckTrio_Fill',(0,-2500,1000),(-15,90,0));fill.light_component.set_editor_property('intensity',1500);fill.light_component.set_editor_property('attenuation_radius',9000);fill.light_component.set_editor_property('source_width',5000);fill.light_component.set_editor_property('source_height',1500)
start=spawn(unreal.PlayerStart,'WreckTrio_PlayerStart',(0,-1800,100),(0,90,0))
assert levels.save_current_level()
(ROOT/'reports/wreck_trio_unreal_import.json').write_text(json.dumps({'map':MAP,'assets':report,'project':unreal.Paths.get_project_file_path(),'engine':unreal.SystemLibrary.get_engine_version(),'original_and_review_maps_untouched':True,'visual_acceptance':'pending live inspection','lods_collision':'pending native live setup'},indent=2))
print('WRECK_TRIO_IMPORT_COMPLETE',flush=True)
