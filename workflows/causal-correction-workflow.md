---
name: causal-correction-workflow
description: "Workflow de correction causale des frictions ERR. Documente la méthode : diagnostiquer, proposer la correction structurelle, implémenter, valider, mettre à jour le PRD/MOC."
version: "1.0.0"
status: active
---

# Workflow — Causal Correction

## Déclencheur

- Détection d'une erreur ERR dans un script/pattern/workflow
- Détection d'un flag `MUSEUM_EFFECT_*` par `dry_run_causal.py`
- Détection d'un gap ontologique par `analyze_ontological_gaps.py`

## Étapes

1. **Diagnostic** : lire le script/pattern, identifier la cause racine.
2. **Correction structurelle** : proposer une modification causale (pas de palliatif).
3. **Implémentation atomique** : commit séparé par correction.
4. **Validation** : `python -m py_compile`, `dry_run_causal.py`, `validate_designs.py --strict`.
5. **Mise à jour PRD/MOC** : cocher la correction dans la section correspondante.
6. **Commit** : message conventionnel, max 3 fichiers.

## Critères d'acceptation

- Aucune erreur ERR connue non corrigée
- `dry_run_causal.py` retourne `PROD READY 100%`
- PRD/MOC mis à jour avec la correction
