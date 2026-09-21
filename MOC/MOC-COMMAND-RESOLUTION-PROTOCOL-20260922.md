---
type: MOC
version: "1.0"
date: "2026-09-22"
status: proposed
intent_hash: 0xMOC_COMMAND_RESOLUTION_PROTOCOL_20260922
---

# MOC — Command Resolution Protocol

**Repo** : `gerivdb/unified-design`  
**Strate** : L0-CANON  
**Statut** : proposed  
**Date** : 2026-09-22  
**Version** : 1.0 (résolution obligatoire commandes externes)

---

## Vue d'ensemble

Ce MOC orchestre la création et l'intégration du design `command-resolution-protocol` dans l'écosystème gerivdb.

## Livrables

| # | Livrable | Chemin cible | Statut | Preuve d'exécution |
|---|----------|--------------|--------|-------------------|
| L1 | Design command resolution protocol | `designs/command-resolution-protocol.md` | ✅ Créé | Commit `à commettre` |
| L2 | Guard pré-pytest | `scripts/run-governance-unit-tests.ps1` | ⬜ | — |
| L3 | Guard pré-push | `.githooks/pre-push.ps1` | ⬜ | — |
| L4 | PRD-MOC | `PRD/PRD-MOC-COMMAND-RESOLUTION-PROTOCOL-20260922.md` | ✅ Créé | Commit `à commettre` |

## Dépendances

| Dépendance | Type | Raison |
|------------|------|--------|
| `designs/command-resolution-protocol.md` | pair | Design source |
| `scripts/run-governance-unit-tests.ps1` | pair | Script existant |
| `.githooks/pre-push.ps1` | pair | Hook existant |
| `BOOTSTRAP_SOUVERAIN.md` | amont | Règle B2 |

## Gates et critères d'acceptation

| Gate | Critère formel | Validation | Statut |
|------|---------------|------------|--------|
| **G1** | Design validé par pre-commit hook | `git commit` | ✅ Passe |
| **G2** | `python` résolu avant `pytest` | Test script | ⏳ À faire |
| **G3** | `python` résolu avant `validate_cross_repo` | Test hook | ⏳ À faire |

## Critères d'acceptation

- [ ] `designs/command-resolution-protocol.md` créé
- [ ] `scripts/run-governance-unit-tests.ps1` résout `python` avant `pytest`
- [ ] `.githooks/pre-push.ps1` résout `python` avant `validate_cross_repo.py`
- [ ] PRD-MOC `PRD-MOC-COMMAND-RESOLUTION-PROTOCOL-20260922.md` créé

## Références

- `designs/command-resolution-protocol.md` — Design source
- `PRD/PRD-MOC-COMMAND-RESOLUTION-PROTOCOL-20260922.md` — Spécification
- `BOOTSTRAP_SOUVERAIN.md` — Règle B2
- `COHERENCE_TRANSVERSE.md` — Cohérence transverse

## Preuves d'exécution

| Action | Date | Commit | Référence |
|--------|------|--------|-----------|
| Création design | 2026-09-22 | `à commettre` | `designs/command-resolution-protocol.md` |
| Création PRD-MOC | 2026-09-22 | `à commettre` | `PRD/PRD-MOC-COMMAND-RESOLUTION-PROTOCOL-20260922.md` |
