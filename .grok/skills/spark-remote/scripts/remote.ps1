param(
    [string]$Script,
    [switch]$Status,
    [int]$ConnectTimeout = 25
)

$ErrorActionPreference = "Stop"
$UserSecret = Join-Path $env:USERPROFILE ".grok\secrets\spark-remote.env"
$SkillDir = Split-Path $PSScriptRoot -Parent
$GrokDir = Split-Path (Split-Path $SkillDir -Parent) -Parent
$ProjectSecret = Join-Path $GrokDir "secrets\spark-remote.env"

function Import-SecretFile {
    param($Path, $Cfg)
    if (-not (Test-Path $Path)) { return }
    Get-Content -LiteralPath $Path | ForEach-Object {
        $line = $_.Trim()
        if ($line -eq "" -or $line.StartsWith("#") -or ($line -notmatch "=")) { return }
        $parts = $line.Split("=", 2)
        $k = $parts[0].Trim()
        $v = $parts[1].Trim()
        switch ($k) {
            "SPARK_SSH_HOST" { $Cfg.Host = $v }
            "SPARK_SSH_PORT" { $Cfg.Port = $v }
            "SPARK_SSH_USER" { $Cfg.User = $v }
            "SPARK_SSH_PASS" { $Cfg.Pass = $v }
        }
    }
}

function Get-SparkConfig {
    $cfg = @{
        Host = "16.tcp.cpolar.top"
        Port = "13938"
        User = "rowsen"
        Pass = ""
    }
    Import-SecretFile -Path $UserSecret -Cfg $cfg
    Import-SecretFile -Path $ProjectSecret -Cfg $cfg
    if ($env:SPARK_SSH_HOST) { $cfg.Host = $env:SPARK_SSH_HOST }
    if ($env:SPARK_SSH_PORT) { $cfg.Port = $env:SPARK_SSH_PORT }
    if ($env:SPARK_SSH_USER) { $cfg.User = $env:SPARK_SSH_USER }
    if ($env:SPARK_SSH_PASS) { $cfg.Pass = $env:SPARK_SSH_PASS }
    if ([string]::IsNullOrWhiteSpace($cfg.Pass)) {
        throw "Missing SPARK_SSH_PASS. Write it to $UserSecret (preferred) or $ProjectSecret"
    }
    return $cfg
}

function Get-GitSsh {
    $git = "C:\Program Files\Git\usr\bin\ssh.exe"
    if (Test-Path $git) { return $git }
    $cmd = Get-Command ssh.exe -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd.Source }
    throw "ssh.exe not found"
}

$StatusScript = @"
hostname
whoami
pwd
date
uname -a
"@

if ($Status) {
    $body = $StatusScript
} elseif ($PSBoundParameters.ContainsKey("Script") -and $Script -ne "") {
    $body = $Script
} else {
    $body = [Console]::In.ReadToEnd()
}
if ([string]::IsNullOrWhiteSpace($body)) {
    throw "No remote command. Use -Script, pipeline, or -Status"
}
$body = $body -replace "`r`n", "`n" -replace "`r", "`n"

$cfg = Get-SparkConfig
$ssh = Get-GitSsh
$ask = Join-Path $env:TEMP ("spark_ssh_askpass_{0}.cmd" -f $PID)
$oldAsk = $env:SSH_ASKPASS
$oldReq = $env:SSH_ASKPASS_REQUIRE
$oldDisp = $env:DISPLAY
try {
    Set-Content -LiteralPath $ask -Value ("@echo off`r`necho {0}`r`n" -f $cfg.Pass) -Encoding ASCII
    $env:SSH_ASKPASS = $ask
    $env:SSH_ASKPASS_REQUIRE = "force"
    $env:DISPLAY = "dummy"
    $target = "{0}@{1}" -f $cfg.User, $cfg.Host
    $cto = "ConnectTimeout={0}" -f $ConnectTimeout
    $body | & $ssh -p $cfg.Port -o "StrictHostKeyChecking=accept-new" -o $cto -o "ServerAliveInterval=15" -o "PreferredAuthentications=password" -o "PubkeyAuthentication=no" -o "NumberOfPasswordPrompts=1" $target "tr -d '\r' | bash -s"
    exit $LASTEXITCODE
} finally {
    if (Test-Path $ask) { Remove-Item -LiteralPath $ask -Force }
    if ($null -eq $oldAsk) { Remove-Item Env:SSH_ASKPASS -ErrorAction SilentlyContinue } else { $env:SSH_ASKPASS = $oldAsk }
    if ($null -eq $oldReq) { Remove-Item Env:SSH_ASKPASS_REQUIRE -ErrorAction SilentlyContinue } else { $env:SSH_ASKPASS_REQUIRE = $oldReq }
    if ($null -eq $oldDisp) { Remove-Item Env:DISPLAY -ErrorAction SilentlyContinue } else { $env:DISPLAY = $oldDisp }
}
