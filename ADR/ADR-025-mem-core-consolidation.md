<<<<<<< HEAD
---
=======
--- 
>>>>>>> 88da000 (feat(ge): implement DAG-3 Graph Engineering design with CTULU L4 master intent)
# ADR-025-MEM-CORE-Consolidation
## Type: ADR
## Status: proposed
## Date: 2026-07-29
## IntentHash: 0xMEM_CORE_CONSOLIDATION_20260729

## Contexte
La proposition MEM-CORE vise à consolider 7 briques mémoire existantes (SPIDX, BLO, KG-SPIDX, TIMX-FEATURE-STORE, HERMES, Mnemo, MIMIR) en un hub mémoire unifié. Cette modification concerne l'architecture logique et introduit un nouveau repo vers évoluer.

## Impact Architectural
- Nouvel element logiciel de niveau N+1 (hub mémoire)
- Modification du Triangle Causal (ajout de MEM-CORE)
- Impact sur les patterns d'archivage et de persistance

## Objectifs
- Unifier l'API mémoire des 7 briques
- Centraliser les mécanismes de traçabilité
- Intégrer la gérerie des signatures temporelles

## Consequences
- Simplification des facettes elementaires
- Réduction de la fragmentation des données
<<<<<<< HEAD
- Centralisation des mécanismes de rollback
- Potentiel Alexandre de nouvelles capabilites d'analyse
=======
- Centralisatio
des mécanismes de rollback
- Potentiel Aleksandre de nouvelles capabilites d'analyse
>>>>>>> 88da000 (feat(ge): implement DAG-3 Graph Engineering design with CTULU L4 master intent)

## Decision Context
- Responsable : Poincaré
- Comisión : Modification non toxique de l'architecture
- Priorité : P0 (fondation technique)

## Reversibility
- Supprimable en cas déclinature
- Le repo existant et les briques demeureront opérationnels

## Liens
- Connaitre les 7 briques via known_repositories.yaml
- Architecture actuelle : unified-design.yaml
- IntentHash existant : 0xMEM_CORE_CONSOLIDATION_20260729