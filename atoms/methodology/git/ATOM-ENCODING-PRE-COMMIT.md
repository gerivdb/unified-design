# ATOM-ENCODING-PRE-COMMIT

## Règle
Vérification ASCII obligatoire avant tout commit Git. Remplacer automatiquement les caractères non-ASCII.

## Mécanisme
- Avant commit : scanner tous les fichiers stagés pour `ord(ch) > 127`
- Remplacer les caractères non-ASCII par leur équivalent ASCII ou les supprimer
- Si des remplacements sont effectués : re-stager les fichiers modifiés
- Log : `[ENCODING_PRE_COMMIT] files_scanned=<n> non_ascii_found=<k> auto_fixed=<k>`

## Application
```powershell
$stagedFiles = git diff --cached --name-only
foreach ($file in $stagedFiles) {
    $content = Get-Content $file -Raw
    $ascii = $content -replace '[^\x00-\x7F]', ''
    if ($content -ne $ascii) {
        Set-Content $file $ascii
        git add $file
        Write-Host "[ENCODING_PRE_COMMIT] Fixed non-ASCII in $file"
    }
}
```