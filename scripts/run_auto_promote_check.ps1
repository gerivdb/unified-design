<#
.SYNOPSIS
Runs auto-promote check in dry-run mode and reports results.
#>

param(
    [switch]$Apply,
    [string]$ReportPath = "reports/auto-promote-report.json"
)

$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root

Write-Host "=== Auto-Promote Check ===" -ForegroundColor Cyan
Write-Host "Mode: $($Apply ? 'APPLY' : 'DRY-RUN')" -ForegroundColor Yellow
Write-Host ""

$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Error "python not found in PATH"
}

$script = Join-Path $root "auto_design_cli.py"
if (-not (Test-Path $script)) {
    Write-Error "auto_design_cli.py not found at $script"
}

$mode = if ($Apply) { "--apply" } else { "--dry-run" }
$output = & python $script promote $mode --repo $root 2>&1
$exitCode = $LASTEXITCODE

Write-Host $output
Write-Host ""

if ($ReportPath) {
    $reportDir = Split-Path -Parent $ReportPath
    if (-not (Test-Path $reportDir)) {
        New-Item -ItemType Directory -Path $reportDir -Force | Out-Null
    }
    $output | Out-File -FilePath $ReportPath -Encoding utf8
    Write-Host "Report saved to: $ReportPath" -ForegroundColor Green
}

if ($exitCode -ne 0) {
    Write-Error "auto-promote check failed with exit code $exitCode"
}

Write-Host "Auto-promote check completed successfully." -ForegroundColor Green
