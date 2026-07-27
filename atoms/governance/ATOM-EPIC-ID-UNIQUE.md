# ATOM-EPIC-ID-UNIQUE

## Règle
Vérification d'unicité des identifiants EPIC avant tout merge dans la branche principale.

## Mécanisme
- Avant merge : parser tous les fichiers YAML/MD dans `EPICS/` pour extraire les champs `id:`
- Vérifier l'unicité : interdire les doublons d'ID
- En cas de doublon : bifurcation = déduction du doublon vers un nouveau nom ou renommage automatique
- Log : `[EPIC_ID_UNIQUE] ids=<list> duplicates=<list> action=<reject|rename|bifurcate>`

## Application
```powershell
$epicFiles = Get-ChildItem -Path "EPICS\" -Recurse -Filter "*.md","*.yaml"
$ids = @{}
foreach ($file in $epicFiles) {
    $content = Get-Content $file -Raw
    if ($content -match 'id:\s*(\S+)') {
        $id = $matches[1]
        if ($ids.ContainsKey($id)) {
            Write-Host "[EPIC_ID_UNIQUE] Doublon détecté pour id=$id dans $($file.FullName)"
            # Bifurcation : dédupliquer ou renommer
        }
        $ids[$id] = $file.FullName
    }
}
```