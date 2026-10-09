import unreal,json,time,math
from pathlib import Path
R=Path(__file__).resolve().parents[1]
world=unreal.EditorLevelLibrary.get_game_world();pawn=unreal.GameplayStatics.get_player_character(world,0);assert pawn and 'BP_TerrainPlayer' in pawn.get_class().get_name()
initial=pawn.get_actor_location();samples=[];beg=time.monotonic();stage=0
def tick(dt):
 global stage,handle
 t=time.monotonic()-beg
 if t<3:pawn.add_movement_input(pawn.get_actor_forward_vector(),1.0)
 p=pawn.get_actor_location();samples.append(dict(t=t,location=list(p.to_tuple()),falling=pawn.character_movement.is_falling(),dt=dt))
 if t>4 and stage==0:
  pawn.jump();stage=1
 if t>8:
  unreal.unregister_slate_post_tick_callback(handle)
  walk=[s for s in samples if 2.8<s['t']<4];jump=[s for s in samples if 4.05<s['t']<6];finish=samples[-1]
  moved=math.dist(initial.to_tuple()[:2],walk[-1]['location'][:2]) if walk else 0
  rise=max(s['location'][2] for s in jump)-walk[-1]['location'][2] if jump and walk else 0
  result=dict(pawn=pawn.get_class().get_name(),walk_distance_cm=moved,jump_rise_cm=rise,ended_grounded=not finish['falling'],checks=[dict(name='independent terrain player possessed',passed=True),dict(name='walk across Landscape',passed=moved>700),dict(name='jump rises and lands',passed=rise>30 and not finish['falling'])],samples=samples,performance_note='Slate tick samples are editor timing, not a game FPS benchmark.')
  (R/'reports/orison_terrain_playtest.json').write_text(json.dumps(result,indent=2));print('ORISON_TERRAIN_PLAYTEST',result['checks'])
handle=unreal.register_slate_post_tick_callback(tick)
