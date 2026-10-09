# /// script
# requires-python = ">=3.12"
# dependencies = ["mcp==2.3.0"]
# ///
"""Apply a movement profile to BP_WreckagePlayer_Runtime in the main editor (port 8000 only).

Usage: uv run tools/apply_movement_tuning.py [reach|original|halo3] [--dry-run]

Reversible: `original` restores the saved pre-tuning CharacterMovement values. The LookSensitivity
variable stays (default 0.6 reproduces the original hard-coded look multiplier exactly).
Only the player Blueprint is saved; maps and environment assets are never saved by this script.
"""
import asyncio
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from movement_mcp import ROOT, ASSET, BPT, OBJ, EDITOR, session
from movement_profiles import ACTIVE_PROFILE, LOOK_SENSITIVITY_DEFAULT, MOVEMENT_FIELDS, PLAYER_BP, PROFILES

ASSET_PATH = PLAYER_BP.split('.')[0]
LOOK_CALLS = {'Pawn|Input|AddControllerYawInput': 1.0, 'Pawn|Input|AddControllerPitchInput': -1.0}


def short(ref):
    return ref['refPath'].split('.')[-1]


async def look_multipliers(call, graph):
    """Multiply nodes feeding mouse delta into yaw/pitch, restricted to exec-reachable look calls."""
    nodes = await call(BPT, 'find_nodes', graph=graph, title='')
    infos = {n['node']['refPath']: n for n in await call(BPT, 'get_node_infos', nodes=nodes)}
    entries = await call(BPT, 'find_nodes', graph=graph, title='', entry_points_only=True)
    reachable, stack = set(), [e['refPath'] for e in entries]
    while stack:
        ref = stack.pop()
        if ref in reachable or ref not in infos:
            continue
        reachable.add(ref)
        for pin in infos[ref]['output_pins']:
            if pin['type_id'] == 'Exec':
                stack += [c['node']['refPath'] for c in pin['connected_pins']]
    found = []
    for ref in reachable:
        sign = LOOK_CALLS.get(infos[ref]['type_id'])
        if sign is None:
            continue
        frontier, seen = [ref], set()
        for _ in range(3):  # Val <- (+) <- (*) : the multiply sits at most a few data hops upstream
            nxt = []
            for r in frontier:
                for pin in infos[r]['input_pins']:
                    if pin['type_id'] == 'Exec':
                        continue
                    for c in pin['connected_pins']:
                        src = c['node']['refPath']
                        if src in seen:
                            continue
                        seen.add(src)
                        nxt.append(src)
                        sources = [infos[x['node']['refPath']]['type_id'] for p in infos[src]['input_pins'] for x in p['connected_pins']]
                        if infos[src]['type_id'] == 'Math|Float|float*float' and 'Game|Player|GetInputMouseDelta' in sources:
                            found.append({'call': ref, 'sign': sign, 'multiply': src})
            frontier = nxt
    return found, infos, len(reachable), len(infos)


