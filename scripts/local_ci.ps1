<# 
.SYNOPSIS
    Local CI Runner - KIVA-CLI Native
    Remplace GitHub Actions par exécution locale via KIVA-CLI
    Zéro dépendance GitHub Actions - tout tourne en local
#>

param(
    [switch]$Quick
)

$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent $PSScriptRoot | Split-Path -Parent

function Run-Cmd {
    param([string[]]$Command, [string]$Desc = "")
    Write-Host "  ▶ $($Command -join ' ')" -ForegroundColor Cyan
    $sw = [System.Diagnostics.Stopwatch]::StartNew()
    try {
        $result = & $Command 2>&1
        $sw.Stop()
        if ($LASTEXITCODE -eq 0) {
            Write-Host "    ✓ OK ($($sw.Elapsed.TotalSeconds) s)" -ForegroundColor Green
            return $true
        } else {
            Write-Host "    ✗ FAIL ($($sw.Elapsed.TotalSeconds) s)" -ForegroundColor Red
            Write-Host "    $result" -ForegroundColor Red
            return $false
        }
    } catch {
        Write-Host "    ✗ ERROR: $_" -ForegroundColor Red
        return $false
    }
}

# Check KIVA-CLI
Write-Host "=" * 60
Write-Host "LOCAL CI PIPELINE (KIVA-CLI Native)" -ForegroundColor Cyan
Write-Host "=" * 60

$kivaCheck = Run-Cmd @("kiva", "--version") "Check KIVA-CLI"
if (-not $kivaCheck) {
    Write-Host "  ✗ KIVA-CLI non trouvé - installez via ECOS-CLI" -ForegroundColor Red
    exit 1
}

$checks = @()

# 1. Meta-design schema
$checks += @{ Name = "Meta-design schema"; Cmd = { Run-Cmd @("python", "scripts/validate_meta_design.py", "meta-design.yaml") "Validate meta-design.yaml" } }

# 2. Meta-design validation
$checks += @{ Name = "Meta-design validation"; Cmd = { Run-Cmd @("python", "scripts/validate_meta_design.py", "meta-design.yaml") "Validate meta-design.yaml" } }

# 3. Atoms YAML
$checks += @{ Name = "Atoms YAML structure"; Cmd = { Run-Cmd @("python", "scripts/validate_yaml.py", "--assert", "name", "atoms/*.yaml") "Validate atoms YAML structure" } }

# 4. Atom registry
$checks += @{ Name = "Atom registry"; Cmd = { Run-Cmd @("python", "scripts/validate_atom_registry.py") "Validate atom registry" } }

# 5. Schema validation
$checks += @{ Name = "Schema validation"; Cmd = { Run-Cmd @("python", "-c", "import json; json.load(open('schemas/meta-design.schema.json')); print('Schema JSON valide')") "Validate meta-design.schema.json" } }

# 6. Dependency loops
$checks += @{ Name = "Dependency loops"; Cmd = { Run-Cmd @("python", "loop_engine/check_loops.py", "--path", ".", "--max-depth", "5") "Check dependency loops" } }

# 7. ADR refs
$checks += @{ Name = "ADR references"; Cmd = { Run-Cmd @("python", "scripts/validate_adr_refs.py") "Validate ADR references" } }

# 8. Simulate atoms (Graph of Loops)
$atoms = @(
    "ATOM-049-symbol-retrieval-mcp.yaml",
    "ATOM-050-agent-worktree-isolation.yaml", 
    "ATOM-051-beads-sql-memory.yaml",
    "ATOM-052-exit-interceptor.yaml",
    "ATOM-053-tdd-airain-law.yaml",
    "ATOM-054-trace-replay-proof.yaml"
)

foreach ($atom in $atoms) {
    $path = "atoms/$atom"
    if (Test-Path $path) {
        $checks += @{ 
            Name = "Simulate $atom"
            Cmd = { Run-Cmd @("python", "loop_engine/simulate.py", $path, "--meta-design", "meta-design.yaml") "Simulate $atom" }
        }
    }
}

# Execute all checks
$results = @()
foreach ($check in $checks) {
    Write-Host "`n[$($check.Name)]" -ForegroundColor Cyan
    $ok = & $check.Cmd
    $results += @{ Name = $check.Name; Passed = $ok }
}

# Summary
Write-Host "`n" + "=" * 60
Write-Host "CI SUMMARY" -ForegroundColor Cyan
Write-Host "=" * 60
$allPassed = $true
foreach ($r in $results) {
    $status = if ($r.Passed) { "PASS" } else { "FAIL" }
    $color = if ($r.Passed) { "Green" } else { "Red" }
    Write-Host "  $status: $($r.Name)" -ForegroundColor $color
    $allPassed = $allPassed -and $r.Passed
}
Write-Host "=" * 60

exit ($allPassed ? 0 : 1)