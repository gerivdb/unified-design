---
type: MOC
version: "1.0"
date: "2026-09-22"
status: in_review
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
| L1 | Corriger `do_not_create` JEVX | `GOVERNANCE-HUB/known_repositories.yaml` | ✅ Fait | SOT JEVX `do_not_create: true` |
| L2 | Corriger `entrypoint` JEVX | `designs/jevx.yaml` | ✅ Fait | Commit `cd6b2d1` |
| L3 | Clarifier `hardware_profile` JEVX | `designs/jevx.yaml` | ✅ Fait | Commit `cd6b2d1` |
| L4 | Aligner `depends_on` JEVX sur MDU | `designs/jevx.yaml`, `designs/jevx-engineering.yaml` | ✅ Fait | Commit `cd6b2d1` |
| L5 | Documenter `consumers` JEVX | `catalog/designs.index.yaml` | ✅ Fait | Commit `6e9de0f` |
| L6 | Documenter `consumers` pipeline JEVX | `catalog/pipelines.index.yaml` | ✅ Fait | Commit `6e9de0f` |
| L7 | Ajouter JEVX dans CLM pipeline | `designs/clm-pipeline/design.yaml` | ✅ Fait | Commit `cd6b2d1` |
| L8 | Corriger `SCOPE.yaml` consumer CLM | `JEVX/SCOPE.yaml` | ✅ Fait | JEVX repo : `gerivdb/CLM` remplacé par `gerivdb/KG-CAUSAL`/`gerivdb/ROOTX` |
| L9 | Dédupliquer `ONTOLOGY_DECLARATION.yaml` | `JEVX/ONTOLOGY_DECLARATION.yaml` | ✅ Fait | JEVX repo : concepts uniques `decision_typed`, `clm_parser`, `dlm_management`, `runner_orchestration`, `jev_variant`, `comparative_study` |
| L10 | Marquer `security_guardrails` draft | `designs/jevx.yaml` | ✅ Fait | Commit `cd6b2d1` |
| L11 | Marquer `constrained-parallel-decoding` draft | `designs/jevx-engineering.yaml` | ✅ Fait | Commit `cd6b2d1` |
| L12 | Aligner `max_queue` sur code | `designs/jevx.yaml` | ✅ Fait | Commit `cd6b2d1` |

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
| **G1** | `do_not_create: true` pour JEVX dans SOT | `known_repositories.yaml` | ✅ Fait |
| **G2** | `entrypoint`, `hardware_profile`, `max_queue` corrigés | `designs/jevx.yaml` | ✅ Fait |
| **G3** | `depends_on` résolus ou déplacés | `designs/jevx.yaml`, `designs/jevx-engineering.yaml` | ✅ Fait |
| **G4** | `security_guardrails` et `constrained-parallel-decoding` marqués `draft` | designs | ✅ Fait |
| **G5** | Consumers documentés dans catalogues | `catalog/designs.index.yaml`, `catalog/pipelines.index.yaml` | ✅ Fait |
| **G6** | CLM pipeline cohérent avec JEVX | `designs/clm-pipeline/design.yaml` | ✅ Fait |
| **G7** | `SCOPE.yaml` et `ONTOLOGY_DECLARATION.yaml` corrigés | JEVX repo | ✅ Fait |

## Critères d'acceptation

- [x] `GOVERNANCE-HUB/known_repositories.yaml` : `do_not_create: true` pour JEVX
- [x] `designs/jevx.yaml` : `entrypoint: src/index.ts`, `hardware_profile` clarifié, `max_queue` aligné
- [x] `designs/jevx.yaml` et `designs/jevx-engineering.yaml` : `depends_on` résolus
- [x] `designs/jevx.yaml` : `security_guardrails` marquées `draft`
- [x] `designs/jevx-engineering.yaml` : `constrained-parallel-decoding` marqué `draft`
- [x] `catalog/designs.index.yaml` et `catalog/pipelines.index.yaml` : consumers documentés
- [x] `designs/clm-pipeline/design.yaml` : cohérence JEVX/CLM
- [x] `JEVX/SCOPE.yaml` : aucune référence invalide
- [x] `JEVX/ONTOLOGY_DECLARATION.yaml` : aucun doublon
- [x] Tous les designs passent validation

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
| Création PRD-MOC | 2026-09-22 | `dbb659e` | `PRD/PRD-MOC-JEVX-MDU-INTEGRATION-FIX-20260922.md` |
| Création MOC | 2026-09-22 | `6f025d2` | `MOC/MOC-JEVX-MDU-INTEGRATION-FIX-20260922.md` |
| Alignement designs JEVX | 2026-09-22 | `cd6b2d1` | `designs/jevx.yaml`, `designs/jevx-engineering.yaml` |
| Update catalog consumers | 2026-09-22 | `6e9de0f` | `catalog/designs.index.yaml`, `catalog/pipelines.index.yaml` |
| CLM pipeline alignment | 2026-09-22 | `cd6b2d1` | `designs/clm-pipeline/design.yaml` |
