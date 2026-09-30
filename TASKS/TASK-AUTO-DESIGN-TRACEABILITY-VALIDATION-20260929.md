---
type: TASK
version: "1.0.0"
date: "2026-09-29"
status: pending
priority: P2
intent_hash: 0xTASK_AUTO_DESIGN_TRACEABILITY_VALIDATION_20260929
parent_epic: EPIC-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md
owner: L0-CANON
repo: gerivdb/unified-design
---

# TASK — Traceability Validation

## Objectif

Ajouter `_validate_traceability()` à `verifier.py` pour valider la traçabilité cross-repo via CTULU `trace_graph.py` et `trace_validator.py`.

## Périmètre

- **Fichier modifié** : `engine/auto_design/verifier.py`
- **Dépendance** : CTULU `tools/traceability/trace_graph.py`, `tools/traceability/trace_validator.py`
- **Tests** : `tests/test_auto_design_argus_ctulu.py::test_traceability_validation`

## Critères d'acceptation

1. `_validate_traceability()` retourne `dict` avec violations
2. Appelle `build_and_save()` puis `TraceabilityValidator().validate()`
3. Détecte orphelins, liens cassés, status mismatch
4. Timeout 120s, fallback si CTULU indisponible
5. Test unitaire passe

## Plan d'exécution

1. Importer `build_and_save`, `TraceabilityValidator` depuis CTULU
2. Construire le graphe de traçabilité
3. Valider la cohérence
4. Retourner les violations
5. Ajouter test unitaire

## Références

- **INTENT** : `INTENT-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md`
- **PRD** : `PRD-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md` (P2-2)
- **MOC** : `MOC-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md` (P2-2)
- **CTULU** : `tools/traceability/trace_graph.py`, `tools/traceability/trace_validator.py`
