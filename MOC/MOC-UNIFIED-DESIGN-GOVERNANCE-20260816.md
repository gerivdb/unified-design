---
type: MOC
version: "1.0"
date: "2026-08-16"
status: active
intent_hash: 0xMOC_UNIFIED_DESIGN_GOVERNANCE_20260816
---

# MOC - Unified Design Governance

> Carte de contenu pour les documents de gouvernance du repo `unified-design`.

## PRD

- `PRD/PRD-UNIFIED-DESIGN-GOVERNANCE-GAPS-2026-08-16.md` - Résolution des lacunes de gouvernance

## ADR

- `ADR/ADR-2026-08-15-001-PR-LIFECYCLE-GATE.md` - PR Lifecycle Gate
- `ADR/ADR-2026-08-15-002-BRANCH-RENAME-GOVERNANCE.md` - Branch Rename Governance
- `ADR/ADR-2026-08-15-003-WIP-BRANCH-WORKFLOW.md` - WIP Branch Workflow

## Atoms

- `atoms/design-schema.yaml` - Schéma de design.yaml
- `atoms/meta-design-triad.yaml` - Méta-design triad
- `atoms/registry-consistency-sentinel.yaml` - Sentinelle de cohérence des registres
- `atoms/friction-based-governance.yaml` - Gouvernance par friction

## Schemas

- `schemas/design.schema.json` - JSON Schema pour designs
- `schemas/meta-design.schema.json` - JSON Schema pour meta-design
- `schemas/registry.schema.json` - JSON Schema pour atoms_registry

## Frictions identifiées

| # | Friction | Design manquant |
|---|----------|-----------------|
| 1 | Hook commit bloque | Validation Conventional Commits en amont |
| 2 | Hook pre-commit bloque encoding | Design encoding normalization |
| 3 | atoms_registry invalide | Schéma JSON registry + validator |
| 4 | Templates zombie-symptom invalides | Template YAML standardisé |
| 5 | Instance zombie-symptom invalide | Validator schema pour instances |
| 6 | registry.schema.json est du markdown | JSON Schema réel pour registry |
| 7 | Conflits stash pop | Workflow migration stash entre branches |
| 8 | Unicode dans META-DESIGN.md | Convention ASCII/encoding markdown |
| 9 | Worktrees orphelins | Nettoyage automatique worktrees |
| 10 | Branche orpheline stash | WAL/NEXUS traçant origine stashes |
