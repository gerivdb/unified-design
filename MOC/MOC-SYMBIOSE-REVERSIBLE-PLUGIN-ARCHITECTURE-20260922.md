---
type: MOC
version: "1.0"
date: "2026-09-22"
status: in_review
intent_hash: 0xMOC_SYMBIOSE_REVERSIBLE_PLUGIN_ARCHITECTURE_20260922
---

# MOC — Symbiose Reversible Plugin Architecture

**Repo** : `gerivdb/unified-design`  
**Strate** : L0-CANON  
**Statut** : in_review  
**Date** : 2026-09-22  
**Version** : 1.0 (création design + tensions assumées)

---

## Vue d'ensemble

Ce MOC orchestre la création et l'intégration du design `symbiose-reversible-plugin-architecture` dans l'architecture de l'écosystème gerivdb.

## Évaluation d'utilité

| Composant | Utilité | Impact | Effort | Justification |
|-----------|---------|--------|--------|---------------|
| Design architecture mapping | ⭐⭐⭐⭐⭐ | P0 | Minimal | Évite réinvention silencieuse |
| Principe noyau minimal explicite | ⭐⭐⭐⭐⭐ | P0 | Minimal | Protège BDCP, swarm lease, IntentHash |
| Contrat symbiose réversible | ⭐⭐⭐⭐⭐ | P0 | Minimal | Garantit dissolution propre |
| Tensions assumées documentées | ⭐⭐⭐⭐ | P1 | Minimal | 3 faux-amis transformés en choix de design |

**Verdict** : 4 P0 + 1 P1. Effort minimal, valeur architecturale élevée.

## Livrables

| # | Livrable | Chemin cible | Statut | Preuve d'exécution |
|---|----------|--------------|--------|-------------------|
| L1 | Design architecture | `designs/symbiose-reversible-plugin-architecture.yaml` | ✅ Créé | Commit `7720f29` — 2026-09-22 |
| L2 | Primitive lifecycle | `primitives/reversible-symbiose-lifecycle.yaml` | ✅ Créé | Commit `7720f29` — 2026-09-22 |
| L3 | Workflow reconfiguration | `workflows/symbiose-coordinated-reload.yaml` | ✅ Créé | Commit `7720f29` — 2026-09-22 |
| L4 | Catalogue index | `catalog/designs.index.yaml` | ✅ Mis à jour | Commit `7720f29` — 2026-09-22 |
| L5 | PRD-MOC design | `PRD/PRD-MOC-SYMBIOSE-REVERSIBLE-PLUGIN-ARCHITECTURE-20260922.md` | ✅ Créé | Commit `à commettre` |
| L6 | PRD-MOC primitive | `PRD/PRD-MOC-REVERSIBLE-SYMBIOSE-LIFECYCLE-20260922.md` | ✅ Créé | Commit `à commettre` |
| L7 | PRD-MOC workflow | `PRD/PRD-MOC-SYMBIOSE-COORDINATED-RELOAD-20260922.md` | ✅ Créé | Commit `à commettre` |
| L8 | ADR backing | `GOVERNANCE-HUB/ADR/ADR-SYMBIOSE-REVERSIBLE-ARCHITECTURE-20260922.md` | ⏳ À créer | — |

## Dépendances

| Dépendance | Type | Raison |
|------------|------|--------|
| `designs/swarm-lease.yaml` | amont | Coordination primitive |
| `designs/safe-action-pattern.yaml` | amont | Contraintes exécutables |
| `designs/design-ops-loop.yaml` | amont | Boucle opérationnelle |
| `designs/kg-l-causal-diff.yaml` | pair | Traçabilité causale |
| `designs/agent-observability-architecture.yaml` | pair | Observabilité |
| `GOVERNANCE-HUB/ADR/ADR-2026-08-28-001` | pair | ADR swarm lease |

## Gates et critères d'acceptation

| Gate | Critère formel | Validation | Statut |
|------|---------------|------------|--------|
| **G1** | Design validé par pre-commit hook | `git commit` | ✅ Passe |
| **G2** | 5 principes documentés + tensions assumées | Review ADR | ⏳ En attente |
| **G3** | Primitive lifecycle avec rollback explicite | Review ADR | ⏳ En attente |
| **G4** | Workflow avec garanties dérivées | Review ADR | ⏳ En attente |
| **G5** | ADR backing créé | GOVERNANCE-HUB | ⏳ À créer |

## Critères d'acceptation

- [x] Design `symbiose-reversible-plugin-architecture.yaml` créé
- [x] Primitive `reversible-symbiose-lifecycle.yaml` créée
- [x] Workflow `symbiose-coordinated-reload.yaml` créé
- [x] Catalogue `catalog/designs.index.yaml` mis à jour
- [x] PRD-MOCs créés pour chaque artefact
- [ ] ADR `ADR-SYMBIOSE-REVERSIBLE-ARCHITECTURE-20260922.md` créé dans GOVERNANCE-HUB

## Références

- `designs/symbiose-reversible-plugin-architecture.yaml`
- `primitives/reversible-symbiose-lifecycle.yaml`
- `workflows/symbiose-coordinated-reload.yaml`
- `designs/swarm-lease.yaml`
- `designs/safe-action-pattern.yaml`
- `designs/design-ops-loop.yaml`
- `designs/kg-l-causal-diff.yaml`
- `designs/agent-observability-architecture.yaml`
- `GOVERNANCE-HUB/ADR/ADR-2026-08-28-001`

## Preuves d'exécution

| Action | Date | Commit | Référence |
|--------|------|--------|-----------|
| Création design + primitive + workflow | 2026-09-22 | `7720f29` | 3 artefacts + catalogue |
| Création PRD-MOCs | 2026-09-22 | `à commettre` | 3 PRD-MOC files |
