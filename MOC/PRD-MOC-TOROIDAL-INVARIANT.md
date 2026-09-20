---
type: PRD-MOC
version: "1.1"
date: "2026-09-20"
status: accepted
intent_hash: 0xPRD_MOC_TOROIDAL_INVARIANT_20260920
citizen: "L0-CANON"
layer: "L0"
author: gerivdb
source_repo: gerivdb/unified-design
source_path: MOC/PRD-MOC-TOROIDAL-INVARIANT.md
parent_doc: PRD-MOC-UNIFIED-DESIGN-GOVERNANCE-20260816.md
related_adr: ADR-2026-09-20-001-toroidal-invariant-formalization.md, ADR-2026-09-05-002-graph-versioning-wazaa.md, ADR-2026-07-30-002-fractal-engineering-strata.md, ADR-2026-09-20-001-ZIG-VALIDATOR-CONTRACT.md
related_intent: INTENT-LLUX-TOROIDAL-CONSUMER
related_moc: PRD-MOC-LLUX-FLEX-INTEGRATION.md, PRD-MOC-LLUX-MASTER.md, PRD-MOC-LLUX-TOROIDAL-INTEGRATION.md, PRD-MOC-CROSS-REPO-DEPENDENCY-GRAPH.md
---

# PRD-MOC — Invariant Toroidal Transverse

## Résumé

Ce MOC documente la formalisation de l'**invariant toroidal transverse** χ=2 comme design canonique L0 de l'écosystème gerivdb. Il définit le noyau invariant commun à toutes les strates (L0-L5) et les points d'extension par strate.

**Source de vérité** : `unified-design/designs/toroidal-invariant/design.yaml`

**État courant** : FLEX (L4) fournit l'implémentation canonique. LLUX (L3) le consomme en local sur ENV2 via `ToroidalConsumer`. L'invariant χ=2 est vérifié avant chaque dispatch `piano_q243`. KG-L type-guard bloque tout fallback FP32.

---

## 1. Invariant Noyau

| Propriété | Valeur | Justification |
|-----------|--------|---------------|
| Caractéristique d'Euler | χ = 2 | Invariant topologique du tore |
| Taille état | 53 triplets | État toroïdal FLEX canonique |
| Modes | 3 (Glace=0, Plasma=1, Hybride=2) | Espace des états FLEX |
| Cœurs NUMA | 8 (2 sockets × 4 cœurs) | ENV2 HP Z600, cible minimale |
| Transfert | XMM 128-bit | SSE4.2, contrainte ENV2 |
| Cache L2 max | 256 KB/core | Westmere-EP |
| Cache L3 max | 12 MB (6 MB/socket) | Westmere-EP |

**Invariant vérifiable** : `invariant(triplet) == 2` pour tout triplet produit par `step()`.

---

## 2. Points d'Extension par Strate

| Strate | Extension | Rôle | Implémentation |
|--------|-----------|------|----------------|
| L0 | `toroidal-invariant` | Invariant mathématique | unified-design |
| L1 | `topology-registry` | Enregistrement SOT topologie | TOPOS, GOVERNANCE-HUB |
| L2 | `pipeline-orchestrator` | Orchestration flux selon topologie | CTULU, TRIX |
| L3 | `runtime-kernel` | Consommation tore pour inférence | LLUX `piano_q243` |
| L4 | `flex-toroidal` | Implémentation bare-metal | FLEX `toroidal/pipeline.zig` |
| L5 | `historical-snapshot` | Snapshot immuable du tore | WAZAA `graph_versions/` |

---

## 3. Consumers et Providers

| Repo | Rôle | Usage |
|------|------|-------|
| **FLEX** (L4) | Provider référence | Implémentation Zig canonique |
| **LLUX** (L3) | Consumer | `transformer.zig` consomme `ToroidalState` |
| **KG-L** (L4) | Provider/Enforcer | Type-guard vérifie χ=2 |
| **CTULU** (L2) | Consumer | Pipeline orchestration |
| **WAZAA** (L1) | Consumer | Event `graph.mutated` avec χ |
| **TOPOS** (L1) | Consumer | Enrichit `topology.yaml` |

---

## 4. Intégration avec FLEX

FLEX est l'**implémentation de référence L4** de l'invariant toroidal.

| Module FLEX | Rôle | Statut |
|-------------|------|--------|
| `src/core/toroidal/pipeline.zig` | État toroïdal + step() + invariant() | ✅ Implémenté |
| `src/core/hybrid/pipeline.zig` | Pipeline hybride tore + VLD + KG-L | ✅ Implémenté |
| `src/core/numa/detector.zig` | Détection topologie NUMA | ✅ Implémenté |
| `src/core/cache/optimizer.zig` | Cache blocking | ✅ Implémenté |
| `src/core/affinity/scheduler.zig` | 4 pools NUMA | ✅ Implémenté |
| `src/core/thermal/monitor.zig` | Surveillance thermique | ⚠️ Validation ENV2 pending |

