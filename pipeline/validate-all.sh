#!/usr/bin/env pwsh
<#
.SYNOPSIS
Validate-all.sh equivalent for unified-design cross-repo CI pipeline.
#>
param(
    [string]$UnifiedDesignRoot = "D:\DO\WEB\TOOLS\L0-CANON\unified-design"
)

$ErrorActionPreference = "Stop"
Push-Location $UnifiedDesignRoot

try {
    python scripts/cross_repo_ci.py --all
}
finally {
    Pop-Location
}
