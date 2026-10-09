"""Import new isolated sample assets through native Unreal editor APIs.

Run as a commandlet only while these new packages are not loaded in live editor.
Never writes original opening, gameplay assets or shared art.
"""
import unreal,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DEST='/Game/LostVanguard/Environment/OpeningReview/Assets'
tools=unreal.AssetToolsHelpers.get_asset_tools();lib=unreal.MaterialEditingLibrary
def imp(source,name,folder,options=None):
 existing=unreal.load_asset(folder+'/'+name)
 if existing and options is None:return existing
 task=unreal.AssetImportTask();task.filename=str(source);task.destination_path=folder;task.destination_name=name;task.automated=True;task.save=True;task.replace_existing=bool(existing)
 if options:task.options=options
 tools.import_asset_tasks([task]);assert task.imported_object_paths,str(source)
 result=unreal.load_asset(task.imported_object_paths[0]);target=folder+'/'+name
 if result.get_path_name().split('.')[0]!=target:
  assert unreal.EditorAssetLibrary.rename_asset(result.get_path_name(),target)
  result=unreal.load_asset(target)
 return result
materials={}
for name,rough,metal in [('Bark',.88,0),('Leaf',.68,0),('ArmorAtlas',.74,.5)]:
 tex=imp(ROOT/'assets/models/forest_wreck/textures'/f'T_{name}_BaseColor.png','T_'+name,DEST+'/Textures')
 tex.set_editor_property('srgb',True);tex.set_editor_property('max_texture_size',1024)
 mat=unreal.load_asset(DEST+'/Materials/M_'+name) or tools.create_asset('M_'+name,DEST+'/Materials',unreal.Material,unreal.MaterialFactoryNew())
 lib.delete_all_material_expressions(mat)
 sample=lib.create_material_expression(mat,unreal.MaterialExpressionTextureSample,-400,0);sample.set_editor_property('texture',tex)
 sample.set_editor_property('sampler_type',unreal.MaterialSamplerType.SAMPLERTYPE_COLOR)
 lib.connect_material_property(sample,'RGB',unreal.MaterialProperty.MP_BASE_COLOR)
 if name=='Leaf':
  mat.set_editor_property('two_sided',True)
 for val,prop,y in [(rough,unreal.MaterialProperty.MP_ROUGHNESS,180),(metal,unreal.MaterialProperty.MP_METALLIC,330)]:
  node=lib.create_material_expression(mat,unreal.MaterialExpressionConstant,-200,y);node.set_editor_property('r',val);lib.connect_material_property(node,'',prop)
 lib.recompile_material(mat)
 for asset in (tex,mat):assert unreal.EditorAssetLibrary.save_loaded_asset(asset)
 materials[name]=mat
result=[]
for item in json.loads((ROOT/'reports/forest_wreck_blender.json').read_text()):
 opt=unreal.FbxImportUI();opt.import_mesh=True;opt.import_materials=False;opt.import_textures=False;opt.import_as_skeletal=False
 opt.static_mesh_import_data.combine_meshes=True;opt.static_mesh_import_data.import_uniform_scale=1;opt.static_mesh_import_data.auto_generate_collision=False
 mesh=imp(item['export'],'SM_'+item['id'],DEST+'/Meshes',opt)
 for i,name in enumerate(item['materials']):mesh.set_material(i,materials[name])
 assert unreal.EditorAssetLibrary.save_loaded_asset(mesh)
 item.update({'mesh':mesh.get_path_name(),'imported':True,'bounds_cm':str(mesh.get_bounding_box()),'collision':'pending live editor','lods':'pending live editor'})
 result.append(item)
(ROOT/'reports/forest_wreck_unreal_import.json').write_text(json.dumps({'assets':result,'destination':DEST,'project_file':unreal.Paths.get_project_file_path(),'engine':unreal.SystemLibrary.get_engine_version()},indent=2))
print('FOREST_WRECK_IMPORT_COMPLETE',flush=True)
