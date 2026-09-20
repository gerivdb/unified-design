---
name: ontology-term-gate-skill
description: >
  Version skill de ontology_term_gate.py.
  Vérifie que les termes d'un PRD/EPIC existent dans ONTOLOGY,
  identifie les termes manquants, et propose des définitions.
version: "1.0.0"
status: active
layer: L0
intent_hash: 0xSKILL_ONTOLOGY_TERM_GATE_20260920
triggers:
  - "valider termes ontologiques"
  - "ontology term gate"
  - "vérifier termes PRD EPIC"
inputs:
  - type: doc_path
    description: "Chemin vers le document PRD/EPIC"
  - type: ontology_path
    description: "Chemin vers ONTOLOGY.yaml"
outputs:
  - type: validation_report
    description: "Rapport de validation des termes"
  - type: missing_terms
    description: "Liste des termes manquants"
tools:
  - yaml_parser
  - filesystem
artifacts:
  - path: reports/ontology-term-gate-*.json
    format: json
governance:
  adr: ADR-2026-09-19-SAFE-ACTION-PATTERN
  design: ecosystem-meta-coherence
  atom: ecosystem-meta-coherence-gate
---

# Skill : Ontology Term Gate

## Description

Version skill de `ontology_term_gate.py`. Vérifie que les termes d'un PRD/EPIC existent dans ONTOLOGY, identifie les termes manquants, et propose des définitions.

## When to use

- Avant tout commit de PRD/EPIC
- Lors de la création d'un nouveau concept
- Lors de la revue de documents de gouvernance

## Process

### ÉTAPE-1 — Extraire les termes
Extraire les termes du document PRD/EPIC.

### ÉTAPE-2 — Vérifier dans ONTOLOGY
Vérifier que chaque terme existe dans ONTOLOGY.yaml.

### ÉTAPE-3 — Identifier les termes manquants
Lister les termes absents.

### ÉTAPE-4 — Proposer des définitions
Proposer des définitions pour les termes manquants.

## Anti-patterns

- Ignorer les termes manquants
- Créer des termes sans validation ontologique
- Considérer un document valide avec des termes manquants

## References

- **Design** : `designs/ecosystem-meta-coherence/design.yaml`
- **Script** : `scripts/ontology_term_gate.py`
- **Ontology** : `ONTOLOGY/ONTOLOGY.yaml`
