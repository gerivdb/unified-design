# ATOM-SAFE-ACTION-GATE

## Description

PATRON-0 atomisé — Inspiré de l'extraction universelle du patron de traversée de rue.

Toute action irréversible en environnement incertain exige 7 fonctions + 3 états + 1 invariant.

## États obligatoires

| État | Nature | Gate |
|---|---|---|
| PROJECT | virtuel, réversible | F5 VALIDER → PROGRESS |
| PROGRESS | engagé, irréversible | F7 VALIDER_RÉEL → BILAN |
| BILAN | constaté, mémorisé | ENREGISTRER → PROJECT suivant |

## Fonctions obligatoires

1. **PERCEVOIR** — multi-source, ordonné, redondant
2. **ÉVALUER** — multi-axes, indépendants
3. **SE_MODÉLISER** — capacité propre + incertitude propre
4. **RÉSERVER** — marge de sûreté / plan de repli
5. **VALIDER** — gate : les 4 précédents sont-ils suffisants ?
6. **AGIR + MONITORER** — engagement, irréversible + invariants surveillés
7. **VALIDER_RÉEL + ENREGISTRER** — succès constaté dans le monde → mémoire

## Règles

1. Aucune action ne passe de PROJECT à PROGRESS sans F5 VALIDER passé
2. Aucune action ne passe de PROGRESS à BILAN sans F7 VALIDER_RÉEL passé
3. Le succès n'est jamais déclaré avant F7 (Proof-of-Life obligatoire)
4. L'agent doit explicitement modéliser sa propre incertitude (F3)
5. Toute action doit avoir un plan de repli (F4)
6. La perception doit utiliser ≥ 2 sources indépendantes (F1)
7. L'évaluation doit documenter le score de confiance (F2)

## Anti-patterns

| Gène manquant | Pathologie |
|---|---|
| Pluralité | Hallucination, code hors contexte |
| Auto-modèle | Surconfiance, pas de « je ne sais pas » |
| Réserve | Casse en prod |
| Validation réelle | « Ça marche chez moi » → échec réel |

## Invariant central

Le succès n'est jamais déclaré avant la fin réelle de l'action. Toute prédiction de succès est une hypothèse, pas un résultat.

## Références

- **Design** : `designs/safe-action-pattern.yaml`
- **ADR** : ADR-2026-09-19-SAFE-ACTION-PATTERN
- **IntentHash** : 0xDESIGN_SAFE_ACTION_PATTERN_20260919
- **Dépôt** : gerivdb/unified-design
