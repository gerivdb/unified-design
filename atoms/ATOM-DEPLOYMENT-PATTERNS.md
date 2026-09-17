# ATOM-DEPLOYMENT-PATTERNS

## Description

Patterns de déploiement — Inspiré de D:\GG-knox\engineering ideas\300-kimi-k3\9.md.

Standards de déploiement pour l'écosystème gerivdb : blue-green, canary, rolling, immuable. Chaque pattern a des critères d'application et des rollbacks.

## Règles

1. Le déploiement en production suit un pattern documenté (blue-green, canary, rolling, immuable)
2. Chaque pattern a un rollback automatique en cas d'échec
3. Le déploiement est tracé dans la preuve d'exécution (PoL)
4. Le déploiement en production nécessite une validation HITL (sauf P4)
5. Le pattern de déploiement est choisi selon la criticité du livrable

## Références

- **Source** : `D:\GG-knox\engineering ideas\300-kimi-k3\9.md`
- **Concept** : Patterns de déploiement
