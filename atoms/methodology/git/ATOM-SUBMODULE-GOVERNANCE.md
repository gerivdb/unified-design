# ATOM-SUBMODULE-GOVERNANCE

## Règle
Tout submodule DOIT être enregistré dans known_repositories.yaml, pinné sur SHA, et synchronisé après chaque pull. Suppression de submodule DOIT mettre à jour .gitmodules et être tracée dans WAL.

## Mécanisme

### Enregistrement préalable
```powershell
# Avant git submodule add, vérifier known_repositories.yaml
$repo = $args[0]
$path = $args[1]
# Ajouter l'entrée dans known_repositories.yaml
# Puis exécuter git submodule add
```

### Ajout de submodule
```powershell
$url = $args[0]
$path = $args[1]
git submodule add $url $path
if ($LASTEXITCODE -ne 0) {
    Write-Error "[SUBMODULE] Failed to add submodule"
    exit 1
}
git submodule update --init --recursive
git add $path .gitmodules
git commit -m "feat(submodule): add $path from $url"
Write-Host "[SUBMODULE] Added: $path"
```

### Synchronisation
```powershell
git submodule update --init --recursive
if ($LASTEXITCODE -ne 0) {
    Write-Error "[SUBMODULE] Sync failed"
    exit 1
}
Write-Host "[SUBMODULE] Synced"
```

### Suppression sécurisée
```powershell
$path = $args[0]
git submodule deinit -f $path
git rm -f $path
Remove-Item -Recurse -Force ".git/modules/$path"
git commit -m "feat(submodule): remove $path"
Write-Host "[SUBMODULE] Removed: $path"
```

### Vérification de pinning
```powershell
$path = $args[0]
$sha = git submodule status $path | ForEach-Object { $_.Trim().Split(' ')[0] }
if ($sha -match '^\+') {
    Write-Warning "[SUBMODULE] $path is not pinned (has uncommitted changes)"
}
Write-Host "[SUBMODULE] $path pinned at $sha"
```

## Application
```powershell
# Ajouter un submodule
$url = "https://github.com/gerivdb/TOOL-FACTORY-1.git"
$path = "tools/tool-factory-1"
git submodule add $url $path
git submodule update --init --recursive
git add $path .gitmodules
git commit -m "feat(submodule): add $path"

# Synchroniser après pull
git pull origin main
git submodule update --init --recursive

# Supprimer un submodule
$path = "tools/tool-factory-1"
git submodule deinit -f $path
git rm -f $path
Remove-Item -Recurse -Force ".git/modules/$path"
git commit -m "feat(submodule): remove $path"
```

## Log
```
[SUBMODULE] action=<add|sync|remove> path=<path> sha=<sha> wal=<logged>
```

## Anti-patterns
- Submodule non enregistré dans known_repositories.yaml
- Submodule sur branche mobile (pas de SHA)
- Submodule dans src/, bin/, config/
- Oublier git submodule update après git pull
- Supprimer submodule sans mettre à jour .gitmodules

## Références
- `designs/git-submodule-management.yaml` — Design source
- `ADR-039-clone-topology-watch.md` — Clone topology watch
- `designs/clone-dedup-rescue.yaml` — Clone dedup rescue
