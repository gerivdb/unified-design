---
type: PRD
version: "1.0"
date: "2026-09-21"
status: proposed
intent_hash: 0xPRD_MOC_SYMBIOSE_ONTOLOGY_20260921
---

# PRD-MOC — Symbiose : relation réifiée durable entre entités autonomes gerivdb

**Repo** : `gerivdb/unified-design`  
**Strate** : L0-CANON  
**Statut** : proposed  
**Date** : 2026-09-21  
**Version** : 1.0 (création concept + intégration MDU)

---

## Contexte

L'écosystème gerivdb modélise déjà des dépendances statiques (`interdependance_ecosystemique`, `interdependance_strates`), mais il lui manque un concept relationnel **dynamique** pour représenter les interactions durables, co-évolutives et mesurables entre entités autonomes (citoyens, runners, services, repos, skills, routines).

Ce gap empêche :
- de qualifier formellement les **mutualismes**, **commensalismes** et **parasitismes** opérationnels ;
- de mesurer le **bénéficeNet** et le **coûtNet** d'une relation indépendamment de sa simple existence ;
- d'appliquer des **contraintes exécutables** (BDCP, swarm lease, KG-L, SOT) sur des relations durables ;
- de détecter et corriger les **parasitismes** via `ARGUS` dans un délai borné.

## Mission

Définir et intégrer le concept ontologique `symbiose` comme **relation réifiée n-aire, durable et co-évolutive** entre entités autonomes distinctes de l'écosystème gerivdb, avec :
- sous-classes `Mutualisme`, `Commensalisme`, `Parasitisme` ;
- dimensions primitives du bénéfice (anti-circularité) ;
- invariant temporel de correction des parasitismes ;
- arbre de décision à 2 temps (t0 structurel, t0+Δ dynamique) ;
- contraintes exécutables gerivdb (BDCP, swarm lease, IntentHash, KG-L, SOT).

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

**Verdict** : 4 P0 + 3 P1. Effort minimal, valeur élevée. Comble le gap entre `interdependance_ecosystemique` (statique) et les relations durables opérationnelles.

## Périmètre

| Inclut | Exclut |
|--------|--------|
| Concept `symbiose` dans ONTOLOGY | Implémentation code d'un moteur de symbiose |
| Sous-classes `Mutualisme`, `Commensalisme`, `Parasitisme` | Classification automatique sans validation humaine |
| Dimensions primitives du bénéfice | Pondérations `w_i` fixées arbitrairement |
| Invariant temporel `N_cycles = 3` | Ajustement automatique de `N_cycles` |
| Arbre de décision t0/t0+Δ | Validation automatique sans HITL |
| Contraintes exécutables gerivdb | Désactivation de BDCP pour symbiose |
| Indexation KG-L | Synchronisation cross-repo automatique |

## Livrables

1. **Concept `symbiose`** — `ONTOLOGY/concepts/symbiose.md` (v3.1 final)
2. **ADR backing** — `GOVERNANCE-HUB/ADR/ADR-SYMBIOSE-ONTOLOGY-20260921.md`
3. **Mise à jour `ONTOLOGY_DECLARATION.yaml`** — ajout du concept dans les concepts actifs
4. **Indexation KG-L** — références `symbiose`, `Mutualisme`, `Commensalisme`, `Parasitisme`
5. **Mise à jour `TOPOS/topology.yaml`** — ajout des relations de symbiose candidates
6. **Première mesure `RLM-METRICS`** sur `CTULU ↔ KG-CAUSAL` (instance candidate la plus documentée)

## Dépendances

| Dépendance | Type | Raison |
|------------|------|--------|
| `ONTOLOGY/concepts/symbiose.md` | amont | Concept ontologique |
| `ONTOLOGY/concepts/interdependance_ecosystemique.md` | amont | Concept parent |
| `ONTOLOGY/concepts/interdependance_strates.md` | amont | Concept parent |
| `ONTOLOGY/concepts/swarm-lease.md` | amont | Coordination trans-repo |
| `GOVERNANCE-HUB/ADR/ADR-SYMBIOSE-ONTOLOGY-20260921.md` | amont | ADR backing |
| `KG-L` | pair | Indexation relations |
| `RLM-METRICS` | pair | Mesure bénéficeNet |
| `TOPOS/topology.yaml` | pair | Dépendances bidirectionnelles |
| `ARGUS` | pair | Audit parasitisme |

## Critères d'acceptation

- [ ] Concept `symbiose` v3.1 final validé par ADR governance gate
- [ ] ADR `ADR-SYMBIOSE-ONTOLOGY-20260921` accepté
- [ ] `ONTOLOGY_DECLARATION.yaml` mis à jour avec le concept `symbiose`
- [ ] KG-L référence les 4 concepts (`symbiose`, `Mutualisme`, `Commensalisme`, `Parasitisme`)
- [ ] `TOPOS/topology.yaml` documente les instances candidates
- [ ] Première mesure `RLM-METRICS` sur `CTULU ↔ KG-CAUSAL` : `bénéficeNet > 0` confirmé

## Risques

| Risque | Impact | Mitigation |
|--------|--------|------------|
| Circularité bénéficeNet/mesure | Élevé | Dimensions primitives avant/après, indépendantes de la relation |
| Parasitisme non détecté | Élevé | Invariant temporel `N_cycles = 3` + ARGUS |
| Sur-déclaration de symbiose | Moyen | Arbre décision t0/t0+Δ + validation HITL |
| Coût indexation KG-L | Moyen | Indexation ciblée, pas systématique |

## Références

- `ONTOLOGY/concepts/symbiose.md` — Concept ontologique v3.1 final
- `ONTOLOGY/concepts/interdependance_ecosystemique.md` — Concept parent
- `ONTOLOGY/concepts/interdependance_strates.md` — Concept parent
- `ONTOLOGY/concepts/abstraction-levels.md` — Niveaux d'abstraction
- `ONTOLOGY/concepts/swarm-lease.md` — Coordination trans-repo
- `ONTOLOGY/concepts/skill-citizen-primus-triade.md` — Triade SKILLS/CITIZENS/PRIMUS
- `GOVERNANCE-HUB/ADR/ADR-SYMBIOSE-ONTOLOGY-20260921.md` — ADR backing
- `GOVERNANCE-HUB/ADR/ADR-001-bdcp-principles-formels.md` — BDCP inviolable
- `GOVERNANCE-HUB/ADR/ADR-0037-CITIZENS-CIRCUIT.md` — Circuit citoyens
- `KG-L` — Knowledge Graph (indexation)
- `RLM-METRICS` — Mesure bénéficeNet
- `TOPOS/topology.yaml` — Dépendances
- `ARGUS` — Audit parasitisme

---

*Generated by governance-doc-writer skill — Pattern C*
