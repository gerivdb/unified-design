---
name: doc-sync-gate-skill
description: >
  Gate de cohérence documentation ↔ implémentation. Avant tout push modifiant
  une interface publique, vérifie que la documentation correspondante dans
  BRAIN-DOCS ou DOC-UNIV-DEV est à jour. Empêche le drift entre le code et sa doc.
version: "1.0.0"
status: active
layer: L0-CANON
intent_hash: 0xSKILL_DOC_SYNC_GATE_20261117
triggers:
  - "vérifier synchronisation doc avant push"
  - "doc-sync-gate pre-push"
  - "vérifier doc à jour sur changement API"
inputs:
  - type: changed_files
    description: "Liste des fichiers modifiés dans le push"
  - type: repo_root
    description: "Racine du repo source modifié"
outputs:
  - type: gate_decision
    description: "ALLOW ou BLOCK avec justification"
  - type: missing_doc
    description: "Liste des docs manquantes à mettre à jour"
tools:
  - filesystem
  - yaml_parser
artifacts:
  - path: reports/doc-sync-gate-*.json
    format: json
governance:
  adr: ADR-2026-11-17-001-STRATE-DOCS-L2-L3
  design: documentation-sync-gate
  atom: atom-documentation-technique
  atom: atom-documentation-universitaire
---

# Skill : Doc Sync Gate Skill

## Description

Gate de cohérence documentation ↔ implémentation. Avant tout push modifiant
une interface publique, vérifie que la documentation correspondante dans
BRAIN-DOCS (technique) ou DOC-UNIV-DEV (universitaire) est à jour.
Empêche le drift entre le code et sa documentation.

## When to use

- En pre-push sur tout repo source modifiant une API publique
- Avant tout merge touchant des interfaces publiques
- Lors d'un audit de cohérence doc ↔ code

## Process

### ÉTAPE-1 — Détecter les changements d'interface publique
Identifier les fichiers modifiés qui exposent une API publique (signature,
endpoint, route, contrat).

### ÉTAPE-2 — Identifier le doc cible
Déterminer si la doc cible est dans BRAIN-DOCS (technique) ou DOC-UNIV-DEV (universitaire).

### ÉTAPE-3 — Vérifier la mise à jour de la doc
Vérifier que le document correspondant a été mis à jour pour refléter le changement.

### ÉTAPE-4 — Vérifier l'IntentHash
Vérifier que chaque document possède un IntentHash valide et référençable.

### ÉTAPE-5 — Décision ALLOW ou BLOCK
- ALLOW : la doc est à jour, push autorisé
- BLOCK : la doc n'est pas à jour, push bloqué avec justification

## Anti-patterns

- Pousser un changement d'API sans mettre à jour la doc correspondante
- Considérer la doc comme optionnelle lors d'un changement d'interface
- Ignorer l'alignement des versions entre code et doc

## References

- **Design** : `designs/documentation-sync-gate/design.yaml`
- **Primitive** : `atoms/documentation-technique.atom.yaml`, `atoms/documentation-universitaire.atom.yaml`
- **Repo cibles** : `gerivdb/BRAIN-DOCS`, `gerivdb/DOC-UNIV-DEV`
