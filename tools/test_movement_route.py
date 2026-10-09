# /// script
# requires-python = ">=3.12"
# dependencies = ["mcp==2.3.0"]
# ///
"""Run the established 19-check mission route test against the main editor (port 8000).

Reuses tools/test_wreckage.py unchanged; only the endpoint and output paths are redirected so the
tracked opening_* reports are not overwritten. Identity is verified before any call is made.
Usage: uv run tools/test_movement_route.py [map]
"""
import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import types
import movement_mcp
from movement_profiles import ACTIVE_PROFILE, PROFILES

# Shared route driver scales its timing to the accepted movement profile.
WALK = PROFILES[ACTIVE_PROFILE]['MaxWalkSpeed']
import test_wreckage as test

MAP = sys.argv[1] if len(sys.argv) > 1 else '/Game/WreckagePrototype/Maps/L_Wreckage_Opening'
PERF = {'refPath': '/Script/UnrealEd.Default__EditorPerformanceSettings'}
_original_client = test.streamable_http_client


def movement_client(_url, *args, **kwargs):
    return _original_client(movement_mcp.URL, *args, **kwargs)


async def run():
    async with movement_mcp.session() as call:  # aborts unless port 8000 is this checkout's editor
        test.report['verified_target'] = call.verified
        before = json.loads(await call(movement_mcp.OBJ, 'get_properties', instance=PERF, properties=['bThrottleCPUWhenNotForeground']))
        await call(movement_mcp.OBJ, 'set_properties', instance=PERF, values=json.dumps({'bThrottleCPUWhenNotForeground': False}))
    try:
        await test.main()
    finally:
        async with movement_mcp.session() as call:
            await call(movement_mcp.OBJ, 'set_properties', instance=PERF, values=json.dumps(before))


test.streamable_http_client = movement_client
test.MAP = MAP
test.OPENING = MAP.endswith('L_Wreckage_Opening')
test.OUT = Path('reports/movement_route_playtest.json')
test.CAPTURE_PREFIX = 'movement_route_'
test.report['map'] = MAP
test.report['driver_timing_scaled_to_walk_speed'] = WALK
test.report['limitations'].append('Run in the integrated main checkout against the current saved map.')
try:
    asyncio.run(run())
except BaseException as error:
    test.report['errors'].append(repr(error))
    test.save()
    raise
