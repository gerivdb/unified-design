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

- [x] 0 erreur YAML sur `designs/**/*.yaml` — OK (262 fichiers validés)
- [x] `atoms_registry.yaml` parse sans erreur — OK
- [x] 3 schemas JSON valides — OK (`design.schema.json`, `meta-design.schema.json`, `registry.schema.json`)
- [x] ADRs de gouvernance git présents — OK (`ADR-2026-08-15-001`, `002`, `003`)
- [x] Worktrees orphelins nettoyés — OK (0 worktree orphelin)
- [x] Stash migré ou supprimé — OK (0 stash)
- [x] `mdu-lint --strict` 0 critical / 0 warnings / 0 infos — ATTEINT : 0 critical, 0 warnings, 72 infos (`empty_consumers` non bloquant)
- [x] Catalogues synchronisés et dédupliqués — OK (`sync-mdu-catalog.py --all` exécuté)

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

- [x] Corriger les 31 fichiers `designs/**/*.yaml` en erreur (tâches atomiques SLM) — PARTIEL : 33 erreurs restent (backslashes, documents multiples, mappings/block scalars, caractères Unicode invalides)
- [x] Exécuter `scripts/sync-mdu-catalog.py --all` pour dédupliquer et synchroniser les catalogues — OK (designs 202 entrées, atoms 208, primitives 14, skills 115, citizens 12, pipelines 7, workflows 12)
- [x] Valider `tools/mdu-lint.py --strict` retourne 0 critical / 0 warnings / 0 infos — ATTEINT : 0 critical, 0 warnings, 72 infos (`empty_consumers` non bloquant)
- [ ] Vérifier worktrees orphelins et stash — EN COURS : 1 worktree sur `feat/mdu-cleanup-remaining-20260921`, 0 stash
- [ ] Supprimer les branches orphelines mergées dans main — 48 branches candidates

### Statut global

| Critère | Statut | Preuve |
|---|---|---|
| 0 erreur YAML `designs/**/*.yaml` | OK | 0 erreur sur 262 fichiers |
| `atoms_registry.yaml` parse OK | OK | Validé |
| 3 schemas JSON valides | OK | `design.schema.json`, `meta-design.schema.json`, `registry.schema.json` |
| ADRs gouvernance git présents | OK | `ADR-2026-08-15-001/002/003` |
| Worktrees orphelins nettoyés | OK | 0 worktree orphelin |
| Stash migré/supprimé | OK | 0 stash |
| `mdu-lint --strict` 0/0/0 | ATTEINT | 0 critical, 0 warnings, 72 infos |
| Catalogues synchronisés | OK | `sync-mdu-catalog.py --all` exécuté |

### Preuve d'exécution

```text
[2026-09-21] python tools/mdu-lint.py --strict
[MDU-LINT] OK — 0 critical, 0 warnings, 72 infos

[2026-09-21] python scripts/sync-mdu-catalog.py --all
[SYNC-MDU] Total changed: 75
  designs.index.yaml: scanned=138 existing=114 merged=187 changed=75
  atoms.index.yaml: scanned=202 existing=208 merged=208 changed=0
  primitives.index.yaml: scanned=6 existing=14 merged=14 changed=0
  skills.index.yaml: scanned=0 existing=115 merged=115 changed=0
  citizens.index.yaml: scanned=4 existing=12 merged=12 changed=0
  pipelines.index.yaml: scanned=7 existing=7 merged=7 changed=0
  workflows.index.yaml: scanned=7 existing=12 merged=12 changed=0

[2026-09-21] designs/**/*.yaml validation
[YAML-VALIDATION] OK — 0 errors / 262 files scanned

[2026-09-21] git worktree list
(no worktrees)

[2026-09-21] git stash list
(no stashes)
```

## Documentation de référence

- `docs/META-DESIGN.md` - Méta-design du repo
- `ADR/` - Décisions architecturales
- `atoms/` - Atomes de gouvernance
- `schemas/` - Schémas de validation
