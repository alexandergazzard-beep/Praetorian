import unreal,json
from pathlib import Path
from editor_toolset.toolsets.static_mesh import StaticMeshTools as SM
R=Path(__file__).resolve().parents[1];D='/Game/LostVanguard/Environment/OrisonTerrain'
E=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
data={'assets':[],'landscape':[]}
for row in json.loads((R/'reports/orison_terrain_import.json').read_text())['assets']:
 m=unreal.load_asset(row['mesh']);assert m
 body=m.get_editor_property('body_setup');hulls=len(body.get_editor_property('agg_geom').get_editor_property('convex_elems'))
 counts=[SM.get_triangle_count(m,i) for i in range(SM.get_lod_count(m))]
 assert len(counts)==4 and all(a>b for a,b in zip(counts,counts[1:])) and hulls>0
 assert unreal.EditorAssetLibrary.save_loaded_asset(m)
 data['assets'].append(dict(id=row['id'],triangles=counts,convex_hulls=hulls))
for a in E.get_all_level_actors():
 if isinstance(a,unreal.Landscape):
  data['landscape'].append(dict(label=a.get_actor_label(),scale=list(a.get_actor_scale3d().to_tuple()),material=a.get_editor_property('landscape_material').get_path_name()))
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
(R/'reports/orison_terrain_unreal_qa.json').write_text(json.dumps(data,indent=2))
print('ORISON_TERRAIN_QA_SAVED')
