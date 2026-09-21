---
type: MOC
version: "1.0"
date: "2026-09-22"
status: in_review
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
| L2 | Guard pré-pytest | `scripts/run-governance-unit-tests.ps1` | ✅ Fait | Commit `6e8955e` |
| L3 | Guard pré-push | `.githooks/pre-push.ps1` | ✅ Fait | Commit `6e8955e` |
| L4 | PRD-MOC | `PRD/PRD-MOC-COMMAND-RESOLUTION-PROTOCOL-20260922.md` | ✅ Fait | Commit `dbb659e` |

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
| **G2** | `python` résolu avant `pytest` | Test script | ✅ Fait |
| **G3** | `python` et `kiva` résolus avant exécution | Test local_ci.ps1 | ✅ Fait |

## Critères d'acceptation

- [x] `designs/command-resolution-protocol.md` créé
- [x] `scripts/run-governance-unit-tests.ps1` résout `python` avant `pytest`
- [x] `scripts/local_ci.ps1` résout `python` et `kiva` avant exécution
- [x] PRD-MOC `PRD-MOC-COMMAND-RESOLUTION-PROTOCOL-20260922.md` créé

## Références

- `designs/command-resolution-protocol.md` — Design source
- `PRD/PRD-MOC-COMMAND-RESOLUTION-PROTOCOL-20260922.md` — Spécification
- `BOOTSTRAP_SOUVERAIN.md` — Règle B2
- `COHERENCE_TRANSVERSE.md` — Cohérence transverse

## Preuves d'exécution

| Action | Date | Commit | Référence |
|--------|------|--------|-----------|
| Création design | 2026-09-22 | `9f211a2` | `designs/command-resolution-protocol.md` |
| Création PRD-MOC | 2026-09-22 | `dbb659e` | `PRD/PRD-MOC-COMMAND-RESOLUTION-PROTOCOL-20260922.md` |
| Création MOC | 2026-09-22 | `6f025d2` | `MOC/MOC-COMMAND-RESOLUTION-PROTOCOL-20260922.md` |
| Création run-governance-unit-tests.ps1 | 2026-09-22 | `0710a0e` | `scripts/run-governance-unit-tests.ps1` |
| Modification local_ci.ps1 | 2026-09-22 | `6e8955e` | `scripts/local_ci.ps1` |
