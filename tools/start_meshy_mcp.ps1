# Official connector; secret stays outside the project and is decrypted only at launch.
$ErrorActionPreference = 'Stop'
[Reflection.Assembly]::LoadWithPartialName('System.Security') | Out-Null
$credentialPath = Join-Path $env:LOCALAPPDATA 'LostVanguard/Meshy/api-key.dpapi'
$aesCredentialPath = Join-Path $env:LOCALAPPDATA 'LostVanguard/Meshy/api-key.aes'
$encryptionKeyPath = Join-Path $env:LOCALAPPDATA 'LostVanguard/Meshy/encryption-key.bin'
if (Test-Path -LiteralPath $aesCredentialPath) { $credentialPath = $aesCredentialPath }
if (-not (Test-Path -LiteralPath $credentialPath)) {
    [Console]::Error.WriteLine('Meshy key not configured. Complete the local masked-key setup first.')
    exit 2
}
$projectRoot = Split-Path $PSScriptRoot -Parent
$serverPath = Join-Path $projectRoot 'tmp/meshy-connector/node_modules/@meshy-ai/meshy-mcp-server/dist/index.js'
if (-not (Test-Path -LiteralPath $serverPath)) {
    [Console]::Error.WriteLine('Official Meshy connector package missing. Reinstall pinned package 0.6.0.')
    exit 3
}
$plainBytes = $null
$encryptionKey = $null
$secureKey = $null
$keyPointer = [IntPtr]::Zero
try {
    if ($credentialPath -eq $aesCredentialPath) {
        Import-Module Microsoft.PowerShell.Security -ErrorAction Stop
        $encryptionKey = [IO.File]::ReadAllBytes($encryptionKeyPath)
        $secureKey = Microsoft.PowerShell.Security\ConvertTo-SecureString ([IO.File]::ReadAllText($credentialPath)) -Key $encryptionKey
        $keyPointer = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secureKey)
        $env:MESHY_API_KEY = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($keyPointer)
    } else {
    # ConvertFrom-SecureString's default DPAPI format is a hexadecimal blob.
    # Use the Windows API directly to avoid module type-data conflicts in child processes.
    $encryptedHex = [IO.File]::ReadAllText($credentialPath).Trim()
    $encryptedBytes = New-Object byte[] ($encryptedHex.Length / 2)
    for ($index = 0; $index -lt $encryptedBytes.Length; $index++) {
        $encryptedBytes[$index] = [Convert]::ToByte($encryptedHex.Substring($index * 2, 2), 16)
    }
    $plainBytes = [Security.Cryptography.ProtectedData]::Unprotect($encryptedBytes, $null, [Security.Cryptography.DataProtectionScope]::CurrentUser)
    $env:MESHY_API_KEY = [Text.Encoding]::Unicode.GetString($plainBytes)
    }
    $env:TRANSPORT = 'stdio'
    & 'C:/Program Files/nodejs/node.exe' $serverPath
    $connectorExitCode = $LASTEXITCODE
} catch {
    [Console]::Error.WriteLine('Meshy local credential/launcher failure: ' + $_.Exception.GetType().Name)
    $connectorExitCode = 4
} finally {
    $env:MESHY_API_KEY = $null
    if ($plainBytes) { [Array]::Clear($plainBytes, 0, $plainBytes.Length) }
    if ($keyPointer -ne [IntPtr]::Zero) { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($keyPointer) }
    if ($secureKey) { $secureKey.Dispose() }
    if ($encryptionKey) { [Array]::Clear($encryptionKey, 0, $encryptionKey.Length) }
}
exit $connectorExitCode
