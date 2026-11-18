---
name: ki-injector
description: >
  Skill d'injection de Knowledge Items (KI) dans RAGX via l'endpoint
  POST /context (port 8853). Envoie un bundle KI avec son IntentHash,
  son timestamp et sa provenance, et vérifie le hash Merkle de retour.
version: "1.0.0"
status: active
layer: L0-CANON
intent_hash: 0xSKILL_KI_INJECTOR_20261117
triggers:
  - "injecter KI dans RAGX"
  - "envoyer contexte ENV2 vers RAGX"
  - "synchroniser knowledge item vers ENV3"
inputs:
  - type: ki_bundle_path
    description: "Chemin vers le fichier .json du bundle KI"
  - type: ragx_url
    description: "URL du endpoint RAGX (defaut: http://127.0.0.1:8853/context)"
outputs:
  - type: merkle_hash
    description: "Hash SHA256 de preuve d'intégrite retournee par RAGX"
  - type: injection_status
    description: "success ou echec"
tools:
  - http_client
  - filesystem
artifacts:
  - path: reports/ki-inject-*.json
    format: json
governance:
  adr: ADR-2026-10-09-001-RAGX-CUBE-A-SEPARATION
  design: documentation-ragx-integration
  atom: atom-documentation-technique
  atom: atom-documentation-universitaire
---

# Skill : KI Injector

## Description

Skill d'injection de Knowledge Items (KI) dans RAGX via l'endpoint
POST /context (port 8853). Envoie un bundle KI avec son IntentHash,
son timestamp et sa provenance, et vérifie le hash Merkle de retour.

## Quand utiliser

- Apres creation d'un nouveau bundle KI dans un repo de documentation
- Avant de synchroniser les connaissances vers NotebookLM (ENV3)
- Lors de la synchronisation periodique des KI vers ENV3

## Processus

### ETAPE-1 — Lire le bundle KI
Lire le fichier JSON du bundle KI (contient intent_hash, provenance, content_summary, etc.)

### ÉTAPE-2 — Construire le payload RAGX
Construire le payload avec les champs : shard_source, payload (le contenu du bundle)

### ÉTAPE-3 — Appeler POST /context
Envoyer le payload vers http://127.0.0.1:8853/context

### ÉTAPE-4 — Verifier le merkle_hash
Verifier que la réponse contient un merkle_hash valide et que le statut est "success"

## Anti-patterns

- Injecter un KI sans intent_hash
- Injecter sans provenance (repo source et fichier d'origine)
- Oublier de verifier le hash de retour

## References

- **Design** : `designs/documentation-ragx-integration/design.yaml`
- **Primitive** : `atoms/documentation-technique/atom-documentation-technique.atom.yaml`
- **Primitive** : `atoms/documentation-universitaire/atom-documentation-universitaire.atom.yaml`
- **Repo cible** : `gerivdb/RAGX` (L0-CANON)
