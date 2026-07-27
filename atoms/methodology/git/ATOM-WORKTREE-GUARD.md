# ATOM-WORKTREE-GUARD

## Règle
Vérification systématique de l'état du working tree avant toute opération critique.

## Mécanisme
- Exécuter `git status --short` avant chaque opération critique (merge, cherry-pick, rebase)
- Si working tree sale (modifications non commitées) : stash, commit ou backup selon le contexte
- Log : `[WORKTREE_GUARD] status=<clean|dirty> action=<proceed|stash|commit|backup>`

## Application
```powershell
$status = git status --short
if ($status) {
    Write-Host "[WORKTREE_GUARD] Working tree sale - stash avant opération"
    git stash push -m "auto-stash-before-critical-op"
}
# Exécuter l'opération critique
# ...
# Restaurer si nécessaire
git stash pop
```