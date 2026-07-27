# ATOM-EMPTY-CHERRY-PICK

## Règle
Détection automatique de cherry-pick vide (contenu déjà intégré) et skip automatique.

## Mécanisme
- Avant cherry-pick : vérifier si le commit cible est déjà présent dans la branche courante
- Si déjà intégré : skip automatique avec log
- Log : `[EMPTY_CHERRY_PICK] commit=<sha> already_integrated=<bool> action=skipped`

## Application
```powershell
function Skip-EmptyCherryPick {
    param([string]$commitSha, [string]$targetBranch)
    $existing = git log $targetBranch --format="%H" | Select-String $commitSha
    if ($existing) {
        Write-Host "[EMPTY_CHERRY_PICK] Commit $commitSha déjà intégré - skip"
        return $true
    }
    return $false
}
```