<#
.SYNOPSIS
Architectural Questionnaire - 4 Mathemates Attracteurs (M1-M4).
Calcule Q(R), H, W(M_a, M_b) avant toute implementation.

.DESCRIPTION
Pour tout probleme, pose les 4 questions d'architecte :
  Q1 (M1) : Topologie
  Q2 (M2) : Information
  Q3 (M3) : Transformation
  Q4 (M4) : Finalite

Calcule :
  - Quorum Q(R) = ceil(Sum w_i(M_i actives) * 0.75)
  - Entropie H = -Sum p_m log2 p_m
  - Distance de Wasserstein W(M_a, M_b)

.PARAMETER Problem
Description du probleme a analyser.

.PARAMETER Mathemes
Liste des mathemes actives (M1, M2, M3, M4).

.PARAMETER Patterns
Liste des patterns actives.

.EXAMPLE
.\architectural-questionnaire.ps1 -Problem "Create PRD" -Mathemes M4 -Patterns @audit
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$Problem,

    [Parameter(Mandatory=$false)]
    [string[]]$Mathemes = @(),

    [Parameter(Mandatory=$false)]
    [string[]]$Patterns = @()
)

$ErrorActionPreference = "Stop"

function Write-Info($msg) { Write-Host "[INFO] $msg" -ForegroundColor Cyan }
function Write-Ok($msg)   { Write-Host "[OK]   $msg" -ForegroundColor Green }
function Write-Warn($msg) { Write-Host "[WARN] $msg" -ForegroundColor Yellow }
function Write-Err($msg)  { Write-Host "[ERR]  $msg" -ForegroundColor Red }

# --- Q1 : Topologie ---
Write-Info "Q1 (M1 - CONTINUITE) : Quelle est la structure topologique ?"
Write-Host "  - Objets : ENV, repos, artifacts"
Write-Host "  - Morphismes : déploiements, transformations, workflows"
Write-Host "  - Invariants : symétries, cycles, points fixes"
Write-Host "  - Faisceau : F_KEEL sur site TOPOS"

# --- Q2 : Information ---
Write-Info "Q2 (M2 - INFORMATION) : Quelle est la mesure d'information ?"
$entropy = 0.0
if ($Patterns.Count -gt 0) {
    $p = 1.0 / $Patterns.Count
    $entropy = -($Patterns.Count * ($p * [math]::Log($p, 2)))
}
Write-Host "  - Entropie H = $entropy (seuil alerte > 0.6)"
if ($entropy -gt 0.6) {
    Write-Warn "Entropie trop élevée : H = $entropy > 0.6"
}

# --- Q3 : Transformation ---
Write-Info "Q3 (M3 - TRANSFORMATION) : Comment transformer ?"
Write-Host "  - Rollback : F^-1o F = id, perte < 10%"
Write-Host "  - Contraintes ENV2 : SSE4.2, 24Go, <50ms"
Write-Host "  - Vérification : Hoare, Milner, Kleene"

# --- Q4 : Finalité ---
Write-Info "Q4 (M4 - FINALITE) : Quel est le contrat de gouvernance ?"
$requiredPersonas = @("grothendieck", "deligne", "hassani", "lurie", "lafforgue", "voevodsky")
$missingPersonas = @()
foreach ($p in $requiredPersonas) {
    $versePath = "D:\DO\WEB\TOOLS\L2-PLATFORM\GeriCode\act-protocol\verses\$p-verse.md"
    if (-not (Test-Path -LiteralPath $versePath)) {
        $versePath = "D:\DO\WEB\TOOLS\L1-INFRA\VERSES\verses\actifs\dev-family\person-verses\$p-verse.md"
        if (-not (Test-Path -LiteralPath $versePath)) {
            $versePath = "D:\DO\WEB\TOOLS\L2-PLATFORM\VERSES\verses\$p-verse.md"
            if (-not (Test-Path -LiteralPath $versePath)) {
                $missingPersonas += $p
            }
        }
    }
}
if ($missingPersonas.Count -gt 0) {
    Write-Warn "Personas L0 manquantes dans VERSES : $($missingPersonas -join ', ')"
} else {
    Write-Ok "Toutes les personas L0 M4 sont présentes dans VERSES"
}

# --- Calcul Quorum ---
Write-Info "Calcul Quorum Q(R)..."
$weights = @{M1=0; M2=0; M3=0; M4=0}
foreach ($m in $Mathemes) {
    if ($weights.ContainsKey($m)) {
        $weights[$m]++
    }
}
$totalWeight = ($weights.Values | Measure-Object -Sum).Sum
$quorum = [math]::Ceiling($totalWeight * 0.75)
$w1 = $weights['M1']; $w2 = $weights['M2']; $w3 = $weights['M3']; $w4 = $weights['M4']
Write-Host "  Poids M1=$w1 M2=$w2 M3=$w3 M4=$w4"
Write-Host "  Q(R) = ceil($totalWeight * 0.75) = $quorum"

if ($quorum -lt 3) {
    Write-Warn "Quorum insuffisant : Q(R) = $quorum < 3"
} else {
    Write-Ok "Quorum suffisant : Q(R) = $quorum"
}

# --- Distance de Wasserstein (simplifiee) ---
Write-Info "Compatibilité entre mathèmes (Wasserstein simplifié)..."
$mathemeList = $Mathemes | Sort-Object -Unique
$maxW = 0.0
for ($i = 0; $i -lt $mathemeList.Count; $i++) {
    for ($j = $i + 1; $j -lt $mathemeList.Count; $j++) {
        $w = [math]::Abs($weights[$mathemeList[$i]] - $weights[$mathemeList[$j]])
        if ($w -gt $maxW) { $maxW = $w }
        Write-Host "  W($($mathemeList[$i]), $($mathemeList[$j])) = $w"
    }
}
Write-Host "  W_max = $maxW (seuil alerte > 0.5)"
if ($maxW -gt 0.5) {
    Write-Warn "Distance de Wasserstein trop élevée : W_max = $maxW > 0.5"
} else {
    Write-Ok "Distances de Wasserstein acceptables"
}

# --- Résumé ---
Write-Host ""
Write-Host "=== RESUME ===" -ForegroundColor Cyan
Write-Host "Problème : $Problem"
Write-Host "Mathèmes activés : $($Mathemes -join ', ')"
Write-Host "Patterns activés : $($Patterns -join ', ')"
Write-Host "Entropie H : $entropy"
Write-Host "Quorum Q(R) : $quorum"
Write-Host "W_max : $maxW"

$passed = $entropy -le 0.6 -and $quorum -ge 3 -and $maxW -le 0.5 -and $missingPersonas.Count -eq 0
if ($passed) {
    Write-Ok "Toutes les validations passent. Workflow autorisé."
    exit 0
} else {
    Write-Err "Validations échouées. Workflow bloqué."
    exit 1
}

