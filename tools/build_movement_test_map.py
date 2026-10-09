# /// script
# requires-python = ">=3.12"
# dependencies = ["mcp==2.3.0"]
# ///
"""Build /Game/MovementTest/Maps/L_Movement_Test in the main editor (port 8000) via editor APIs.

A separate test map owned by the movement task; the shared mission map is never opened for editing.
Rebuilds are idempotent: actors in the MovementTest outliner folder are replaced.
Searchers spawned by the player Blueprint attack only when the player's X is 1650..3200, so every
station except the deliberate enemy-fire spot stays outside that band.
"""
import asyncio
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from movement_mcp import ROOT, ASSET, SCENE, OBJ, EDITOR, session

MAP = '/Game/MovementTest/Maps/L_Movement_Test'
TEMPLATE = '/Engine/Maps/Templates/Template_Default'
GAME_MODE = '/Game/WreckagePrototype/Blueprints/BP_WreckageGameMode_Runtime.BP_WreckageGameMode_Runtime_C'
CUBE = '/Engine/BasicShapes/Cube'
FOLDER = 'MovementTest'

LANE_X = -3600            # front face of every obstacle; tests start at x = -4000
STEPS = {20: -1000, 35: -1200, 44: -1400, 46: -1600, 55: -1800}          # height cm -> lane y
SLOPES = {30: 1000, 40: 1200, 44: 1400, 46: 1600, 50: 1800}             # degrees -> lane y
LEDGES = {120: -3200, 150: -3400, 165: -3600, 180: -3800, 200: -4000, 220: -4200, 250: -4400, 290: -4600}  # 290 = exit gate
CROUCH_BAR_Y = -2400
PLATFORM = (-4000, 3000, 1000)  # x, y, top height
STATIONS = {'flat_start': (-4000, 0), 'drop_column': (-1000, 3500), 'enemy_fire': (2000, -480),
            'off_map': (0, 6800), 'platform_top': (-4000, 3000)}


def box(name, center, size, rotation=(0, 0, 0)):
    return {'name': name, 'xform': {'location': dict(zip('xyz', map(float, center))),
                                    'rotation': dict(zip(('pitch', 'yaw', 'roll'), map(float, rotation))),
                                    'scale': dict(zip('xyz', (s / 100.0 for s in size)))}}


def layout():
    items = [box('MT_Floor', (0, 0, -50), (12000, 12000, 100))]
    for h, y in STEPS.items():
        items.append(box(f'MT_Step_{h}cm', (LANE_X + 150, y, h / 2), (300, 150, h)))
    for deg, y in SLOPES.items():
        t, length, thick = math.radians(deg), 600.0, 20.0
        cx = LANE_X + (length / 2) * math.cos(t) + (thick / 2) * math.sin(t)
        items.append(box(f'MT_Slope_{deg}deg', (cx, y, (length / 2) * math.sin(t)), (length, 150, thick), (deg, 0, 0)))
    items.append(box('MT_CrouchBar_125cm', (LANE_X + 90, CROUCH_BAR_Y, 180), (180, 400, 110)))  # stays clear of other lanes
    for h, y in LEDGES.items():
        items.append(box(f'MT_Ledge_{h}cm', (LANE_X + 750, y, h / 2), (1500, 150, h)))  # deep enough to land and stop on
    x, y, top = PLATFORM
    items.append(box('MT_Platform_10m', (x, y, top / 2), (400, 400, top)))
    return items


async def main():
    report = {'map': MAP, 'actors': [], 'stations': STATIONS}
    async with session() as call:
        report['verified_target'] = call.verified
        if await call(EDITOR, 'IsPIERunning'):
            await call(EDITOR, 'StopPIE')
        current = await call(SCENE, 'get_current_level')
        if current != MAP and await call(ASSET, 'is_dirty', asset_path=current):
            raise SystemExit(f'{current} has unsaved changes; refusing to switch levels.')
        if not await call(ASSET, 'exists', path=MAP):
            await call(ASSET, 'duplicate', path=TEMPLATE, new_path=MAP)
            report['created_from'] = TEMPLATE
        if await call(ASSET, 'is_dirty', asset_path=MAP):
            assert await call(ASSET, 'save_assets', asset_paths=[MAP])
        await call(SCENE, 'load_level', level_path=MAP)
        assert await call(SCENE, 'get_current_level') == MAP
        # Replace template floor/start and any earlier MovementTest actors.
        for actor_type in ['/Script/Engine.StaticMeshActor', '/Script/Engine.PlayerStart']:
            for actor in await call(SCENE, 'find_actors', name='', tag='', collision_channels=[], actor_type={'refPath': actor_type}):
                await call(SCENE, 'remove_from_scene', actor=actor)
        ws = (await call(SCENE, 'find_actors', name='', tag='', collision_channels=[],
                         actor_type={'refPath': '/Script/Engine.WorldSettings'}))[0]
        await call(OBJ, 'set_properties', instance=ws, values=json.dumps({'DefaultGameMode': {'refPath': GAME_MODE}}))
        for item in layout():
            actor = await call(SCENE, 'add_to_scene_from_asset', asset_path=CUBE, name=item['name'], xform=item['xform'], snap_to_ground=False)
            await call(SCENE, 'set_actor_folder', actor=actor, folder_path=FOLDER)
            report['actors'].append(item)
        start = await call(SCENE, 'add_to_scene_from_class', actor_type={'refPath': '/Script/Engine.PlayerStart'}, name='MT_PlayerStart',
                           xform={'location': {'x': 0.0, 'y': 0.0, 'z': 100.0}, 'rotation': {'pitch': 0.0, 'yaw': 0.0, 'roll': 0.0},
                                  'scale': {'x': 1.0, 'y': 1.0, 'z': 1.0}}, snap_to_ground=False)
        await call(SCENE, 'set_actor_folder', actor=start, folder_path=FOLDER)
        assert await call(ASSET, 'save_assets', asset_paths=[MAP])
        report['dirty_after_save'] = await call(ASSET, 'is_dirty', asset_path=MAP)
        # Ground-truth collision probes from the saved layout.
        probes = {'floor': ((-4000, 0, 500), (-4000, 0, -500)),
                  'platform_top': ((PLATFORM[0], PLATFORM[1], 1500), (PLATFORM[0], PLATFORM[1], 0)),
                  'off_map_empty': ((0, 6800, 500), (0, 6800, -2000))}
        report['traces'] = {k: await call(SCENE, 'trace_world', start=dict(zip('xyz', map(float, a))), end=dict(zip('xyz', map(float, b))))
                            for k, (a, b) in probes.items()}
    (ROOT / 'reports' / 'movement_test_map_build.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps({'actors': len(report['actors']), 'dirty_after_save': report['dirty_after_save'], 'traces': report['traces']}, indent=2))


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    asyncio.run(main())
