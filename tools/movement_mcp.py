# /// script
# requires-python = ">=3.12"
# dependencies = ["mcp==2.3.0"]
# ///
"""Guarded MCP session for the integrated main editor (main checkout, port 8000).

Every session verifies two independent facts before any editor call is allowed:
1. The process listening on the port was launched with this checkout's .uproject.
2. The editor can read this checkout's private marker token from its own Saved/ folder.
If either check fails the session aborts, so no mutation can reach Codex's editor (port 8000).
"""
import asyncio
import contextlib
import json
import subprocess
import sys
from pathlib import Path

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

ROOT = Path(__file__).resolve().parents[1]
PROJECT_DIR = ROOT / 'Unreal' / 'LostVanguard 5.8'
UPROJECT = PROJECT_DIR / 'LostVanguard.uproject'
MARKER = PROJECT_DIR / 'Saved' / 'movement_checkout_marker.json'
PORT = 8000
URL = f'http://127.0.0.1:{PORT}/mcp'

SCENE = 'editor_toolset.toolsets.scene.SceneTools'
OBJ = 'editor_toolset.toolsets.object.ObjectTools'
ACTOR = 'editor_toolset.toolsets.actor.ActorTools'
ASSET = 'editor_toolset.toolsets.asset.AssetTools'
BPT = 'editor_toolset.toolsets.blueprint.BlueprintTools'
EDITOR = 'EditorToolset.EditorAppToolset'


def listener_command_line(port=PORT):
    """Return the command line of the process listening on 127.0.0.1:<port>."""
    script = (f"$c=Get-NetTCPConnection -LocalAddress 127.0.0.1 -LocalPort {port} -State Listen -ErrorAction Stop;"
              "(Get-CimInstance Win32_Process -Filter \"ProcessId=$($c[0].OwningProcess)\").CommandLine")
    out = subprocess.run(['powershell.exe', '-NoProfile', '-Command', script], capture_output=True, text=True, timeout=30)
    return out.stdout.strip()


def norm(text):
    return text.replace('\\', '/').lower()


@contextlib.asynccontextmanager
async def session(timeout=60):
    cmd = listener_command_line()
    if norm(str(UPROJECT)) not in norm(cmd):
        raise SystemExit(f'Port {PORT} is not the movement checkout editor. Listener command line: {cmd!r}')
    token = json.loads(MARKER.read_text(encoding='utf-8'))['token']
    async with streamable_http_client(URL) as (reader, writer):
        async with ClientSession(reader, writer) as s:
            await s.initialize()

            async def call(toolset, tool, timeout_s=timeout, **args):
                result = await asyncio.wait_for(
                    s.call_tool('call_tool', {'toolset_name': toolset, 'tool_name': tool, 'arguments': args}), timeout_s)
                if result.is_error:
                    raise RuntimeError(f'{tool}: {result.content}')
                if result.content and result.content[0].type == 'text':
                    return json.loads(result.content[0].text).get('returnValue')
                return None

            seen = await call(ASSET, 'read_file', file_path=str(MARKER).replace('\\', '/'))
            if token not in str(seen):
                raise SystemExit('Editor could not read this checkout marker; targeting is ambiguous. No calls made.')
            call.raw = s
            call.verified = {'port': PORT, 'listener': cmd, 'marker_token_matched': True}
            yield call


async def _cli():
    async with session() as call:
        print(json.dumps(call.verified, indent=2))
        if len(sys.argv) > 1 and sys.argv[1] == 'toolsets':
            listed = await call.raw.call_tool('list_toolsets', {})
            out = ROOT / 'reports' / 'movement_mcp_toolsets.json'
            out.write_text(listed.model_dump_json(indent=2), encoding='utf-8')
            print(listed.content[0].text[:6000])
        elif len(sys.argv) > 2 and sys.argv[1] == 'describe':
            described = await call.raw.call_tool('describe_toolset', {'toolset_name': sys.argv[2]})
            out = ROOT / 'reports' / ('movement_schema_' + sys.argv[2].split('.')[-1] + '.json')
            out.write_text(described.model_dump_json(indent=2), encoding='utf-8')
            print(out)


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    asyncio.run(_cli())
