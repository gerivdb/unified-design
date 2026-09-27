---
type: MOC
version: "1.0"
date: "2026-09-22"
status: approved
intent_hash: 0xMOC_SYMBIOSE_COORDINATED_RELOAD_20260922
---

# MOC — Symbiose Coordinated Reload

**Repo** : `gerivdb/unified-design`  
**Strate** : L0-CANON  
**Statut** : approved  
**Date** : 2026-09-22  
**Version** : 1.0 (création workflow + garanties dérivées)

---

## Vue d'ensemble

Ce MOC orchestre la création et l'intégration du workflow `symbiose-coordinated-reload` dans l'architecture de l'écosystème gerivdb.

## Évaluation d'utilité

| Composant | Utilité | Impact | Effort | Justification |
|-----------|---------|--------|--------|---------------|
| Reconfiguration coordonnée | ⭐⭐⭐⭐⭐ | P0 | Minimal | Rend les symbiotes maintenables sans coupure |
| Garanties dérivées (lease TTL / 2) | ⭐⭐⭐⭐⭐ | P0 | Minimal | Borne vérifiable, pas magique |
| Drain inbound calls | ⭐⭐⭐⭐ | P1 | Minimal | Évite appels orphelins pendant swap |
| Concurrent reload check | ⭐⭐⭐⭐ | P1 | Minimal | Respecte swarm lease SL3 |
| Rollback WAL-based | ⭐⭐⭐⭐ | P1 | Minimal | Idempotence garantie |

**Verdict** : 2 P0 + 3 P1. Effort minimal, valeur opérationnelle élevée.

## Livrables

| # | Livrable | Chemin cible | Statut | Preuve d'exécution |
|---|----------|--------------|--------|-------------------|
| L1 | Workflow reconfiguration | `workflows/symbiose-coordinated-reload.yaml` | ✅ Créé | Commit `7720f29` — 2026-09-22 |
| L2 | Design parent | `designs/symbiose-reversible-plugin-architecture.yaml` | ✅ Créé | Commit `7720f29` — 2026-09-22 |
| L3 | Primitive lifecycle | `primitives/reversible-symbiose-lifecycle.yaml` | ✅ Créé | Commit `7720f29` — 2026-09-22 |
| L4 | Catalogue index | `catalog/designs.index.yaml` | ✅ Mis à jour | Commit `7720f29` — 2026-09-22 |
| L5 | PRD-MOC | `PRD/PRD-MOC-SYMBIOSE-COORDINATED-RELOAD-20260922.md` | ✅ Créé | Commit `efa046a` — 2026-09-22 |

## Dépendances

| Dépendance | Type | Raison |
|------------|------|--------|
| `designs/swarm-lease.yaml` | amont | Lease + exclusivité scope |
| `designs/safe-action-pattern.yaml` | amont | Contraintes exécutables |
| `primitives/reversible-symbiose-lifecycle.yaml` | pair | dissolution() + WAL snapshot |
| `designs/agent-observability-architecture.yaml` | pair | Observabilité |

## Gates et critères d'acceptation

| Gate | Critère formel | Validation | Statut |
|------|---------------|------------|--------|
| **G1** | Workflow validé par pre-commit hook | `git commit` | ✅ Passe |
| **G2** | Garanties dérivées documentées | Review ADR | ⏳ En attente |
| **G3** | Drain inbound + concurrent check | Review ADR | ⏳ En attente |
| **G4** | Rollback borné par lease TTL / 2 | Review ADR | ⏳ En attente |
| **G5** | ADR backing créé | GOVERNANCE-HUB | ⏳ À créer |

## Critères d'acceptation

- [x] Workflow `symbiose-coordinated-reload.yaml` créé avec 8 étapes + validation par étape
- [x] Garanties dérivées : at-least-once delivery, lease-held exclusivity, WAL-based idempotence
- [x] Rollback borné par `lease TTL / 2`
- [x] Drain inbound calls + concurrent reload check
- [ ] ADR `ADR-SYMBIOSE-COORDINATED-RELOAD-20260922.md` créé dans GOVERNANCE-HUB

## Références

- `designs/symbiose-reversible-plugin-architecture.yaml`
- `workflows/symbiose-coordinated-reload.yaml`
- `primitives/reversible-symbiose-lifecycle.yaml`
- `designs/swarm-lease.yaml`
- `designs/safe-action-pattern.yaml`
- `designs/agent-observability-architecture.yaml`

## Preuves d'exécution

| Action | Date | Commit | Référence |
|--------|------|--------|-----------|
| Création workflow | 2026-09-22 | `7720f29` | `workflows/symbiose-coordinated-reload.yaml` |
