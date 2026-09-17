# ATOM-STOP-CONDITION

## Description

Loop Engineering — Condition d'arrêt — Inspiré de D:\GG-knox\engineering ideas\300-kimi-k3\1.md.

Toute boucle d'ingénierie (itération, pipeline, révision) doit avoir une condition d'arrêt explicite. Sans condition d'arrêt, la boucle risque de diverger ou de s'arrêter prématurément.

## Règles

1. Toute boucle d'itération doit avoir une condition d'arrêt explicite
2. La condition d'arrêt peut être : convergence, budget épuisé, timeout, validation humaine
3. Si la condition d'arrêt est atteinte sans convergence → escalader vers HITL
4. Si la boucle dépasse le budget sans convergence → STOP automatique
5. La condition d'arrêt est documentée dans le design/atom correspondant

## Références

- **Source** : `D:\GG-knox\engineering ideas\300-kimi-k3\1.md`
- **Concept** : Loop Engineering, condition d'arrêt
