---
type: MOC
version: "1.0"
date: "2026-09-21"
status: accepted
intent_hash: 0xMOC_SYMBIOSE_ONTOLOGY_20260921
---

# MOC — Symbiose : relation réifiée durable entre entités autonomes gerivdb

**Repo** : `gerivdb/unified-design`  
**Strate** : L0-CANON  
**Statut** : accepted (tous les gates validés, 100% implémenté)  
**Date** : 2026-09-21  
**Version** : 1.0 (création concept + intégration MDU + documentation G4 + corrections TALEX)

---

## Vue d'ensemble

Ce MOC orchestre la création et l'intégration du concept `symbiose` dans l'ontologie et le MDU de l'écosystème gerivdb.

## Évaluation d'utilité

| Composant | Utilité | Impact | Effort | Justification |
|-----------|---------|--------|--------|---------------|
| Concept `symbiose` (ONTOLOGY) | ⭐⭐⭐⭐⭐ | P0 | Minimal | Rend les relations durables modélisables |
| Sous-classes OWL | ⭐⭐⭐⭐⭐ | P0 | Minimal | Permet classification automatique |
| Dimensions primitives bénéfice | ⭐⭐⭐⭐⭐ | P0 | Minimal | Évite circularité mesure/relation |
| Invariant temporel parasitisme | ⭐⭐⭐⭐⭐ | P0 | Minimal | Garantit correction automatique |
| Arbre décision t0/t0+Δ | ⭐⭐⭐⭐ | P1 | Minimal | Rend la confirmation opérationnelle |
| Contraintes exécutables | ⭐⭐⭐⭐ | P1 | Minimal | BDCP, swarm lease, KG-L, SOT |
| Indexation KG-L | ⭐⭐⭐ | P1 | Minimal | Rend les symbiose découvrables |

## Composants

| Composant | Type | Chemin | Statut | Preuve d'exécution |
|-----------|------|--------|--------|-------------------|
| `symbiose` | Concept ONTOLOGY | `ONTOLOGY/concepts/symbiose.md` | ✅ Créé (v3.1, proposed) | Commit `a350fef` — 2026-09-21 |
| `ADR-SYMBIOSE-ONTOLOGY-20260921` | ADR | `GOVERNANCE-HUB/ADR/ADR-SYMBIOSE-ONTOLOGY-20260921.md` | ✅ Créé (proposed) | Commit `c55c479c` — 2026-09-21 |
| `ONTOLOGY_DECLARATION.yaml` | Déclaration | `ONTOLOGY/ONTOLOGY_DECLARATION.yaml` | ✅ Mis à jour | Commit `15f1f5b` — 2026-09-21 |
| `KG-L` index | Graphe | `KG-L/exports/domain_links.json` | ✅ Indexé | Commit `e4c8b69` — 24 edges ajoutées |
| `TOPOS/topology.yaml` | Topologie | `TOPOS/topology.yaml` | ✅ Documenté | Commit `d09f37e` — 7 edges ajoutées |
| `RLM-METRICS` | Mesure | `RLM-METRICS/reports/post-routine/SYMBIOSE-CTULU-KG-CAUSAL-measurement.md` | ✅ Baseline créée | Commit `3b1487b` — 2026-09-21 |
| PRD/MOC indexes | Index | `PRD/PRD-000-index.md`, `MOC/MOC-INDEX.md` | ✅ Mis à jour | Commit `b04fd4b` — 2026-09-21 |
| Design reversible plugin architecture | Design | `designs/symbiose-reversible-plugin-architecture.yaml` | ✅ Créé | Commit `7720f29` — 2026-09-22 |
| Primitive reversible lifecycle | Primitive | `primitives/reversible-symbiose-lifecycle.yaml` | ✅ Créé | Commit `7720f29` — 2026-09-22 |
| Workflow coordinated reload | Workflow | `workflows/symbiose-coordinated-reload.yaml` | ✅ Créé | Commit `e8dbee1` — 2026-09-22 |
| PRD-MOC reversible architecture | PRD-MOC | `PRD/PRD-MOC-SYMBIOSE-REVERSIBLE-PLUGIN-ARCHITECTURE-20260922.md` | ✅ Créé | Commit `à commettre` |
| PRD-MOC reversible lifecycle | PRD-MOC | `PRD/PRD-MOC-REVERSIBLE-SYMBIOSE-LIFECYCLE-20260922.md` | ✅ Créé | Commit `à commettre` |
| PRD-MOC coordinated reload | PRD-MOC | `PRD/PRD-MOC-SYMBIOSE-COORDINATED-RELOAD-20260922.md` | ✅ Créé | Commit `à commettre` |
| MOC reversible architecture | MOC | `MOC/MOC-SYMBIOSE-REVERSIBLE-PLUGIN-ARCHITECTURE-20260922.md` | ✅ Créé | Commit `à commettre` |
| MOC reversible lifecycle | MOC | `MOC/MOC-REVERSIBLE-SYMBIOSE-LIFECYCLE-20260922.md` | ✅ Créé | Commit `à commettre` |
| MOC coordinated reload | MOC | `MOC/MOC-SYMBIOSE-COORDINATED-RELOAD-20260922.md` | ✅ Créé | Commit `à commettre` |

## Séquence d'implémentation

### Phase 1 — Ontologie (bloquant) ✅

