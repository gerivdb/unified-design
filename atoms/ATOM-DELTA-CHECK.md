# ATOM-DELTA-CHECK

## Description

Delta Check — Inspiré de D:\GG-knox\engineering ideas\300-kimi-k3\3.md.

Vérification du delta entre l'état attendu et l'état réel. Mesure l'écart entre ce qui est documenté (SOT, ADR, PRD) et ce qui est implémenté (code, tests, config).

## Règles

1. Le delta est calculé à chaque étape de validation
2. Delta = 0 → validation PASS
3. Delta > seuil → validation WARN ou FAIL selon criticité
4. Le delta est documenté dans la preuve d'exécution (PoL)
5. Le delta est tracé dans le temps pour détecter la dérive

## Références

- **Source** : `D:\GG-knox\engineering ideas\300-kimi-k3\3.md`
- **Concept** : Delta Check
