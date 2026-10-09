import unreal,json
from pathlib import Path
from editor_toolset.toolsets.scene import SceneTools
R=Path(__file__).resolve().parents[1];E=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);checks=[]
for i,row in enumerate(json.loads((R/'reports/orison_terrain_import.json').read_text())['assets']):
 a=E.spawn_actor_from_class(unreal.StaticMeshActor,unreal.Vector(10000+i*2000,0,500));a.static_mesh_component.set_static_mesh(unreal.load_asset(row['mesh']));a.static_mesh_component.set_collision_profile_name('BlockAll')
 origin,extent=a.get_actor_bounds(False);dist=SceneTools.trace_world(unreal.Vector(origin.x,origin.y,origin.z+extent.z+300),unreal.Vector(origin.x,origin.y,400))
 checks.append(dict(name=row['id']+' isolated collision trace',passed=dist is not None,distance=dist));E.destroy_actor(a)
for y in [-2300,-1000,0,1500,2500]:
 dist=SceneTools.trace_world(unreal.Vector(0,y,1000),unreal.Vector(0,y,-100));checks.append(dict(name='Landscape ground at y='+str(y),passed=dist is not None,distance=dist))
(R/'reports/orison_terrain_collision.json').write_text(json.dumps(checks,indent=2));assert all(c['passed'] for c in checks)
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level();print('ORISON_COLLISION_CHECKS',len(checks))
