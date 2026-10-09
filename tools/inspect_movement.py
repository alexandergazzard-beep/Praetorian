# /// script
# requires-python = ">=3.12"
# dependencies = ["mcp==2.3.0"]
# ///
"""Inspect the player's movement defaults (movement editor only).

Usage: uv run tools/inspect_movement.py [report-name.json] [--dsl]
--dsl also dumps the EventGraph. Note: the editor's read_graph_dsl tool marks the Blueprint as modified,
so with --dsl the asset shows unsaved changes afterwards (content is unchanged; choose Don't Save).
"""
import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from movement_mcp import ROOT, ASSET, BPT, OBJ, SCENE, EDITOR, session
from movement_profiles import MOVEMENT_FIELDS, CAPSULE_FIELDS, PLAYER_BP

ARGS = [a for a in sys.argv[1:] if not a.startswith('--')]
OUT = ROOT / 'reports' / (ARGS[0] if ARGS else 'movement_inspection.json')


async def main():
    async with session() as call:
        bp = {'refPath': PLAYER_BP}
        cdo = await call(BPT, 'get_default_object', blueprint=bp)
        cdo_props = json.loads(await call(OBJ, 'get_properties', instance=cdo,
                                          properties=['CharacterMovement', 'CapsuleComponent', 'bUseControllerRotationYaw',
                                                      'JumpMaxHoldTime', 'JumpMaxCount']))
        move = json.loads(await call(OBJ, 'get_properties', instance=cdo_props['CharacterMovement'], properties=MOVEMENT_FIELDS))
        capsule = json.loads(await call(OBJ, 'get_properties', instance=cdo_props['CapsuleComponent'], properties=CAPSULE_FIELDS))
        variables = await call(BPT, 'list_variables', blueprint=bp)
        dsl = None
        if '--dsl' in sys.argv:
            graph = await call(BPT, 'get_graph', blueprint=bp, graph_name='EventGraph')
            dsl = await call(BPT, 'read_graph_dsl', graph=graph)
        report = {'verified_target': call.verified, 'cdo': cdo, 'cdo_properties': cdo_props,
                  'character_movement': move, 'capsule': capsule, 'variables': variables,
                  'current_level': await call(SCENE, 'get_current_level'), 'pie_running': await call(EDITOR, 'IsPIERunning'),
                  'player_blueprint_dirty': await call(ASSET, 'is_dirty', asset_path=PLAYER_BP.split('.')[0]),
                  'event_graph_dsl': dsl}
        OUT.write_text(json.dumps(report, indent=2), encoding='utf-8')
        print(json.dumps({k: v for k, v in report.items() if k != 'event_graph_dsl'}, indent=2)[:6000])


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    asyncio.run(main())
