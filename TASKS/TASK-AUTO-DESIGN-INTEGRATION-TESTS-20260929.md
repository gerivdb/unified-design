---
type: TASK
version: "1.0.0"
date: "2026-09-29"
status: pending
priority: P1
intent_hash: 0xTASK_AUTO_DESIGN_INTEGRATION_TESTS_20260929
parent_epic: EPIC-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md
owner: L0-CANON
repo: gerivdb/unified-design
---

# TASK — Intégration Tests

## Objectif

Créer `tests/test_auto_design_argus_ctulu.py` avec 8 tests couvrant les intégrations P0.

## Périmètre

- **Fichier créé** : `tests/test_auto_design_argus_ctulu.py`
- **Dépendances** : pytest, ARGUS, CTULU
- **Couverture cible** : 80%

## Critères d'acceptation

1. `test_conventional_commit_scoring` — passe
2. `test_atomic_commit_checking` — passe
3. `test_commit_message_generation` — passe
4. `test_argus_bridge_validation` — passe
5. `test_argus_crossref_validation` — passe
6. `test_auto_commit_on_deploy` — passe (mock)
7. `test_branch_commit_coupling` — passe (mock)
8. `test_fallback_without_argus` — passe

## Plan d'exécution

1. Créer le fichier de tests
2. Mocker les appels ARGUS/CTULU
3. Écrire les 8 tests
4. Vérifier couverture 80%
5. Intégrer au pipeline pytest

## Références

- **INTENT** : `INTENT-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md`
- **PRD** : `PRD-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md` (P1-4)
- **MOC** : `MOC-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md` (P1-4)
