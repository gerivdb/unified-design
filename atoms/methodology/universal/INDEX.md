---
type: RPT
id: METHODOLOGY-UNIVERSAL-INDEX
version: 1.0.0
date: 2026-07-16
title: "Bibliothèque méthodologique universelle — Index des atomes N+3"
intent_hash: 0xMETHODOLOGY_UNIVERSAL_INDEX_20260716
---

# Bibliothèque Méthodologique Universelle

## Vue d'ensemble

Cette bibliothèque regroupe les **atomes N+3** — principes méthodologiques universels extraits d'analyses de bugs et de défis techniques. Ces atomes capturent les lois fondamentales qui s'appliquent à tous les langages compilés et leurs interfaces FFI.

## Structure

```
[Rapport Zig] ──extraction──> [Lois universelles]
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
            ffi-abi-boundary  definition-order  namespace-collision
                    │               │               │
                    └───────────────┼───────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
            cache-invalidation  interface-contract  error-diagnostic-tree
                                    │
                            [Atomes N+3]
                                    │
                            [EPIC-312: générateur wrappers]
```

## Atomes disponibles

| ID | Titre | Description |
|---|---|---|
| ATOM-001 | FFI ABI Boundary | Loi fondamentale des interfaces entre langages compilés |
| ATOM-002 | Definition Order Constraint | Contrainte d'ordre de déclaration dans les compilateurs stricts |
| ATOM-003 | Namespace Collision Prevention | Stratégie de préfixage pour éviter les collisions de noms |
| ATOM-004 | Cache Invalidation Hygiene | Purge systématique du cache après changements structurels |
| ATOM-005 | Interface Contract | Formalisation explicite des exports C pour FFI |
| ATOM-006 | Error Diagnostic Tree | Transformation des bugs en arbre de décision pour diagnostic |

## Prochaines étapes

1. **EPIC-312** : Développer le générateur automatique de wrappers FFI qui applique ces lois
2. **Validation** : Tester les atomes sur d'autres projets FFI (Rust, C, Python)
3. **Intégration** : Ajouter les atomes dans les hooks de pré-commit pour les validations automatiques

## Références

- Rapport Zig 2026-06-21 (analyse des bugs Zig 0.15)
- ADR-PRIM-001-MASSIVE-DECOMPOSITION
- ADR-2026-06-28-001-LOGICAL-ARCHITECTURE-N1-N4

## Référence ADR
- **ADR** : ADR-2026-07-16-007-METHODOLOGY-UNIVERSAL-INDEX
- **IntentHash** : 0xADR_METHODOLOGY_UNIVERSAL_20260716
- **Dépôt** : gerivdb/LLM-REPO
- **Statut ADR** : proposed
- **Màj requise si** : statut ADR → deprecated ou superseded