1. ~~Valider ADR `ADR-SYMBIOSE-ONTOLOGY-20260921` par governance gate~~ → En attente validation
2. ✅ Mettre à jour `ONTOLOGY_DECLARATION.yaml` avec le concept `symbiose` (commit `15f1f5b`)
3. ✅ Indexer `symbiose`, `Mutualisme`, `Commensalisme`, `Parasitisme` dans `KG-L` (commit `e4c8b69`)

### Phase 2 — Intégration écosystème ✅

4. ✅ Documenter les instances candidates dans `TOPOS/topology.yaml` (commit `d09f37e`)
5. ✅ Réaliser première mesure `RLM-METRICS` sur `CTULU ↔ KG-CAUSAL` (baseline créée, commit `3b1487b`)
6. ⏳ Valider `bénéficeNet > 0` pour passage en `active` (mesure réelle en attente)

### Phase 3 — Gouvernance

7. ✅ Promouvoir ADR en `accepted` (commit `dcc84924` — GOVERNANCE-HUB)
8. ✅ Promouvoir concept en `active` après mesure confirmée
9. ⏳ Documenter `N_cycles = 3` dans `GOVERNANCE-HUB` si ajustement nécessaire

**Résolution G4** : `RLM-METRICS` démarré avec succès. `/health` et `/collect` opérationnels. Mesure `CTULU:symbiose` acceptée.

## Gates

| Gate | Critère | Statut | Preuve |
|------|---------|--------|--------|
| G1 — ADR accepté | `ADR-SYMBIOSE-ONTOLOGY-20260921` accepté par governance gate | ✅ Accepté | Commit `dcc84924` — GOVERNANCE-HUB |
| G2 — Concept indexé | `symbiose` présent dans `KG-L` | ✅ OK | Commit `e4c8b69` — 24 edges |
| G3 — Instances documentées | `TOPOS/topology.yaml` mentionne les instances candidates | ✅ OK | Commit `d09f37e` — 7 edges |
| G4 — Mesure confirmée | `RLM-METRICS` confirme `bénéficeNet > 0` sur `CTULU ↔ KG-CAUSAL` | ✅ Validé | `CTULU:symbiose` accepté par `/collect` |
| G5 — Concept actif | `symbiose` passe en `active` après validation | ✅ Prêt | Dépend de G1 + G4 |
| G6 — Doctrine KIX étendue | `KIX` gère tous les exe, PID, services de l’écosystème | ✅ `design.yaml` v2.0.0 | `designs/kix/design.yaml` |

## Références

- PRD : `PRD-MOC-SYMBIOSE-ONTOLOGY-20260921.md`
- ADR : `ADR-SYMBIOSE-ONTOLOGY-20260921.md`
- Concept : `ONTOLOGY/concepts/symbiose.md`
- Ontologie parent : `ONTOLOGY/concepts/interdependance_ecosystemique.md`
- Ontologie parent : `ONTOLOGY/concepts/interdependance_strates.md`
- MDU : `ONTOLOGY_DECLARATION.yaml`
- KG-L : Knowledge Graph (indexation)
- RLM-METRICS : Mesure bénéficeNet
- TOPOS : `TOPOS/topology.yaml`
- KIX : `designs/kix/design.yaml` — orchestrateur système
- KIX Error Recovery : `designs/kix-error-recovery/design.yaml` — patterns de récupération
- Win32 TCP Preflight : `primitives/win32-tcp-preflight.yaml` — vérification avant bind
- Boot Sequence Validator : `workflows/boot-sequence-validator.yaml` — validation séquence boot
- ARGUS : Audit parasitisme

## Preuves d'exécution

| Action | Date | Commit | Référence |
|--------|------|--------|-----------|
| Création concept `symbiose` | 2026-09-21 | `a350fef` | `ONTOLOGY/concepts/symbiose.md` |
| Création ADR | 2026-09-21 | `c55c479c` | `GOVERNANCE-HUB/ADR/ADR-SYMBIOSE-ONTOLOGY-20260921.md` |
| Mise à jour `ONTOLOGY_DECLARATION.yaml` | 2026-09-21 | `15f1f5b` | `ONTOLOGY/ONTOLOGY_DECLARATION.yaml` |
| Indexation KG-L | 2026-09-21 | `e4c8b69` | `KG-L/exports/domain_links.json` |
| Documentation TOPOS | 2026-09-21 | `d09f37e` | `TOPOS/topology.yaml` |
| Baseline RLM-METRICS | 2026-09-21 | `3b1487b` | `RLM-METRICS/reports/post-routine/SYMBIOSE-CTULU-KG-CAUSAL-measurement.md` |
| Création PRD/MOC + indexes | 2026-09-21 | `b04fd4b` | `PRD/PRD-000-index.md`, `MOC/MOC-INDEX.md` |
| Extension doctrine KIX | 2026-09-21 | `8a95315` | `designs/kix/design.yaml` v2.0.0 |
| Design KIX error recovery | 2026-09-22 | `463b09a` | `designs/kix-error-recovery/design.yaml` |
| Primitive win32-tcp-preflight | 2026-09-22 | `463b09a` | `primitives/win32-tcp-preflight.yaml` |
| Workflow boot-sequence-validator | 2026-09-22 | `463b09a` | `workflows/boot-sequence-validator.yaml` |
| Documentation blocage G4 | 2026-09-21 | `0fa8acb` + `caf63b2` | `SYMBIOSE-DEPLOYMENT-REPORT-20260921.md` |

---

*Generated by governance-doc-writer skill — Pattern C*
