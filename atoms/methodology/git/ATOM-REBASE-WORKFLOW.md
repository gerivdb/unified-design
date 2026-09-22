# ATOM-REBASE-WORKFLOW

## Règle
Rebase autorisé uniquement sur branches locales non partagées. Merge obligatoire pour branches partagées. Backup branch obligatoire avant rebase interactif. Max 5 conflits par rebase.

## Mécanisme

### Décision rebase vs merge
- **Rebase autorisé** : branches locales, WIP branches, `feat/*` non poussées
- **Merge obligatoire** : branches partagées, `main`, `develop`, `hotfix/*` publiées

### Backup avant rebase
```powershell
$branch = git rev-parse --abbrev-ref HEAD
$backup = "backup-$(Get-Date -Format 'yyyyMMdd-HHmmss')-$branch"
git branch $backup
Write-Host "[REBASE] Backup branch created: $backup"
```

### Rebase interactif avec autosquash
```powershell
git rebase -i --autosquash origin/main
```

### Résolution de conflits
```powershell
$conflicts = git diff --name-only --diff-filter=U
if ($conflicts.Count -gt 5) {
    Write-Error "[REBASE] Too many conflicts ($($conflicts.Count)) - STOP + HITL"
    exit 1
}
foreach ($file in $conflicts) {
    git mergetool $file
    git add $file
}
git rebase --continue
```

### Validation post-rebase
```powershell
git status --short
git log --oneline -5
git diff main...HEAD --stat
```

### Cleanup
```powershell
git branch -d $backup
```

## Application
```powershell
# Workflow complet
$branch = git rev-parse --abbrev-ref HEAD
$base = "origin/main"

# Décision
if ($branch -in @("main", "develop")) {
    Write-Host "[REBASE] Merge required for protected branch"
    exit 0
}

# Backup
$backup = "backup-$(Get-Date -Format 'yyyyMMdd-HHmmss')-$branch"
git branch $backup

# Rebase
git rebase -i --autosquash $base
if ($LASTEXITCODE -ne 0) {
    Write-Error "[REBASE] Rebase failed - restore backup"
    git reset --hard $backup
    exit 1
}

# Validation
git status --short
git log --oneline -5

# Cleanup
git branch -d $backup
```

## Log
```
[REBASE] branch=<name> base=<base> backup=<sha> conflicts=<n> result=<OK|FAIL>
```

## Anti-patterns
- Rebase sur branche partagée
- Rebase sans backup
- Rebase avec > 5 conflits sans HITL
- Skip conflit sans inspection

## Références
- `designs/git-rebase-workflow.yaml` — Design source
- `designs/conflict-resolver-pattern/design.yaml` — Pattern de résolution
- `workflows/rebase-validation.md` — Workflow de validation
