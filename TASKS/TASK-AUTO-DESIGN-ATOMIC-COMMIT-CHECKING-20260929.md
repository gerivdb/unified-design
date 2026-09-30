---
type: TASK
version: "1.0.0"
date: "2026-09-29"
status: pending
priority: P0
intent_hash: 0xTASK_AUTO_DESIGN_ATOMIC_COMMIT_CHECKING_20260929
parent_epic: EPIC-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md
owner: L0-CANON
repo: gerivdb/unified-design
---

# TASK — Atomic Commit Checking

## Objectif

Ajouter `_check_atomic_commits()` à `verifier.py` pour vérifier que les commits sont atomiques (≤3 fichiers par commit).

## Périmètre

- **Fichier modifié** : `engine/auto_design/verifier.py`
- **Dépendance** : CTULU `trix-git-workflow.py` (`run_git()`)
- **Tests** : `tests/test_auto_design_argus_ctulu.py::test_atomic_commit_checking`

## Critères d'acceptation

1. `_check_atomic_commits()` retourne `dict` avec `atomic` (bool), `max_files` (int), `violations` (list)
2. Détecte les commits >3 fichiers
3. Retourne le SHA et le nombre de fichiers pour chaque violation
4. Fallback local si CTULU indisponible
5. Test unitaire passe

## Plan d'exécution

1. Importer `run_git` depuis CTULU `trix-git-workflow.py`
2. Récupérer les 20 derniers SHAs
3. Pour chaque SHA, compter les fichiers modifiés via `diff-tree`
4. Identifier les violations (>3 fichiers)
5. Retourner le rapport
6. Ajouter test unitaire

## Références

- **INTENT** : `INTENT-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md`
- **PRD** : `PRD-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md` (P0-2)
- **MOC** : `MOC-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md` (P0-2)
- **CTULU** : `tools/trix-box/trix-git-workflow.py` → `run_git()`
