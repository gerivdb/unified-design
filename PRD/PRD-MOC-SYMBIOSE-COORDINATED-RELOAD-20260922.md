---
type: PRD
version: "1.0"
date: "2026-09-22"
status: in_review
intent_hash: 0xPRD_MOC_SYMBIOSE_COORDINATED_RELOAD_20260922
---

# PRD-MOC — Symbiose Coordinated Reload

**Repo** : `gerivdb/unified-design`  
**Strate** : L0-CANON  
**Statut** : in_review  
**Date** : 2026-09-22  
**Version** : 1.0 (création workflow + garanties dérivées)

---

## Contexte

Le workflow initialement nommé `symbiose-hot-reload` souffre d'un faux-ami conceptuel : Cordis hot-reload est intra-processus et atomique, mais gerivdb est trans-repo et nécessite une coordination explicite.

Le workflow `symbiose-coordinated-reload` résout cette tension en :
1. Renommant conceptuellement l'opération ;
2. Documentant 3 garanties réelles (at-least-once delivery, lease-held exclusivity, WAL-based idempotence) ;
3. Dérivant la borne de rollback de `lease TTL / 2` plutôt que d'une valeur arbitraire ;
4. Ajoutant un drain explicite des appels entrants pendant la fenêtre de reconfiguration.

## Mission

Créer le workflow `symbiose-coordinated-reload` qui implémente la reconfiguration transactionnelle coordonnée des symbiotes gerivdb, avec :
- 8 étapes séquentielles avec validation par étape ;
- garanties dérivées de paramètres existants ;
- rollback automatique en cas d'échec ;
- anti-patterns explicites ;
- conformité swarm lease + WAZAA + KG-L + RLM-METRICS.

## Évaluation d'utilité

| Composant | Utilité | Impact | Effort | Justification |
|-----------|---------|--------|--------|---------------|
| Reconfiguration coordonnée | ⭐⭐⭐⭐⭐ | P0 | Minimal | Rend les symbiotes maintenables sans coupure |
| Garanties dérivées (lease TTL / 2) | ⭐⭐⭐⭐⭐ | P0 | Minimal | Borne vérifiable, pas magique |
| Drain inbound calls | ⭐⭐⭐⭐ | P1 | Minimal | Évite appels orphelins pendant swap |
| Concurrent reload check | ⭐⭐⭐⭐ | P1 | Minimal | Respecte swarm lease SL3 |
| Rollback WAL-based | ⭐⭐⭐⭐ | P1 | Minimal | Idempotence garantie |

**Verdict** : 2 P0 + 3 P1. Effort minimal, valeur opérationnelle élevée. Rend la maintenance des symbiotes sûre et auditable.

## Périmètre

| Inclut | Exclut |
|--------|--------|
| Workflow `symbiose-coordinated-reload.yaml` | Hot-reload atomique intra-processus |
| 8 étapes avec validation | Désactivation de BDCP pour maintenance |
| Garanties dérivées | Plugin system pour Flask/KIX |
| Drain inbound + concurrent check | Synchronisation cross-repo automatique |

## Livrables

| # | Livrable | Chemin cible | Statut | Preuve d'exécution |
|---|----------|--------------|--------|-------------------|
| L1 | Workflow reconfiguration | `workflows/symbiose-coordinated-reload.yaml` | ✅ Créé | Commit `7720f29` — 2026-09-22 |
| L2 | Design parent | `designs/symbiose-reversible-plugin-architecture.yaml` | ✅ Créé | Commit `7720f29` — 2026-09-22 |
| L3 | Primitive lifecycle | `primitives/reversible-symbiose-lifecycle.yaml` | ✅ Créé | Commit `7720f29` — 2026-09-22 |
| L4 | Catalogue index | `catalog/designs.index.yaml` | ✅ Mis à jour | Commit `7720f29` — 2026-09-22 |
| L5 | ADR backing | `GOVERNANCE-HUB/ADR/ADR-SYMBIOSE-COORDINATED-RELOAD-20260922.md` | ⏳ À créer | — |
| L6 | MOC orchestration | `MOC/MOC-SYMBIOSE-COORDINATED-RELOAD-20260922.md` | ⏳ À créer | — |

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
- [x] Anti-patterns explicites
- [ ] ADR `ADR-SYMBIOSE-COORDINATED-RELOAD-20260922.md` créé dans GOVERNANCE-HUB

## Risques

| Risque | Impact | Mitigation |
|--------|--------|------------|
| Fenêtre de reconfiguration trop longue | Élevé | Borne dérivée de lease TTL ; WAZAA drain_start/end |
| Appels entrants perdus | Moyen | Drain explicite + buffer optionnel |
| Reconfigurations concurrentes | Moyen | Swarm lease SL3 + check preflight |
| Rollback incomplet | Moyen | WAL snapshot + replay déterministe |

## Références

- `designs/symbiose-reversible-plugin-architecture.yaml` — Design parent
- `designs/swarm-lease.yaml` — Coordination primitive
- `designs/safe-action-pattern.yaml` — Contraintes exécutables
- `primitives/reversible-symbiose-lifecycle.yaml` — Lifecycle reversible
- `designs/agent-observability-architecture.yaml` — Observabilité

## Preuves d'exécution

| Action | Date | Commit | Référence |
|--------|------|--------|-----------|
| Création workflow | 2026-09-22 | `7720f29` | `workflows/symbiose-coordinated-reload.yaml` |
