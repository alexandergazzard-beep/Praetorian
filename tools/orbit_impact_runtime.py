import unreal,math,time,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
world=unreal.EditorLevelLibrary.get_game_world();assert world
cams=unreal.GameplayStatics.get_all_actors_of_class(world,unreal.CineCameraActor);cam=next(a for a in cams if a.get_actor_label()=='Impact_CinematicCamera')
original=cam.get_actor_transform();started=time.monotonic();records=[];handle=None
def orbit(dt):
 global handle
 elapsed=time.monotonic()-started
 angle=math.atan2(-2000,-1350)+math.radians(24)*min(elapsed/18,1)
 loc=unreal.Vector(2413*math.cos(angle),2413*math.sin(angle),340)
 rot=unreal.MathLibrary.find_look_at_rotation(loc,unreal.Vector(0,0,290));cam.set_actor_location_and_rotation(loc,rot,False,False)
 records.append({'t':elapsed,'position':[loc.x,loc.y,loc.z]})
 if elapsed>18:
  unreal.unregister_slate_post_tick_callback(handle)
  (R/'reports/space_impact_v2_camera_motion.json').write_text(json.dumps({'continuous_runtime_camera_motion':True,'duration_seconds':elapsed,'samples':len(records),'start':records[0],'end':records[-1]},indent=2))
  print('IMPACT_ORBIT_COMPLETE',flush=True)
handle=unreal.register_slate_post_tick_callback(orbit)
print('IMPACT_ORBIT_STARTED',flush=True)
