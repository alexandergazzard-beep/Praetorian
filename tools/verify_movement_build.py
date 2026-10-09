"""Editor-Python check that a rebuilt player Blueprint carries the movement profile and LookSensitivity.

Run with UnrealEditor-Cmd -run=pythonscript -script=<this file> after build_wreckage_gameplay.py.
Writes Saved/movement_build_verification.json; read-only apart from that report.
"""
import json
import sys
from pathlib import Path
import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as BP

sys.path.insert(0, str(Path(__file__).parent))
from movement_profiles import ACTIVE_PROFILE, PROFILES

NAMES = {'MaxWalkSpeed': 'max_walk_speed', 'MaxWalkSpeedCrouched': 'max_walk_speed_crouched', 'MaxAcceleration': 'max_acceleration',
         'JumpZVelocity': 'jump_z_velocity', 'GravityScale': 'gravity_scale', 'AirControl': 'air_control'}
player = unreal.load_asset('/Game/WreckagePrototype/Blueprints/BP_WreckagePlayer_Runtime')
cdo = BP.get_default_object(player)
move = cdo.character_movement
values = {k: move.get_editor_property(v) for k, v in NAMES.items()}
graph = BP.get_graph(player, 'EventGraph')
report = {'profile': ACTIVE_PROFILE, 'values': values,
          'matches_profile': all(abs(values[k] - v) < 1e-3 for k, v in PROFILES[ACTIVE_PROFILE].items()),
          'look_sensitivity': cdo.get_editor_property('LookSensitivity'),
          'event_graph_nodes': len(BP.find_nodes(graph, '')),
          }
# The DSL view follows the exec-connected chain, i.e. the code that actually runs each tick.
dsl = BP.read_graph_dsl(graph)
look_lines = [line.strip() for line in dsl.splitlines() if 'AddControllerYawInput' in line or 'AddControllerPitchInput' in line]
report['active_look_lines'] = look_lines
report['active_look_uses_sensitivity'] = bool(look_lines) and all('GetLookSensitivity' in line for line in look_lines)
try:
    BP.compile_blueprint(player, True)
    report['compiled_warnings_as_errors'] = True
except Exception as error:  # report rather than hide a compile failure
    report['compiled_warnings_as_errors'] = False
    report['compile_error'] = str(error)
(Path(unreal.Paths.project_saved_dir()) / 'movement_build_verification.json').write_text(json.dumps(report, indent=2))
