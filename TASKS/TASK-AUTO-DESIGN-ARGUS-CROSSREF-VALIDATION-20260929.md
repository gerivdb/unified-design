---
type: TASK
version: "1.0.0"
date: "2026-09-29"
status: pending
priority: P0
intent_hash: 0xTASK_AUTO_DESIGN_ARGUS_CROSSREF_VALIDATION_20260929
parent_epic: EPIC-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md
owner: L0-CANON
repo: gerivdb/unified-design
---

# TASK — ARGUS Crossref Validation

## Objectif

Ajouter `_validate_crossrefs_argus()` à `verifier.py` pour valider les cross-refs via ARGUS `crossref_check.py`.

## Périmètre

- **Fichier modifié** : `engine/auto_design/verifier.py`
- **Dépendance** : ARGUS `scanners/crossref_check.py`
- **Tests** : `tests/test_auto_design_argus_ctulu.py::test_argus_crossref_validation`

## Critères d'acceptation

1. `_validate_crossrefs_argus()` retourne `dict` avec findings ARGUS
2. Appelle `crossref_check.py --repo <repo> --json`
3. Agrège les findings ORPHAN, GAP, STALE, BROKEN
4. Timeout 120s, fallback si ARGUS indisponible
5. Test unitaire passe

## Plan d'exécution

1. Importer `subprocess`, `json`
2. Construire le chemin vers ARGUS `scanners/crossref_check.py`
3. Exécuter avec `--repo` et `--json`
4. Parser le JSON de sortie
5. Retourner les findings
6. Ajouter test unitaire

## Références

- **INTENT** : `INTENT-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md`
- **PRD** : `PRD-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md` (P0-5)
- **MOC** : `MOC-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md` (P0-5)
- **ARGUS** : `scanners/crossref_check.py` → `scan_repo()`