async def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    profile_name = args[0] if args else ACTIVE_PROFILE
    dry_run = '--dry-run' in sys.argv
    target = PROFILES[profile_name]
    report = {'profile': profile_name, 'target': target, 'dry_run': dry_run, 'steps': []}
    async with session() as call:
        report['verified_target'] = call.verified
        if await call(EDITOR, 'IsPIERunning'):
            raise SystemExit('PIE is running in the main editor; stop it before editing.')
        bp = {'refPath': PLAYER_BP}
        cdo = await call(BPT, 'get_default_object', blueprint=bp)
        move = json.loads(await call(OBJ, 'get_properties', instance=cdo, properties=['CharacterMovement']))['CharacterMovement']
        before = json.loads(await call(OBJ, 'get_properties', instance=move, properties=MOVEMENT_FIELDS))
        report['before'] = before
        original_file = ROOT / 'reports' / 'movement_original_settings.json'
        if not original_file.exists():
            original_file.write_text(json.dumps({'asset': PLAYER_BP, 'character_movement': before,
                                                 'look_multiplier': {'yaw': 0.6, 'pitch': -0.6}}, indent=2), encoding='utf-8')
        if dry_run:
            print(json.dumps(report, indent=2))
            return

        await call(OBJ, 'set_properties', instance=move, values=json.dumps(target))
        report['steps'].append('Set CharacterMovement defaults on the Blueprint class default object')

        if 'LookSensitivity' not in await call(BPT, 'list_variables', blueprint=bp):
            await call(BPT, 'add_variable', blueprint=bp, name='LookSensitivity', type_name='float')
            await call(BPT, 'compile_blueprint', blueprint=bp)
            cdo = await call(BPT, 'get_default_object', blueprint=bp)
            await call(OBJ, 'set_properties', instance=cdo, values=json.dumps({'LookSensitivity': LOOK_SENSITIVITY_DEFAULT}))
            report['steps'].append('Added float LookSensitivity (default 0.6)')
        await call(BPT, 'set_variable_instance_editable', blueprint=bp, variable_name='LookSensitivity', instance_editable=True)

        graph = await call(BPT, 'get_graph', blueprint=bp, graph_name='EventGraph')
        found, infos, reachable, total = await look_multipliers(call, graph)
        report['graph'] = {'nodes': total, 'exec_reachable': reachable, 'look_multipliers': found}
        if len(found) != 2:
            raise SystemExit(f'Expected one yaw and one pitch mouse multiplier, found {found}')
        getter_type = None
        for item in found:
            mul = infos[item['multiply']]
            sources = {x['node']['refPath']: infos[x['node']['refPath']] for p in mul['input_pins'] for x in p['connected_pins']}
            if any(s['type_id'].endswith('GetLookSensitivity') for s in sources.values()):
                report['steps'].append(f"{short(mul['node'])} already scaled by LookSensitivity")
                continue
            literal = next(s for s in sources.values() if s['type_id'] == 'Math|Float|MakeLiteralFloat')
            old = float(literal['input_pins'][0]['value'])
            assert math.isclose(abs(old), LOOK_SENSITIVITY_DEFAULT, rel_tol=1e-6), old
            await call(BPT, 'set_pin_value', pin=literal['input_pins'][0]['pin_id'], value=str(item['sign']))
            if getter_type is None:
                types = await call(BPT, 'find_node_types', graph=graph, type_id_filter='GetLookSensitivity', context_pins=[])
                getter_type = next(t if isinstance(t, str) else t.get('type_id') for t in types)
            pos = {'x': mul['position']['x'], 'y': mul['position']['y'] + 160}
            getter = await call(BPT, 'create_node', graph=graph, type_id=getter_type, pos=pos)
            getter_out = (await call(BPT, 'get_node_infos', nodes=[getter]))[0]['output_pins'][0]['pin_id']
            new_pin = await call(BPT, 'add_node_pin', node=mul['node'])
            await call(BPT, 'connect_pins', output_pin=getter_out, input_pin=new_pin)
            report['steps'].append(f"{short(mul['node'])}: literal {old} -> {item['sign']}, added x LookSensitivity")

        await call(BPT, 'compile_blueprint', blueprint=bp, warnings_as_errors=True)
        cdo = await call(BPT, 'get_default_object', blueprint=bp)
        move = json.loads(await call(OBJ, 'get_properties', instance=cdo, properties=['CharacterMovement']))['CharacterMovement']
        after = json.loads(await call(OBJ, 'get_properties', instance=move, properties=MOVEMENT_FIELDS))
        look = json.loads(await call(OBJ, 'get_properties', instance=cdo, properties=['LookSensitivity']))
        mismatches = {k: (v, after[k]) for k, v in target.items() if not math.isclose(float(after[k]), float(v), rel_tol=1e-4)}
        report.update({'after': after, 'look': look, 'mismatches': mismatches})
        if mismatches:
            raise SystemExit(f'Read-back mismatch: {mismatches}')
        assert await call(ASSET, 'save_assets', asset_paths=[ASSET_PATH])
        report['saved'] = ASSET_PATH
        report['dirty_after_save'] = await call(ASSET, 'is_dirty', asset_path=ASSET_PATH)
    out = ROOT / 'reports' / f'movement_apply_{profile_name}.json'
    out.write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps({k: report[k] for k in ['profile', 'steps', 'mismatches', 'saved', 'dirty_after_save', 'look']}, indent=2))


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    asyncio.run(main())
