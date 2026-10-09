"""Run the existing Meshy launcher with sanitized stderr classification only."""
import subprocess,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=subprocess.run(['C:/Windows/System32/WindowsPowerShell/v1.0/powershell.exe','-NoProfile','-ExecutionPolicy','Bypass','-File',str(ROOT/'tools/start_meshy_mcp.ps1')],input='',capture_output=True,text=True,timeout=20)
s=p.stderr.lower()
print(json.dumps({'exit_code':p.returncode,'markers':{v:v in s for v in ['key not configured','cryptographicexception','cannot be used in this state','protecteddata','cannot find','type data','module','invalid api key','401','403','api-key','node','connection','access denied']},'stdout_bytes':len(p.stdout),'stderr_bytes':len(s)}))
