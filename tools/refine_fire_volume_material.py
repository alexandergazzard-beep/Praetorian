import unreal
D='/Game/LostVanguard/Environment/SpaceImpact';p=D+'/Materials/MI_ImpactFireVolume'
mi=unreal.load_asset(p)
if not mi:mi=unreal.EditorAssetLibrary.duplicate_asset('/NiagaraFluids/Materials/Grid3D/Instances/MI_3DGas_Base',p)
unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(mi,'FireGain',.08)
unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(mi,'Albedo',.35)
unreal.EditorAssetLibrary.save_loaded_asset(mi)
print('VOLUME_MATERIAL_REFINED',flush=True)
