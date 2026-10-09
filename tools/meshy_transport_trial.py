# /// script
# requires-python = ">=3.12"
# dependencies = ["mcp==2.3.0"]
# ///
"""One authorized image submission; later invocations resume without resubmitting."""
import asyncio
import json
import tempfile
from pathlib import Path
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports/meshy_transport_t6_trial.json"
IMAGE = ROOT / "assets/concepts/transports/transport_t6_nano_banana_pro_two_views_v1.png"
PROMPT = "Original military sci-fi troop/cargo dropship: bulky armored cabin, faceted cockpit glass, detailed gray hull, olive markings, rear loading ramp. Moderate straight wings with two integrated engines, bilateral symmetry, landing gear. Fresh design, no franchise logos. Two-view sheet on neutral background: LEFT centered orthographic TOP view, nose up; RIGHT front THREE-QUARTER view of the SAME craft. Match hull, wings, engines and details across views. Realistic game concept art, crisp mechanical detail, entire craft visible in both views. No wreckage or extra views."

def save(report):
    REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")

def data(result):
    if result.is_error:
        raise RuntimeError("Connector operation rejected")
    if result.structured_content:
        return result.structured_content
    for block in result.content:
        if block.type == "text":
            try:
                return json.loads(block.text)
            except json.JSONDecodeError:
                pass
    return {}

async def main():
    assert len(PROMPT) <= 600
    report = json.loads(REPORT.read_text()) if REPORT.exists() else {
        "model": "nano-banana-pro", "task_type": "text-to-image", "prompt": PROMPT,
        "expected_credits": 9, "authorized_images": 1,
    }
    if report.get("local_paths"):
        print(json.dumps({"status": "SAVED", "local_paths": report["local_paths"]}))
        return
    stage = "initializing"
    params = StdioServerParameters(command="C:/Windows/System32/WindowsPowerShell/v1.0/powershell.exe", args=["-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(ROOT / "tools/start_meshy_mcp.ps1")])
    try:
        with tempfile.TemporaryFile(mode="w+", encoding="utf-8") as errors:
            async with stdio_client(params, errlog=errors) as (reader, writer):
                async with ClientSession(reader, writer) as session:
                    await session.initialize()
                    if not report.get("task_id"):
                        if report.get("submission_started"):
                            raise RuntimeError("Submission outcome uncertain; do not resubmit")
                        stage = "balance before"
                        balance = await session.call_tool("meshy_check_balance", {})
                        report["balance_before"] = [b.text for b in balance.content if b.type == "text"]
                        stage = "submitting"
                        report["submission_started"] = True
                        save(report)
                        created = data(await session.call_tool("meshy_text_to_image", {
                            "ai_model": "nano-banana-pro", "prompt": PROMPT,
                            "generate_multi_view": False, "aspect_ratio": "16:9", "response_format": "json",
                        }))
                        report["task_id"] = created["task_id"]
                        report["status"] = created.get("status", "PENDING")
                        save(report)
                        print(json.dumps({"status": report["status"], "submitted_images": 1}), flush=True)
                    stage = "checking progress"
                    progress = data(await session.call_tool("meshy_get_task_status", {
                        "task_id": report["task_id"], "task_type": "text-to-image",
                        "wait": False, "timeout_seconds": 40, "response_format": "json",
                    }))
                    report["status"] = progress.get("status", "UNKNOWN")
                    report["progress"] = progress.get("progress")
                    save(report)
                    if report["status"] == "SUCCEEDED":
                        stage = "saving image"
                        IMAGE.parent.mkdir(parents=True, exist_ok=True)
                        downloaded = data(await session.call_tool("meshy_download_model", {
                            "task_id": report["task_id"], "task_type": "text-to-image", "save_to": str(IMAGE),
                        }))
                        report["local_paths"] = downloaded["local_paths"]
                        stage = "balance after"
                        balance = await session.call_tool("meshy_check_balance", {})
                        report["balance_after"] = [b.text for b in balance.content if b.type == "text"]
                        report.pop("failure_stage", None)
                        report.pop("failure_type", None)
                        save(report)
                    print(json.dumps({k: report[k] for k in ("status", "progress", "local_paths", "balance_before", "balance_after") if k in report}), flush=True)
    except Exception as error:
        report["failure_stage"] = stage
        report["failure_type"] = type(error).__name__
        def types(e):
            return [type(e).__name__] + [t for child in getattr(e, "exceptions", []) for t in types(child)]
        report["failure_types"] = types(error)
        save(report)
        print(json.dumps({"failure_stage": stage, "failure_types": types(error), "submitted": bool(report.get("task_id"))}), flush=True)
        raise SystemExit(1)

if __name__ == "__main__":
    asyncio.run(main())
