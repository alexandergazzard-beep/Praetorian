# /// script
# requires-python = ">=3.12"
# dependencies = ["mcp==2.3.0"]
# ///
"""Inspect or call the local Unreal MCP endpoint; calls run sequentially."""
import asyncio
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client


async def main():
    async with streamable_http_client("http://127.0.0.1:8000/mcp") as (reader, writer):
        async with ClientSession(reader, writer) as session:
            initialized = await session.initialize()
            if len(sys.argv) > 1:
                raw = sys.argv[2] if len(sys.argv) > 2 else "{}"
                args = json.loads(Path(raw[1:]).read_text(encoding="utf-8") if raw.startswith("@") else raw)
                result = await session.call_tool(sys.argv[1], args)
                Path("reports/unreal_last_tool_result.json").write_text(result.model_dump_json(indent=2), encoding="utf-8")
                for item in result.content:
                    if hasattr(item, "text"):
                        print(item.text)
                if result.is_error:
                    raise RuntimeError("Unreal tool returned an error")
            else:
                available = await session.list_tools()
                report = {
                    "server": initialized.model_dump(mode="json"),
                    "tools": available.model_dump(mode="json"),
                    "verified": "MCP initialization and tool discovery only",
                }
                target = Path(__file__).resolve().parents[1] / "reports/unreal_mcp_verification.json"
                target.write_text(json.dumps(report, indent=2), encoding="utf-8")
                print(json.dumps(report, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
