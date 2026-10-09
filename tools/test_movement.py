# /// script
# requires-python = ">=3.12"
# dependencies = ["mcp==2.3.0"]
# ///
"""Measure player movement in PIE on L_Movement_Test (main editor, port 8000 only).

Usage: uv run tools/test_movement.py <label> [expected-profile]
Drives the player's existing editor test inputs (DebugForward/Right/Crouch, RequestJump/Restart),
which feed the same AddMovementInput/Jump/Crouch calls as the keyboard. Times use the game clock:
DebugMoveTime is reduced by DeltaSeconds every tick, so (start - value) is elapsed game time.
Sample resolution is limited by MCP round trips; timings are therefore approximate (+/- one sample).
"""
import asyncio
import base64
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from movement_mcp import ROOT, ACTOR, EDITOR, OBJ, SCENE, session
from movement_profiles import MOVEMENT_FIELDS, PROFILES
from build_movement_test_map import CROUCH_BAR_Y, LANE_X, LEDGES, MAP, PLATFORM, SLOPES, STATIONS, STEPS

LABEL = sys.argv[1] if len(sys.argv) > 1 else 'current'
EXPECTED = PROFILES.get(sys.argv[2] if len(sys.argv) > 2 else LABEL)
PERF = {'refPath': '/Script/UnrealEd.Default__EditorPerformanceSettings'}
PLAYER_CLASS = '/Game/WreckagePrototype/Blueprints/BP_WreckagePlayer_Runtime.BP_WreckagePlayer_Runtime_C'
CLOCK = 1000.0
STAND_Z = 90.0  # capsule centre when standing on z=0 (88 half-height + floor contact offset)
OUT = ROOT / 'reports' / f'movement_tests_{LABEL}.json'
report = {'label': LABEL, 'map': MAP, 'expected_profile': EXPECTED, 'checks': [], 'measurements': {}, 'errors': [],
          'limitations': ['Automated test inputs, not a physical keyboard/mouse; feel requires the hands-on checklist.',
                          'Timing uses sampled game time; sample spacing is reported with each timed result.']}


def save():
    OUT.write_text(json.dumps(report, indent=2), encoding='utf-8')


async def main():
    async with session() as call:
        report['verified_target'] = call.verified
        if await call(EDITOR, 'IsPIERunning'):
            await call(EDITOR, 'StopPIE')
        # A background editor throttles to ~3 fps; disable for this process only (not saved to config).
        throttle = json.loads(await call(OBJ, 'get_properties', instance=PERF, properties=['bThrottleCPUWhenNotForeground']))
        report['editor_background_throttle_before'] = throttle['bThrottleCPUWhenNotForeground']
        await call(OBJ, 'set_properties', instance=PERF, values=json.dumps({'bThrottleCPUWhenNotForeground': False}))
        try:
            await suite(call)
        finally:
            if await call(EDITOR, 'IsPIERunning'):
                await call(EDITOR, 'StopPIE')
            await call(OBJ, 'set_properties', instance=PERF, values=json.dumps(throttle))
    print('SUMMARY', json.dumps({'passed': sum(c['passed'] for c in report['checks']), 'total': len(report['checks'])}))


