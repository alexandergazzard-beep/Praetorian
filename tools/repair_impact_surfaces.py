"""Repair unstable presentation materials; writes only owned scene packages."""
import unreal,json
from pathlib import Path
from editor_toolset.toolsets.material import MaterialTools as MT
ROOT=Path(__file__).resolve().parents[1];D='/Game/LostVanguard/Environment/SpaceImpact';L=unreal.MaterialEditingLibrary
tex=unreal.load_asset(D+'/Textures/T_ImpactSoil');before={k:str(tex.get_editor_property(k)) for k in ['compression_settings','mip_gen_settings','filter','srgb']}
tex.set_editor_property('compression_settings',unreal.TextureCompressionSettings.TC_DEFAULT);tex.set_editor_property('mip_gen_settings',unreal.TextureMipGenSettings.TMGS_FROM_TEXTURE_GROUP);tex.set_editor_property('filter',unreal.TextureFilter.TF_DEFAULT);tex.set_editor_property('lod_group',unreal.TextureGroup.TEXTUREGROUP_WORLD);tex.set_editor_property('srgb',True);assert unreal.EditorAssetLibrary.save_loaded_asset(tex)
for name in ['M_CharredDampSoil','M_ImpactStone']:
 m=unreal.load_asset(D+'/Materials/'+name)
 flat=L.create_material_expression(m,unreal.MaterialExpressionConstant3Vector);flat.set_editor_property('constant',unreal.LinearColor(0,0,1,1));assert L.connect_material_property(flat,'',unreal.MaterialProperty.MP_NORMAL)
 for ex in MT.get_expressions(m):
  if isinstance(ex,unreal.MaterialExpressionTextureSample):ex.set_editor_property('sampler_type',unreal.MaterialSamplerType.SAMPLERTYPE_COLOR)
 MT.delete_unused_expressions(m);L.recompile_material(m);assert unreal.EditorAssetLibrary.save_loaded_asset(m)
# Hide old refractive cards until the revised fire passes the moving-camera test.
actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
for a in actors.get_all_level_actors():
 label=a.get_actor_label()
 if label.startswith('Impact_Heat'):a.static_mesh_component.set_visibility(False);a.set_actor_hidden_in_game(True)
 if label=='Impact_MetalSoftbox':a.light_component.set_editor_property('intensity',3200);a.light_component.set_editor_property('source_width',1600);a.light_component.set_editor_property('source_height',1200)
 if label=='Impact_Mist':
  f=a.get_component_by_class(unreal.ExponentialHeightFogComponent);f.set_editor_property('fog_density',.017);f.set_editor_property('fog_height_falloff',.2)
assert unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
(ROOT/'reports/space_impact_surface_repair.json').write_text(json.dumps({'before':before,'ground_mips_fixed':True,'camera_dependent_normal_removed':True,'user_rejected_previous_visual_quality':True},indent=2));print('IMPACT_SURFACES_REPAIRED',flush=True)
