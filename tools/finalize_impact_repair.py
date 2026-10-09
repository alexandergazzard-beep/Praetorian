import unreal,json
from pathlib import Path
R=Path(__file__).resolve().parents[1];D='/Game/LostVanguard/Environment/SpaceImpact';L=unreal.MaterialEditingLibrary
for a in unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors():
 if not a.get_actor_label().startswith('Impact_'):continue
 for c in a.get_components_by_class(unreal.LightComponentBase):c.set_mobility(unreal.ComponentMobility.MOVABLE)
 if a.get_actor_label()=='Impact_DuskRim':a.light_component.set_editor_property('intensity',12)
for name in ['M_WindPBR','M_WindLeaf']:
 m=unreal.load_asset(D+'/Materials/'+name)
 metal=L.create_material_expression(m,unreal.MaterialExpressionConstant);metal.set_editor_property('r',0);L.connect_material_property(metal,'',unreal.MaterialProperty.MP_METALLIC)
 rough=L.create_material_expression(m,unreal.MaterialExpressionConstant);rough.set_editor_property('r',.78);L.connect_material_property(rough,'',unreal.MaterialProperty.MP_ROUGHNESS)
 L.recompile_material(m);unreal.EditorAssetLibrary.save_loaded_asset(m)
for p in ['NS_ImpactFireVolume','NS_ImpactEmbers']:unreal.EditorAssetLibrary.save_loaded_asset(unreal.load_asset(D+'/FX/'+p))
assert unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
print('IMPACT_REPAIR_SAVED',flush=True)
