# /// script
# requires-python = ">=3.12"
# dependencies = ["mcp==2.3.0"]
# ///
"""Read-only connection check: initialize, discover, check balance. No generation."""
import asyncio
import json
import tempfile
from pathlib import Path
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

ROOT = Path(__file__).resolve().parents[1]

async def main():
    report = {"connector_version": "0.6.0", "generation_submitted": False, "verified": False}
    params = StdioServerParameters(command="C:/Windows/System32/WindowsPowerShell/v1.0/powershell.exe", args=["-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(ROOT / "tools/start_meshy_mcp.ps1")])
    stage = "starting connector"
    try:
        with tempfile.TemporaryFile(mode="w+", encoding="utf-8") as errors:
            async with stdio_client(params, errlog=errors) as (reader, writer):
                async with ClientSession(reader, writer) as session:
                    stage = "initializing connector"
                    initialized = await session.initialize()
                    report["server_version"] = initialized.server_info.version
                    stage = "discovering tools"
                    available = await session.list_tools()
                    report["tools"] = [tool.name for tool in available.tools]
                    assert "meshy_check_balance" in report["tools"]
                    stage = "checking balance"
                    balance = await session.call_tool("meshy_check_balance", {})
                    if balance.is_error:
                        raise RuntimeError("Balance query rejected")
                    report["balance"] = [c.text for c in balance.content if c.type == "text"]
                    report["verified"] = True
    except Exception as error:
        report["failure_stage"] = stage
        report["failure_type"] = type(error).__name__
        def error_types(e):
            return [type(e).__name__] + [name for child in getattr(e, "exceptions", []) for name in error_types(child)]
        report["failure_types"] = error_types(error)
        def missing_attributes(e):
            own = [e.name] if isinstance(e, AttributeError) and isinstance(e.name, str) else []
            return own + [name for child in getattr(e, "exceptions", []) for name in missing_attributes(child)]
        report["missing_attributes"] = missing_attributes(error)
        report["limitation"] = "Connection or balance verification failed. Check local credential setup and network access; no generation was attempted."
    (ROOT / "reports/meshy_mcp_verification.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    if not report["verified"]:
        raise SystemExit(1)

if __name__ == "__main__":
    asyncio.run(asyncio.wait_for(main(), 60))
