"""Native commandlet import into new isolated packages; no map/shared asset edits."""
import unreal,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'assets/models/forest_wreck/F01_HybridCanopy'
DEST='/Game/LostVanguard/Environment/OpeningReview/Assets/F01_HybridCanopy'
tools=unreal.AssetToolsHelpers.get_asset_tools();lib=unreal.MaterialEditingLibrary
def imp(file,name,options=None):
 existing=unreal.load_asset(DEST+'/'+name)
 if existing:return existing
 task=unreal.AssetImportTask();task.filename=str(file);task.destination_path=DEST;task.destination_name=name;task.automated=True;task.save=True;task.replace_existing=False
 if options:task.options=options
 tools.import_asset_tasks([task]);assert task.imported_object_paths,str(file)
 return unreal.load_asset(task.imported_object_paths[0])
def make(name):
 assert not unreal.EditorAssetLibrary.does_asset_exist(DEST+'/'+name),'Preserve existing authored packages; do not rerun importer'
 return tools.create_asset(name,DEST,unreal.Material,unreal.MaterialFactoryNew())
def expr(mat,cls,x=0,y=0):return lib.create_material_expression(mat,cls,x,y)
wood=make('M_F01_WoodPBR');textures={}
for i,(param,file,prop,sampler) in enumerate([
 ('BaseColor','base_color',unreal.MaterialProperty.MP_BASE_COLOR,unreal.MaterialSamplerType.SAMPLERTYPE_COLOR),
 ('Normal','normal',unreal.MaterialProperty.MP_NORMAL,unreal.MaterialSamplerType.SAMPLERTYPE_NORMAL),
 ('Roughness','roughness',unreal.MaterialProperty.MP_ROUGHNESS,unreal.MaterialSamplerType.SAMPLERTYPE_LINEAR_COLOR),
 ('Metallic','metallic',unreal.MaterialProperty.MP_METALLIC,unreal.MaterialSamplerType.SAMPLERTYPE_LINEAR_COLOR)]):
 tex=imp(ROOT/'assets/models/forest_wreck/F01_MeshyCanopy/source/meshy_original_textures'/f'{file}.png','T_F01_Wood_'+param)
 tex.set_editor_property('srgb',param=='BaseColor');tex.set_editor_property('max_texture_size',2048)
 if param=='Normal':tex.set_editor_property('compression_settings',unreal.TextureCompressionSettings.TC_NORMALMAP);tex.set_editor_property('flip_green_channel',True)
 elif param in ('Roughness','Metallic'):tex.set_editor_property('compression_settings',unreal.TextureCompressionSettings.TC_MASKS)
 node=expr(wood,unreal.MaterialExpressionTextureSample,-400,i*180);node.set_editor_property('texture',tex);node.set_editor_property('sampler_type',sampler)
 assert lib.connect_material_property(node,'RGB' if i<2 else 'R',prop)
 assert unreal.EditorAssetLibrary.save_loaded_asset(tex);textures[param]=tex.get_path_name()
leaf=make('M_F01_TaperedLeaf');leaf.set_editor_property('two_sided',True)
tex=imp(ROOT/'assets/models/forest_wreck/textures/T_Leaf_BaseColor.png','T_F01_Leaf_BaseColor')
sample=expr(leaf,unreal.MaterialExpressionTextureSample,-600,0);sample.set_editor_property('texture',tex);sample.set_editor_property('sampler_type',unreal.MaterialSamplerType.SAMPLERTYPE_COLOR)
back=expr(leaf,unreal.MaterialExpressionConstant3Vector,-600,180);back.set_editor_property('constant',unreal.LinearColor(.038,.023,.053,1))
sign=expr(leaf,unreal.MaterialExpressionTwoSidedSign,-600,350);clamp=expr(leaf,unreal.MaterialExpressionClamp,-400,350);clamp.set_editor_property('min_default',0);clamp.set_editor_property('max_default',1)
mix=expr(leaf,unreal.MaterialExpressionLinearInterpolate,-150,0)
for src,out,dst,input in [(sign,'',clamp,'Input'),(clamp,'',mix,'Alpha'),(back,'',mix,'A'),(sample,'RGB',mix,'B')]:
 if hasattr(lib,'get_material_expression_input_names'):print('MATERIAL_INPUTS',dst.get_class().get_name(),list(lib.get_material_expression_input_names(dst)))
 connected=lib.connect_material_expressions(src,out,dst,input)
 if not connected and dst==clamp:connected=lib.connect_material_expressions(src,out,dst,'')
 assert connected,str((src.get_class().get_name(),out,dst.get_class().get_name(),input))
assert lib.connect_material_property(mix,'',unreal.MaterialProperty.MP_BASE_COLOR)
rough=expr(leaf,unreal.MaterialExpressionConstant,-150,200);rough.set_editor_property('r',.78);assert lib.connect_material_property(rough,'',unreal.MaterialProperty.MP_ROUGHNESS)
opt=unreal.FbxImportUI();opt.import_mesh=True;opt.import_materials=False;opt.import_textures=False;opt.import_as_skeletal=False
opt.static_mesh_import_data.combine_meshes=True;opt.static_mesh_import_data.auto_generate_collision=False
mesh=imp(BASE/'export/SM_F01_HybridCanopy.fbx','SM_F01_HybridCanopy',opt)
mesh.set_material(0,wood);mesh.set_material(1,leaf)
for mat in (wood,leaf):lib.recompile_material(mat)
for asset in (wood,leaf,tex,mesh):assert unreal.EditorAssetLibrary.save_loaded_asset(asset)
report={'mesh':mesh.get_path_name(),'materials':[wood.get_path_name(),leaf.get_path_name()],'textures':textures,'bounds_cm':str(mesh.get_bounding_box()),'project':unreal.Paths.get_project_file_path(),'engine':unreal.SystemLibrary.get_engine_version(),'imported':True,'integrated':False,'visual_acceptance':'pending Unreal inspection'}
(ROOT/'reports/f01_hybrid_unreal_import.json').write_text(json.dumps(report,indent=2));print('F01_HYBRID_IMPORT_COMPLETE',json.dumps(report))
