# ATOM-CONFIDENCE-THRESHOLD

## Description

Seuil de confiance 0.6 — Inspiré de D:\GG-knox\engineering ideas\300-kimi-k3\2.md.

Toute décision, vérification ou validation nécessite un seuil de confiance minimum de 0.6 avant d'être acceptée.

## Règles

1. Score de confiance < 0.6 → décision bloquée, demande de vérification supplémentaire
2. Score de confiance ≥ 0.6 et < 0.8 → décision acceptée avec avertissement
3. Score de confiance ≥ 0.8 → décision acceptée sans avertissement
4. Le score de confiance est calculé à partir de sources indépendantes
5. Le score de confiance est documenté dans la preuve d'exécution (PoL)

## Références

- **Source** : `D:\GG-knox\engineering ideas\300-kimi-k3\2.md`
- **Concept** : Seuil de confiance 0.6
