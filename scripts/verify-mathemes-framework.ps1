<#
.SYNOPSIS
Vérifie la complétude du framework Mathèmes/Personas/Orchestration.

.DESCRIPTION
Vérifie que :
- Toutes les personas L0 listées ont un verse dans VERSES/verses/
- Toutes les personas L0 listées ont un atome dans unified-design/atoms/mathemes/
- Toutes les personas L0 listées ont un citizen dans citizens/
- Le config.admg existe et contient les 4 mathèmes
- Le script architectural-questionnaire.ps1 est présent

.EXAMPLE
.\verify-mathemes-framework.ps1
#>

param()

$ErrorActionPreference = "Stop"

$REPO_ROOT = "D:\DO\WEB\TOOLS\L2-PLATFORM\GeriCode"
$VERSES_DIRS = @(
    "D:\DO\WEB\TOOLS\L2-PLATFORM\GeriCode\act-protocol\verses"
    "D:\DO\WEB\TOOLS\L1-INFRA\VERSES\verses\actifs\dev-family\person-verses"
    "D:\DO\WEB\TOOLS\L2-PLATFORM\VERSES\verses"
)
$ATOMS_DIR = "D:\DO\WEB\TOOLS\L0-CANON\unified-design\atoms\mathemes"
$CITIZENS_DIR = "$REPO_ROOT\citizens"
$CONFIG_FILE = "$REPO_ROOT\.admg\config.admg"

function Write-Info($msg) { Write-Host "[INFO] $msg" -ForegroundColor Cyan }
function Write-Ok($msg)   { Write-Host "[OK]   $msg" -ForegroundColor Green }
function Write-Warn($msg) { Write-Host "[WARN] $msg" -ForegroundColor Yellow }
function Write-Err($msg)  { Write-Host "[ERR]  $msg" -ForegroundColor Red }

$requiredPersonas = @(
    "poincare", "maxwell", "mandelbrot", "julia", "feigenbaum", "berry",
    "dijkstra", "wolfram", "nash", "bellman",
    "shannon", "kolmogorov", "carnot", "knuth", "hilbert", "vapnik",
    "mackay", "scholkopf", "lecun", "jordan", "schmidhuber",
    "brouwer", "turing", "vonneumann", "feynman", "hoare", "milner",
    "sifakis", "mccarthy", "musk", "bellard", "gardien",
    "grothendieck", "deligne", "hassani", "lurie", "lafforgue", "voevodsky",
    "codd", "gray", "ellison", "simonyi", "karpathy", "steinberger",
    "illusie", "fantechi", "audit"
)

$missingVerses = @()
$missingAtomes = @()
$missingCitizens = @()

# Vérification VERSES
Write-Info "Vérification VERSES/verses/..."
foreach ($p in $requiredPersonas) {
    $found = $false
    foreach ($dir in $VERSES_DIRS) {
        $versePath = Join-Path $dir "$p-verse.md"
        if (Test-Path -LiteralPath $versePath) {
            $found = $true
            break
        }
    }
    if (-not $found) {
        $missingVerses += $p
    }
}
if ($missingVerses.Count -eq 0) {
    Write-Ok "Toutes les personas L0 ont un verse"
} else {
    Write-Warn "Verses manquants : $($missingVerses -join ', ')"
}

# Vérification atomes
Write-Info "Vérification unified-design/atoms/mathemes/..."
foreach ($p in $requiredPersonas) {
    $found = $false
    $possiblePaths = @(
        "ATOM-M4-$($p.ToUpper()).md"
        "ATOM-M1-$($p.ToUpper()).md"
        "ATOM-M2-$($p.ToUpper()).md"
        "ATOM-M3-$($p.ToUpper()).md"
    )
    foreach ($path in $possiblePaths) {
        $atomPath = Join-Path $ATOMS_DIR $path
        if (Test-Path -LiteralPath $atomPath) {
            $found = $true
            break
        }
    }
    if (-not $found) {
        $missingAtomes += $p
    }
}
if ($missingAtomes.Count -eq 0) {
    Write-Ok "Toutes les personas L0 ont un atome"
} else {
    Write-Warn "Atomes manquants : $($missingAtomes -join ', ')"
}

# Vérification citizens
Write-Info "Vérification citizens/..."
foreach ($p in $requiredPersonas) {
    $citizenPath = Join-Path $CITIZENS_DIR "$p.yaml"
    if (-not (Test-Path -LiteralPath $citizenPath)) {
        $missingCitizens += $p
    }
}
if ($missingCitizens.Count -eq 0) {
    Write-Ok "Toutes les personas L0 ont un citizen"
} else {
    Write-Warn "Citizens manquants : $($missingCitizens -join ', ')"
}

# Vérification config.admg
Write-Info "Vérification .admg/config.admg..."
if (Test-Path -LiteralPath $CONFIG_FILE) {
    $content = Get-Content -LiteralPath $CONFIG_FILE -Raw
    if ($content -match 'M1_continuite' -and $content -match 'M2_information' -and $content -match 'M3_transformation' -and $content -match 'M4_finalite') {
        Write-Ok "config.admg contient les 4 mathèmes"
    } else {
        Write-Warn "config.admg ne contient pas tous les mathèmes"
    }
} else {
    Write-Warn "config.admg n'existe pas"
}

# Vérification script
Write-Info "Vérification architectural-questionnaire.ps1..."
$scriptPath = "D:\DO\WEB\TOOLS\L0-CANON\unified-design\scripts\architectural-questionnaire.ps1"
if (Test-Path -LiteralPath $scriptPath) {
    Write-Ok "architectural-questionnaire.ps1 présent"
} else {
    Write-Err "architectural-questionnaire.ps1 absent"
}

# Résumé
Write-Host ""
Write-Host "=== RESUME ===" -ForegroundColor Cyan
Write-Host "Personas L0 requises : $($requiredPersonas.Count)"
Write-Host "Verses manquants : $($missingVerses.Count)"
Write-Host "Atomes manquants : $($missingAtomes.Count)"
Write-Host "Citizens manquants : $($missingCitizens.Count)"

$totalMissing = $missingVerses.Count + $missingAtomes.Count + $missingCitizens.Count
if ($totalMissing -eq 0) {
    Write-Ok "Framework complet !"
    exit 0
} else {
    Write-Warn "Framework incomplet : $totalMissing élément(s) manquant(s)"
    exit 1
}

