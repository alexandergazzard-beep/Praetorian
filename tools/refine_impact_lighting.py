import unreal,json
from pathlib import Path
R=Path(__file__).resolve().parents[1];D='/Game/LostVanguard/Environment/SpaceImpact';L=unreal.MaterialEditingLibrary
mi=unreal.load_asset('/NiagaraFluids/Materials/Grid3D/Instances/MI_3DGas_Base')
params={str(n):L.get_material_instance_scalar_parameter_value(mi,n) for n in L.get_scalar_parameter_names(mi)}
(R/'reports/volume_material_parameters.json').write_text(json.dumps(params,indent=2))
sub=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
for a in sub.get_all_level_actors():
 label=a.get_actor_label()
 if label=='Impact_DuskRim':a.light_component.set_editor_property('intensity',30);a.light_component.set_light_color(unreal.LinearColor(.42,.54,.72,1))
 if label=='Impact_Sky':a.light_component.set_editor_property('intensity',2.5)
 if label=='Impact_Mist':
  c=a.get_component_by_class(unreal.ExponentialHeightFogComponent);c.set_editor_property('fog_density',.025);c.set_editor_property('fog_inscattering_luminance',unreal.LinearColor(.075,.105,.16,1))
 if label=='Impact_MetalSoftbox':a.light_component.set_editor_property('intensity',1900)
 if label.startswith('Impact_Firelight'):a.light_component.set_editor_property('intensity',220);a.light_component.set_editor_property('attenuation_radius',600)
unreal.EditorAssetLibrary.save_loaded_asset(unreal.load_asset(D+'/FX/NS_ImpactFireVolume'))
unreal.EditorAssetLibrary.save_loaded_asset(unreal.load_asset(D+'/FX/NS_ImpactEmbers'))
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
print('IMPACT_LIGHTING_REFINED',params,flush=True)
