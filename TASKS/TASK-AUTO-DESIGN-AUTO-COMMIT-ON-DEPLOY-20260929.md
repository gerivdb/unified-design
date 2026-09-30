---
type: TASK
version: "1.0.0"
date: "2026-09-29"
status: pending
priority: P1
intent_hash: 0xTASK_AUTO_DESIGN_AUTO_COMMIT_ON_DEPLOY_20260929
parent_epic: EPIC-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md
owner: L0-CANON
repo: gerivdb/unified-design
---

# TASK — Auto-Commit on Deploy

## Objectif

Ajouter `deploy_with_auto_commit()` à `industrializer.py` pour commit et push automatiquement les changements après déploiement.

## Périmètre

- **Fichier modifié** : `engine/auto_design/industrializer.py`
- **Dépendance** : CTULU `tools/trix-box/trix-commit-monitor.py`
- **Tests** : `tests/test_auto_design_argus_ctulu.py::test_auto_commit_on_deploy`

## Critères d'acceptation

1. `deploy_with_auto_commit()` commit les changements après déploiement
2. Message de commit : `feat(auto_design): industrialize <repo_name>`
3. Push automatique si configuré
4. Gestion d'erreur : rollback si commit échoue
5. Test unitaire passe

## Plan d'exécution

1. Importer `git_status`, `git_add`, `git_commit`, `git_push` depuis CTULU
2. Exécuter `deploy()`
3. Vérifier les changements via `git_status()`
4. Stage et commit avec message standardisé
5. Push si remote configuré
6. Gérer les erreurs
7. Ajouter test unitaire

## Références

- **INTENT** : `INTENT-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md`
- **PRD** : `PRD-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md` (P1-2)
- **MOC** : `MOC-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md` (P1-2)
- **CTULU** : `tools/trix-box/trix-commit-monitor.py` → `git_status()`, `git_add()`, `git_commit()`, `git_push()`
