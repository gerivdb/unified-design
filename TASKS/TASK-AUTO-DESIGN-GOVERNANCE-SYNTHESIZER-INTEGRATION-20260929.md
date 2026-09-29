---
type: TASK
version: "1.0.0"
date: "2026-09-29"
status: pending
priority: P2
intent_hash: 0xTASK_AUTO_DESIGN_GOVERNANCE_SYNTHESIZER_INTEGRATION_20260929
parent_epic: EPIC-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md
owner: L0-CANON
repo: gerivdb/unified-design
---

# TASK — Governance Synthesizer Integration

## Objectif

Intégrer CTULU `vibe-governance-synthesizer` dans `auto_promote.py` pour générer 6 artifacts (INTENT, EPIC, PRD, ADR, ISSUE, IMPENSE) + commit automatique.

## Périmètre

- **Fichier modifié** : `engine/auto_design/auto_promote.py`
- **Dépendance** : CTULU `tools/vibe-governance-synthesizer/`
- **Tests** : `tests/test_auto_design_argus_ctulu.py::test_governance_synthesizer_integration`

## Critères d'acceptation

1. `auto_promote.py` appelle `vibe-governance-synthesizer` pour promotion avancée
2. Génère 6 artifacts : INTENT, EPIC, PRD, ADR, ISSUE, IMPENSE
3. Commit automatique avec message conventionnel
4. Gestion d'erreur : rollback si synthèse échoue
5. Test unitaire passe

## Plan d'exécution

1. Importer `PromptParser`, `synthesizer` depuis CTULU
2. Adapter `promote()` pour détecter les candidats à promotion avancée
3. Appeler `PromptParser.parse()` puis synthèse
4. Commit automatique des artifacts générés
5. Gérer les erreurs
6. Ajouter test unitaire

## Références

- **INTENT** : `INTENT-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md`
- **PRD** : `PRD-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md` (P2-5)
- **MOC** : `MOC-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md` (P2-5)
- **CTULU** : `tools/vibe-governance-synthesizer/` → `synthesizer.py`
