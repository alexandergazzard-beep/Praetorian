"""Connect the compiled runtime assets and tune the authored prototype map."""
import json
from pathlib import Path
import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as BP
ROOT='/Game/WreckagePrototype'
MAP=ROOT+'/Maps/L_Wreckage_Playable'
levels=unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
if not unreal.EditorAssetLibrary.does_asset_exist(MAP):
    assert unreal.EditorAssetLibrary.duplicate_asset(ROOT+'/Maps/L_Wreckage',MAP)
assert levels.load_level(MAP)
actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
for actor in actors.get_all_level_actors():
    label=actor.get_actor_label()
    if label=='DamagedPanel':actor.set_editor_property('tags',[unreal.Name('LV_Debris')])
    if label=='ExitGate':actor.set_editor_property('tags',[unreal.Name('LV_ExitGate')])
    if label=='Break_SafetyFloor':actor.set_actor_location(unreal.Vector(1150,0,-100),False,False)
    if isinstance(actor,unreal.PointLight):
        actor.point_light_component.set_editor_property('intensity',30)
    if isinstance(actor,unreal.SkyLight):
        actor.light_component.set_editor_property('intensity',.7)
    if label=='Sun':actor.light_component.set_editor_property('intensity',1.5)
    if isinstance(actor,unreal.Light):
        assert unreal.ToolsetLibrary.set_object_properties(actor.light_component,'{"Mobility":"Movable"}')
mode=unreal.load_asset(ROOT+'/Blueprints/BP_WreckageGameMode_Runtime') or BP.create(ROOT+'/Blueprints','BP_WreckageGameMode_Runtime',unreal.GameModeBase.static_class())
player=unreal.load_asset(ROOT+'/Blueprints/BP_WreckagePlayer_Runtime')
enemy=unreal.load_asset(ROOT+'/Blueprints/BP_SearcherPlaceholder_Runtime')
for bp in [player,enemy,mode]:BP.compile_blueprint(bp,True)
# Character capsule presets normally ignore visibility traces; this prototype
# uses those traces for searcher fire, so the player capsule must block them.
BP.get_default_object(player).capsule_component.set_collision_profile_name('BlockAllDynamic')
assert unreal.EditorAssetLibrary.save_loaded_asset(player)
BP.get_default_object(mode).set_editor_property('default_pawn_class',player.generated_class())
hud=unreal.load_asset(ROOT+'/Blueprints/BP_WreckageHUD')
BP.compile_blueprint(hud,True)
BP.get_default_object(mode).set_editor_property('hud_class',hud.generated_class())
unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world().get_world_settings().set_editor_property('default_game_mode',mode.generated_class())
assert unreal.EditorAssetLibrary.save_loaded_asset(mode)
assert levels.save_current_level()
Path(unreal.Paths.project_saved_dir(),'wreckage_final_map.json').write_text(json.dumps({'map':MAP,'game_mode':mode.get_path_name(),'player':player.get_path_name(),'compiled':True,'actor_count':len(actors.get_all_level_actors())},indent=2))
