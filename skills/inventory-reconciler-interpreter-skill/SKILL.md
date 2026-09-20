---
name: inventory-reconciler-interpreter-skill
description: >
  Version skill unifiée de inventory-reconciler-interpreter.
  Filtre les faux positifs de l'inventory reconciler (do_not_create=true,
  archived, etc.) et ne garde que les BLOCKING.
version: "1.0.0"
status: active
layer: L0
intent_hash: 0xSKILL_INVENTORY_RECONCILER_INTERPRETER_20260920
triggers:
  - "interpréter inventory reconciler"
  - "filtre faux positifs inventory"
  - "inventory blocking"
inputs:
  - type: inventory_report
    description: "Rapport d'inventory reconciler"
  - type: sot_path
    description: "Chemin vers known_repositories.yaml"
outputs:
  - type: filtered_report
    description: "Rapport filtré (BLOCKING uniquement)"
  - type: action_plan
    description: "Plan d'action pour les BLOCKING"
tools:
  - yaml_parser
  - json_parser
artifacts:
  - path: reports/inventory-reconciler-*.json
    format: json
governance:
  adr: ADR-2026-09-19-SAFE-ACTION-PATTERN
  design: ecosystem-meta-coherence
  atom: ecosystem-meta-coherence-gate
---

# Skill : Inventory Reconciler Interpreter

## Description

Version skill unifiée de `inventory-reconciler-interpreter`. Filtre les faux positifs de l'inventory reconciler (`do_not_create=true`, `archived`, etc.) et ne garde que les BLOCKING.

## When to use

- Quand l'inventory reconciler bloque le push
- Lors de l'analyse de rapports d'inventory
- Avant de corriger les champs SOT manquants

## Process

### ÉTAPE-1 — Charger le rapport
Charger le rapport d'inventory reconciler.

### ÉTAPE-2 — Filtrer les faux positifs
Exclure les entrées `do_not_create=true`, `archived`, `dormant`.

### ÉTAPE-3 — Garder les BLOCKING
Conserver uniquement les entrées qui bloquent réellement le push.

### ÉTAPE-4 — Générer le plan d'action
Générer un plan d'action pour les BLOCKING.

## Anti-patterns

- Traiter tous les BLOCKING comme critiques
- Ignorer les faux positifs
- Corriger sans vérifier le contexte SOT

## References

- **Design** : `designs/ecosystem-meta-coherence/design.yaml`
- **Script** : `scripts/inventory_reconciler_interpreter.py`
- **Workflow** : `workflows/pre-push-validation.md`
