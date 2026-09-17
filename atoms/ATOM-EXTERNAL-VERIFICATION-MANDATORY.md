# ATOM-EXTERNAL-VERIFICATION-MANDATORY

## Description

"L'agent ne se relit pas" — Inspiré de D:\GG-knox\engineering ideas\300-kimi-k3\2.md.

Toute vérification critique doit être effectuée par une entité externe. Un agent ne peut pas valider sa propre production sans contre-vérification externe.

## Règles

1. Tout test d'intégrité doit être exécuté par un agent différent de l'agent producteur
2. Toute preuve d'exécution (PoL) doit être horodatée et signée par un agent externe
3. Toute validation Poincaré doit être effectuée par ARGUS, pas par l'agent qui a créé le DAG
4. Toute revue de code doit être effectuée par un agent différent de l'auteur
5. Le seuil de confiance minimum pour une vérification externe est de 0.6

## Références

- **Source** : `D:\GG-knox\engineering ideas\300-kimi-k3\2.md`
- **Concept** : "L'agent ne se relit pas"
