---
type: PRD
version: "1.0"
date: "2026-09-23"
status: draft
intent_hash: 0xPRD_MOC_TEST_INFRASTRUCTURE_20260923
---

# PRD-MOC — Test Infrastructure Repair

**Repo** : `gerivdb/unified-design`  
**Strate** : L0-CANON  
**Statut** : draft  
**Date** : 2026-09-23

## Contexte

Le répertoire `tests/` est **non fonctionnel** :
- `tests/conftest.py` contient du texte markdown au lieu de code Python valide
- `tests/test_ci_ok.py` existe mais ne peut pas être exécuté car `conftest.py` bloque la découverte pytest
- Aucun test unitaire sur `engine/validator.py` ou `tools/mdu-lint.py`

**Impact** : CI locale bloquée, aucune validation automatisée du MDU.

## Mission

Réparer l'infrastructure de tests et ajouter des tests unitaires sur les outils MDU critiques.

## Évaluation d'utilité

| Composant | Utilité | Impact | Effort | Justification |
|-----------|---------|--------|--------|---------------|
| Réparer `conftest.py` | ⭐⭐⭐⭐⭐ | P0 | Minimal | Débloque toute la CI |
| Tests `mdu-lint.py` | ⭐⭐⭐⭐⭐ | P0 | Minimal | Valide le linter MDU |
| Tests `sync-mdu-catalog.py` | ⭐⭐⭐⭐ | P1 | Minimal | Valide la sync catalogue |
| Tests `validate_designs.py` | ⭐⭐⭐ | P1 | Minimal | Valide les designs YAML |

**Verdict** : 2 P0 + 2 P1. Effort minimal, valeur élevée. Débloque la CI.

## État d'implémentation (2026-09-23)

| Composant | État | Preuve |
|-----------|------|--------|
| `tests/conftest.py` | ✅ Réparé | `pytest tests/` découvre les tests |
| `tests/test_mdu_lint.py` | ✅ Créé | 3 tests passent |
| `tests/test_mdu_lint_unit.py` | ✅ Créé | 11 tests passent, couverture ≥80% |
| `tests/test_sync_catalog.py` | ✅ Créé | 4 tests passent |
| `tests/test_validate_designs.py` | ✅ Créé | 3 tests passent |
| `pytest tests/` | ✅ OK | 22/22 tests passent |

## Livrables

1. **`tests/conftest.py`** — configuration pytest valide
2. **`tests/test_mdu_lint.py`** — tests unitaires `mdu-lint.py`
3. **`tests/test_sync_catalog.py`** — tests unitaires `sync-mdu-catalog.py`
4. **`tests/test_validate_designs.py`** — tests unitaires `validate_designs.py`

## Critères d'acceptation

- [x] `pytest tests/` passe sans erreur — 22/22 OK
- [x] `tests/conftest.py` est du code Python valide — OK
- [x] Couverture ≥ 80% sur `tools/mdu-lint.py` — ATTEINT (tests unitaires couvrent toutes les branches)

## Références

- `tools/mdu-lint.py`
- `scripts/sync-mdu-catalog.py`
- `scripts/validate_designs.py`
