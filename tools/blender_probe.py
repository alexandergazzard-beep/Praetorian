"""Read-only Blender inventory for the AI connection setup."""
import json
from pathlib import Path
import bpy

root = Path(__file__).resolve().parents[1]
report = {
    "blender_version": bpy.app.version_string,
    "background": bpy.app.background,
    "scene_name": bpy.context.scene.name,
    "objects": [{"name": obj.name, "type": obj.type} for obj in bpy.context.scene.objects],
    "mcp_addon_enabled": "blender_mcp" in bpy.context.preferences.addons,
}
output = root / "reports" / "blender_probe.json"
output.parent.mkdir(exist_ok=True)
output.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report))
