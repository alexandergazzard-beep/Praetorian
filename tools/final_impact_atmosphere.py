import unreal
from editor_toolset.toolsets.material import MaterialTools as MT
D='/Game/LostVanguard/Environment/SpaceImpact';m=unreal.load_asset(D+'/Materials/M_HeatHaze')
for ex in MT.get_expressions(m):
 if isinstance(ex,unreal.MaterialExpressionConstant) and abs(ex.get_editor_property('r')-1.025)<.001:ex.set_editor_property('r',1.003)
 if isinstance(ex,unreal.MaterialExpressionCustom):ex.set_editor_property('code',ex.get_editor_property('code').replace(')*.1;',')*.035;').replace('*.12','*.06'))
unreal.MaterialEditingLibrary.recompile_material(m);unreal.EditorAssetLibrary.save_loaded_asset(m)
ground=unreal.load_asset(D+'/Materials/M_CharredDampSoil')
for ex in MT.get_expressions(ground):
 if isinstance(ex,unreal.MaterialExpressionCustom):
  code=ex.get_editor_property('code')
  if 'return B*lerp(' in code:ex.set_editor_property('code',code.replace('return B*lerp(', 'B=lerp(B,float3(.055,.047,.035),smoothstep(1600,3400,length(P.xy))); return B*lerp('))
unreal.MaterialEditingLibrary.recompile_material(ground);unreal.EditorAssetLibrary.save_loaded_asset(ground)
for a in unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors():
 if a.get_actor_label()=='Impact_Mist':
  f=a.get_component_by_class(unreal.ExponentialHeightFogComponent);f.set_editor_property('fog_density',.035);f.set_editor_property('fog_height_falloff',.12);f.set_editor_property('fog_max_opacity',.65);f.set_editor_property('fog_inscattering_luminance',unreal.LinearColor(.028,.042,.068,1))
assert unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level();print('IMPACT_ATMOSPHERE_FINAL',flush=True)
