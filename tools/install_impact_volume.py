import unreal,json
from pathlib import Path
R=Path(__file__).resolve().parents[1];D='/Game/LostVanguard/Environment/SpaceImpact'
sub=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
fire=unreal.load_asset(D+'/FX/NS_ImpactFireVolume');embers=unreal.load_asset(D+'/FX/NS_ImpactEmbers')
assert fire and embers
for a in sub.get_all_level_actors():
 label=a.get_actor_label()
 if label.startswith('Impact_Burn_'):
  c=a.get_component_by_class(unreal.NiagaraComponent);c.set_asset(embers)
 if label.startswith('Impact_VolumeFire_'):sub.destroy_actor(a)
for i,(x,y,z,res) in enumerate([(-450,-210,-45,112),(440,-110,0,80),(720,380,-25,80)]):
 a=sub.spawn_actor_from_class(unreal.NiagaraActor,unreal.Vector(x,y,z));a.set_actor_label('Impact_VolumeFire_'+str(i));a.set_folder_path('SpaceImpact/FX')
 c=a.get_component_by_class(unreal.NiagaraComponent);c.set_asset(fire);c.set_variable_int('User.ResolutionMaxAxis',res);c.set_variable_bool('User.DrawBounds',False);c.set_variable_vec3('User.WorldSpaceSize',unreal.Vector(240,240,450));c.set_editor_property('auto_activate',True);c.activate(True)
unreal.EditorAssetLibrary.save_loaded_asset(fire);unreal.EditorAssetLibrary.save_loaded_asset(embers)
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
print('IMPACT_VOLUME_INSTALLED',flush=True)
