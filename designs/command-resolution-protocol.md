---
type: DESIGN
version: "1.0.0"
intent_hash: 0xDESIGN_COMMAND_RESOLUTION_PROTOCOL_20260922
date: "2026-09-22"
status: proposed
layer: L0
source: PRD-MOC-COMMAND-RESOLUTION-PROTOCOL-20260922
---

# Command Resolution Protocol

## Principe

> Tout script PowerShell qui invoque une commande externe DOIT la résoudre
> avant exécution. Absence = échec bruyant, pas de fallback silencieux.

Ce design applique la règle B2 de `BOOTSTRAP_SOUVERAIN.md` au governance stack :
*« Le bootstrap exécute `check-services-coherence --pre-launch` AVANT tout lancement :
binaire absent ou config invalide = échec bruyant »*.

## Règles

| # | Règle |
|---|-------|
| 1 | `Get-Command <cmd> -ErrorAction SilentlyContinue` avant invocation |
| 2 | Si absent : `Write-Error` + `exit 1` avec message explicite |
| 3 | Si présent : utiliser le chemin résolu (`$cmd.Source`) |
| 4 | Documenter les commandes requises dans l'en-tête du script |
| 5 | Pour les chemins critiques : fallback sur chemins standards (`$env:LOCALAPPDATA\Programs\Python\Python312\python.exe`, etc.) |

## Pattern

```powershell
# Pré-vérification
$cmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $cmd) {
    $fallbacks = @(
        Join-Path $env:LOCALAPPDATA "Programs\Python\Python312\python.exe",
        Join-Path $env:LOCALAPPDATA "Programs\Python\Python311\python.exe"
    )
    foreach ($fb in $fallbacks) {
        if (Test-Path $fb) { $cmd = @{ Source = $fb }; break }
    }
}
if (-not $cmd) {
    Write-Error "python not found in PATH or common install paths."
    exit 1
}

# Exécution avec chemin résolu
& $cmd.Source -m pytest <args> 2>&1
```

## Application

- `scripts/run-governance-unit-tests.ps1` : résoudre `python` avant `pytest`
- `.githooks/pre-push.ps1` : résoudre `python` avant `validate_cross_repo.py`
- Tout script `.ps1` du governance stack invoquant `git`, `kiva`, `ecos`, `pytest`

## Anti-patterns

- Invoquer `python` directement sans vérification
- Utiliser `where.exe python` dans un script à `$ErrorActionPreference = "Stop"`
- Supposer que `python` est dans le PATH de l'agent d'exécution

## Références

- Design L0 : `BOOTSTRAP_SOUVERAIN.md` (0xDESIGN_BOOTSTRAP_SOUVERAIN_20260823)
- Design L0 : `COHERENCE_TRANSVERSE.md` (0xDESIGN_COHERENCE_TRANSVERSE_20260823)
- ADR : ADR-2026-09-20-001-YAML-VALIDATION-BEFORE-COMMIT
- PRD-MOC : PRD-MOC-COMMAND-RESOLUTION-PROTOCOL-20260922
