# ATOM-CONFLICT-RESOLVE

## Règle
Résolution obligatoire des conflits de merge avant toute poursuite.

## Mécanisme
- Détecter les marqueurs de conflit `<<<<<<<`, `=======`, `>>>>>>>` dans les fichiers
- Résoudre le conflit puis exécuter `git add <fichier> + git cherry-pick --continue`
- Ne jamais passer outre (`--skip`) ou abandonner (`--abort`) sans inspection préalable
- Log : `[CONFLICT_RESOLVE] file=<path> markers_found=<n> resolved=<bool>`

## Application
```powershell
$conflictFiles = git diff --name-only --diff-filter=U
foreach ($file in $conflictFiles) {
    $content = Get-Content $file -Raw
    if ($content -match '<<<<<<<') {
        # Détecter et résoudre les conflits
        $resolved = Resolve-Conflict -Content $content
        Set-Content $file $resolved
        git add $file
    }
}
git cherry-pick --continue
```