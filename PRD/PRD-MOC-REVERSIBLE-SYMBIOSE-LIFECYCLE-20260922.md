---
type: PRD
version: "1.0"
date: "2026-09-22"
status: approved
intent_hash: 0xPRD_MOC_REVERSIBLE_SYMBIOSE_LIFECYCLE_20260922
---

# PRD-MOC — Reversible Symbiose Lifecycle

**Repo** : `gerivdb/unified-design`  
**Strate** : L0-CANON  
**Statut** : approved  
**Date** : 2026-09-22  
**Version** : 1.0 (création primitive + dissolution_cost)

---

## Contexte

Le design `symbiose-reversible-plugin-architecture.yaml` établit la réversibilité comme invariant de premier ordre. Il manque une **primitive exécutable** qui implémente ce invariant sur le cycle de vie des symbiotes :

- **Formation** : contrat, lease, KG-L edges, WAZAA hello, WAL snapshot
- **Maintenance** : mesure bénéficeNet, heartbeat, renouvellement lease
- **Dissolution** : arrêt flux, release lease, révocation edges, WAZAA bye, WAL compact, IntentHash

La primitive doit garantir que **toute dissolution est coûteuse et tracée** (tension #1 résolue).

## Mission

Créer la primitive `reversible-symbiose-lifecycle` qui implémente le cycle de vie réversible des symbiotes gerivdb, avec :
- preconditions/postconditions par phase ;
- rollback explicite pour chaque phase réversible ;
- `dissolution_cost` documenté (planifié vs non planifié) ;
- événement ARGUS systématique pour dissolution non planifiée ;
- validation par commandes gerivdb existantes.

## Évaluation d'utilité

| Composant | Utilité | Impact | Effort | Justification |
|-----------|---------|--------|--------|---------------|
| Lifecycle formation/maintenance/dissolution | ⭐⭐⭐⭐⭐ | P0 | Minimal | Rend la symbiose opérationnelle |
| Rollback par phase | ⭐⭐⭐⭐⭐ | P0 | Minimal | Garantit réversibilité effective |
| dissolution_cost planifié/non planifié | ⭐⭐⭐⭐⭐ | P0 | Minimal | Résout tension réversibilité ↔ durabilité |
| Événement ARGUS systématique | ⭐⭐⭐⭐ | P1 | Minimal | Auditabilité dissolution |
| Validation par commandes existantes | ⭐⭐⭐⭐ | P1 | Minimal | Intégration immédiate |

**Verdict** : 4 P0 + 1 P1. Effort minimal, valeur opérationnelle élevée. Rend le design réversible exécutable.

## Périmètre

| Inclut | Exclut |
|--------|--------|
| Primitive `reversible-symbiose-lifecycle.yaml` | Moteur de résolution `ctx.<service>` |
| dissolution_cost planifié/non planifié | Hot-reload atomique intra-processus |
| Événement ARGUS pour dissolution non planifiée | Désactivation de BDCP pour symbiose |
| Validation par commandes gerivdb existantes | Synchronisation cross-repo automatique |

## Livrables

| # | Livrable | Chemin cible | Statut | Preuve d'exécution |
|---|----------|--------------|--------|-------------------|
| L1 | Primitive lifecycle | `primitives/reversible-symbiose-lifecycle.yaml` | ✅ Créé | Commit `7720f29` — 2026-09-22 |
| L2 | Design parent | `designs/symbiose-reversible-plugin-architecture.yaml` | ✅ Créé | Commit `7720f29` — 2026-09-22 |
| L3 | Catalogue index | `catalog/designs.index.yaml` | ✅ Mis à jour | Commit `7720f29` — 2026-09-22 |
| L4 | ADR backing | `GOVERNANCE-HUB/ADR/ADR-REVERSIBLE-SYMBIOSE-LIFECYCLE-20260922.md` | ⏳ À créer | — |

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
- [x] Validation par commandes gerivdb existantes (`balise`, `KG-L`, `WAZAA`, `RLM-METRICS`)
- [ ] ADR `ADR-REVERSIBLE-SYMBIOSE-LIFECYCLE-20260922.md` créé dans GOVERNANCE-HUB

## Risques

| Risque | Impact | Mitigation |
|--------|--------|------------|
| Dissolution coûteuse = dissuasion | Élevé | dissolution_cost n'empêche pas la dissolution, il la rend tracée |
| ARGUS overhead | Moyen | Événement unique par dissolution, pas par mesure |
| Rollback partiel | Moyen | WAL snapshot + replay déterministe |

## Références

- `designs/symbiose-reversible-plugin-architecture.yaml` — Design parent
- `designs/swarm-lease.yaml` — Coordination primitive
- `designs/safe-action-pattern.yaml` — Contraintes exécutables
- `designs/kg-l-causal-diff.yaml` — Traçabilité causale
- `designs/agent-observability-architecture.yaml` — Observabilité

## Preuves d'exécution

| Action | Date | Commit | Référence |
|--------|------|--------|-----------|
| Création primitive | 2026-09-22 | `7720f29` | `primitives/reversible-symbiose-lifecycle.yaml` |
