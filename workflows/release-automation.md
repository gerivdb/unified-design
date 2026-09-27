# Workflow — Release Automation

**IntentHash** : `0xWORKFLOW_RELEASE_AUTOMATION_20260923`  
**Design** : `git-tag-release-management`  
**Atom** : `ATOM-TAG-RELEASE-GOVERNANCE`

---

## Déclencheur

Toute demande de release (tag) dans l'écosystème gerivdb.

## Étapes

### ÉTAPE-1 — Validation de version

1. Vérifier que la version suit SemVer strict : `^\d+\.\d+\.\d+$`
2. Vérifier que la version n'est pas interdite : pas de `latest`, `stable`, `v1`, `current`
3. Vérifier que la version n'existe pas déjà : `git tag | grep v<version>`

### ÉTAPE-2 — Vérification pre-release

1. Vérifier le working tree : `git status --short` → doit être clean
2. Vérifier le CHANGELOG.md : doit contenir `## [<version>]`
3. Vérifier la branche : doit être sur `main` ou `develop`

### ÉTAPE-3 — Création release branch

1. Créer la branche : `git checkout -b release/v<version> main`
2. Mettre à jour CHANGELOG.md : `python scripts/generate_changelog.py --version <version>`
3. Commit : `git add CHANGELOG.md && git commit -m 'docs: update changelog for v<version>'`

### ÉTAPE-4 — Création tag

1. Créer le tag signé : `git tag -s v<version> -m 'Release v<version>'`
2. Vérifier : `git tag -v v<version>`

### ÉTAPE-5 — Merge et push

1. Merger la release branch : `git checkout main && git merge --no-ff release/v<version>`
2. Push : `git push origin main --tags`
3. Supprimer la release branch : `git push origin --delete release/v<version>`

### ÉTAPE-6 — Validation post-release

1. Vérifier le tag sur remote : `git ls-remote --tags origin | grep v<version>`
2. Vérifier le CHANGELOG sur main : `git show main:CHANGELOG.md | grep <version>`
3. Vérifier la cohérence : `git log --oneline -5`

## Sortie

- Rapport de release
- Tag créé et signé
- CHANGELOG.md mis à jour
- Release branch supprimée

## Anti-patterns

- Tag sans SemVer valide
- Tag non signé
- Tag sans CHANGELOG.md
- Tag direct sur main
- Tag sur working tree sale
- Oublier de supprimer la release branch

## Journalisation

```
[RELEASE] version=<version> signed=<true|false> changelog=<updated|missing> branch=<release|main>
```

## Governance

- **Design** : `designs/git-tag-release-management.yaml`
- **Atom** : `ATOM-TAG-RELEASE-GOVERNANCE`
- **ADR** : ADR-2026-08-29-005-KERNEL-VERSIONING-POLICY
