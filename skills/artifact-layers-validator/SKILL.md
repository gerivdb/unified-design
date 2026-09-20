---
name: artifact-layers-validator
description: >
  Vérifie en une passe que src/, config/, tools/, scripts/, tests/, docs/, markdown/
  existent et sont conformes dans un repo. Complète yaml-structure-validator
  par de la structure causale repo-level.
version: "1.0.0"
status: active
layer: L0
intent_hash: 0xSKILL_ARTIFACT_LAYERS_VALIDATOR_20260920
triggers:
  - "valider structure repo"
  - "artifact layers"
  - "vérifier src config tools scripts tests docs markdown"
inputs:
  - type: repo_root
    description: "Racine du repo à valider"
outputs:
  - type: validation_report
    description: "Rapport de validation des layers"
  - type: missing_layers
    description: "Liste des layers manquants"
tools:
  - filesystem
  - yaml_parser
artifacts:
  - path: reports/artifact-layers-validation-*.json
    format: json
governance:
  adr: ADR-2026-09-19-SAFE-ACTION-PATTERN
  design: artifact-layers-design
  atom: ecosystem-meta-coherence-gate
---

# Skill : Artifact Layers Validator

## Description

Vérifie en une passe que `src/`, `config/`, `tools/`, `scripts/`, `tests/`, `docs/`, `markdown/` existent et sont conformes dans un repo. Complète `yaml-structure-validator` par de la structure causale repo-level.

## When to use

- Avant tout commit touchant la structure d'un repo
- Lors de la création d'un nouveau repo
- Lors de l'audit d'un repo existant

## Process

### ÉTAPE-1 — Vérifier src/
Vérifier que `src/` existe et contient du code source.

### ÉTAPE-2 — Vérifier config/
Vérifier que `config/` existe et contient de la configuration.

### ÉTAPE-3 — Vérifier tools/
Vérifier que `tools/` existe et contient des outils.

### ÉTAPE-4 — Vérifier scripts/
Vérifier que `scripts/` existe et contient des scripts.

### ÉTAPE-5 — Vérifier tests/
Vérifier que `tests/` existe et contient des tests.

### ÉTAPE-6 — Vérifier docs/
Vérifier que `docs/` existe et contient de la documentation.

### ÉTAPE-7 — Vérifier markdown/
Vérifier que `markdown/` existe et contient des documents Markdown.

## Anti-patterns

- Valider sans vérifier tous les layers
- Ignorer les layers manquants
- Considérer un repo valide avec seulement 5/7 layers

## References

- **Design** : `designs/artifact-layers-design/design.yaml`
- **Primitive** : `primitives/artifact-layers-primitive.yaml`
- **Workflow** : `workflows/workflow-artifact-layers-validation.md`
