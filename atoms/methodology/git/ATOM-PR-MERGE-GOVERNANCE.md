# ATOM-PR-MERGE-GOVERNANCE

## Règle
Merge commit par défaut pour branches de feature publiques. Squash autorisé uniquement pour WIP branches ou feat/* avec < 5 commits. Rebase interdit sur branches partagées. Toute PR DOIT avoir la stratégie annotée.

## Mécanisme

### Annotation de stratégie
```powershell
# Dans la description de la PR :
# /merge-strategy merge|squash|rebase
$strategy = "merge" # par défaut
if ($prDescription -match '/merge-strategy (\w+)') {
    $strategy = $Matches[1]
}
Write-Host "[MERGE] Strategy: $strategy"
```

### Sélection de stratégie
```powershell
$branch = $args[0]
$commitCount = (git log --oneline origin/main..$branch).Count

if ($branch -match '^wip/') {
    $strategy = "squash"
} elseif ($commitCount -lt 5 -and $branch -match '^feat/') {
    $strategy = "squash"
} else {
    $strategy = "merge"
}
Write-Host "[MERGE] Strategy selected: $strategy for $branch ($commitCount commits)"
```

### Dryrun avant merge
```powershell
$branch = $args[0]
git merge --no-commit --no-ff $branch
if ($LASTEXITCODE -ne 0) {
    Write-Error "[MERGE] Dryrun failed"
    git merge --abort
    exit 1
}
$conflicts = git diff --name-only --diff-filter=U
if ($conflicts.Count -gt 5) {
    Write-Error "[MERGE] Too many conflicts ($($conflicts.Count))"
    git merge --abort
    exit 1
}
git merge --abort
Write-Host "[MERGE] Dryrun passed"
```

### Exécution du merge
```powershell
$branch = $args[0]
$strategy = $args[1]

if ($strategy -eq "squash") {
    git merge --squash $branch
    git commit -m "feat: merge $branch (squash)"
} else {
    git merge --no-ff $branch
}
if ($LASTEXITCODE -ne 0) {
    Write-Error "[MERGE] Merge failed"
    exit 1
}
$mergeSha = git rev-parse HEAD
Write-Host "[MERGE] Merge commit: $mergeSha"
```

### Traçabilité
```powershell
$mergeSha = $args[0]
$strategy = $args[1]
$branch = $args[2]
Write-WAL "MERGE: strategy=$strategy sha=$mergeSha branch=$branch ts=$(Get-Date)"
Write-Host "[MERGE] WAL entry created"
```

### Cleanup
```powershell
$branch = $args[0]
git branch -d $branch
git push origin --delete $branch
Write-Host "[MERGE] Branch deleted: $branch"
```

## Application
```powershell
# Merge complet
$branch = "feat/gov-hub-registry-20260921"
$strategy = "merge" # ou "squash" pour WIP

# Dryrun
git merge --no-commit --no-ff $branch
git merge --abort

# Merge
if ($strategy -eq "squash") {
    git merge --squash $branch
    git commit -m "feat: merge $branch (squash)"
} else {
    git merge --no-ff $branch
}

# Tracer
$mergeSha = git rev-parse HEAD
Write-WAL "MERGE: strategy=$strategy sha=$mergeSha branch=$branch ts=$(Get-Date)"

# Cleanup
git branch -d $branch
git push origin --delete $branch
```

## Log
```
[MERGE] strategy=<merge|squash> sha=<sha> branch=<name> wal=<logged> cleanup=<done>
```

## Anti-patterns
- Squash sur branche partagée avec > 5 commits
- Rebase sur branche avec PR ouverte
- Merge sans dryrun
- Merge sans annotation de stratégie
- Oublier le cleanup de branche

## Références
- `designs/pr-merge-strategy.yaml` — Design source
- `designs/merge-fork-balance.yaml` — Méta-design merge/fork
- `scripts/pr-auto-merge-orchestrator.py` — Orchestrateur auto-merge
