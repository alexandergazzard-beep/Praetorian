"""Combine terrain, saved flora and accepted movement through Unreal editor APIs."""
import unreal,json,sys
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as BP
from editor_toolset.toolsets.scene import SceneTools
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from movement_profiles import PROFILES,ACTIVE_PROFILE
S=unreal.get_editor_subsystem(unreal.LevelEditorSubsystem);E=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
source='/Game/LostVanguard/Environment/OrisonTerrain/Maps/L_OrisonTerrain_Review'
MAP='/Game/LostVanguard/Environment/OrisonTerrain/Maps/L_Orison_Combined_Review'
assert S.save_current_level()
assert not unreal.EditorAssetLibrary.does_asset_exist(MAP)
assert S.new_level_from_template(MAP,source)
base='/Game/LostVanguard/Environment/OrisonTerrain/Blueprints/'
player=unreal.EditorAssetLibrary.duplicate_asset(base+'BP_TerrainPlayer',base+'BP_CombinedTerrainPlayer');assert player
mode=unreal.EditorAssetLibrary.duplicate_asset(base+'BP_TerrainGameMode',base+'BP_CombinedTerrainGameMode');assert mode
names={'MaxWalkSpeed':'max_walk_speed','MaxWalkSpeedCrouched':'max_walk_speed_crouched','MaxAcceleration':'max_acceleration','JumpZVelocity':'jump_z_velocity','GravityScale':'gravity_scale','AirControl':'air_control'}
for k,v in PROFILES[ACTIVE_PROFILE].items():BP.get_default_object(player).character_movement.set_editor_property(names[k],v)
BP.compile_blueprint(player,True);assert unreal.EditorAssetLibrary.save_loaded_asset(player)
BP.get_default_object(mode).set_editor_property('default_pawn_class',player.generated_class());BP.compile_blueprint(mode,True);assert unreal.EditorAssetLibrary.save_loaded_asset(mode)
unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world().get_world_settings().set_editor_property('default_game_mode',mode.generated_class())
rows=json.loads((R/'reports/combined_flora_import.json').read_text())['assets'];placed=[]
def height(x,y):
 d=SceneTools.trace_world(unreal.Vector(x,y,2000),unreal.Vector(x,y,-1000));assert d is not None
 return 2000-d
positions={'F13_Expansion71':[(-1900,-1900),(2050,1400)],'F14_Expansion71':[(2100,-1750),(-2300,1850)],'F16_Expansion71':[(-2100,300),(1800,2250)],'F19_Expansion71':[(-420,-1500),(550,-400),(-650,1500)],'F21_Expansion71':[(550,-1800),(-520,200),(650,1900)]}
for row in rows:
 for i,(x,y) in enumerate(positions[row['id']]):
  z=height(x,y);a=E.spawn_actor_from_class(unreal.StaticMeshActor,unreal.Vector(x,y,z));a.set_actor_label('Combined_'+row['id']+'_'+str(i));a.static_mesh_component.set_static_mesh(unreal.load_asset(row['mesh']));a.static_mesh_component.set_collision_profile_name('NoCollision');a.static_mesh_component.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION);a.set_actor_rotation(unreal.Rotator(0,i*117,0),False)
  placed.append({'id':row['id'],'location':[x,y,z]})
# Invisible trunk blockers on both the old and new trees; canopies remain clear.
traces=[]
for a in list(E.get_all_level_actors()):
 label=a.get_actor_label()
 if not (label.startswith('Terrain_Tree_') or any(label.startswith('Combined_'+k) for k in ['F13','F14','F16'])):continue
 a.static_mesh_component.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)
 loc=a.get_actor_location();b=E.spawn_actor_from_class(unreal.StaticMeshActor,unreal.Vector(loc.x,loc.y,loc.z+150));b.set_actor_label('Combined_Trunk_'+label);b.static_mesh_component.set_static_mesh(unreal.load_asset('/Engine/BasicShapes/Cube'));b.set_actor_scale3d(unreal.Vector(.65,.65,3));b.set_actor_hidden_in_game(True);b.static_mesh_component.set_visibility(False);b.static_mesh_component.set_collision_profile_name('BlockAll')
 d=SceneTools.trace_world(unreal.Vector(loc.x-150,loc.y,loc.z+160),unreal.Vector(loc.x+150,loc.y,loc.z+160));traces.append({'tree':label,'passed':d is not None,'distance':d})
assert all(t['passed'] for t in traces)
assert S.save_current_level();assert S.load_level(MAP)
(R/'reports/combined_orison_build.json').write_text(json.dumps({'map':MAP,'source_map':source,'new_plant_placements':placed,'trunk_checks':traces,'profile':PROFILES[ACTIVE_PROFILE],'player':player.get_path_name(),'strict_compile':True,'saved_reload':True},indent=2))
# Raise mission gates while preserving their objective-controlled actor/tag.
gates=[]
for m in ['/Game/WreckagePrototype/Maps/L_Wreckage_Playable','/Game/WreckagePrototype/Maps/L_Wreckage_Opening','/Game/LostVanguard/Environment/OpeningReview/Maps/L_ForestWreck_Review']:
 assert S.load_level(m)
 found=[a for a in E.get_all_level_actors() if a.get_actor_label()=='ExitGate']
 assert len(found)==1,m
 a=found[0];loc=a.get_actor_location();scale=a.get_actor_scale3d();bottom=loc.z-scale.z*50
 a.set_actor_location(unreal.Vector(loc.x,loc.y,bottom+225),False,False);a.set_actor_scale3d(unreal.Vector(scale.x,scale.y,4.5))
 assert S.save_current_level();gates.append({'map':m,'gate_top_cm':bottom+450,'tag_present':a.actor_has_tag('LV_ExitGate')})
(R/'reports/combined_gate_fix.json').write_text(json.dumps(gates,indent=2))
assert S.load_level(MAP)
print('COMBINED_ORISON_BUILD_COMPLETE')
