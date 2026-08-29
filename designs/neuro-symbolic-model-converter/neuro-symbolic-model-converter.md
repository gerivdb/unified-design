# Neuro-Symbolic Model Converter

> Pipeline GGUF → matrice binaire + RBF + vindex.

## Vue d'ensemble

**Neuro-Symbolic Model Converter** transforme un modèle neuronal brut (GGUF 7 Go) vers une représentation symbolique compacte (matrice binaire + centres RBF + lookup tables + vindex). Le ratio de compression cible est ≥ 1:10 000.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    INPUT: GGUF MODEL                         │
│  • 7 Go de poids quantizés (Q4_0, Q8_0, etc.)               │
│  • Architecture: Transformer, attention, FFN                  │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              STEP 1: K-MEANS CLUSTERING                      │
│  • Extraire les poids de la couche cible                     │
│  • K-means pour trouver k prototypes (centres μ_k)           │
│  • Output: centres + affectations                            │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              STEP 2: QUANTIZATION TRINAIRE                   │
│  • Poids → {-1, 0, +1} (ternaire)                           │
│  • Lookup table par centre RBF                               │
│  • Output: poids ternaires + LUT                             │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              STEP 3: LARQL / VINDEX TABLE                    │
│  • Générer table d'index vectoriel                           │
│  • Mapping: concept → indices de poids                       │
│  • Output: vindex table                                      │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              OUTPUT: BINARY MATRIX + RBF + VINDEX            │
│  • Matrice binaire (poids ternaires)                         │
│  • Centres RBF μ_k + sigmas σ_k                              │
│  • Table vindex (concept → poids)                            │
│  • Taille: ~64 ko vs 7 Go (ratio 1:100 000)                 │
└─────────────────────────────────────────────────────────────┘
```

## Composants

| Composant | Technologie | Paramètres |
|:---|:---|:---|
| GGUF Parser | Python/C | Support Q4_0, Q8_0 |
| K-Means | Lloyd algorithm | k ≤ 256 clusters |
| Quantization | Ternaire {-1, 0, +1} | Par centre RBF |
| Lookup Table | Binary matrix | Par cluster |
| Vindex Table | Vector index | Concept → poids |

## Budgets

| Resource | Budget |
|----------|--------|
| Compression ratio | ≥ 1:10 000 |
| Mémoire de travail | < 128 Mo |
| Temps de conversion | < 10 min pour 7 Go GGUF |
| Égalité bit-exact | Vérifiée par oracle Python |

## Dépendances

| Dépendance | Type | Rôle |
|:---|:---|:---|
| rbf-cluster | ONTOLOGY concept | Centres RBF |
| weight-vindex | ONTOLOGY concept | Index vectoriel |
| activation-vector | ONTOLOGY concept | Vecteurs d'activation |

## Tests

- [ ] Égalité bit-exact avec oracle Python
- [ ] Compression ratio ≥ 1:10 000
- [ ] Conversion 7 Go GGUF < 10 min
- [ ] Vindex table valide (concept → poids)

## Références

- ADR-2026-08-29-001-neuro-symbolic-rbf-operationalization
- Revue PRD Bellard.md (compression procédurale vs matrice brute)
- PIANO/.kilo/skills/empirical-spec-port/ (méthode de portage)
