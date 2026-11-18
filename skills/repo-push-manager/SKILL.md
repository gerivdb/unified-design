---
name: repo-push-manager
description: >
  Skill de poussage de commits locaux vers le remote d'un repo donne.
  Verifie que le remote est correct, que la branche est celle attendue,
  et effectue le push avec verification.
version: "1.0.0"
status: active
layer: L0-CANON
intent_hash: 0xSKILL_REPO_PUSH_MANAGER_20261117
triggers:
  - "pousser commits repo"
  - "sync remote repo"
  - "verifier remote avant push"
inputs:
  - type: repo_path
    description: "Chemin vers le repo local a pousser"
  - type: remote_name
    description: "Nom du remote (defaut: origin)"
  - type: branch_name
    description: "Nom de la branche a pousser (defaut: main)"
outputs:
  - type: push_status
    description: "success ou echec"
  - type: remote_url
    description: "URL du remote verifie"
tools:
  - git
artifacts:
  - path: reports/repo-push-*.json
    format: json
governance:
  adr: ADR-2026-07-28-018-EMERGENCY-ROLLBACK-PIPELINE
  design: documentation-ragx-integration
---

# Skill : Repo Push Manager

## Description

Skill de poussage de commits locaux vers le remote d'un repo donne.
Verifie que le remote est correct, que la branche est celle attendue,
et effectue le push avec verification.

## Quand utiliser

- Apres avoir committer des modifications dans un repo local
- Avant de declarer une tache comme terminee
- Pour synchroniser l'etat local avec le remote

## Processus

### ETAPE-1 — Verifier le remote
Verifier que l'URL du remote correspond a l'attendu pour ce repo.

### ÉTAPE-2 — Verifier la branche
Verifier que la branche courante est celle attendue (main, feat/..., etc.)

### ETAPE-3 — Pousser les commits
Effectuer le git push vers le remote et la branche cible.

### ÉTAPE-4 — Verifier le push
Verifier que le push a reussi en verifiant le log distant.

## Anti-patterns

- Pousser sans verifier le remote (risque de pousser sur le mauvais repo)
- Pousser sur la mauvaise branche
- Pousser sans verifier que le remote existe

## References

- **Design** : `designs/documentation-ragx-integration/design.yaml`
