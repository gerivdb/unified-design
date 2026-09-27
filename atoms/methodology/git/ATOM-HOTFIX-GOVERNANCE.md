# ATOM-HOTFIX-GOVERNANCE

## Règle
Hotfix DOIT être créé depuis main, merge avec validation minimale, et accompagné d'un plan de rollback. Branche hotfix/* DOIT être supprimée dans les 7 jours.

## Mécanisme

### Création hotfix
```powershell
$slug = $args[0]
git checkout -b "hotfix/$slug" main
Write-Host "[HOTFIX] Branch created: hotfix/$slug"
```

### Merge d'urgence
```powershell
$branch = $args[0]
git checkout main
git merge --no-ff $branch
if ($LASTEXITCODE -ne 0) {
    Write-Error "[HOTFIX] Merge failed"
    exit 1
}
$mergeSha = git rev-parse HEAD
Write-Host "[HOTFIX] Merge commit: $mergeSha"
```

### Plan de rollback
```powershell
$mergeSha = $args[0]
$rollbackPlan = @"
# Rollback Plan
## Commit à revert
$mergeSha

## Commande de rollback
git revert $mergeSha

## Validation
git log --oneline -3
"@
Set-Content -Path "rollback-plan.md" -Value $rollbackPlan
Write-Host "[HOTFIX] Rollback plan documented"
```

### Post-mortem
```powershell
$resolutionTime = $args[0]
if ($resolutionTime -gt 2) {
    $postMortem = @"
# Post-Mortem
## Incident
## Résolution
## Temps: $resolutionTime heures
"@
    Set-Content -Path "incident/post-mortem-$(Get-Date -Format 'yyyyMMdd').md" -Value $postMortem
    Write-Host "[HOTFIX] Post-mortem generated"
}
```

### Cleanup
```powershell
$branch = $args[0]
git branch -d $branch
git push origin --delete $branch
Write-Host "[HOTFIX] Branch deleted: $branch"
```

## Application
```powershell
# Workflow complet
$slug = "critical-fix-001"
git checkout -b "hotfix/$slug" main
# ... implémenter le fix ...
git add -A
git commit -m "fix: critical issue $slug"
git checkout main
git merge --no-ff "hotfix/$slug"
$mergeSha = git rev-parse HEAD
# Documenter rollback
Set-Content -Path "rollback-plan.md" -Value "git revert $mergeSha"
# Cleanup après 7 jours
git branch -d "hotfix/$slug"
git push origin --delete "hotfix/$slug"
```

## Log
```
[HOTFIX] branch=<name> merge=<sha> rollback=<documented> post_mortem=<generated|skipped> cleanup=<done>
```

## Anti-patterns
- Hotfix créé depuis une feature branch
- Merge sans plan de rollback
- Branche hotfix/* conservée > 7 jours
- Force push sur hotfix/*
- Hotfix sans traçabilité WAL

## Références
- `designs/hotfix-workflow.yaml` — Design source
- `ADR-014-git-policy.md` — Politique Git
- `ADR-030-hitl-session-protocol.md` — Protocole HITL
