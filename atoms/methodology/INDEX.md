# Index des Atomes N+3 — Bibliothèque Mémotechnique

## Vue d'ensemble

Cette bibliothèque contient **17 atomes** organisés par catégorie.

## Récapitulatif par catégorie

| Catégorie | Dossier | Atomes | Statut principal |
|-----------|---------|--------|------------------|
| Universal | `universal/` | 8 | 11 proposed |
| C | `c/` | 3 | 1 approved |
| Python | `python/` | 3 | 3 approved |
| Rust | `rust/` | 3 | 3 approved |

## Atomes par catégorie

### Universal (Loi fondamentale)

- **METHODOLOGY-INDEX** — Méthodologie N+3 — Bibliothèque d'atomes par langage
  - Fichier: `methodology\INDEX.md`
  - Références: ATOM-001-c-memory-management, ATOM-003-c-makefile-pitfalls, ATOM-001-python-ctypes-ffi, ATOM-001-rust-borrow-checker, ATOM-003-python-gil-limitations, ATOM-002-python-asyncio-pitfalls, ATOM-002-c-segfault-debugging, ATOM-003-rust-cargo-build-pitfalls, ATOM-002-rust-unsafe-ffi
  - Statut: approved

- **ATOM-001-ffi-abi-boundary** — FFI ABI Boundary — Loi fondamentale des interfaces entre langages compilés
  - Fichier: `methodology\universal\ATOM-001-ffi-abi-boundary.md`
  - Références: ATOM-001-ffi-abi-boundary
  - Statut: proposed

- **ATOM-002-definition-order-constraint** — Definition Order Constraint — Contrainte d'ordre de déclaration dans les compilateurs stricts
  - Fichier: `methodology\universal\ATOM-002-definition-order-constraint.md`
  - Références: ATOM-002-definition-order-constraint
  - Statut: proposed

- **ATOM-003-namespace-collision-prevention** — Namespace Collision Prevention — Stratégie de préfixage pour éviter les collisions de noms
  - Fichier: `methodology\universal\ATOM-003-namespace-collision-prevention.md`
  - Références: ATOM-003-namespace-collision-prevention
  - Statut: proposed

- **ATOM-004-cache-invalidation-hygiene** — Cache Invalidation Hygiene — Purge systématique du cache après changements structurels
  - Fichier: `methodology\universal\ATOM-004-cache-invalidation-hygiene.md`
  - Références: ATOM-004-cache-invalidation-hygiene
  - Statut: proposed

- **ATOM-005-interface-contract** — Interface Contract — Formalisation explicite des exports C pour FFI
  - Fichier: `methodology\universal\ATOM-005-interface-contract.md`
  - Références: ATOM-005-interface-contract
  - Statut: proposed

- **ATOM-006-error-diagnostic-tree** — Error Diagnostic Tree — Transformation des bugs en arbre de décision pour diagnostic
  - Fichier: `methodology\universal\ATOM-006-error-diagnostic-tree.md`
  - Références: ATOM-006-error-diagnostic-tree
  - Statut: proposed

- **METHODOLOGY-UNIVERSAL-INDEX** — Bibliothèque méthodologique universelle — Index des atomes N+3
  - Fichier: `methodology\universal\INDEX.md`
  - Références: Aucune
  - Statut: draft

### C

- **ATOM-001-c-memory-management** — C Memory Management — malloc/free, dangling pointers, valgrind
  - Fichier: `methodology\c\ATOM-001-c-memory-management.md`
  - Références: ATOM-001-c-memory-management, ATOM-004-cache-invalidation-hygiene
  - Statut: approved

- **ATOM-002-c-segfault-debugging** — C Segfault Debugging — gdb, address sanitizer, backtrace analysis
  - Fichier: `methodology\c\ATOM-002-c-segfault-debugging.md`
  - Références: ATOM-002-c-segfault-debugging, ATOM-004-cache-invalidation-hygiene
  - Statut: approved

- **ATOM-003-c-makefile-pitfalls** — C Makefile Pitfalls — Implicit dependencies, PHONY, environment variables
  - Fichier: `methodology\c\ATOM-003-c-makefile-pitfalls.md`
  - Références: ATOM-003-c-makefile-pitfalls, ATOM-004-cache-invalidation-hygiene
  - Statut: approved

### Python

- **ATOM-001-python-ctypes-ffi** — Python ctypes FFI — Contrat explicite des types pour les interfaces C
  - Fichier: `methodology\python\ATOM-001-python-ctypes-ffi.md`
  - Références: ATOM-005-interface-contract, ATOM-001-ffi-abi-boundary, ATOM-001-python-ctypes-ffi
  - Statut: approved

- **ATOM-002-python-asyncio-pitfalls** — Python asyncio Pitfalls — Pièges de l'event loop et concurrence
  - Fichier: `methodology\python\ATOM-002-python-asyncio-pitfalls.md`
  - Références: ATOM-004-cache-invalidation-hygiene, ATOM-002-python-asyncio-pitfalls
  - Statut: approved

- **ATOM-003-python-gil-limitations** — Python GIL Limitations — Compréhension des limites du Global Interpreter Lock
  - Fichier: `methodology\python\ATOM-003-python-gil-limitations.md`
  - Références: ATOM-004-cache-invalidation-hygiene, ATOM-003-python-gil-limitations
  - Statut: approved

### Rust

- **ATOM-001-rust-borrow-checker** — Rust Borrow Checker — Stratégies pour surmonter les restrictions d'emprunt
  - Fichier: `methodology\rust\ATOM-001-rust-borrow-checker.md`
  - Références: ATOM-001-rust-borrow-checker, ATOM-002-definition-order-constraint
  - Statut: approved

- **ATOM-002-rust-unsafe-ffi** — Rust unsafe FFI — Bonnes pratiques pour les interfaces non sûres
  - Fichier: `methodology\rust\ATOM-002-rust-unsafe-ffi.md`
  - Références: ATOM-005-interface-contract, ATOM-001-ffi-abi-boundary, ATOM-002-rust-unsafe-ffi
  - Statut: approved

- **ATOM-003-rust-cargo-build-pitfalls** — Rust Cargo Build Pitfalls — Cache, features et linking
  - Fichier: `methodology\rust\ATOM-003-rust-cargo-build-pitfalls.md`
  - Références: ATOM-003-rust-cargo-build-pitfalls, ATOM-004-cache-invalidation-hygiene
  - Statut: approved

## Graphe de dépendances

```
[Atomes N+3] → [Index Global]
       │
       ├───> [C atoms]
       ├───> [Python atoms]
       ├───> [Rust atoms]
```
