---
type: MOC
version: "1.0.0"
date: "2026-09-29"
status: draft
intent_hash: 0xMOC_AUTO_DESIGN_AUFHEBUNG_20260929
parent_prd: PRD-AUTO-DESIGN-AUFHEBUNG-20260929.md
pole_id: POLE-MEMORY-001
owner: L0-CANON
repo: gerivdb/unified-design
---

# MOC — Auto-Design comme Aufhebung et Autonomie de l'Écosystème

## Objectif

Mettre en œuvre le PRD `PRD-AUTO-DESIGN-AUFHEBUNG-20260929.md` :
- moteur `engine/auto_design/` avec 5 primitives
- CLI `scripts/auto_design_cli.py`
- templates runtimes `templates/auto_design/`
- design canonique `designs/auto-design/design.yaml`
- skill `skills/auto-design-readiness/SKILL.md`

## Périmètre

### P0 — Essentiel

| ID | Livrable | Chemin cible | Statut |
|---|---|---|---|
| P0-1 | `analyzer.py` | `engine/auto_design/analyzer.py` | ✅ |
| P0-2 | `generator.py` | `engine/auto_design/generator.py` | ✅ |
| P0-3 | `industrializer.py` | `engine/auto_design/industrializer.py` | ✅ |
| P0-4 | `verifier.py` | `engine/auto_design/verifier.py` | ✅ |
| P0-5 | `reporter.py` | `engine/auto_design/reporter.py` | ✅ |
| P0-6 | `auto_design_cli.py` | `scripts/auto_design_cli.py` | ✅ |
| P0-7 | Templates runtimes | `templates/auto_design/*.py` | ✅ |
| P0-8 | `design.yaml` | `designs/auto-design/design.yaml` | ✅ |

### P1 — Important

| ID | Livrable | Chemin cible | Statut |
|---|---|---|---|
| P1-1 | Skill | `skills/auto-design-readiness/SKILL.md` | ✅ |
| P1-2 | Tests unitaires | `tests/test_auto_design_*.py` | 🔄 |
| P1-3 | Hook pre-commit | `.kilocode/hooks/pre-commit-auto-design-verifier.py` | 🔄 |

### P2 — Nice-to-have

| ID | Livrable | Chemin cible | Statut |
|---|---|---|---|
| P2-1 | CI step local | `scripts/run_auto_design_check.ps1` | 🔄 |
| P2-2 | Documentation | `docs/auto-design/` | 🔄 |
| P2-3 | Auto-debug pathways | `designs/auto-design/auto_debug_pathways.yaml` | 🔄 |

## Plan d'exécution SLM

### Phase 1 — P0 (atomic, commits séparés)

1. `feat(engine): add auto_design analyzer` — `analyzer.py`
2. `feat(engine): add auto_design generator` — `generator.py`
3. `feat(engine): add auto_design industrializer and verifier` — `industrializer.py` + `verifier.py`
4. `feat(engine): add auto_design reporter` — `reporter.py`
5. `feat(scripts): add auto_design_cli` — CLI unifiée
6. `feat(templates): add auto_design runtimes` — 3 templates
7. `docs(design): add auto-design design.yaml and skill` — motif canonique + skill

### Phase 2 — P1 (atomic, commits séparés)

8. `test(engine): add auto_design unit tests` — pytest
9. `feat(hooks): add pre-commit-auto-design-verifier` — hook

### Phase 3 — P2 (atomic, commits séparés)

10. `docs(scripts): add run_auto_design_check.ps1` — CI locale
11. `docs(auto-design): add documentation` — guide + exemples
12. `docs(design): add auto_debug_pathways.yaml` — pathways

## Critères d'Acceptation

1. `python scripts/auto_design_cli.py analyze <repo>` retourne JSON avec `auto_design_readiness` 0-100
2. `python scripts/auto_design_cli.py verify unified-design` retourne `auto_design_score >= 80`
3. `python scripts/auto_design_cli.py report --global` couvre 100% des repos `active`
4. Tous les livrables P0 sont commités et pre-commit passent
5. Skill `auto-design-readiness` documenté et invocable
6. Hook pre-commit bloque si `design.yaml` absent sur repo `active`

## Références

- **PRD** : `PRD-AUTO-DESIGN-AUFHEBUNG-20260929.md`
- **INTENT** : `INTENTS/INTENT-AUTO-DESIGN-AUFHEBUNG-20260929.md`
- **Design** : `designs/auto-design/design.yaml`
- **ADR** : `ADR/ADR-2026-09-29-auto-design-aufhebung.md` (à créer)
