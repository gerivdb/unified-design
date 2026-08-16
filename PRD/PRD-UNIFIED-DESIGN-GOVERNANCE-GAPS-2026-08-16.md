---
type: PRD
version: "1.0"
date: "2026-08-16"
status: approved
intent_hash: 0xPRD_UNIFIED_DESIGN_GOVERNANCE_GAPS_20260816
---

# PRD - Unified Design Governance Gaps Resolution

## Contexte

Le repo `unified-design` présente des lacunes de design et de gouvernance qui ont conduit à :
- 3 PRs successives (#52, #53, #54) pour stabiliser les schémas et la validation
- PR #55 pour la gouvernance git (PR Lifecycle, Branch Rename, WIP workflow)
- Données YAML invalides dans `designs/` et `atoms_registry.yaml`
- Stash orphelin sur branche fantôme
- Worktrees Agent Manager non nettoyés

Ces frictions rallongent les sessions et risquent la perte de travail.

## Objectif

Éliminer les frictions récurrentes en comblant les designs/docs manquants identifiés dans la session précédente.

## Périmètre

### 1. Schémas et validation
- `schemas/design.schema.json` : valider les `designs/*.yaml`
- `schemas/meta-design.schema.json` : valider `meta-design.yaml`
- `schemas/registry.schema.json` : valider `atoms_registry.yaml`
- Hook CI/validation multi-doc YAML

### 2. Données YAML
- Normaliser `atoms_registry.yaml` (doublons, hash, encoding)
- Corriger `designs/buzz-persistent-state.yaml` (encoding)
- Convertir templates `zombie-symptom` en YAML valide
- Corriger instance `process-zombie-proliferation`

### 3. Gouvernance git
- ADR PR Lifecycle Gate
- ADR Branch Rename Governance
- ADR WIP Branch Workflow
- Procédure de stash migration entre branches

### 4. Workflow Agent Manager
- Nettoyage automatique des worktrees orphelins
- Validation pré-merge des schemas

## Critères d'acceptation

- [ ] 0 erreur YAML sur `designs/**/*.yaml`
- [ ] `atoms_registry.yaml` parse sans erreur
- [ ] 3 schemas JSON valides
- [ ] ADRs de gouvernance git présents
- [ ] Worktrees orphelins nettoyés automatiquement
- [ ] Stash migré ou supprimé

## Documentation de référence

- `docs/META-DESIGN.md` - Méta-design du repo
- `ADR/` - Décisions architecturales
- `atoms/` - Atomes de gouvernance
- `schemas/` - Schémas de validation
