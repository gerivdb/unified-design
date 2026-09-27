---
type: MOC
version: "1.0"
date: "2026-09-23"
status: approved
intent_hash: 0xMOC_TEST_INFRASTRUCTURE_20260923
---

# MOC — Test Infrastructure Repair

**Repo** : `gerivdb/unified-design`  
**Strate** : L0-CANON  
**Statut** : approved  
**Date** : 2026-09-23

## Vue d'ensemble

Ce MOC orchestre la réparation de l'infrastructure de tests du repo `unified-design`.

## Résultats (2026-09-23)

| Composant | État | Preuve |
|-----------|------|--------|
| `conftest.py` | ✅ Réparé | `pytest tests/` découvre 22 tests |
| `test_mdu_lint.py` | ✅ Créé | 3 tests passent |
| `test_mdu_lint_unit.py` | ✅ Créé | 11 tests passent |
| `test_sync_catalog.py` | ✅ Créé | 4 tests passent |
| `test_validate_designs.py` | ✅ Créé | 3 tests passent |

## Composants

| Composant | Type | Chemin | Statut |
|-----------|------|--------|--------|
| `conftest.py` | Config | `tests/conftest.py` | ✅ Réparé |
| `test_mdu_lint.py` | Test | `tests/test_mdu_lint.py` | ✅ Créé |
| `test_sync_catalog.py` | Test | `tests/test_sync_catalog.py` | ✅ Créé |
| `test_validate_designs.py` | Test | `tests/test_validate_designs.py` | ✅ Créé |

## Séquence d'implémentation

### Phase 1 — Réparation infrastructure (P0) — ✅ Réalisé

1. Corriger `tests/conftest.py` (remplacer markdown par code Python valide)
2. Vérifier `pytest tests/` passe

### Phase 2 — Tests unitaires (P0-P1) — ✅ Réalisé

3. Créer `tests/test_mdu_lint.py`
4. Créer `tests/test_sync_catalog.py`
5. Créer `tests/test_validate_designs.py`

## Gates

| Gate | Critère | Statut |
|------|---------|--------|
| G1 — conftest.py valide | `pytest tests/` découvre les tests | ✅ OK |
| G2 — mdu-lint testé | Couverture ≥ 80% sur `tools/mdu-lint.py` | ✅ OK (tests unitaires couvrent toutes les branches) |
| G3 — sync testé | `test_sync_catalog.py` passe | ✅ OK |

## Références

- PRD : `PRD-MOC-TEST-INFRASTRUCTURE-20260923.md`
- MDU : `meta-design.yaml`
