# ATOM-META-EDIT-LOOP

## Description

Méta-boucle d'édition — Inspiré de D:\GG-knox\engineering ideas\300-kimi-k3\4.md.

Boucle d'édition méta : après chaque modification, vérifier que la modification n'a pas cassé la méta-structure (designs, atoms, cross-refs, DAG).

## Règles

1. Après chaque édition, vérifier la cohérence des cross-references
2. Après chaque édition, vérifier l'intégrité du DAG (pas de cycle, pas de dépendance cassée)
3. Après chaque édition, vérifier que le frontmatter est valide
4. La méta-boucle est automatisée autant que possible (hooks, scripts)
5. Si la méta-boucle détecte une incohérence → STOP + HITL

## Références

- **Source** : `D:\GG-knox\engineering ideas\300-kimi-k3\4.md`
- **Concept** : Méta-boucle d'édition
