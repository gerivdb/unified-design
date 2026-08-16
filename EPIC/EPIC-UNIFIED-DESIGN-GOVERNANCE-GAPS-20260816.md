---
intent_hash: 0xEPIC_UNIFIED_DESIGN_GOVERNANCE_GAPS_20260816
status: active
priority: P1
owner: gerivdb
repo: gerivdb/unified-design
---

# EPIC - Unified Design Governance Gaps Resolution

## Contexte

Le repo `unified-design` a accumulé des lacunes de design et de gouvernance qui ont causé :
- 4 PRs correctives successives (#52 -> #55)
- Frictions répétées : validation YAML, encoding, schémas, stash, worktrees
- Perte de temps et risque de perte de travail

## Objectif

Combler les designs/docs manquants pour éliminer les frictions récurrentes.

## Scope

### Inclus
- PRD : `PRD/PRD-UNIFIED-DESIGN-GOVERNANCE-GAPS-2026-08-16.md`
- MOC : `MOC/MOC-UNIFIED-DESIGN-GOVERNANCE-20260816.md`
- ADRs : `ADR-2026-08-15-001`, `002`, `003` (déjà présents)
- Schemas : `schemas/design.schema.json`, `schemas/meta-design.schema.json`, `schemas/registry.schema.json`
- Atoms : `atoms_registry.yaml`, `atoms/design-schema.yaml`, `atoms/meta-design-triad.yaml`
- Designs : normalisation `designs/**/*.yaml`

### Exclu
- Modifications métier des designs existants
- Refonte architecturale du méta-design

## Critères d'acceptation

- [ ] PRD et MOC créés et validés
- [ ] 0 erreur YAML sur `designs/**/*.yaml`
- [ ] `atoms_registry.yaml` valide
- [ ] 3 schemas JSON valides
- [ ] ADRs de gouvernance git présents
- [ ] Worktrees orphelins nettoyés
- [ ] Stash tracé ou supprimé

## Documentation

- `PRD/PRD-UNIFIED-DESIGN-GOVERNANCE-GAPS-2026-08-16.md`
- `MOC/MOC-UNIFIED-DESIGN-GOVERNANCE-20260816.md`
- `ADR/ADR-2026-08-15-001-PR-LIFECYCLE-GATE.md`
- `ADR/ADR-2026-08-15-002-BRANCH-RENAME-GOVERNANCE.md`
- `ADR/ADR-2026-08-15-003-WIP-BRANCH-WORKFLOW.md`
