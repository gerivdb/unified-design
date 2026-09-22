# ATOM-TAG-RELEASE-GOVERNANCE

## Règle
Tout tag DOIT suivre SemVer strict, être signé pour les repos critiques, et être accompagné d'un CHANGELOG.md mis à jour. Les tags sont créés uniquement sur release branches, jamais directement sur main.

## Mécanisme

### Validation de tag
```powershell
$version = $args[0]
if ($version -notmatch '^\d+\.\d+\.\d+$') {
    Write-Error "[TAG] Invalid SemVer: $version"
    exit 1
}
if ($version -in @("latest", "stable", "v1", "current")) {
    Write-Error "[TAG] Forbidden tag name: $version"
    exit 1
}
```

### Création de tag signé
```powershell
$version = $args[0]
$message = "Release $version"
git tag -s $version -m $message
if ($LASTEXITCODE -ne 0) {
    Write-Error "[TAG] Failed to create signed tag"
    exit 1
}
Write-Host "[TAG] Signed tag created: $version"
```

### Vérification pre-tag
```powershell
$status = git status --short
if ($status) {
    Write-Error "[TAG] Working tree not clean"
    exit 1
}
$changelog = Get-Content CHANGELOG.md -Raw
if ($changelog -notmatch "## \[$version\]") {
    Write-Error "[TAG] CHANGELOG.md not updated for $version"
    exit 1
}
```

### Release branch workflow
```powershell
$version = $args[0]
git checkout -b "release/v$version" main
# Update CHANGELOG.md
python scripts/generate_changelog.py --version $version
git add CHANGELOG.md
git commit -m "docs: update changelog for v$version"
git tag -s "v$version" -m "Release v$version"
git checkout main
git merge --no-ff "release/v$version"
git push origin main --tags
git push origin --delete "release/v$version"
```

## Application
```powershell
# Créer une release
$version = "1.2.0"
git checkout -b "release/v$version" main
python scripts/generate_changelog.py --version $version
git add CHANGELOG.md
git commit -m "docs: update changelog for v$version"
git tag -s "v$version" -m "Release v$version"
git checkout main
git merge --no-ff "release/v$version"
git push origin main --tags
git push origin --delete "release/v$version"
```

## Log
```
[TAG] version=<version> signed=<true|false> changelog=<updated|missing> branch=<release|main>
```

## Anti-patterns
- Tag sans SemVer valide
- Tag non signé sur repo critique
- Tag sans CHANGELOG.md mis à jour
- Tag direct sur main sans release branch
- Tag sur working tree sale

## Références
- `designs/git-tag-release-management.yaml` — Design source
- `conventions/versioning/SEMVER_AND_CHANGELOG.md` — Convention SemVer
- `ADR-2026-08-29-005-KERNEL-VERSIONING-POLICY.md` — Kernel versioning
