---
type: MOC
version: "1.0"
date: "2026-09-22"
status: proposed
intent_hash: 0xMOC_JEVX_MDU_INTEGRATION_FIX_20260922
---

# MOC — JEVX MDU Integration Fix

**Repo** : `gerivdb/unified-design`  
**Strate** : L0-CANON  
**Statut** : proposed  
**Date** : 2026-09-22  
**Version** : 1.0 (corrections d'alignement JEVX/MDU)

---

## Vue d'ensemble

Ce MOC orchestre la correction des incohérences d'intégration de JEVX dans le MDU et les registres écosystémiques.

## Livrables

| # | Livrable | Chemin cible | Statut | Preuve d'exécution |
|---|----------|--------------|--------|-------------------|
| L1 | Corriger `do_not_create` JEVX | `GOVERNANCE-HUB/known_repositories.yaml` | ⬜ | — |
| L2 | Corriger `entrypoint` JEVX | `designs/jevx.yaml` | ⬜ | — |
| L3 | Clarifier `hardware_profile` JEVX | `designs/jevx.yaml` | ⬜ | — |
| L4 | Aligner `depends_on` JEVX sur MDU | `designs/jevx.yaml`, `designs/jevx-engineering.yaml` | ⬜ | — |
| L5 | Documenter `consumers` JEVX | `catalog/designs.index.yaml` | ⬜ | — |
| L6 | Documenter `consumers` pipeline JEVX | `catalog/pipelines.index.yaml` | ⬜ | — |
| L7 | Ajouter JEVX dans CLM pipeline | `designs/clm-pipeline/design.yaml` | ⬜ | — |
| L8 | Corriger `SCOPE.yaml` consumer CLM | `JEVX/SCOPE.yaml` | ⬜ | — |
| L9 | Dédupliquer `ONTOLOGY_DECLARATION.yaml` | `JEVX/ONTOLOGY_DECLARATION.yaml` | ⬜ | — |
| L10 | Marquer `security_guardrails` draft | `designs/jevx.yaml` | ⬜ | — |
| L11 | Marquer `constrained-parallel-decoding` draft | `designs/jevx-engineering.yaml` | ⬜ | — |
| L12 | Aligner `max_queue` sur code | `designs/jevx.yaml` | ⬜ | — |

## Dépendances

| Dépendance | Type | Raison |
|------------|------|--------|
| `PRD/PRD-MOC-JEVX-MDU-INTEGRATION-FIX-20260922.md` | amont | Spécification |
| `designs/jevx.yaml` | pair | Design JEVX |
| `designs/jevx-engineering.yaml` | pair | Design JEVX Engineering |
| `catalog/designs.index.yaml` | pair | Catalogue MDU |
| `catalog/pipelines.index.yaml` | pair | Catalogue pipelines |
| `GOVERNANCE-HUB/known_repositories.yaml` | pair | SOT repos |

## Gates et critères d'acceptation

| Gate | Critère formel | Validation | Statut |
|------|---------------|------------|--------|
| **G1** | `do_not_create: true` pour JEVX dans SOT | `known_repositories.yaml` | ⏳ À faire |
| **G2** | `entrypoint`, `hardware_profile`, `max_queue` corrigés | `designs/jevx.yaml` | ⏳ À faire |
| **G3** | `depends_on` résolus ou déplacés | `designs/jevx.yaml`, `designs/jevx-engineering.yaml` | ⏳ À faire |
| **G4** | `security_guardrails` et `constrained-parallel-decoding` marqués `draft` | designs | ⏳ À faire |
| **G5** | Consumers documentés dans catalogues | `catalog/designs.index.yaml`, `catalog/pipelines.index.yaml` | ⏳ À faire |
| **G6** | CLM pipeline cohérent avec JEVX | `designs/clm-pipeline/design.yaml` | ⏳ À faire |
| **G7** | `SCOPE.yaml` et `ONTOLOGY_DECLARATION.yaml` corrigés | JEVX repo | ⏳ À faire |

## Critères d'acceptation

- [ ] `GOVERNANCE-HUB/known_repositories.yaml` : `do_not_create: true` pour JEVX
- [ ] `designs/jevx.yaml` : `entrypoint: src/index.ts`, `hardware_profile` clarifié, `max_queue` aligné
- [ ] `designs/jevx.yaml` et `designs/jevx-engineering.yaml` : `depends_on` résolus
- [ ] `designs/jevx.yaml` : `security_guardrails` marquées `draft`
- [ ] `designs/jevx-engineering.yaml` : `constrained-parallel-decoding` marqué `draft`
- [ ] `catalog/designs.index.yaml` et `catalog/pipelines.index.yaml` : consumers documentés
- [ ] `designs/clm-pipeline/design.yaml` : cohérence JEVX/CLM
- [ ] `JEVX/SCOPE.yaml` : aucune référence invalide
- [ ] `JEVX/ONTOLOGY_DECLARATION.yaml` : aucun doublon
- [ ] Tous les designs passent validation

## Références

- `PRD/PRD-MOC-JEVX-MDU-INTEGRATION-FIX-20260922.md` — Spécification
- `PRD/PRD-MOC-JEVX-SOVEREIGN-OVERLAY-20260920.md` — Parent
- `designs/jevx.yaml` — Design JEVX
- `designs/jevx-engineering.yaml` — Design JEVX Engineering
- `catalog/designs.index.yaml` — Catalogue designs
- `catalog/pipelines.index.yaml` — Catalogue pipelines
- `GOVERNANCE-HUB/known_repositories.yaml` — SOT repos

## Preuves d'exécution

| Action | Date | Commit | Référence |
|--------|------|--------|-----------|
| Création MOC | 2026-09-22 | `à commettre` | `MOC/MOC-JEVX-MDU-INTEGRATION-FIX-20260922.md` |
