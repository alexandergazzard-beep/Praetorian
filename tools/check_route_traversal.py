# /// script
# requires-python = ">=3.12"
# dependencies = ["mcp==2.3.0"]
# ///
"""Check what the tuned jump can now climb in the opening mission map (movement editor only).

1. Static scan: collidable actors inside the route, their real collision tops (downward traces), and
   which are newly climbable compared with the original jump; flags launch points that could reach the
   360 cm wall tops or the 290 cm exit gate.
2. Live attempt: from the comms panel top, a running crouch-jump toward the exit gate in PIE.
Read-only for the map: nothing is saved.
"""
import asyncio
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from movement_mcp import ROOT, ACTOR, EDITOR, OBJ, SCENE, session
from movement_profiles import PROFILES

MAP = '/Game/WreckagePrototype/Maps/L_Wreckage_Opening'
PLAYER_CLASS = '/Game/WreckagePrototype/Blueprints/BP_WreckagePlayer_Runtime.BP_WreckagePlayer_Runtime_C'
PERF = {'refPath': '/Script/UnrealEd.Default__EditorPerformanceSettings'}
ROUTE = {'min': {'x': -600.0, 'y': -800.0, 'z': -50.0}, 'max': {'x': 4600.0, 'y': 800.0, 'z': 420.0}, 'isValid': True}
WALL_TOP, GATE_TOP, GATE_X = 360.0, 290.0, (4017.5, 4062.5)
CAPSULE_ALLOWANCE = 10.0  # measured on L_Movement_Test: rounded capsule base catches ~10 cm above feet clearance


def reach(profile):
    p = PROFILES[profile]
    clearance = p['JumpZVelocity'] ** 2 / (2 * 980.0 * p['GravityScale'])
    return {'standing': round(clearance + CAPSULE_ALLOWANCE, 1), 'crouch_jump': round(clearance + 44 + CAPSULE_ALLOWANCE, 1)}


