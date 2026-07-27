# ATOM-MERGE-PARENT-SELECT

## Règle
Sélection automatique du parent correct pour les merge commits lors de cherry-pick.

## Mécanisme
- Avant cherry-pick d'un merge commit : vérifier `git show --stat <sha>` pour identifier le nombre de parents
- Si le commit a plusieurs parents (merge commit) : utiliser `-m 1` pour sélectionner le parent principal
- Log : `[MERGE_PARENT_SELECT] sha=<sha> parents=<n> parent_selected=<n> action=<cherry-pick|skip>`

## Application
```powershell
$stat = git show --stat $commitSha
$parentCount = ($stat -match "Merge:").Count
if ($parentCount -gt 0) {
    git cherry-pick -m 1 $commitSha
    Write-Host "[MERGE_PARENT_SELECT] Merge commit détecté - utilisation de -m 1"
} else {
    git cherry-pick $commitSha
}
```