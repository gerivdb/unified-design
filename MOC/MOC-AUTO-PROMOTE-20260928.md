---
type: MOC
version: "1.0.0"
date: "2026-09-29"
status: draft
intent_hash: 0xMOC_AUTO_PROMOTE_20260928
parent_prd: PRD-MOC-AUTO-PROMOTE-20260928.md
pole_id: POLE-MEMORY-001
owner: L0-CANON
repo: gerivdb/unified-design
---

# MOC — Auto-Promote : promotion automatique des ADR/Designs/INTENTS

## Objectif

Mettre en œuvre le PRD `PRD-MOC-AUTO-PROMOTE-20260928.md` :
- moteur de promotion automatique des documents de gouvernance
- critères objectifs de promotion ADR/Design/INTENT
- intégration avec le moteur auto-design

## Périmètre

### P0 — Essentiel

| ID | Livrable | Chemin cible | Statut |
|---|---|---|---|
| P0-1 | Moteur auto-promote | `engine/auto_design/auto_promote.py` | 🔄 |
| P0-2 | Critères promotion ADR | `designs/auto-promote/adr-criteria.yaml` | 🔄 |
| P0-3 | Critères promotion Design | `designs/auto-promote/design-criteria.yaml` | 🔄 |
| P0-4 | Critères promotion INTENT | `designs/auto-promote/intent-criteria.yaml` | 🔄 |

### P1 — Important

| ID | Livrable | Chemin cible | Statut |
|---|---|---|---|
| P1-1 | Tests unitaires | `tests/test_auto_promote_*.py` | 🔄 |
| P1-2 | Hook pre-commit | `.kilocode/hooks/pre-commit-auto-promote.py` | 🔄 |

### P2 — Nice-to-have

| ID | Livrable | Chemin cible | Statut |
|---|---|---|---|
| P2-1 | CI step local | `scripts/run_auto_promote_check.ps1` | 🔄 |
| P2-2 | Documentation | `docs/auto-promote/README.md` | 🔄 |

## Plan d'exécution SLM

### Phase 1 — P0 (atomic, commits séparés)

1. `feat(engine): add auto_promote` — moteur de promotion
2. `docs(design): add auto-promote criteria` — critères YAML
3. `feat(hooks): add pre-commit-auto-promote` — hook

### Phase 2 — P1 (atomic, commits séparés)

4. `test(engine): add auto_promote unit tests` — pytest
5. `docs(scripts): add run_auto_promote_check.ps1` — CI locale

### Phase 3 — P2 (atomic, commits séparés)

6. `docs(auto-promote): add README` — guide

## Critères d'Acceptation

1. `python scripts/auto_design_cli.py promote --dry-run` retourne liste des documents promouvables
2. `python scripts/auto_design_cli.py promote --apply` applique les promotions avec preuve horodatée
3. Hook pre-commit bloque si promotion manquée sur document `proposed` avec critères remplis
4. Tests unitaires passent (pytest 5 passed)

## Références

- **PRD** : `PRD-MOC-AUTO-PROMOTE-20260928.md`
- **INTENT** : `INTENT-UNIFIED-DESIGN-METACOHERENCE-AUTOMATION-20260927.md`
- **Design** : `designs/auto-promote/`