---

## 5. Intégration avec LLUX

LLUX consomme l'invariant toroidal via `INTENT-LLUX-TOROIDAL-CONSUMER` :

| Point d'Entrée | Fichier | Rôle |
|----------------|---------|------|
| `ToroidalConsumer` | `src/transformer.zig` | Consomme `FLEX.ToroidalState` |
| `dispatchLayer()` | `src/transformer.zig` | Vérifie `invariant() == 2` avant `piano_q243` |
| `build.zig` | `build.zig` | Link FLEX lib + includes |
| Type-guard | `KG-L/exports/domain_links.json` | Domaine `toroidal_invariant` |

---

## 6. Type-Guard KG-L

```json
{
  "term": "toroidal_invariant",
  "definition": "Invariant toroidal χ=2 pour dispatch piano_q243",
  "constraints": ["chi == 2", "triplets == 53", "mode in [0,1,2]"]
}
```

Vérifications :
- Tout dispatch `piano_q243` précédé d'un `step()` toroidal
- `invariant(triplet) == 2` avant dispatch
- Aucun fallback FP32 ne contourne le mode Hybride

---

## 7. Critères de Validation

- [x] `unified-design/designs/toroidal-invariant/design.yaml` validé par `validate_designs.py`
- [x] `ATOM-TOROIDAL-INVARIANT` créé dans `unified-design/atoms/`
- [x] `designs/flex/design.yaml` mis à jour avec `inherits: [toroidal-invariant]`
- [x] `INTENT-LLUX-TOROIDAL-CONSUMER` créé et référencé (status: accepted)
- [x] Tests LLUX : 4 tests toroidaux passent dans `zig build test -Dcpu=westmere`
- [x] Type-guard KG-L bloque fallback FP32
- [x] Build réussi : `zig build -Dcpu=westmere` (0 erreurs)
- [x] FLEX `ToroidalPipeline` consommé par LLUX sans duplication d’état

---

## 8. Proof-of-Life

- [x] FLEX module root `src/core/toroidal.zig` créé pour consommation LLUX
- [x] `pipeline.zig` migré Zig 0.15 : 11 erreurs API corrigées
- [x] `ToroidalConsumer` LLUX créé dans `src/transformer_toroidal.zig`
- [x] `transformer.zig` intégré : `enableToroidal()` + vérification invariant
- [x] `build.zig` : module FLEX + 4 tests toroidaux enregistrés
- [x] `domain_links.json` : terme `toroidal_invariant` ajouté
- [x] `zig build -Dcpu=westmere` : 0 erreur
- [x] `zig build test -Dcpu=westmere` : 103/103 tests passed
- [x] Commit `2a717b0` — docs(LLUX): add TALEX postmortem 2026-09-20

---

## 9. Principe Écosystémique ENV2

Pour tous les repos de l'écosystème LLUX/FLEX/PIANO/KG-L, on vise le **fonctionnel en local sur ENV2** (ressources legacy limitées : 24 Go DDR3 ECC, Westmere/SSE4.2).

**Règle d'or** : FLEX reste la **source de vérité unique** de l’état toroïdal. LLUX ne crée pas d’état toroïdal propre ; il consomme FLEX via `ToroidalConsumer`.

**Frontières de propriété** :
- `FLEX/src/core/toroidal.zig` + `pipeline.zig` → FLEX seul propriétaire
- `LLUX/src/transformer_toroidal.zig` → LLUX consomme uniquement
- `LLUX/src/transformer.zig` → intégration `ToroidalConsumer` dans `Engine`
- `KG-L/exports/domain_links.json` → terme `toroidal_invariant` ajouté

---

## 8. Références

| Document | Rôle |
|----------|------|
| `unified-design/designs/toroidal-invariant/design.yaml` | Design L0 source |
| `ATOM-TOROIDAL-INVARIANT` | Atome MDU |
| `ADR-2026-09-20-001-toroidal-invariant-formalization.md` | ADR backing |
| `ADR-2026-09-05-002-graph-versioning-wazaa.md` | χ=2 invariant WAZAA |
| `ADR-2026-07-30-002-fractal-engineering-strata.md` | Fractal strata |
| `PRD-MOC-LLUX-FLEX-INTEGRATION.md` | Intégration FLEX↔LLUX |
| `FLEX/src/core/toroidal/pipeline.zig` | Implémentation canonique |
| `FLEX/src/core/hybrid/pipeline.zig` | Pipeline hybride |

---

**IntentHash** : 0xPRD_MOC_TOROIDAL_INVARIANT_20260920
**Status** : proposed
**Date** : 2026-09-20