async def suite(call):
    if True:
        if await call(SCENE, 'get_current_level') != MAP:
            await call(SCENE, 'load_level', level_path=MAP)
        try:
            await call(EDITOR, 'StartPIE', options={'bSimulate': False, 'playMode': 'PlayMode_InViewPort', 'warmupSeconds': 0})
        except RuntimeError as error:
            if 'PIE ended before warmup completed' not in str(error) or not await call(EDITOR, 'IsPIERunning'):
                raise
        await asyncio.sleep(1.0)
        player = (await call(SCENE, 'find_actors', name='', tag='', collision_channels=[], actor_type={'refPath': PLAYER_CLASS}))[0]
        refs = json.loads(await call(OBJ, 'get_properties', instance=player, properties=['CharacterMovement', 'CapsuleComponent']))
        move, capsule = refs['CharacterMovement'], refs['CapsuleComponent']

        async def props(obj, names):
            return json.loads(await call(OBJ, 'get_properties', instance=obj, properties=names))

        async def setp(obj=None, **values):
            await call(OBJ, 'set_properties', instance=obj or player, values=json.dumps(values))

        async def sample():
            p = await props(player, ['DebugMoveTime', 'Health', 'Dead', 'bIsCrouched', 'Objective', 'Step'])
            m = await props(move, ['Velocity', 'MovementMode'])
            c = await props(capsule, ['RelativeLocation', 'CapsuleHalfHeight'])
            v = m['Velocity']
            return {'t': CLOCK - p['DebugMoveTime'], 'x': c['RelativeLocation']['x'], 'y': c['RelativeLocation']['y'],
                    'z': c['RelativeLocation']['z'], 'vx': v['x'], 'vy': v['y'], 'vz': v['z'],
                    'hspeed': math.hypot(v['x'], v['y']), 'mode': m['MovementMode'], 'half': c['CapsuleHalfHeight'],
                    'health': p['Health'], 'dead': p['Dead'], 'crouched': p['bIsCrouched'], 'objective': p['Objective'],
                    'step': p['Step']}

        async def check(name, passed, observed):
            report['checks'].append({'name': name, 'passed': bool(passed), 'observed': observed})
            save()
            print(('PASS ' if passed else 'FAIL ') + name + ' :: ' + json.dumps(observed)[:300], flush=True)

        async def reset(x, y, z=STAND_Z, settle=0.6, **inputs):
            """Teleport, clear velocity and inputs, then restart the clock."""
            await setp(DebugForward=0.0, DebugRight=0.0, DebugLook=0.0, DebugCrouch=False, RequestJump=False,
                       DebugMoveTime=CLOCK)
            await call(ACTOR, 'set_actor_transform', actor=player, worldspace=True,
                       xform={'location': {'x': float(x), 'y': float(y), 'z': float(z)}})
            await setp(move, Velocity={'x': 0.0, 'y': 0.0, 'z': 0.0})
            await asyncio.sleep(settle)
            await setp(DebugMoveTime=CLOCK, **inputs)

        async def record(seconds, until=None):
            out, start = [], None
            while True:
                s = await sample()
                start = s['t'] if start is None else start
                out.append(s)
                if until and until(s, out):
                    break
                if s['t'] - start >= seconds:
                    break
            return out

        def spacing(samples):
            gaps = [b['t'] - a['t'] for a, b in zip(samples, samples[1:])]
            return round(sum(gaps) / len(gaps), 4) if gaps else None

        # 1. Saved defaults are what the running player uses.
        live = await props(move, MOVEMENT_FIELDS)
        live['LookSensitivity'] = (await props(player, ['LookSensitivity']))['LookSensitivity']
        report['measurements']['runtime_settings'] = live
        if EXPECTED:
            diffs = {k: (v, live[k]) for k, v in EXPECTED.items() if not math.isclose(float(live[k]), float(v), rel_tol=1e-4)}
            await check('Runtime movement equals saved profile', not diffs, diffs or EXPECTED)
        await check('Look sensitivity variable present at runtime (default 0.6)', math.isclose(live['LookSensitivity'], 0.6, rel_tol=1e-6), live['LookSensitivity'])

        # 2. Ground speed, acceleration and stopping on the flat lane.
        x0, y0 = STATIONS['flat_start']
        await reset(x0, y0, DebugForward=1.0)
        run = await record(2.5)
        top = max(s['hspeed'] for s in run)
        t90 = next((s['t'] - run[0]['t'] for s in run if s['hspeed'] >= 0.9 * top), None)
        await setp(DebugForward=0.0)
        stop = await record(2.0, until=lambda s, o: s['hspeed'] < 5)
        stop_dist = math.hypot(stop[-1]['x'] - stop[0]['x'], stop[-1]['y'] - stop[0]['y'])
        report['measurements']['ground'] = {'top_speed_cm_s': round(top, 1), 'time_to_90pct_s': t90,
                                            'stop_time_s': round(stop[-1]['t'] - stop[0]['t'], 3),
                                            'stop_distance_cm': round(stop_dist, 1),
                                            'sample_spacing_s': spacing(run)}
        if EXPECTED:
            await check('Top walk speed within 2% of profile', abs(top - EXPECTED['MaxWalkSpeed']) <= 0.02 * EXPECTED['MaxWalkSpeed'], report['measurements']['ground'])
        await check('Stops within 0.4 s of releasing input', stop[-1]['hspeed'] < 5 and stop[-1]['t'] - stop[0]['t'] <= 0.4, report['measurements']['ground'])

        # 3. Standing jump: apex height and airtime from rest.
        await reset(x0, y0)
        base = await sample()  # baseline before the request; the first sample after it is already airborne
        await setp(RequestJump=True)
        jump = await record(3.0, until=lambda s, o: len(o) > 3 and s['mode'] == 'MOVE_Walking' and o[-2]['mode'] == 'MOVE_Falling')
        air = [s for s in jump if s['mode'] == 'MOVE_Falling']
        apex = max(s['z'] for s in jump) - base['z']
        airtime = (jump[-1]['t'] - air[0]['t']) if air else None
        report['measurements']['jump'] = {'apex_cm': round(apex, 1), 'airtime_s': round(airtime, 3) if airtime else None,
                                          'sample_spacing_s': spacing(jump), 'health_after': jump[-1]['health']}
        if EXPECTED:
            g = 980.0 * EXPECTED['GravityScale']
            predicted = {'apex_cm': EXPECTED['JumpZVelocity'] ** 2 / (2 * g), 'airtime_s': 2 * EXPECTED['JumpZVelocity'] / g}
            report['measurements']['jump']['predicted'] = {k: round(v, 3) for k, v in predicted.items()}
            await check('Jump apex within 5% of prediction', abs(apex - predicted['apex_cm']) <= 0.05 * predicted['apex_cm'], report['measurements']['jump'])
            tol = max(0.1, 2 * (spacing(jump) or 0))
            await check('Jump airtime within one-sample tolerance of prediction', airtime is not None and abs(airtime - predicted['airtime_s']) <= tol, report['measurements']['jump'])

        # 4. Air control: running jump with and without mid-air strafe/brake input.
        async def running_jump(after_takeoff):
            await reset(x0, y0, DebugForward=1.0)
            await record(1.2)
            start = await sample()
            await setp(RequestJump=True)
            await record(1.0, until=lambda s, o: s['mode'] == 'MOVE_Falling')
            await setp(**after_takeoff)
            flight = await record(3.0, until=lambda s, o: len(o) > 2 and s['mode'] == 'MOVE_Walking')
            await setp(DebugForward=0.0, DebugRight=0.0)
            return {'forward_cm': round(flight[-1]['x'] - start['x'], 1), 'lateral_cm': round(flight[-1]['y'] - start['y'], 1)}
        report['measurements']['air_control'] = {
            'hold_forward': await running_jump({'DebugForward': 1.0}),
            'release_all': await running_jump({'DebugForward': 0.0}),
            'pull_back': await running_jump({'DebugForward': -1.0}),
            'strafe_right_only': await running_jump({'DebugForward': 0.0, 'DebugRight': 1.0})}
        save()

        # 5. Crouch speed, capsule and the 125 cm bar.
        await reset(x0, y0, DebugCrouch=True)
        await record(0.4)
        await setp(DebugForward=1.0)
        crouch = await record(2.0)
        ctop = max(s['hspeed'] for s in crouch)
        report['measurements']['crouch'] = {'top_speed_cm_s': round(ctop, 1), 'half_height': crouch[-1]['half'], 'crouched': crouch[-1]['crouched']}
        if EXPECTED:
            await check('Crouch speed within 2% of profile', abs(ctop - EXPECTED['MaxWalkSpeedCrouched']) <= 0.02 * EXPECTED['MaxWalkSpeedCrouched'], report['measurements']['crouch'])
        bar_back = LANE_X + 180
        for crouched in (False, True):
            await reset(-4000, CROUCH_BAR_Y, DebugCrouch=crouched)
            await record(0.3)
            await setp(DebugForward=1.0)
            trip = await record(3.0)
            passed = trip[-1]['x'] > bar_back + 40
            name = 'Crouched player passes under 125 cm bar' if crouched else 'Standing player is blocked by 125 cm bar'
            await check(name, passed if crouched else not passed, {'final_x': round(trip[-1]['x'], 1), 'bar_back_x': bar_back})

        # 6. Steps (MaxStepHeight) and slopes (WalkableFloorAngle) walked with forward input only.
        steps = {}
        for h, y in STEPS.items():
            await reset(-4000, y, DebugForward=1.0)
            trip = await record(1.2)
            peak = max(s['z'] for s in trip)
            steps[h] = {'climbed': peak > STAND_Z + h - 10, 'peak_z': round(peak, 1), 'final_x': round(trip[-1]['x'], 1)}
        report['measurements']['steps'] = steps
        limit = live['MaxStepHeight']
        # UE keeps ~2 cm between capsule and floor, so the practical step limit sits just below MaxStepHeight.
        await check('Steps of 20/35 cm climb; 46/55 cm block (MaxStepHeight 45)',
                    all(steps[h]['climbed'] for h in (20, 35)) and not any(steps[h]['climbed'] for h in (46, 55)),
                    {'limit_cm': limit, 'steps': steps})
        slopes = {}
        for deg, y in SLOPES.items():
            await reset(-4000, y, DebugForward=1.0)
            trip = await record(3.0)
            top_z = 600 * math.sin(math.radians(deg))
            gain = max(s['z'] for s in trip) - STAND_Z
            slopes[deg] = {'height_gained_cm': round(gain, 1), 'ramp_height_cm': round(top_z, 1), 'walkable': gain > 0.8 * top_z}
        report['measurements']['slopes'] = slopes
        angle = live['WalkableFloorAngle']
        await check('Slopes walkable exactly up to WalkableFloorAngle', all(v['walkable'] == (d <= angle) for d, v in slopes.items()), {'limit_deg': angle, 'slopes': slopes})

        # 7. Ledges: jump from standstill against the face, with and without mid-air crouch.
        ledges = {}
        for crouch_jump in (False, True):
            for h, y in LEDGES.items():
                await reset(LANE_X - 36, y, DebugForward=1.0)
                await record(0.3)
                await setp(RequestJump=True)
                if crouch_jump:
                    await record(1.0, until=lambda s, o: s['mode'] == 'MOVE_Falling')
                    await setp(DebugCrouch=True)
                trip = await record(1.6)
                await setp(DebugCrouch=False, DebugForward=0.0)
                await record(0.6)
                final = await sample()
                ledges[f"{'crouch_' if crouch_jump else ''}{h}"] = {'reached_top': final['z'] > h + 40, 'final_z': round(final['z'], 1),
                                                                    'peak_feet_cm': round(max(s['z'] - s['half'] for s in trip), 1)}
        report['measurements']['ledges'] = ledges
        if EXPECTED:
            # Practical reach = feet clearance (+44 cm when crouched mid-air) + ~10 cm, because the capsule's
            # rounded base can ride over a corner that is still at a walkable contact angle.
            reach = EXPECTED['JumpZVelocity'] ** 2 / (2 * 980.0 * EXPECTED['GravityScale'])
            practical = lambda k: reach + (44 if k.startswith('crouch') else 0) + 10
            expected = {k: int(k.split('_')[-1]) < practical(k) for k in ledges if abs(int(k.split('_')[-1]) - practical(k)) > 12}
            await check('Ledge reach matches jump clearance (+44 crouch, +~10 capsule), boundary cases excluded',
                        all(ledges[k]['reached_top'] == v for k, v in expected.items()),
                        {'clearance_cm': round(reach, 1), 'expected': expected, 'ledges': ledges})
        await check('No jump or crouch-jump reaches the 290 cm exit-gate height',
                    not ledges['290']['reached_top'] and not ledges['crouch_290']['reached_top'],
                    {'290': ledges['290'], 'crouch_290': ledges['crouch_290'], 'crouch_250': ledges['crouch_250']})
        save()

        # 8. Landings from several heights: health must stay unchanged (no fall damage).
        landings = {}
        drop_x, drop_y = STATIONS['drop_column']
        for h in (200, 500, 1000, 2000, 4000, 10000):
            await reset(drop_x, drop_y, z=STAND_Z + h, settle=0.0)
            fall = await record(15.0, until=lambda s, o: len(o) > 2 and s['mode'] == 'MOVE_Walking')
            await record(0.5)
            after = await sample()
            landings[h] = {'impact_speed_cm_s': round(max(abs(s['vz']) for s in fall), 1), 'health': after['health'],
                           'dead': after['dead'], 'landed_z': round(after['z'], 1)}
        report['measurements']['landings'] = landings
        await check('No fall damage from 2 m to 100 m drops', all(v['health'] == 100 and not v['dead'] for v in landings.values()), landings)
        px, py, top = PLATFORM
        await reset(px, py, z=top + STAND_Z, DebugForward=1.0)
        off = await record(6.0, until=lambda s, o: len(o) > 5 and s['mode'] == 'MOVE_Walking' and s['z'] < 200)
        await setp(DebugForward=0.0)
        await record(0.5)
        after = await sample()
        await check('Walking off the 10 m platform causes no damage', after['health'] == 100 and not after['dead'] and after['z'] < 200,
                    {'health': after['health'], 'dead': after['dead'], 'z': after['z']})

        # 9. Leaving the playable world is still caught; restart recovers.
        ox, oy = STATIONS['off_map']
        await reset(ox, oy, z=200, settle=0.0)
        fell = await record(8.0, until=lambda s, o: s['dead'])
        await check('Falling out of the world is caught (death + restart prompt)', fell[-1]['dead'] and 'fell' in fell[-1]['objective'].lower(),
                    {'z': fell[-1]['z'], 'dead': fell[-1]['dead'], 'objective': fell[-1]['objective']})
        await setp(RequestRestart=True)
        await record(0.6)
        back = await sample()
        await check('Restart after out-of-world restores the player', back['health'] == 100 and not back['dead'] and back['z'] > 0,
                    {'health': back['health'], 'dead': back['dead'], 'z': back['z']})

        # 10. Enemy damage still applies (searchers fire only when 1650 < x < 3200).
        ex, ey = STATIONS['enemy_fire']
        await reset(ex, ey, settle=0.0)
        shot = await record(5.0, until=lambda s, o: s['health'] < 100)
        await check('Enemy fire still damages the player', shot[-1]['health'] < 100, {'health': shot[-1]['health'], 'game_time_s': round(shot[-1]['t'] - shot[0]['t'], 2)})
        await setp(RequestRestart=True)
        await record(0.6)
        healed = await sample()
        await check('Restart after enemy damage restores 100 health', healed['health'] == 100 and not healed['dead'], {'health': healed['health']})

        data = (await call(EDITOR, 'CaptureEditorImage'))['data']
        (ROOT / 'reports' / f'movement_test_{LABEL}.png').write_bytes(base64.b64decode(data))
        await call(EDITOR, 'StopPIE')


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    try:
        asyncio.run(main())
    except BaseException as error:
        report['errors'].append(repr(error))
        save()
        raise
    save()
