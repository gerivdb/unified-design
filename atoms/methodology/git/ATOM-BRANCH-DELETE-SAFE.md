# ATOM-BRANCH-DELETE-SAFE

## Règle
Suppression sécurisée des branches Git avec vérification préalable et trace WAL.

## Mécanisme
- Vérifier les branches distantes avec `git branch -r` avant suppression
- Utiliser `-d` (safe delete) en premier, puis `-D` (force) seulement si nécessaire
- Traiter une branche à la fois
- Tracer chaque suppression dans le WAL
- Log : `[BRANCH_DELETE_SAFE] branch=<name> remote=<exists> action=<deleted|skipped>`

## Application
```powershell
$branches = git branch -r | ForEach-Object { $_.Trim() }
foreach ($branch in $branches) {
    if ($branch -notmatch "main|master|develop") {
        git branch -d $branch
        Write-WAL "BRANCH_DELETE_SAFE: deleted $branch at $(Get-Date)"
    }
}
```