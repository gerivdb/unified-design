---
name: doc-univ-validator
description: >
  Vérifie la structure et la cohérence d'un repo de documentation universitaire
  (DOC-UNIV-DEV, L3-CITIZENS). Contrôle la présence des layers docs/*,
  la rigueur académique (citations), et l'absence de duplication avec BRAIN-DOCS.
version: "1.0.0"
status: active
layer: L3-CITIZENS
intent_hash: 0xSKILL_DOC_UNIV_VALIDATOR_20261117
triggers:
  - "valider structure doc universitaire"
  - "documentation universitaire DOC-UNIV-DEV"
  - "vérifier rigueur académique citations"
inputs:
  - type: repo_root
    description: "Racine du repo de documentation universitaire à valider"
outputs:
  - type: validation_report
    description: "Rapport de validation des layers docs/* universitaires"
  - type: missing_citations
    description: "Liste des concepts sans citation académique"
  - type: duplication_alerts
    description: "Liste des duplications avec BRAIN-DOCS"
tools:
  - filesystem
  - yaml_parser
artifacts:
  - path: reports/doc-univ-validation-*.json
    format: json
governance:
  adr: ADR-2026-11-17-001-STRATE-DOCS-L2-L3
  design: documentation-universitaire
  atom: atom-documentation-universitaire
---

# Skill : Doc Univ Validator

## Description

Vérifie la structure et la cohérence d'un repo de documentation universitaire
(DOC-UNIV-DEV, L3-CITIZENS). Contrôle la présence des layers `docs/*`,
la rigueur académique (citations pour chaque concept), et l'absence
de duplication avec BRAIN-DOCS (documentation technique).

## When to use

- Avant tout commit touchant la documentation universitaire dans DOC-UNIV-DEV
- Lors de la création d'un nouveau concept académique
- Lors de l'audit de cohérence avec BRAIN-DOCS (pas de duplication)
- Lors de la révision trimestrielle de la veille technologique

## Process

### ÉTAPE-1 — Vérifier docs/glossaire
Vérifier que `docs/glossaire/` existe et contient des définitions de concepts sourcées.

### ÉTAPE-2 — Vérifier docs/papers
Vérifier que `docs/papers/` existe et contient des papers fondamentaux annotés.

### ÉTAPE-3 — Vérifier docs/patterns
Vérifier que `docs/patterns/` existe et contient des patterns d'implémentation.

### ÉTAPE-4 — Vérifier docs/tendances
Vérifier que `docs/tendances/` existe et contient de la veille technologique révisée.

### ÉTAPE-5 — Vérifier docs/ressources
Vérifier que `docs/ressources/` existe et contient des sources qualifiées.

### ÉTAPE-6 — Vérifier la rigueur académique
Vérifier que chaque concept est sourcé par une citation académique valide.

### ÉTAPE-7 — Vérifier l'absence de duplication avec BRAIN-DOCS
Vérifier qu'aucun contenu de doc technique n'est dupliqué depuis BRAIN-DOCS.

## Anti-patterns

- Valider sans vérifier la rigueur académique (citations manquantes)
- Dupliquer du contenu de BRAIN-DOCS (doc technique) dans DOC-UNIV-DEV
- Considérer un repo valide avec des concepts sans citation

## References

- **Design** : `designs/documentation-universitaire/design.yaml`
- **Primitive** : `atoms/documentation-universitaire/atom-documentation-universitaire.atom.yaml`
- **Repo cible** : `gerivdb/DOC-UNIV-DEV`
