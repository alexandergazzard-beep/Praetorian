"""Create a separate neutral-lit review map without touching the gameplay map."""
import unreal,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MAP='/Game/LostVanguard/Art/Review/L_Debris_FirstPair_Review'
level=unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
assert level.new_level(MAP)
actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
def spawn(cls,name,xyz,rot=(0,0,0)):
    a=actors.spawn_actor_from_class(cls,unreal.Vector(*xyz),unreal.Rotator(*rot));a.set_actor_label(name);return a
floor=spawn(unreal.StaticMeshActor,'Review_Floor',(0,0,-5))
floor.static_mesh_component.set_static_mesh(unreal.load_asset('/Engine/BasicShapes/Cube'))
floor.set_actor_scale3d(unreal.Vector(20,20,.1))
data=json.loads((ROOT/'reports/debris_pair_unreal_qa.json').read_text())['assets']
for a,xyz,rot in [(data[0],(0,0,0),(0,0,0)),(data[1],(0,-110,0),(0,0,0))]:
    o=spawn(unreal.StaticMeshActor,'Review_'+a['id'],xyz,rot)
    o.static_mesh_component.set_static_mesh(unreal.load_asset(a['mesh']))
for name,xyz,rot,power,color in [
    ('Key',(-130,-180,220),(-45,40,0),5000,(1,.94,.86,1)),
    ('Fill',(80,-80,160),(-55,145,0),3500,(.86,.92,1,1)),
    ('Rim',(100,170,220),(-50,-110,0),5000,(1,1,1,1))]:
    a=spawn(unreal.RectLight,name,xyz,rot)
    c=a.light_component;c.set_editor_property('intensity',power)
    c.set_editor_property('attenuation_radius',1000)
    c.set_editor_property('source_width',150);c.set_editor_property('source_height',150)
    c.set_light_color(unreal.LinearColor(*color))
sky=spawn(unreal.SkyLight,'Review_Sky',(0,0,400))
sky.light_component.set_editor_property('intensity',.7)
post=spawn(unreal.PostProcessVolume,'Review_Exposure',(0,0,0))
post.set_editor_property('unbound',True)
settings=post.get_editor_property('settings')
settings.set_editor_property('override_auto_exposure_min_brightness',True)
settings.set_editor_property('override_auto_exposure_max_brightness',True)
settings.set_editor_property('auto_exposure_min_brightness',8)
settings.set_editor_property('auto_exposure_max_brightness',8)
post.set_editor_property('settings',settings)
assert level.save_current_level()
(ROOT/'reports/debris_review_map.json').write_text(json.dumps({'map':MAP,'purpose':'Neutral inspection of actual imported meshes; not gameplay or performance benchmark.'},indent=2))
print('REVIEW_MAP_CREATED')
