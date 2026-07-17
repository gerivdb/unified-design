---
type: GUI
version: 1.0.0
status: active
intent_hash: 0xATOM_038_TQL_INTERFACE_CONTRACT
---

# ATOM-038 : TQL Interface Contract

## Définition

TQL (Ternary Query Language) est l'**interface de requête pour l'ONTOLOGY**. Il permet aux agents et aux développeurs de rechercher des concepts dans l'ontologie sémantique.

## Caractéristiques

- **Paradigme** : Think-Do-Check
- **Récursion** : fractale (max_depth: 10)
- **Court-circuit** : NEUTRE
- **Opérateurs** : 12 opérateurs cognitifs

## Structure

```
TQL/
├── README.md              # Ce fichier
├── CHANGELOG.md           # Journal des modifications
├── grammar/               # Grammaire formelle (EBNF + PEG)
│   ├── tql.ebnf           # Grammaire EBNF canonique
│   └── tql.peg            # Parser PEG
├── spec/                  # Spécifications versionnées
│   └── TQL_SPEC_v0.1.md   # Spec v0.1
├── tests/
│   └── fixtures/          # Fixtures de test
└── hypotheses/            # Hypothèses testables
```

## Les 12 Opérateurs Cognitifs

| Opérateur | Type | Sémantique |
|-----------|------|------------|
| `diagnostic()` | Think | collect + analyze |
| `vision()` | Think | analyze + plan |
| `recherche()` | Think | act + plan |
| `acquis()` | Do | collect + validate |
| `besoin()` | Do | validate + act |
| `strategie()` | Do | collect + act |
| `ecart()` | Check | analyze + validate |
| `revision()` | Check | validate + plan |
| `alignement()` | Check | collect + plan |
| `ajustement()` | Coord | analyze + act |
| `deploiement()` | Coord | analyze + act + plan |
| `controle()` | Coord | validate + act + plan |

## Exemples de requêtes

### Requête simple

```tql
SELECT concept WHERE name = 'ATOM-035'
```

### Requête récursive

```tql
SELECT concepts FROM hierarchy WHERE depth <= 3
```

### Vérification de cohérence

```tql
CHECK IF 'ATOM-025' IMPLEMENTS 'default-fail'
```

## Intra-écosystème

| Composant | Rôle | Dépôt |
|-----------|------|-------|
| **TQL** (ce repo) | Grammaire + Spec + Fixtures | `gerivdb/TQL` |
| **BRAIN** | Interpréteur TQL → IR exécutable | `gerivdb/BRAIN` |
| **NEXUS** | Données + runtime requêtes | `gerivdb/NEXUS` |
| **UAE** | Scoring d'attention pour CHECK | `gerivdb/UAE` |
| **KEEL** | Compilation TQL → IR versionné | `gerivdb/KEEL` |

## Bridge Architecture

```
[TQL] ──grammar──▶ [BRAIN] ──execute──▶ [NEXUS]
                          │
                     ◀──score── [UAE]
```

## Règles associées

1. **TQL-BRAIN-GRAMMAR** : TQL produit la spec, BRAIN consomme pour parser
2. **BRAIN-NEXUS-TQL** : BRAIN exécute les requêtes TQL sur les données NEXUS
3. **UAE-NEXUS-S3** : UAE fournit les scores pour la phase CHECK

## Validation

### Conformité normative

- [OK] **ADR-0012** : Méthode scientifique interne
- [OK] **ADR-0013** : Triptyque ternaire normatif
- [OK] **ADR-0014** : Principe topologique du calcul

## Références

- [TQL](https://github.com/gerivdb/TQL) — Grammaire et spécification
- [TQL README](D:\DO\WEB\TOOLS\L4-TOOLS\TQL\README.md) — Documentation
- [ATOM-035](ATOM-035-ONTOLOGY_ANCHORING.md) — Ancrage requis

## Référence ADR

- **ADR** : ADR-2026-07-17-004-TQL-INTERFACE-CONTRACT
- **IntentHash** : 0xATOM_038_TQL_INTERFACE_CONTRACT_20260717
- **Dépôt** : gerivdb/GOVERNANCE-HUB
- **Statut ADR** : proposed
- **Màj requise si** : statut ADR → deprecated ou superseded