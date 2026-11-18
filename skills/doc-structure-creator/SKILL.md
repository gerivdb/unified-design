---
name: doc-structure-creator
description: >
  Crée la structure complète de documentation dans un repo cible :
  docs/api, docs/guides, docs/runbooks, docs/adr, docs/changelog,
  docs/ki-bundles, docs/ki-context avec leurs fichiers README.md respectifs.
version: "1.0.0"
status: active
layer: L0-CANON
intent_hash: 0xSKILL_DOC_STRUCTURE_CREATOR_20261117
triggers:
  - "creer structure docs"
  - "initialiser documentation repo"
  - "ajouter dossiers docs complets"
inputs:
  - type: repo_root
    description: "Racine du repo cible où créer la structure docs/"
  - type: repo_name
    description: "Nom du repo (ex: gerivdb/MON-REPO)"
outputs:
  - type: created_directories
    description: "Liste des dossiers créés"
  - type: created_files
    description: "Liste des fichiers README.md créés"
tools:
  - filesystem
artifacts:
  - path: reports/doc-structure-creation-*.json
    format: json
governance:
  adr: ADR-2026-11-17-001-STRATE-DOCS-L2-L3
  design: documentation-technique
  design: documentation-universitaire
  atom: atom-documentation-technique
  atom: atom-documentation-universitaire
---

# Skill : Doc Structure Creator

## Description

Crée la structure complète de documentation dans un repo cible :
`docs/api`, `docs/guides`, `docs/runbooks`, `docs/adr`, `docs/changelog`,
`docs/ki-bundles`, `docs/ki-context` avec leurs fichiers `README.md` respectifs.

## Quand utiliser

- Lors de la création d'un nouveau repo de documentation
- Quand un repo actif n'a pas encore de dossier `docs/`
- Lors de la migration d'un repo legacy vers la structure canonique

## Processus

### ÉTAPE-1 — Créer les 7 dossiers
Créer `docs/api`, `docs/guides`, `docs/runbooks`, `docs/adr`,
`docs/changelog`, `docs/ki-bundles`, `docs/ki-context`.

### ÉTAPE-2 — Créer les fichiers README.md
Chaque sous-dossier reçoit un `README.md` avec son description et son rôle.

## Anti-patterns

- Créer un dossier docs/ sans les 7 sous-dossiers
- Oublier le fichier README.md dans un sous-dossier
- Créer les dossiers dans le mauvais ordre

## Références

- **Design** : `designs/documentation-technique/design.yaml`
- **Design** : `designs/documentation-universitaire/design.yaml`
- **Primitive** : `atoms/documentation-technique/atom-documentation-technique.atom.yaml`
- **Primitive** : `atoms/documentation-universitaire/atom-documentation-universitaire.atom.yaml`
