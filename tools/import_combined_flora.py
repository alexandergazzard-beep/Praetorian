"""Author new selected wreck packages and an isolated inspection map through Unreal APIs."""
import unreal,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SPECS=json.loads((ROOT/'reports/flora_expansion71_specs.json').read_text())
DEST='/Game/LostVanguard/Environment/OpeningReview/Assets/FloraExpansion71'
MAP='/Game/LostVanguard/Environment/OpeningReview/Maps/L_Orison_Combined_Review'
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
assert not unreal.EditorAssetLibrary.does_asset_exist(DEST+'/M_FloraExpansion_PBR')
master=tools.create_asset('M_FloraExpansion_PBR',DEST,unreal.Material,unreal.MaterialFactoryNew());master.set_editor_property('two_sided',True);nodes={}
for i,(param,prop,sampler) in enumerate([
 ('BaseColor',unreal.MaterialProperty.MP_BASE_COLOR,unreal.MaterialSamplerType.SAMPLERTYPE_COLOR),
 ('Normal',unreal.MaterialProperty.MP_NORMAL,unreal.MaterialSamplerType.SAMPLERTYPE_NORMAL),
 ('Roughness',unreal.MaterialProperty.MP_ROUGHNESS,unreal.MaterialSamplerType.SAMPLERTYPE_LINEAR_COLOR),
 ('Metallic',unreal.MaterialProperty.MP_METALLIC,unreal.MaterialSamplerType.SAMPLERTYPE_LINEAR_COLOR)]):
 node=lib.create_material_expression(master,unreal.MaterialExpressionTextureSampleParameter2D,-400,i*180)
 node.set_editor_property('parameter_name',param);node.set_editor_property('sampler_type',sampler);nodes[param]=node
 assert lib.connect_material_property(node,'RGB' if i<2 else 'R',prop)
for asset in list(SPECS):
 base=ROOT/'assets/models/forest_wreck'/asset;folder=DEST+'/'+asset
 opt=unreal.FbxImportUI();opt.import_mesh=True;opt.import_materials=False;opt.import_textures=False;opt.import_as_skeletal=False
 opt.static_mesh_import_data.combine_meshes=True;opt.static_mesh_import_data.auto_generate_collision=False
 mesh=imp(base/'export'/('SM_'+asset+'.fbx'),'SM_'+asset,folder,opt)
 mat=tools.create_asset('MI_'+asset,folder,unreal.MaterialInstanceConstant,unreal.MaterialInstanceConstantFactoryNew());lib.set_material_instance_parent(mat,master)
 textures={}
 for param,file in [('BaseColor','base_color'),('Normal','normal'),('Roughness','roughness'),('Metallic','metallic')]:
  tex=imp(base/'source/meshy_original_textures'/(file+'.png'),'T_'+asset+'_'+param,folder)
  tex.set_editor_property('srgb',param=='BaseColor');tex.set_editor_property('max_texture_size',4096)
  if param=='Normal':tex.set_editor_property('compression_settings',unreal.TextureCompressionSettings.TC_NORMALMAP);tex.set_editor_property('flip_green_channel',True)
  elif param in ['Roughness','Metallic']:tex.set_editor_property('compression_settings',unreal.TextureCompressionSettings.TC_MASKS)
  lib.set_material_instance_texture_parameter_value(mat,param,tex);textures[param]=tex.get_path_name()
  if asset==next(iter(SPECS)):nodes[param].set_editor_property('texture',tex)
  assert unreal.EditorAssetLibrary.save_loaded_asset(tex)
 mesh.set_material(0,mat)
 lib.update_material_instance(mat)
 for item in [mesh,mat]:assert unreal.EditorAssetLibrary.save_loaded_asset(item)
 report.append({'id':asset,'mesh':mesh.get_path_name(),'material':mat.get_path_name(),'textures':textures,'bounds_cm':str(mesh.get_bounding_box())})
lib.recompile_material(master);assert unreal.EditorAssetLibrary.save_loaded_asset(master)

from editor_toolset.toolsets.static_mesh import StaticMeshTools as SM
for row in report:
 mesh=unreal.load_asset(row['mesh'])
 SM.generate_lods(mesh,[.5,.22,.08]);SM.set_lod_thresholds(mesh,[1,.4,.16,.06]);SM.set_nanite_enabled(mesh,False)
 row['triangles']=[SM.get_triangle_count(mesh,i) for i in range(SM.get_lod_count(mesh))]
 assert len(row['triangles'])==4 and all(a>b for a,b in zip(row['triangles'],row['triangles'][1:]))
 assert unreal.EditorAssetLibrary.save_loaded_asset(mesh)
(ROOT/'reports/combined_flora_import.json').write_text(json.dumps({'assets':report},indent=2))
print('COMBINED_FLORA_IMPORTED')
