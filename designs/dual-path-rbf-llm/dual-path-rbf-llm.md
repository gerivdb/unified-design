# Dual-Path RBF/LLM Engine

> Runner fast-path RBF/LLM — 95% trafic < 3 ms, 5% fallback LLM.

## Vue d'ensemble

**Dual-Path RBF/LLM** est un moteur d'inférence hybride qui aiguille les requêtes vers un **Fast-Path RBF déterministe** (95% du trafic, < 3 ms) ou un **Slow-Path LLM** (5% du trafic, ambiguïté élevée).

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    REQUEST (prompt)                          │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              FAST-PATH RBF ENGINE                            │
│  • Centres μ_k (K-means, k prototypes de concepts)          │
│  • Sigmas σ_k adaptatifs                                     │
│  • Poids W_k résolus analytiquement (LMS / pseudo-inverse)   │
│  • Distance: ||x - μ_k||² / (2σ_k²)                         │
│  • Seuil de confiance: τ = 0.85                              │
│  • SIMD SSE4.2/AVX pour [512]f32                            │
│  • Latence: < 3 ms (16 threads, no GPU)                     │
└─────────────────────────────┬───────────────────────────────┘
                              │
                  distance < τ │ distance ≥ τ
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
┌──────────────────────┐         ┌──────────────────────┐
│  RESPONSE RBF        │         │  SLOW-PATH LLM       │
│  (déterministe)      │         │  (autoregressif)     │
│  • HTML/CSS/DB       │         │  • Génération créative│
│  • Score + Confidence│         │  • Ambiguïté élevée   │
│  • Fallback autorisé │         │  • Coût: ~50 ms       │
└──────────────────────┘         └──────────────────────┘
```

## Composants

| Composant | Technologie | Paramètres |
|:---|:---|:---|
| Feature Vector | [512]f32 | SIMD SSE4.2/AVX |
| RBF Kernel | Gaussian | k centres, σ adaptatifs |
| Distance Metric | Euclidienne normalisée | ||x - μ_k||² / (2σ_k²) |
| Threshold | τ = 0.85 | Ajustable par calibration |
| Fast-Path Output | HTML/CSS/DB | Déterministe |
| Slow-Path Output | LLM génératif | Autoregressif |

## Budgets

| Resource | Budget |
|----------|--------|
| Latence Fast-Path | < 3 ms |
| Mémoire (pas de heap) | < 64 ko |
| Threads | 16 (SSE4.2/AVX) |
| Contexte | [512]f32 |
| Seuil de confiance | τ = 0.85 |

## Dépendances

| Dépendance | Type | Rôle |
|:---|:---|:---|
| rbf-cluster | ONTOLOGY concept | Moteur RBF |
| activation-vector | ONTOLOGY concept | Sonde dynamique |
| runner-contract | ONTOLOGY concept | Contrat ACP |

## Tests

- [ ] Bench P50/P99 < 3 ms (Dual Xeon E5620)
- [ ] Calibration threshold τ sur dataset représentatif
- [ ] Fallback LLM déclenché si distance ≥ τ
- [ ] 0 heap allocation en fast-path

## Références

- ADR-2026-08-29-001-neuro-symbolic-rbf-operationalization
- RBF neurone KG.md (LARQL / vindex)
- ADR-2026-08-28-001-META-COHERENCE-ENGINE (RADX intégré)
