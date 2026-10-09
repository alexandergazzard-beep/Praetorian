"""Use native component methods because reflected BodyInstance edits reset collision flags."""
import unreal,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
mesh=unreal.load_asset('/Game/LostVanguard/Environment/OpeningReview/Assets/F01_HybridCanopy/SM_F01_HybridCanopy')
assert mesh
levels=unreal.get_editor_subsystem(unreal.LevelEditorSubsystem);actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
report=[]
for level in ['/Game/LostVanguard/Environment/OpeningReview/Maps/L_ForestWreck_Inspection','/Game/LostVanguard/Environment/OpeningReview/Maps/L_ForestWreck_Review']:
 assert levels.load_level(level)
 trees=[a for a in actors.get_all_level_actors() if a.get_actor_label().startswith('FWR_F01')];assert len(trees)==1
 tree=trees[0];comp=tree.static_mesh_component;comp.set_static_mesh(mesh)
 comp.set_collision_profile_name('NoCollision');comp.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)
 boxes=tree.get_components_by_class(unreal.BoxComponent);assert len(boxes)==1
 box=boxes[0];box.set_collision_profile_name('BlockAll');box.set_collision_enabled(unreal.CollisionEnabled.QUERY_AND_PHYSICS)
 if level.endswith('_Review'):
  for old in actors.get_all_level_actors():
   if old.get_actor_label() in ['OV_TreeTrunk_0','OV_Canopy_0_0','OV_Canopy_0_1','OV_Canopy_0_2']:
    old.set_actor_hidden_in_game(True)
    for old_comp in old.get_components_by_class(unreal.PrimitiveComponent):
     old_comp.set_visibility(False);old_comp.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)
 if level.endswith('_Inspection'):
  if not any(a.get_actor_label()=='Inspection_Atmosphere' for a in actors.get_all_level_actors()):
   atmosphere=actors.spawn_actor_from_class(unreal.SkyAtmosphere,unreal.Vector(0,0,0));atmosphere.set_actor_label('Inspection_Atmosphere')
  for lighting in actors.get_all_level_actors():
   if lighting.get_actor_label()=='Inspection_SoftFill':lighting.light_component.set_editor_property('intensity',250)
   if lighting.get_actor_label()=='Inspection_Sun':lighting.light_component.set_editor_property('atmosphere_sun_light',True)
   if lighting.get_actor_label()=='Inspection_Sky':lighting.light_component.set_editor_property('real_time_capture',True)
   if lighting.get_actor_label()=='Inspection_Exposure':
    settings=lighting.get_editor_property('settings');settings.set_editor_property('auto_exposure_bias',0);lighting.set_editor_property('settings',settings)
 assert levels.save_current_level()
 report.append({'map':level,'tree_actor':tree.get_actor_label(),'mesh_collision':str(comp.get_collision_enabled()),'trunk_collision':str(box.get_collision_enabled())})
(ROOT/'reports/f01_native_collision_fix.json').write_text(json.dumps(report,indent=2));print('NATIVE_F01_COLLISION_FIX_COMPLETE',json.dumps(report))
