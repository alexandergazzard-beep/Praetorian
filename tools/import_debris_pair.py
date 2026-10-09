"""Native Unreal editor asset authoring; new debris assets only, no level writes."""
import unreal,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DEST='/Game/LostVanguard/Art/Debris/FirstPair'
tools=unreal.AssetToolsHelpers.get_asset_tools()
lib=unreal.MaterialEditingLibrary
report=[]
def import_asset(source,name,folder,options=None):
    existing=unreal.load_asset(folder+'/'+name)
    if existing:return existing
    t=unreal.AssetImportTask();t.filename=str(source);t.destination_path=folder;t.destination_name=name;t.automated=True;t.save=True;t.replace_existing=False
    if options:t.options=options
    tools.import_asset_tasks([t])
    assert t.imported_object_paths,str(source)
    result=unreal.load_asset(t.imported_object_paths[0])
    target=folder+'/'+name
    if result.get_path_name().split('.')[0]!=target:
        assert unreal.EditorAssetLibrary.rename_asset(result.get_path_name(),target)
        result=unreal.load_asset(target)
    return result
master=unreal.load_asset(DEST+'/M_Debris_PBR') or tools.create_asset('M_Debris_PBR',DEST,unreal.Material,unreal.MaterialFactoryNew())
lib.delete_all_material_expressions(master)
nodes={}
for index,(param,prop,sampler) in enumerate([
    ('BaseColor',unreal.MaterialProperty.MP_BASE_COLOR,unreal.MaterialSamplerType.SAMPLERTYPE_COLOR),
    ('Normal',unreal.MaterialProperty.MP_NORMAL,unreal.MaterialSamplerType.SAMPLERTYPE_NORMAL),
    ('Roughness',unreal.MaterialProperty.MP_ROUGHNESS,unreal.MaterialSamplerType.SAMPLERTYPE_LINEAR_COLOR),
    ('Metallic',unreal.MaterialProperty.MP_METALLIC,unreal.MaterialSamplerType.SAMPLERTYPE_LINEAR_COLOR)]):
    n=lib.create_material_expression(master,unreal.MaterialExpressionTextureSampleParameter2D,-400,index*180)
    n.set_editor_property('parameter_name',param)
    n.set_editor_property('sampler_type',sampler)
    nodes[param]=n
    assert lib.connect_material_property(n,'RGB' if index<2 else 'R',prop)
for asset in ['M17_supply_trunk','S04_vent_grille']:
    base=ROOT/'assets/models/debris'/asset;folder=DEST+'/'+asset
    opt=unreal.FbxImportUI();opt.import_mesh=True;opt.import_materials=False;opt.import_textures=False;opt.import_as_skeletal=False
    opt.static_mesh_import_data.combine_meshes=True;opt.static_mesh_import_data.import_uniform_scale=1
    opt.static_mesh_import_data.auto_generate_collision=False
    mesh=import_asset(base/'export'/('SM_'+asset+'.fbx'),'SM_'+asset,folder,opt)
    material=unreal.load_asset(folder+'/MI_'+asset) or tools.create_asset('MI_'+asset,folder,unreal.MaterialInstanceConstant,unreal.MaterialInstanceConstantFactoryNew())
    lib.set_material_instance_parent(material,master)
    textures={}
    for param,file in [('BaseColor','base_color'),('Normal','normal'),('Roughness','roughness'),('Metallic','metallic')]:
        tex=import_asset(base/'source/meshy_original_textures'/(file+'.png'),'T_'+asset+'_'+param,folder)
        tex.set_editor_property('srgb',param=='BaseColor')
        if param=='Normal':
            tex.set_editor_property('compression_settings',unreal.TextureCompressionSettings.TC_NORMALMAP)
            tex.set_editor_property('flip_green_channel',True)
        elif param in ['Roughness','Metallic']:tex.set_editor_property('compression_settings',unreal.TextureCompressionSettings.TC_MASKS)
        tex.set_editor_property('max_texture_size',2048 if asset.startswith('M17') else 1024)
        lib.set_material_instance_texture_parameter_value(material,param,tex)
        textures[param]=tex.get_path_name();unreal.EditorAssetLibrary.save_loaded_asset(tex)
        # Give the master valid defaults before compiling its texture parameters.
        if asset.startswith('M17'):
            nodes[param].set_editor_property('texture',tex)
    mesh.set_material(0,material)
    lib.update_material_instance(material)
    for a in [mesh,material]:assert unreal.EditorAssetLibrary.save_loaded_asset(a)
    report.append({'id':asset,'mesh':mesh.get_path_name(),'material':material.get_path_name(),'textures':textures,'collision_and_lods':'pending live editor setup','bounds_cm':str(mesh.get_bounding_box())})
lib.recompile_material(master)
assert unreal.EditorAssetLibrary.save_loaded_asset(master)
(ROOT/'reports/debris_pair_unreal_import.json').write_text(json.dumps(report,indent=2))
print('DEBRIS_IMPORT_COMPLETE',json.dumps(report))
