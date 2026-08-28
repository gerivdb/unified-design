# RADX Design

> Runner L3 fast-path WAZAA — RBF 300 neurones, < 3 ms P99 sur Dual Xeon E5620.

## Vue d'ensemble

**RADX** (Radial Activation Distributed eXtreme) est le runner fast-path du bus social WAZAA. Il implémente un moteur RBF (Radial Basis Function) parallélisé avec 300 neurones, optimisé pour la latence ultra-faible (< 3 ms P99) sur matériel legacy (2× Xeon E5620, 24 Go DDR3 ECC).

## Architecture

### Pipeline principal

```
Input (512-d vector) 
    → N-Gram Feature Hashing (SHA-256 → 512-d)
    → RBF Layer (300 neurones, cosine similarity, threshold 0.48)
    → Ridge Regression (weights appris via LVQ supervisé)
    → Output (activation score)
```

### Composants clés

| Composant | Technologie | Paramètres |
|:---|:---|:---|
| Feature Hashing | N-Gram + SHA-256 | 512 dimensions |
| RBF Kernel | Cosine Similarity | 300 neurones, threshold 0.48 |
| Entraînement | LVQ Supervisé | Prototypes par classe |
| Poids sortie | Ridge Regression | α=1.0 régularisation |

## Capacités MDU

### latency-bound
- **max_latency_ms**: 3
- **p99_latency_ms**: 2.9 (mesuré sur bench ReleaseFast)

### fast-path-rbf
- **neurons**: 300
- **dimensions**: 512
- **kernel**: cosine-similarity
- **threshold**: 0.48

### wazaa-acp
- **protocol**: ACP (Agent Communication Protocol)
- **fallback**: llux
- **timeout_ms**: 5

## Dépendances

| Dépendance | Type | Rôle |
|:---|:---|:---|
| wazaa-social-bus | Design parent | Bus de communication agents |
| llux | Fallback | Modèle LLM léger local |
| plix | Codec | Sérialisation binaire |
| larql-243 | Query | Moteur requêtes ternaires |
| ontology-l0 | Ontologie | Ancrage sémantique |

## Intégration WAZAA ACP

RADX s'intègre au bus WAZAA via le protocole ACP :
- **Message types** : `radx.query`, `radx.train`, `radx.health`
- **Serialization** : PLIX codec
- **Transport** : TCP localhost:8787 (configurable)
- **Fallback** : Si timeout > 5ms → délégation à LLUX

## Benchmarks (ReleaseFast, Dual Xeon E5620)

| Métrique | Valeur | Cible |
|:---|:---|:---|
| P50 latency | 0.775 ms | < 1 ms |
| P99 latency | 2.900 ms | < 3 ms |
| Throughput | ~3,400 req/s | > 1,000 req/s |
| Memory | ~45 MB | < 100 MB |

## Tests

- 7/7 tests Zig (unit + integration)
- 7/7 tests Python (bindings + ACP)
- Pipeline CI : `zig build test && pytest tests/`

## Références

- ADR-0001 : N-Gram Feature Hashing vs SHA-256
- ADR-0002 : LVQ Supervised Training
- ADR-0003 : Ridge Regression Weights
- ADR-0004 : Cosine Similarity Kernel
- ADR-0005 : WAZAA ACP Integration
- PRD Master : `PRD-RADX-L3-MVP-2026-08-28.md`
- EPIC : `EPIC-RADX-L3-MVP-2026-08-28.md'
