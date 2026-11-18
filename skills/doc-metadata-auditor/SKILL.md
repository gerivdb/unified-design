---
name: doc-metadata-auditor
description: >
  Vérifie que chaque fichier .md d'un dépôt de documentation (BRAIN-DOCS, DOC-UNIV-DEV, ou tout repo
  avec dossier docs/) possède les métadonnées obligatoires : intent_hash, profil, source_repo.
  Détecte les fichiers manquants et génère un rapport de conformité.
version: "1.0.0"
status: active
layer: L0-CANON
intent_hash: 0xSKILL_DOC_METADATA_AUDITOR_20261117
triggers:
  - "valider métadonnées docs"
  - "verifier intent_hash fichiers md"
  - "audit métadonnées documentation"
inputs:
  - type: repo_root
    description: "Racine du repo à auditer"
  - type: docs_path
    description: "Chemin vers le dossier docs/ (optionnel, déduit si absent)"
outputs:
  - type: validation_report
    description: "Rapport JSON avec liste des fichiers non conformes"
  - type: missing_metadata
    description: "Liste des fichiers avec métadonnées manquantes"
tools:
  - filesystem
  - yaml_parser
artifacts:
  - path: reports/doc-metadata-audit-*.json
    format: json
governance:
  adr: ADR-2026-11-17-001-STRATE-DOCS-L2-L3
  design: documentation-technique
  atom: atom-documentation-technique
  atom: atom-documentation-universitaire
---

# Skill : Doc Metadata Auditor

## Description

Vérifie que chaque fichier `.md` d'un dépôt de documentation (BRAIN-DOCS, DOC-UNIV-DEV, ou tout repo avec dossier docs/)
possède les métadonnées obligatoires : `intent_hash`, `profil`, `source_repo`.

## Quand utiliser

- Avant tout commit touchant la documentation dans BRAIN-DOCS ou DOC-UNIV-DEV
- Lors de la création d'un nouveau document technique ou universitaire
- Lors de l'audit de cohérence des métadonnées sur tous les 139 repos du SOT
- Avant d'injecter un KI dans RAGX (le hash doit exister)

## Processus

### ÉTAPE-1 — Scanner tous les fichiers .md
Parcourir récursivement le dossier `docs/` du repo et identifier tous les fichiers `.md`.

### ÉTAPE-2 — Vérifier les métadonnées obligatoires
Pour chaque fichier `.md`, vérifier la présence de :
- `intent_hash` : identifiant unique au format `0x...`
- `profil` : profil du document (DOC, CORE, INFRA, TOOL, etc.)
- `source_repo` : nom du repo source (ex: `gerivdb/BRAIN-DOCS`)

### ÉTAPE-3 — Générer le rapport
Produire un rapport JSON listant :
- Les fichiers conformes (avec toutes les métadonnées)
- Les fichiers non conformes (avec liste des métadonnées manquantes)

## Anti-patterns

- Valider un doc sans vérifier les 3 métadonnées obligatoires
- Considérer un fichier valide avec seulement 2 métadonnées sur 3
- Ignorer les fichiers sans frontmatter YAML

## Références

- **Design** : `designs/documentation-technique/design.yaml`
- **Design** : `designs/documentation-universitaire/design.yaml`
- **Primitive** : `atoms/documentation-technique/atom-documentation-technique.atom.yaml`
- **Primitive** : `atoms/documentation-universitaire/atom-documentation-universitaire.atom.yaml`
- **Repo cible** : `gerivdb/BRAIN-DOCS`, `gerivdb/DOC-UNIV-DEV`
