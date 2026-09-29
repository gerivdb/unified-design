---
type: TASK
version: "1.0.0"
date: "2026-09-29"
status: pending
priority: P2
intent_hash: 0xTASK_AUTO_DESIGN_META_COHERENCE_GATE_20260929
parent_epic: EPIC-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md
owner: L0-CANON
repo: gerivdb/unified-design
---

# TASK — Meta-Coherence Gate

## Objectif

Ajouter `_check_meta_coherence()` à `verifier.py` pour bloquer le déploiement si ARGUS détecte des gaps/drifts écosystémiques.

## Périmètre

- **Fichier modifié** : `engine/auto_design/verifier.py`
- **Dépendance** : ARGUS `PRD/ecosystem_meta_coherence.py`
- **Tests** : `tests/test_auto_design_argus_ctulu.py::test_meta_coherence_gate`

## Critères d'acceptation

1. `_check_meta_coherence()` retourne `dict` avec `status` (OK/GAP_DETECTED)
2. Appelle `verify_meta_coherence(context)` depuis ARGUS
3. Bloque le déploiement si `status != OK`
4. Timeout 120s, fallback si ARGUS indisponible
5. Test unitaire passe

## Plan d'exécution

1. Importer `verify_meta_coherence` depuis ARGUS
2. Construire le contexte avec repo, design, bridges
3. Appeler `verify_meta_coherence(context)`
4. Interpréter le résultat
5. Retourner le statut
6. Ajouter test unitaire

## Références

- **INTENT** : `INTENT-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md`
- **PRD** : `PRD-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md` (P2-1)
- **MOC** : `MOC-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md` (P2-1)
- **ARGUS** : `PRD/ecosystem_meta_coherence.py` → `verify_meta_coherence()`
