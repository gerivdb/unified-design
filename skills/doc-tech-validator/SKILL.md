---
name: doc-tech-validator
description: >
  Vérifie la structure et la cohérence d'un repo de documentation technique
  (BRAIN-DOCS, L2-PLATFORM). Contrôle la présence des layers docs/*,
  les liens vers les repos source, et l'alignement des versions.
version: "1.0.0"
status: active
layer: L2-PLATFORM
intent_hash: 0xSKILL_DOC_TECH_VALIDATOR_20261117
triggers:
  - "valider structure doc technique"
  - "documentation technique BRAIN-DOCS"
  - "vérifier liens repo source docs"
inputs:
  - type: repo_root
    description: "Racine du repo de documentation technique à valider"
outputs:
  - type: validation_report
    description: "Rapport de validation des layers docs/*"
  - type: missing_layers
    description: "Liste des layers docs manquants"
  - type: broken_links
    description: "Liste des liens vers repos source brisés"
tools:
  - filesystem
  - yaml_parser
artifacts:
  - path: reports/doc-tech-validation-*.json
    format: json
governance:
  adr: ADR-2026-11-17-001-STRATE-DOCS-L2-L3
  design: documentation-technique
  atom: atom-documentation-technique
---

# Skill : Doc Tech Validator

## Description

Vérifie la structure et la cohérence d'un repo de documentation technique
(BRAIN-DOCS, L2-PLATFORM). Contrôle la présence des layers `docs/*`,
les liens vers les repos source, et l'alignement des versions entre
la documentation et le code source.

## When to use

- Avant tout commit touchant la documentation technique dans BRAIN-DOCS
- Lors de la création d'un nouveau document technique
- Lors de l'audit de cohérence doc ↔ code
- Quand une API change dans un repo source (déclenche mise à jour doc)

## Process

### ÉTAPE-1 — Vérifier docs/api
Vérifier que `docs/api/` existe et contient la référence API des repos source.

### ÉTAPE-2 — Vérifier docs/guides
Vérifier que `docs/guides/` existe et contient les guides d'intégration.

### ÉTAPE-3 — Vérifier docs/runbooks
Vérifier que `docs/runbooks/` existe et contient les runbooks opérationnels.

### ÉTAPE-4 — Vérifier docs/adr
Vérifier que `docs/adr/` existe et contient les ADR documentées.

### ÉTAPE-5 — Vérifier docs/changelog
Vérifier que `docs/changelog/` existe et contient l'historique des modifications.

### ÉTAPE-6 — Vérifier les liens vers repos source
Vérifier que chaque document cite son repo source via IntentHash ou lien canonique.

### ÉTAPE-7 — Vérifier l'alignement des versions
Vérifier que la version de la doc correspond à la version du repo source.

## Anti-patterns

- Valider sans vérifier tous les layers docs/*
- Considérer un repo valide avec des liens vers repos source brisés
- Ignorer le désalignement de versions entre doc et code

## References

- **Design** : `designs/documentation-technique/design.yaml`
- **Primitive** : `atoms/documentation-technique/atom-documentation-technique.atom.yaml`
- **Repo cible** : `gerivdb/BRAIN-DOCS`
