[CmdletBinding()]
param(
    [ValidateSet("check","plan","strict","all")]
    [string]$Mode = "all"
)

$ErrorActionPreference = 'Stop'
Set-Location "D:\DO\WEB\TOOLS\L0-CANON\unified-design"

function Invoke-Step {
    param([string]$Name, [scriptblock]$Script)
    Write-Host "`n=== $Name ===" -ForegroundColor Cyan
    try {
        & $Script
        Write-Host "[OK] $Name" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "[FAIL] $Name : $_" -ForegroundColor Red
        return $false
    }
}

$results = @{}

if ($Mode -eq "all" -or $Mode -eq "check") {
    $results["meta_coherence_check"] = Invoke-Step -Name "Meta-Coherence Check" -Script {
        python .kilo/check_meta_coherence.py --mode check
    }
}

if ($Mode -eq "all" -or $Mode -eq "plan") {
    $results["meta_coherence_plan"] = Invoke-Step -Name "Meta-Coherence Plan" -Script {
        python .kilo/check_meta_coherence.py --mode plan
    }
}

if ($Mode -eq "all" -or $Mode -eq "strict") {
    $results["meta_coherence_strict"] = Invoke-Step -Name "Meta-Coherence Strict" -Script {
        python .kilo/check_meta_coherence.py --mode strict
    }
}

if ($Mode -eq "all") {
    $results["unit_tests"] = Invoke-Step -Name "Unit Tests" -Script {
        pytest .kilo/tests/test_check_meta_coherence.py -q
    }
    
    $results["designs_validate"] = Invoke-Step -Name "Designs Validate" -Script {
        python scripts/validate_designs.py --strict
    }
    
    $results["ascii_check"] = Invoke-Step -Name "ASCII Check" -Script {
        python tools/check_ascii.py
    }
}

Write-Host "`n=== CI Summary ===" -ForegroundColor Cyan
$failed = 0
foreach ($key in $results.Keys) {
    $status = if ($results[$key]) { "PASS" } else { "FAIL" }
    $color = if ($results[$key]) { "Green" } else { "Red" }
    Write-Host "$key : $status" -ForegroundColor $color
    if (-not $results[$key]) { $failed++ }
}

if ($failed -gt 0) {
    Write-Host "`nCI FAILED: $failed step(s) failed" -ForegroundColor Red
    exit 1
}
else {
    Write-Host "`nCI PASSED: all steps succeeded" -ForegroundColor Green
    exit 0
}
