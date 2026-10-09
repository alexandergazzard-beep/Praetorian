"""Author review/inspection maps with editor APIs; original assets preserved."""
import unreal,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REVIEW='/Game/LostVanguard/Environment/OpeningReview/Maps/L_ForestWreck_Review'
INSPECT='/Game/LostVanguard/Environment/OpeningReview/Maps/L_ForestWreck_Inspection'
levels=unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
data=json.loads((ROOT/'reports/forest_wreck_unreal_import.json').read_text())['assets']
def spawn(cls,label,pos,rot=(0,0,0)):
 a=actors.spawn_actor_from_class(cls,unreal.Vector(*pos),unreal.Rotator(*rot));a.set_actor_label(label);a.set_folder_path('LostVanguard/ForestWreckReview');return a
def mesh(item,pos,rot=(0,0,0),scale=1):
 a=spawn(unreal.StaticMeshActor,'FWR_'+item['id'],pos,rot);a.static_mesh_component.set_static_mesh(unreal.load_asset(item['mesh']));a.set_actor_scale3d(unreal.Vector(scale,scale,scale));return a
assert levels.new_level(INSPECT)
floor=spawn(unreal.StaticMeshActor,'Inspection_Ground',(0,0,-10));floor.static_mesh_component.set_static_mesh(unreal.load_asset('/Engine/BasicShapes/Cube'));floor.set_actor_scale3d(unreal.Vector(50,50,.2))
mesh(data[0],(-550,-350,0));mesh(data[1],(600,650,0),(0,12,0))
sun=spawn(unreal.DirectionalLight,'Inspection_Sun',(0,0,1500),(-28,-35,0));sun.light_component.set_editor_property('intensity',1.8);sun.light_component.set_light_color(unreal.LinearColor(.48,.73,1,1))
sky=spawn(unreal.SkyLight,'Inspection_Sky',(0,0,1500));sky.light_component.set_editor_property('intensity',.5)
fill=spawn(unreal.PointLight,'Inspection_CoolBounce',(-500,-1000,330));fill.point_light_component.set_editor_property('intensity',28);fill.point_light_component.set_editor_property('attenuation_radius',1600);fill.point_light_component.set_light_color(unreal.LinearColor(.07,.28,.40,1))
post=spawn(unreal.PostProcessVolume,'Inspection_Exposure',(0,0,0));post.set_editor_property('unbound',True)
settings=post.get_editor_property('settings')
for name,value in {'override_auto_exposure_method':True,'auto_exposure_method':unreal.AutoExposureMethod.AEM_MANUAL,'override_auto_exposure_apply_physical_camera_exposure':True,'auto_exposure_apply_physical_camera_exposure':False,'override_auto_exposure_bias':True,'auto_exposure_bias':1.25}.items():settings.set_editor_property(name,value)
post.set_editor_property('settings',settings);post.brush_component.set_visibility(False)
assert levels.save_current_level()
assert levels.load_level(REVIEW)
for item,pos,rot in [(data[0],(650,-680,-90),(0,0,0)),(data[1],(3470,400,220),(0,80,7))]:mesh(item,pos,rot)
assert levels.save_current_level()
(ROOT/'reports/forest_wreck_sample_maps.json').write_text(json.dumps({'review_map':REVIEW,'inspection_map':INSPECT,'samples_integrated':2,'original_unchanged':True,'sample_acceptance':'pending live inspection, collision, LOD and gameplay checks'},indent=2))
print('FOREST_WRECK_SAMPLE_MAPS_SAVED',flush=True)
