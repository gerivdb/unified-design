[CmdletBinding()]
param(
    [ValidateSet("analyze", "verify", "report", "all")]
    [string]$Command = "all"
)

$ErrorActionPreference = 'Stop'
$RepoRoot = "D:\DO\WEB\TOOLS\L0-CANON\unified-design"
Set-Location $RepoRoot

$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Error "python not found"
    exit 1
}

function Invoke-AutoDesignCheck {
    param([string]$SubCommand, [string]$Arg = "")
    
    Write-Host "[AUTO-DESIGN] Running: $SubCommand $Arg" -ForegroundColor Cyan
    $args = @("scripts/auto_design_cli.py", $SubCommand)
    if ($Arg) {
        $args += $Arg
    }
    & python @args
    if ($LASTEXITCODE -ne 0) {
        Write-Error "AUTO-DESIGN $SubCommand failed"
        exit $LASTEXITCODE
    }
    Write-Host "[AUTO-DESIGN] $SubCommand OK" -ForegroundColor Green
}

switch ($Command) {
    "analyze" { Invoke-AutoDesignCheck -SubCommand "analyze" -Arg "." }
    "verify"  { Invoke-AutoDesignCheck -SubCommand "verify" -Arg "." }
    "report"  { Invoke-AutoDesignCheck -SubCommand "report" }
    "all" {
        Invoke-AutoDesignCheck -SubCommand "analyze" -Arg "."
        Invoke-AutoDesignCheck -SubCommand "verify" -Arg "."
        Invoke-AutoDesignCheck -SubCommand "report"
        Write-Host "[AUTO-DESIGN] All checks passed" -ForegroundColor Green
    }
}
