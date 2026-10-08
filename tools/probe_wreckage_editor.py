"""Read editor APIs from a separate Unreal Python commandlet; no asset writes."""
import json
from pathlib import Path
import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools
result = {
    "version": unreal.SystemLibrary.get_engine_version(),
    "level_subsystem": [n for n in dir(unreal.LevelEditorSubsystem) if 'level' in n],
    "graph_api": [n for n in dir(unreal.BlueprintEditorLibrary) if 'graph' in n or 'variable' in n],
    "mount_api": [n for n in dir(unreal) if 'ackage' in n or 'eaturePack' in n],
    "python_import": str(BlueprintTools),
}
Path(unreal.Paths.project_saved_dir(), 'wreckage_editor_probe.json').write_text(json.dumps(result, indent=2))
