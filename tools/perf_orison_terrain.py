import unreal,time,json,statistics
from pathlib import Path
R=Path(__file__).resolve().parents[1];w=unreal.EditorLevelLibrary.get_game_world();assert w
previous=unreal.SystemLibrary.get_console_variable_int_value('t.MaxFPS');unreal.SystemLibrary.execute_console_command(w,'t.MaxFPS 60')
beg=time.monotonic();samples=[]
def sample(dt):
 global handle
 elapsed=time.monotonic()-beg
 if elapsed>3:
  delta=unreal.GameplayStatics.get_world_delta_seconds(w)
  if delta>0:samples.append(delta)
 if elapsed>13:
  unreal.unregister_slate_post_tick_callback(handle);unreal.SystemLibrary.execute_console_command(w,'t.MaxFPS '+str(previous))
  s=sorted(samples);result=dict(context='Unreal5.8.3 editor PIE, stationary starting view, local workstation, capped60, ten-second sample after three seconds warmup',samples=len(s),mean_frame_ms=statistics.mean(s)*1000,median_frame_ms=statistics.median(s)*1000,p95_frame_ms=s[int((len(s)-1)*.95)]*1000,average_fps=1/statistics.mean(s),previous_maxfps_restored=previous,limitation='Editor timing only; not packaged-game, moving-camera or target-hardware validation.')
  (R/'reports/orison_terrain_performance.json').write_text(json.dumps(result,indent=2));print('ORISON_PERFORMANCE',result)
handle=unreal.register_slate_post_tick_callback(sample)
