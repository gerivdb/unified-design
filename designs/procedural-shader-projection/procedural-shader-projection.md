# Procedural Shader Projection

> État compact → rendu DOM/HTML/DB via shaders procéduraux.

## Vue d'ensemble

**Procedural Shader Projection** dissocie l'état compact (728 spins + shaders + centres RBF, ~2 ko) de la vue générée (HTML/CSS/DB). L'état est projectif : la vue complète est générée à la demande par des shaders procéduraux, sans stockage intermédiaire.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    COMPACT STATE                              │
│  • 728 spins ternaires {-1, 0, +1}                          │
│  • Centres RBF μ_k                                           │
│  • Shaders procéduraux (générateurs de motifs)               │
│  • Taille: ~2 ko                                             │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              PROCEDURAL PROJECTION                           │
│  • Shader 1: HTML structure (arbre DOM)                     │
│  • Shader 2: CSS styling (couleurs, layout)                 │
│  • Shader 3: DB query generation (SQL/NoSQL)                │
│  • Output: vue complète (HTML + CSS + DB)                   │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    RENDERED VIEW                             │
│  • HTML/CSS prêt pour navigateur                             │
│  • DB query prête pour exécution                             │
│  • Aucun stockage de vue intermédiaire                       │
└─────────────────────────────────────────────────────────────┘
```

## Composants

| Composant | Technologie | Paramètres |
|:---|:---|:---|
| Compact State | 728 spins + RBF | < 4 ko |
| Shader 1 | HTML structure | Arbre DOM procédural |
| Shader 2 | CSS styling | Couleurs, layout |
| Shader 3 | DB query | SQL/NoSQL génératif |
| Projection | Synchrone | < 1 ms |

## Budgets

| Resource | Budget |
|----------|--------|
| Taille état compact | < 4 ko |
| Nombre de shaders | ≤ 4 |
| Temps de projection | < 1 ms |
| Mémoire tampon | < 8 ko |

## Dépendances

| Dépendance | Type | Rôle |
|:---|:---|:---|
| quasicrystal-lattice | ONTOLOGY concept | Spins + pavage |
| rbf-cluster | ONTOLOGY concept | Centres RBF |

## Tests

- [ ] Projection < 1 ms pour 728 spins
- [ ] HTML/CSS valide W3C
- [ ] DB query exécutable sans erreur
- [ ] État compact < 4 ko

## Références

- ADR-2026-08-29-001-neuro-symbolic-rbf-operationalization
- Revue PRD Bellard.md (Kolmogorov ≤ 64 ko, génération procédurale)
