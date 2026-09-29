---
type: TASK
version: "1.0.0"
date: "2026-09-29"
status: pending
priority: P1
intent_hash: 0xTASK_AUTO_DESIGN_COMMIT_TEMPLATES_20260929
parent_epic: EPIC-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md
owner: L0-CANON
repo: gerivdb/unified-design
---

# TASK — Commit Templates

## Objectif

Créer les templates `commit_validator.py` et `commit_monitor.py` dans `templates/auto_design/` pour déploiement dans les repos industrialisés.

## Périmètre

- **Fichiers créés** :
  - `templates/auto_design/commit_validator.py` — valide conventional commits + atomicité
  - `templates/auto_design/commit_monitor.py` — auto-commit multi-repo
- **Dépendance** : CTULU `tools/trix-box/trix-git-workflow.py`
- **Tests** : déploiement test sur repo factice

## Critères d'acceptation

1. `commit_validator.py` valide conventional commits et atomicité
2. `commit_monitor.py` commit/push automatiquement les changements
3. Templates déployables via `industrializer.py`
4. Fonctionnent sur repo test

## Plan d'exécution

1. Créer `commit_validator.py` basé sur CTULU `trix-git-workflow.py`
2. Créer `commit_monitor.py` basé sur CTULU `trix-commit-monitor.py`
3. Adapter pour déploiement via `industrializer.py`
4. Tester déploiement sur repo factice

## Références

- **INTENT** : `INTENT-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md`
- **PRD** : `PRD-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md` (P1-1)
- **MOC** : `MOC-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md` (P1-1)
- **CTULU** : `tools/trix-box/trix-git-workflow.py`, `tools/trix-box/trix-commit-monitor.py`
