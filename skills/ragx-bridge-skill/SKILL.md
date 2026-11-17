---
name: ragx-bridge-skill
description: >
  Skill de pont RAGX (ENV2 ↔ ENV3). Permet l'injection de contexte ENV2 vers RAGX
  via l'endpoint POST /context (port 8853), la synchronisation des Knowledge Items
  vers NotebookLM via POST /sync (mode hors-bande ADR-0209), et la validation
  de l'intégrité des KI injectées.
version: "1.0.0"
status: active
layer: L0-CANON
intent_hash: 0xSKILL_RAGX_BRIDGE_20261117
triggers:
  - "injecter contexte ENV2 vers RAGX"
  - "synchroniser KI vers NotebookLM"
  - "pont RAGX ENV2 ENV3"
inputs:
  - type: context_payload
    description: "Payload JSON de contexte ENV2 (timestamp, strate_source, payload)"
  - type: ki_bundle
    description: "Bundle KI avec IntentHash, TTL et provenance"
outputs:
  - type: gate_decision
    description: "ALLOW ou BLOCK avec justification"
  - type: merkle_hash
    description: "Hash SHA256 de preuve d'intégrité du contexte injecté"
tools:
  - filesystem
  - http_client
artifacts:
  - path: reports/ragx-bridge-*.json
    format: json
governance:
  adr: ADR-2026-10-09-001-RAGX-CUBE-A-SEPARATION
  design: documentation-ragx-integration
  atom: atom-documentation-technique
  atom: atom-documentation-universitaire
---

# Skill : RAGX Bridge

## Description

Skill de pont RAGX (ENV2 ↔ ENV3). Permet l'injection de contexte ENV2 vers RAGX
via l'endpoint POST /context (port 8853), la synchronisation des Knowledge Items
vers NotebookLM via POST /sync (mode hors-bande ADR-0209), et la validation
de l'intégrité des KI injectées.

## When to use

- Avant tout push modifiant une documentation technique ou universitaire
- Quand un nouveau Knowledge Item doit être injecté dans RAGX
- Lors de la synchronisation périodique des KI vers NotebookLM (ENV3)

## Process

### ÉTAPE-1 — Préparer le bundle KI
Vérifier que le bundle KI possède un IntentHash, un TTL et une provenance
(repo source BRAIN-DOCS ou DOC-UNIV-DEV, fichier d'origine).

### ÉTAPE-2 — Injecter le contexte dans RAGX
Appeler POST http://127.0.0.1:8853/context avec le payload JSON du bundle KI.

### ÉTAPE-3 — Vérifier le hash Merkle
Vérifier que le hash SHA256 retourné correspond au contenu injecté.

### ÉTAPE-4 — Synchroniser vers NotebookLM (optionnel)
Appeler POST http://127.0.0.1:8853/sync pour pousser le bundle vers NotebookLM
en mode hors-bande (ADR-0209).

## Anti-patterns

- Injecter un KI sans IntentHash
- Injecter un KI sans provenance (repo source et fichier d'origine)
- Utiliser notebooklm-py sur ENV2 (interdit par ADR-0209)

## References

- **Design** : `designs/documentation-ragx-integration/design.yaml`
- **Primitive** : `atoms/documentation-technique.atom.yaml`, `atoms/documentation-universitaire.atom.yaml`
- **Repo cible** : `gerivdb/RAGX` (L0-CANON)
