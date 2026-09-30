---
type: TASK
version: "1.0.0"
date: "2026-09-29"
status: pending
priority: P0
intent_hash: 0xTASK_AUTO_DESIGN_CONVENTIONAL_COMMIT_SCORING_20260929
parent_epic: EPIC-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md
owner: L0-CANON
repo: gerivdb/unified-design
---

# TASK — Conventional Commit Scoring

## Objectif

Ajouter `_score_conventional_commit_adherence()` à `analyzer.py` pour évaluer la conformité des commits du repo aux conventional commits.

## Périmètre

- **Fichier modifié** : `engine/auto_design/analyzer.py`
- **Dépendance** : CTULU `trix-git-workflow.py` (`get_recent_commits()`)
- **Tests** : `tests/test_auto_design_argus_ctulu.py::test_conventional_commit_scoring`

## Critères d'acceptation

1. `_score_conventional_commit_adherence()` retourne un int 0-100
2. Le score reflète le % de commits conformes parmi les 20 derniers
3. Pattern reconnu : `^(feat|fix|docs|test|refactor|chore|ci|build|revert|style|perf)`
4. Fallback local si CTULU indisponible
5. Test unitaire passe

## Plan d'exécution

1. Importer `get_recent_commits` depuis CTULU `trix-git-workflow.py`
2. Récupérer les 20 derniers commits
3. Appliquer le pattern regex
4. Calculer le score
5. Ajouter le score à `scores` dans `analyze()`
6. Mettre à jour `_recommendations()` si score < 80
7. Ajouter test unitaire

## Références

- **INTENT** : `INTENT-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md`
- **PRD** : `PRD-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md` (P0-1)
- **MOC** : `MOC-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md` (P0-1)
- **CTULU** : `tools/trix-box/trix-git-workflow.py` → `get_recent_commits()`
