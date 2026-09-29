---
type: TASK
version: "1.0.0"
date: "2026-09-29"
status: pending
priority: P1
intent_hash: 0xTASK_AUTO_DESIGN_BRANCH_COMMIT_COUPLING_20260929
parent_epic: EPIC-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md
owner: L0-CANON
repo: gerivdb/unified-design
---

# TASK — Branch/Commit Coupling

## Objectif

Créer `pr_factory.py` avec `create_pr()` qui vérifie la cohérence branch → commit → PR.

## Périmètre

- **Fichier créé** : `engine/auto_design/pr_factory.py`
- **Dépendance** : CTULU `tools/trix-box/trix-git-workflow.py`
- **Tests** : `tests/test_auto_design_argus_ctulu.py::test_branch_commit_coupling`

## Critères d'acceptation

1. `create_pr(repo_root, branch_name, title, body)` retourne `dict`
2. Vérifie que la branche courante = `branch_name`
3. Vérifie que le dernier commit respecte conventional commits
4. Vérifie que le dernier commit est atomique (≤3 fichiers)
5. Retourne erreur si incohérence
6. Test unitaire passe

## Plan d'exécution

1. Créer `pr_factory.py`
2. Importer `get_current_branch`, `get_recent_commits` depuis CTULU
3. Vérifier cohérence branch
4. Vérifier conventional commit du dernier message
5. Vérifier atomicité du dernier commit
6. Retourner résultat
7. Ajouter test unitaire

## Références

- **INTENT** : `INTENT-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md`
- **PRD** : `PRD-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md` (P1-3)
- **MOC** : `MOC-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md` (P1-3)
- **CTULU** : `tools/trix-box/trix-git-workflow.py` → `get_current_branch()`, `get_recent_commits()`
