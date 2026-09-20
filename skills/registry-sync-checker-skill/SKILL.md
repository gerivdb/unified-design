---
name: registry-sync-checker-skill
description: >
  Version skill de registry-sync-checker.py.
  Vérifie la cohérence du registre tripartite (known_repositories.yaml,
  registry/repos.json, physical state) et détecte les drifts.
version: "1.0.0"
status: active
layer: L0
intent_hash: 0xSKILL_REGISTRY_SYNC_CHECKER_20260920
triggers:
  - "vérifier cohérence registre"
  - "registry sync"
  - "détecter drift registre"
inputs:
  - type: registry_path
    description: "Chemin vers known_repositories.yaml"
  - type: repos_json_path
    description: "Chemin vers registry/repos.json"
outputs:
  - type: sync_report
    description: "Rapport de synchronisation"
  - type: drift_list
    description: "Liste des drifts détectés"
tools:
  - yaml_parser
  - json_parser
  - filesystem
artifacts:
  - path: reports/registry-sync-*.json
    format: json
governance:
  adr: ADR-2026-09-19-SAFE-ACTION-PATTERN
  design: ecosystem-meta-coherence
  atom: ecosystem-meta-coherence-gate
---

# Skill : Registry Sync Checker

## Description

Version skill de `registry-sync-checker.py`. Vérifie la cohérence du registre tripartite (`known_repositories.yaml`, `registry/repos.json`, physical state) et détecte les drifts.

## When to use

- Avant tout push touchant `known_repositories.yaml`
- Lors de l'ajout d'un nouveau repo
- Lors de la détection de drift cross-repo

## Process

### ÉTAPE-1 — Charger known_repositories.yaml
Parser le fichier YAML de la Source of Truth.

### ÉTAPE-2 — Charger registry/repos.json
Parser le fichier JSON du registre.

### ÉTAPE-3 — Vérifier la cohérence
Comparer les deux sources et détecter les drifts.

### ÉTAPE-4 — Signaler les anomalies
Générer un rapport des anomalies détectées.

## Anti-patterns

- Ignorer les drifts mineurs
- Modifier le registre sans vérifier la cohérence
- Considérer le registre comme cohérent sans vérification

## References

- **Design** : `designs/ecosystem-meta-coherence/design.yaml`
- **Script** : `scripts/registry-sync-checker.py`
- **Workflow** : `workflows/pre-push-validation.md`
