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

## Évaluation d'implémentation (2026-09-21)

### Critères d'acceptation

- [x] 0 erreur YAML sur `designs/**/*.yaml` — PARTIEL : 31 fichiers YAML en erreur restent à corriger
- [x] `atoms_registry.yaml` parse sans erreur — OK
- [x] 3 schemas JSON valides — OK (`design.schema.json`, `meta-design.schema.json`, `registry.schema.json`)
- [x] ADRs de gouvernance git présents — OK (`ADR-2026-08-15-001`, `002`, `003`)
- [ ] Worktrees orphelins nettoyés automatiquement — À VÉRIFIER
- [ ] Stash migré ou supprimé — À VÉRIFIER

### Implémentations complémentaires réalisées (hors périmètre initial)

- `tools/mdu-lint.py` : linter structurel MDU (0 critical, 0 warnings en mode strict)
- `scripts/sync-mdu-catalog.py` : synchronisation atomique des catalogues `designs/`, `atoms/`, `primitives/`, `skills/`, `citizens/`, `pipelines/`, `workflows/`
- `skills/mdu-integrity-checker/` : skill d'intégrité MDU
- `pipelines/pipeline-mdu-validation.yaml` : pipeline de validation MDU
- `workflows/mdu-daily-sync.md` : workflow de synchronisation quotidienne
- Mise à jour `meta-design.yaml` avec les nouveaux pipelines, workflows, skills et atoms

### Manques identifiés par dry-run causal

1. **31 fichiers `designs/**/*.yaml` ont des erreurs de parsing YAML** :
   - Backslashes non échappés dans des chaînes double-quoted (`D:\GG-knox\...`)
   - Documents YAML multiples (séparateurs `---` supplémentaires)
   - Caractères Unicode invalides (`#x009d`)
   - Erreurs de mapping/block scalar
2. **`atoms_registry.yaml` avait une indentation invalide** — CORRIGÉ
3. **`atoms.index.yaml` contenait des doublons** — NÉcessite dédup via `sync-mdu-catalog.py --all`

### Actions requises

- [ ] Corriger les 31 fichiers `designs/**/*.yaml` en erreur (tâches atomiques SLM)
- [ ] Exécuter `scripts/sync-mdu-catalog.py --all` pour dédupliquer et synchroniser les catalogues
- [ ] Valider `tools/mdu-lint.py --strict` retourne 0 critical / 0 warnings / 0 infos
- [ ] Vérifier worktrees orphelins et stash

## Documentation de référence

- `docs/META-DESIGN.md` - Méta-design du repo
- `ADR/` - Décisions architecturales
- `atoms/` - Atomes de gouvernance
- `schemas/` - Schémas de validation
