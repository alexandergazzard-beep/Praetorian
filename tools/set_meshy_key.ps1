# User-operated masked entry. Never print the key or put it in project records.
$ErrorActionPreference = 'Stop'
# Load encryption commands before entering the Windows Forms event callback.
Import-Module Microsoft.PowerShell.Security -ErrorAction Stop
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
$form = New-Object System.Windows.Forms.Form
$form.Text = 'Connect Meshy to Lost Vanguard'
$form.ClientSize = New-Object System.Drawing.Size(490,180)
$form.StartPosition = 'CenterScreen'
$form.FormBorderStyle = 'FixedDialog'
$form.MaximizeBox = $false
$label = New-Object System.Windows.Forms.Label
$label.Text = "Paste your Meshy API key below. Encrypted files stay in your local user folder.`nNo generation or credit purchase will be submitted."
$label.Location = New-Object System.Drawing.Point(15,15)
$label.Size = New-Object System.Drawing.Size(455,45)
$entry = New-Object System.Windows.Forms.TextBox
$entry.Location = New-Object System.Drawing.Point(15,70)
$entry.Size = New-Object System.Drawing.Size(455,25)
$entry.UseSystemPasswordChar = $true
$save = New-Object System.Windows.Forms.Button
$save.Text = 'Save key'
$save.Location = New-Object System.Drawing.Point(275,120)
$save.Size = New-Object System.Drawing.Size(95,30)
$cancel = New-Object System.Windows.Forms.Button
$cancel.Text = 'Cancel'
$cancel.Location = New-Object System.Drawing.Point(375,120)
$cancel.Size = New-Object System.Drawing.Size(95,30)
$cancel.DialogResult = [System.Windows.Forms.DialogResult]::Cancel
$form.CancelButton = $cancel
$form.AcceptButton = $save
$save.Add_Click({
    if ([string]::IsNullOrWhiteSpace($entry.Text)) { return }
    $credentialDirectory = Join-Path $env:LOCALAPPDATA 'LostVanguard/Meshy'
    $credentialPath = Join-Path $credentialDirectory 'api-key.aes'
    $encryptionKeyPath = Join-Path $credentialDirectory 'encryption-key.bin'
    $saveStage = 'restricting local file access'
    $secret = $null
    $encryptionKey = $null
    try {
        [IO.Directory]::CreateDirectory($credentialDirectory) | Out-Null
        $folderSecurity = New-Object Security.AccessControl.DirectorySecurity
        $folderSecurity.SetAccessRuleProtection($true, $false)
        $ownerSid = [Security.Principal.WindowsIdentity]::GetCurrent().User
        $folderSecurity.SetOwner($ownerSid)
        foreach ($allowedSid in @($ownerSid, (New-Object Security.Principal.SecurityIdentifier('S-1-5-18')))) {
            $accessRule = New-Object Security.AccessControl.FileSystemAccessRule($allowedSid, 'FullControl', 'ContainerInherit,ObjectInherit', 'None', 'Allow')
            $folderSecurity.AddAccessRule($accessRule)
        }
        [IO.Directory]::SetAccessControl($credentialDirectory, $folderSecurity)
        $saveStage = 'preparing local encryption'
        if ([IO.File]::Exists($encryptionKeyPath)) {
            $encryptionKey = [IO.File]::ReadAllBytes($encryptionKeyPath)
            if ($encryptionKey.Length -ne 32) { throw 'Unexpected local encryption key length.' }
        } else {
            $encryptionKey = New-Object byte[] 32
            $random = [Security.Cryptography.RandomNumberGenerator]::Create()
            try { $random.GetBytes($encryptionKey) } finally { $random.Dispose() }
            [IO.File]::WriteAllBytes($encryptionKeyPath, $encryptionKey)
        }
        $saveStage = 'encrypting the key'
        $secret = Microsoft.PowerShell.Security\ConvertTo-SecureString ($entry.Text.Trim()) -AsPlainText -Force
        $encrypted = Microsoft.PowerShell.Security\ConvertFrom-SecureString $secret -Key $encryptionKey
        $saveStage = 'writing the encrypted key'
        [IO.File]::WriteAllText($credentialPath, $encrypted)
        $saveStage = 'checking the encrypted file'
        $readback = Microsoft.PowerShell.Security\ConvertTo-SecureString ([IO.File]::ReadAllText($credentialPath)) -Key $encryptionKey
        $readback.Dispose()
        $entry.Clear()
        $form.DialogResult = [System.Windows.Forms.DialogResult]::OK
        $form.Close()
    } catch {
        # Only report the operation and exception type; never expose exception text or key.
        $failureType = $_.Exception.GetType().Name
        [System.Windows.Forms.MessageBox]::Show("Local key saving failed while $saveStage ($failureType).`nThis is a storage check, not a Meshy connection test. You can retry Save key.", 'Meshy setup') | Out-Null
    } finally {
        if ($secret) { $secret.Dispose() }
        if ($encryptionKey) { [Array]::Clear($encryptionKey, 0, $encryptionKey.Length) }
    }
})
$form.Controls.AddRange(@($label,$entry,$save,$cancel))
$result = $form.ShowDialog()
$entry.Clear()
$form.Dispose()
if ($result -eq [System.Windows.Forms.DialogResult]::OK) { Write-Output 'Meshy key saved locally with encryption and restricted file access.' } else { Write-Output 'Meshy key setup cancelled.' }
