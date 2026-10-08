"""Verify MCP discovery and a read-only live Blender scene query."""
import asyncio
import json
import os
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    uvx = Path(os.environ["LOCALAPPDATA"]) / "Programs/Python/Python312/Scripts/uvx.exe"
    env = dict(os.environ, DISABLE_TELEMETRY="true")
    params = StdioServerParameters(
        command=str(uvx),
        args=["--from", "mcp-for-blender==2.1.9", "mcp-for-blender"],
        env=env,
    )
    async with stdio_client(params) as (reader, writer):
        async with ClientSession(reader, writer) as session:
            initialized = await session.initialize()
            available = await session.list_tools()
            names = [tool.name for tool in available.tools]
            if "get_scene_info" not in names:
                raise RuntimeError(f"Expected scene inspection tool missing; available: {names}")
            result = await session.call_tool("get_scene_info", {})
            content = [item.text for item in result.content if hasattr(item, "text")]
            failed = getattr(result, "is_error", getattr(result, "isError", False))
            if failed:
                raise RuntimeError(f"Scene query failed: {content}")
            report = {
                "server": getattr(initialized, "server_info", getattr(initialized, "serverInfo", None)).model_dump(mode="json"),
                "tools": names,
                "scene_query": content,
                "verified": "MCP initialization, tool discovery, and read-only live scene query",
            }
            if "--write-test" in sys.argv:
                target = Path(__file__).resolve().parents[1] / "reports/blender_connection_test.blend"
                code = f'''import bpy, json, uuid
before = len(bpy.data.objects)
mesh = bpy.data.meshes.new("AI_CONNECTION_TEST_" + uuid.uuid4().hex)
marker = bpy.data.objects.new(mesh.name, mesh)
try:
    mesh.from_pydata([(0,0,0),(1,0,0),(0,1,0)], [], [(0,1,2)])
    bpy.context.scene.collection.objects.link(marker)
    marker.location = (1,2,3)
    assert tuple(marker.location) == (1,2,3)
    bpy.ops.wm.save_as_mainfile(filepath={str(target)!r}, copy=True)
finally:
    bpy.data.objects.remove(marker, do_unlink=True)
    bpy.data.meshes.remove(mesh)
assert len(bpy.data.objects) == before
print(json.dumps({{"created_moved_saved_removed": True, "scene_object_count_restored": before}}))
'''
                changed = await session.call_tool("execute_blender_code", {"code": code})
                if getattr(changed, "is_error", getattr(changed, "isError", False)):
                    raise RuntimeError(str(changed))
                if not target.is_file():
                    raise RuntimeError("Blender did not save the test copy")
                report["write_test"] = [item.text for item in changed.content if hasattr(item, "text")]
                report["test_scene_copy"] = str(target)
                report["verified"] += "; temporary mesh creation/transform, save copy, and cleanup"
            output = Path(__file__).resolve().parents[1] / "reports/blender_mcp_verification.json"
            output.parent.mkdir(exist_ok=True)
            output.write_text(json.dumps(report, indent=2), encoding="utf-8")
            print(json.dumps(report))


if __name__ == "__main__":
    asyncio.run(main())
