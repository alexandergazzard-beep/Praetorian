"""Final isolated scene polish via native editor APIs; preserves shared originals."""
import unreal,json
from pathlib import Path
from editor_toolset.toolsets.material import MaterialTools as MT
ROOT=Path(__file__).resolve().parents[1];D='/Game/LostVanguard/Environment/SpaceImpact';L=unreal.MaterialEditingLibrary;E=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
for name in ['M_EntryScarredMetal','M_CharredDampSoil','M_WindPBR','M_HeatHaze']:
 m=unreal.load_asset(D+'/Materials/'+name)
 for ex in MT.get_expressions(m):
  if isinstance(ex,unreal.MaterialExpressionCustom):
   code=ex.get_editor_property('code')
   if name=='M_EntryScarredMetal':code=code.replace(')),35)*.14', ')),35)*.025').replace('streak*.12','streak*.035')
   if name=='M_CharredDampSoil':code=code.replace('lerp(.7,.18,burn)','lerp(.4,.12,burn)')
   if name=='M_WindPBR':code=code.replace('h/650','h/260')
   ex.set_editor_property('code',code)
 L.recompile_material(m);assert unreal.EditorAssetLibrary.save_loaded_asset(m)
for a in E.get_all_level_actors():
 label=a.get_actor_label()
 if label=='Impact_MetalSoftbox':a.light_component.set_editor_property('intensity',5000)
 if label=='Impact_CinematicCamera':
  a.set_actor_location_and_rotation(unreal.Vector(-1350,-2000,340),unreal.Rotator(pitch=-1,yaw=57,roll=0),False,False);a.get_cine_camera_component().set_editor_property('current_focal_length',30)
 if label=='Impact_Grade':
  s=a.get_editor_property('settings');s.set_editor_property('auto_exposure_bias',-1.3);a.set_editor_property('settings',s)
 if label.startswith('Impact_Heat'):a.set_actor_hidden_in_game(False)
assert unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
report=json.loads((ROOT/'reports/space_impact_build.json').read_text());report.update(camera_cm=[-1350,-2000,340],camera_rotation_degrees=[-1,57,0],effects='Three infinite Niagara systems: fire/smoke/sparks; shader wind, flickering coals/firelight, pixel-normal heat refraction',new_stone_meshes=3)
(ROOT/'reports/space_impact_build.json').write_text(json.dumps(report,indent=2));print('SPACE_IMPACT_POLISHED',flush=True)
