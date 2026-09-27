# ATOM-REVERT-RESET-GOVERNANCE

## Règle
`git revert` est la commande par défaut pour annuler un commit public. `git reset` est autorisé UNIQUEMENT sur branches locales non poussées. Tout reset --hard DOIT être précédé d'un backup. `git push --force` est interdit.

## Mécanisme

### Decision tree revert vs reset
```powershell
$branch = git rev-parse --abbrev-ref HEAD
$isLocal = -not (git branch -r | Where-Object { $_ -match $branch })
if (-not $isLocal) {
    Write-Host "[REVERT-RESET] Branch is shared - use revert"
    $action = "revert"
} else {
    Write-Host "[REVERT-RESET] Branch is local - reset allowed with backup"
    $action = "reset"
}
```

### Revert
```powershell
$sha = $args[0]
git revert $sha
if ($LASTEXITCODE -ne 0) {
    Write-Error "[REVERT-RESET] Revert failed"
    exit 1
}
Write-Host "[REVERT-RESET] Reverted: $sha"
```

### Reset avec backup
```powershell
$sha = $args[0]
$branch = git rev-parse --abbrev-ref HEAD
$backup = "backup-$(Get-Date -Format 'yyyyMMdd-HHmmss')-$branch"
git branch $backup
git reset --hard $sha
if ($LASTEXITCODE -ne 0) {
    Write-Error "[REVERT-RESET] Reset failed - restore backup"
    git reset --hard $backup
    exit 1
}
Write-Host "[REVERT-RESET] Reset to $sha (backup: $backup)"
```

### Vérification reflog
```powershell
$reflog = git reflog | Select-Object -First 20
Write-Host "[REVERT-RESET] Reflog:"
$reflog | ForEach-Object { Write-Host "  $_" }
```

### Force push interdit
```powershell
# INTERDIT
# git push --force origin main

# AUTORISÉ
git push --force-with-lease origin main
```

## Application
```powershell
# Revert sur branche partagée
$sha = "abc1234"
git revert $sha
git push origin main

# Reset sur branche locale
$sha = "abc1234"
$branch = git rev-parse --abbrev-ref HEAD
$backup = "backup-$(Get-Date -Format 'yyyyMMdd-HHmmss')-$branch"
git branch $backup
git reset --hard $sha
# Vérifier
git status --short
git log --oneline -5
# Si OK, supprimer backup
git branch -d $backup
```

## Log
```
[REVERT-RESET] action=<revert|reset> sha=<sha> backup=<sha|null> branch=<name> result=<OK|FAIL>
```

## Anti-patterns
- Reset sur branche partagée
- Reset --hard sans backup
- Force push sans --force-with-lease
- Revert sans vérifier le diff
- Ignorer le reflog avant rollback

## Références
- `designs/git-revert-reset-strategy.yaml` — Design source
- `ADR-094-git-remote-safety-protocol.md` — Remote safety
- `workflows/safe-rollback.md` — Workflow de rollback
