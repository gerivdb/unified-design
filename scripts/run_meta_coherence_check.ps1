[CmdletBinding()]
param(
    [ValidateSet("check","plan","strict")]
    [string]$Mode = "check"
)

$ErrorActionPreference = 'Stop'
Set-Location "D:\DO\WEB\TOOLS\L0-CANON\unified-design"
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Error "python not found"
    exit 1
}
$args = @(".kilo/check_meta_coherence.py", "--mode", $Mode)
& python @args
exit $LASTEXITCODE
