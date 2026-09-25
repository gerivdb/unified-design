---
type: MOC
version: "1.0"
date: "2026-09-22"
status: approved
intent_hash: 0xMOC_REVERSIBLE_SYMBIOSE_LIFECYCLE_20260922
---

# MOC — Reversible Symbiose Lifecycle

**Repo** : `gerivdb/unified-design`  
**Strate** : L0-CANON  
**Statut** : approved  
**Date** : 2026-09-22  
**Version** : 1.0 (création primitive + dissolution_cost)

---

## Vue d'ensemble

Ce MOC orchestre la création et l'intégration de la primitive `reversible-symbiose-lifecycle` dans l'architecture de l'écosystème gerivdb.

## Évaluation d'utilité

| Composant | Utilité | Impact | Effort | Justification |
|-----------|---------|--------|--------|---------------|
| Lifecycle formation/maintenance/dissolution | ⭐⭐⭐⭐⭐ | P0 | Minimal | Rend la symbiose opérationnelle |
| Rollback par phase | ⭐⭐⭐⭐⭐ | P0 | Minimal | Garantit réversibilité effective |
| dissolution_cost planifié/non planifié | ⭐⭐⭐⭐⭐ | P0 | Minimal | Résout tension réversibilité ↔ durabilité |
| Événement ARGUS systématique | ⭐⭐⭐⭐ | P1 | Minimal | Auditabilité dissolution |

**Verdict** : 4 P0 + 1 P1. Effort minimal, valeur opérationnelle élevée.

## Livrables

| # | Livrable | Chemin cible | Statut | Preuve d'exécution |
|---|----------|--------------|--------|-------------------|
| L1 | Primitive lifecycle | `primitives/reversible-symbiose-lifecycle.yaml` | ✅ Créé | Commit `7720f29` — 2026-09-22 |
| L2 | Design parent | `designs/symbiose-reversible-plugin-architecture.yaml` | ✅ Créé | Commit `7720f29` — 2026-09-22 |
| L3 | Catalogue index | `catalog/designs.index.yaml` | ✅ Mis à jour | Commit `7720f29` — 2026-09-22 |
| L4 | PRD-MOC | `PRD/PRD-MOC-REVERSIBLE-SYMBIOSE-LIFECYCLE-20260922.md` | ✅ Créé | Commit `efa046a` — 2026-09-22 |

## Dépendances

| Dépendance | Type | Raison |
|------------|------|--------|
| `designs/swarm-lease.yaml` | amont | Lease formation/dissolution |
| `designs/safe-action-pattern.yaml` | amont | Contraintes exécutables |
| `designs/kg-l-causal-diff.yaml` | pair | Traçabilité IntentHash |
| `designs/agent-observability-architecture.yaml` | pair | Observabilité |

## Gates et critères d'acceptation

| Gate | Critère formel | Validation | Statut |
|------|---------------|------------|--------|
| **G1** | Primitive validée par pre-commit hook | `git commit` | ✅ Passe |
| **G2** | dissolution_cost documenté + ARGUS obligatoire | Review ADR | ⏳ En attente |
| **G3** | Rollback par phase explicite | Review ADR | ⏳ En attente |
| **G4** | ADR backing créé | GOVERNANCE-HUB | ⏳ À créer |

## Critères d'acceptation

- [x] Primitive `reversible-symbiose-lifecycle.yaml` créée avec lifecycle 3 phases + rollback
- [x] `dissolution_cost` planifié/non planifié documenté
- [x] Événement ARGUS systématique pour dissolution non planifiée
- [ ] ADR `ADR-REVERSIBLE-SYMBIOSE-LIFECYCLE-20260922.md` créé dans GOVERNANCE-HUB

## Références

- `designs/symbiose-reversible-plugin-architecture.yaml`
- `primitives/reversible-symbiose-lifecycle.yaml`
- `designs/swarm-lease.yaml`
- `designs/safe-action-pattern.yaml`
- `designs/kg-l-causal-diff.yaml`
- `designs/agent-observability-architecture.yaml`

## Preuves d'exécution

| Action | Date | Commit | Référence |
|--------|------|--------|-----------|
| Création primitive | 2026-09-22 | `7720f29` | `primitives/reversible-symbiose-lifecycle.yaml` |
