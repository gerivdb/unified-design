---
type: TASK
version: "1.0.0"
date: "2026-09-29"
status: pending
priority: P2
intent_hash: 0xTASK_AUTO_DESIGN_NODEX_CLASSIFICATION_20260929
parent_epic: EPIC-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md
owner: L0-CANON
repo: gerivdb/unified-design
---

# TASK — NODEX Component Classification

## Objectif

Intégrer ARGUS `nodex.py` dans `generator.py` pour classifier les composants avec KG-L et ontologie.

## Périmètre

- **Fichier modifié** : `engine/auto_design/generator.py`
- **Dépendance** : ARGUS `runners/nodex.py`
- **Tests** : `tests/test_auto_design_argus_ctulu.py::test_nortex_classification`

## Critères d'acceptation

1. `_detect_components()` utilise NODEX pour classifier les composants
2. Retourne les composants avec type sémantique (REPO, TOOL, SERVICE, etc.)
3. Alignement ontologique vérifié
4. Fallback heuristique si NODEX indisponible
5. Test unitaire passe

## Plan d'exécution

1. Importer `NodexRunnerEffective` depuis ARGUS
2. Pour chaque composant détecté, appeler `_execute({"entity_id": comp, "query_type": "classify"})`
3. Filtrer les composants avec `ontology_alignment.type_valid`
4. Retourner la liste classée
5. Ajouter test unitaire

## Références

- **INTENT** : `INTENT-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md`
- **PRD** : `PRD-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md` (P2-3)
- **MOC** : `MOC-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md` (P2-3)
- **ARGUS** : `runners/nodex.py` → `NodexRunnerEffective()._execute()`
- **KG-L** : `ecosystem_kg_full.json`