async def main():
    report = {'map': MAP, 'reach_cm': {k: reach(k) for k in ('original', 'reach')}, 'props': [], 'risks': [], 'live_attempt': None}
    async with session() as call:
        report['verified_target'] = call.verified
        if await call(EDITOR, 'IsPIERunning'):
            await call(EDITOR, 'StopPIE')
        if await call(SCENE, 'get_current_level') != MAP:
            await call(SCENE, 'load_level', level_path=MAP)
        actors = await call(SCENE, 'find_actors', name='', tag='', bounds=ROUTE, collision_channels=['ObjectTypeQuery1', 'ObjectTypeQuery2'])
        # Route blockers by name too: the overlap query does not return every BlockAll box in this map.
        for name in ['ExitGate', 'CommsPanel', 'SearchTerminal', 'Comms_Wall', 'Exit_Wall', 'Bay_Wall', 'MainHullFlank']:
            actors += await call(SCENE, 'find_actors', name=name, tag='', collision_channels=[])
        actors = list({a['refPath']: a for a in actors}.values())
        for actor in actors:
            box = await call(ACTOR, 'get_actor_bounds', actor=actor)
            lo, hi = box['min'], box['max']
            if hi['z'] - lo['z'] > 2000 or (hi['x'] - lo['x']) * (hi['y'] - lo['y']) > 4e6:
                continue  # ground slabs / huge backdrop pieces
            cx, cy = (lo['x'] + hi['x']) / 2, (lo['y'] + hi['y']) / 2
            hit = await call(SCENE, 'trace_world', start={'x': cx, 'y': cy, 'z': 1000.0}, end={'x': cx, 'y': cy, 'z': -100.0})
            top = None if hit is None else round(1000.0 - hit, 1)
            if top is None or abs(top - hi['z']) > 5:
                item_note = 'centre trace hit another surface; using bounds top'
                top = round(hi['z'], 1)
            else:
                item_note = 'collision top from downward trace'
            if top is None or top < 30 or top > 600:
                continue
            label = await call(ACTOR, 'get_label', actor=actor)
            item = {'label': label, 'top_cm': top, 'top_source': item_note, 'center': [round(cx), round(cy)],
                    'footprint': [round(lo['x']), round(hi['x']), round(lo['y']), round(hi['y'])]}
            for prof, r in report['reach_cm'].items():
                item[f'climbable_{prof}'] = 'standing' if top <= r['standing'] else 'crouch_jump' if top <= r['crouch_jump'] else 'no'
            report['props'].append(item)
            r = report['reach_cm']['reach']
            if item['climbable_reach'] != 'no':
                from_top = top + r['crouch_jump']
                to_gate = max(GATE_X[0] - hi['x'], lo['x'] - GATE_X[1], 0)
                if from_top >= GATE_TOP and to_gate < 450 and abs(cy) < 400:
                    report['risks'].append({'prop': label, 'risk': 'launch point over exit gate', 'prop_top': top,
                                            'crouch_jump_reach_from_top': round(from_top, 1), 'horizontal_gap_cm': round(to_gate)})
                if from_top >= WALL_TOP:
                    report['risks'].append({'prop': label, 'risk': 'could reach 360 cm wall tops if within ~1 m of a wall',
                                            'prop_top': top, 'crouch_jump_reach_from_top': round(from_top, 1)})
        report['props'].sort(key=lambda p: p['center'][0])

        # Live attempt from the comms panel toward the exit gate.
        await call(OBJ, 'set_properties', instance=PERF, values=json.dumps({'bThrottleCPUWhenNotForeground': False}))
        try:
            try:
                await call(EDITOR, 'StartPIE', options={'bSimulate': False, 'playMode': 'PlayMode_InViewPort', 'warmupSeconds': 0})
            except RuntimeError as error:
                if 'PIE ended before warmup completed' not in str(error):
                    raise
            await asyncio.sleep(1.0)
            player = (await call(SCENE, 'find_actors', name='', tag='', collision_channels=[], actor_type={'refPath': PLAYER_CLASS}))[0]
            move = json.loads(await call(OBJ, 'get_properties', instance=player, properties=['CharacterMovement']))['CharacterMovement']
            panel = next((p for p in report['props'] if p['label'].startswith('CommsPanel')), None)
            attempt = {'panel': panel}
            if panel:
                await call(ACTOR, 'set_actor_transform', actor=player, worldspace=True,
                           xform={'location': {'x': panel['footprint'][0] + 40.0, 'y': float(panel['center'][1]), 'z': panel['top_cm'] + 95.0}})
                await call(OBJ, 'set_properties', instance=move, values=json.dumps({'Velocity': {'x': 0.0, 'y': 0.0, 'z': 0.0}}))
                await asyncio.sleep(0.8)
                start = await call(ACTOR, 'get_actor_transform', actor=player)
                await call(OBJ, 'set_properties', instance=player, values=json.dumps({'DebugForward': 1.0, 'DebugMoveTime': 1000.0}))
                for _ in range(200):
                    tr = await call(ACTOR, 'get_actor_transform', actor=player)
                    if tr['location']['x'] >= panel['footprint'][1] - 20:
                        break
                await call(OBJ, 'set_properties', instance=player, values=json.dumps({'RequestJump': True}))
                await asyncio.sleep(0.12)
                await call(OBJ, 'set_properties', instance=player, values=json.dumps({'DebugCrouch': True}))
                peak = 0.0
                for _ in range(120):
                    tr = await call(ACTOR, 'get_actor_transform', actor=player)
                    peak = max(peak, tr['location']['z'])
                    await asyncio.sleep(0.01)
                await call(OBJ, 'set_properties', instance=player, values=json.dumps({'DebugCrouch': False, 'DebugForward': 0.0, 'DebugMoveTime': 0.0}))
                await asyncio.sleep(0.6)
                end = await call(ACTOR, 'get_actor_transform', actor=player)
                state = json.loads(await call(OBJ, 'get_properties', instance=player, properties=['Step', 'CommsRestored', 'Health', 'Dead']))
                attempt.update({'start': start['location'], 'end': end['location'], 'peak_center_z': round(peak, 1), 'state_after': state,
                                'crossed_gate': end['location']['x'] > GATE_X[1] + 34})
            report['live_attempt'] = attempt
        finally:
            if await call(EDITOR, 'IsPIERunning'):
                await call(EDITOR, 'StopPIE')
            await call(OBJ, 'set_properties', instance=PERF, values=json.dumps({'bThrottleCPUWhenNotForeground': True}))
        report['map_dirty_after'] = await call('editor_toolset.toolsets.asset.AssetTools', 'is_dirty', asset_path=MAP)
    (ROOT / 'reports' / 'movement_route_traversal.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps({'reach_cm': report['reach_cm'], 'props_in_route': len(report['props']),
                      'newly_climbable': [(p['label'], p['top_cm'], p['climbable_reach']) for p in report['props']
                                          if p['climbable_original'] == 'no' and p['climbable_reach'] != 'no'],
                      'risks': report['risks'], 'live_attempt': report['live_attempt'], 'map_dirty_after': report['map_dirty_after']}, indent=1))


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    asyncio.run(main())
