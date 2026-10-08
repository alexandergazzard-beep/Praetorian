param([string]$Script = 'build_wreckage.py', [string]$Log = 'WreckageBuild.log')
$projectRoot=Split-Path $PSScriptRoot -Parent
$project=(Join-Path $projectRoot 'Unreal/LostVanguard/LostVanguard.uproject').Replace('\','/')
$source=(Join-Path $PSScriptRoot $Script).Replace('\','/')
$arguments='"'+$project+'" -run=pythonscript -script="'+$source+'" -unattended -nosplash -nullrhi -log='+$Log
Start-Process -FilePath 'C:/Program Files/Epic Games/UE_5.8/Engine/Binaries/Win64/UnrealEditor-Cmd.exe' -ArgumentList $arguments -WorkingDirectory $projectRoot -WindowStyle Hidden -PassThru | Select-Object Id
