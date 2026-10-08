param([string]$Tool, [string]$ArgumentFile, [string]$EvidenceName)
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
$outPath = Join-Path $projectRoot "reports/$EvidenceName.stdout.txt"
$errPath = Join-Path $projectRoot "reports/$EvidenceName.stderr.txt"
$callArgs = @('run', 'tools/unreal_mcp.py', $Tool, "@$ArgumentFile")
$client = Start-Process -FilePath 'C:/Users/alexa/AppData/Local/Programs/Python/Python312/Scripts/uv.exe' -ArgumentList $callArgs -WorkingDirectory $projectRoot -WindowStyle Hidden -RedirectStandardOutput $outPath -RedirectStandardError $errPath -PassThru
if (-not $client.WaitForExit(25000)) { Write-Output "Pending client PID $($client.Id); inspect $outPath before another call."; exit 2 }
Get-Content -LiteralPath $outPath
Get-Content -LiteralPath $errPath
exit $client.ExitCode
