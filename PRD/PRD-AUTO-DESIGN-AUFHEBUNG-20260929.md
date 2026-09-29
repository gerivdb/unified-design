---
type: PRD
version: "1.0.0"
date: "2026-09-29"
status: draft
intent_hash: 0xPRD_AUTO_DESIGN_AUFHEBUNG_20260929
parent_intent: INTENT-AUTO-DESIGN-AUFHEBUNG-20260929.md
pole_id: POLE-MEMORY-001
owner: L0-CANON
repo: gerivdb/unified-design
---

# PRD — Auto-Design comme Aufhebung et Autonomie de l'Écosystème

## Objectif

Établir `auto-design` comme fonction native de `unified-design`, capable d'analyser, générer, industrialiser, vérifier et reporter l'auto-design readiness de tout repo `gerivdb/*`.

## Périmètre

### P0 — Essentiel

| ID | Livrable | Chemin cible | Critère d'acceptation |
|---|---|---|---|
| P0-1 | `engine/auto_design/analyzer.py` | `engine/auto_design/analyzer.py` | `analyze_repo()` retourne JSON valide avec scores 0-100 |
| P0-2 | `engine/auto_design/generator.py` | `engine/auto_design/generator.py` | `generate_repo()` dry-run produit `design.yaml` + bridges valides |
| P0-3 | `engine/auto_design/industrializer.py` | `engine/auto_design/industrializer.py` | `deploy_repo()` copie templates runtimes sans erreur |
| P0-4 | `engine/auto_design/verifier.py` | `engine/auto_design/verifier.py` | `verify_repo()` retourne `auto_design_score` + breakdown |
| P0-5 | `engine/auto_design/reporter.py` | `engine/auto_design/reporter.py` | `report_global()` couvre 100% repos `active` |
| P0-6 | `scripts/auto_design_cli.py` | `scripts/auto_design_cli.py` | CLI `analyze|generate|deploy|verify|report` fonctionnelle |
| P0-7 | `templates/auto_design/*.py` | `templates/auto_design/` | 3 templates : `cycle_runner.py`, `bridge_executor.py`, `pr_factory.py` |
| P0-8 | `designs/auto-design/design.yaml` | `designs/auto-design/design.yaml` | Définit motif canonique avec `implementation_contract` + bridges |

### P1 — Important

| ID | Livrable | Chemin cible | Critère d'acceptation |
|---|---|---|---|
| P1-1 | `skills/auto-design-readiness/SKILL.md` | `skills/auto-design-readiness/SKILL.md` | Skill documenté et testé |
| P1-2 | Tests unitaires | `tests/test_auto_design_*.py` | 5 tests minimum (analyzer, generator, industrializer, verifier, reporter) |
| P1-3 | Hook pre-commit | `.kilocode/hooks/pre-commit-auto-design-verifier.py` | Bloque commit si `design.yaml` absent sur repo `active` |

### P2 — Nice-to-have

| ID | Livrable | Chemin cible | Critère d'acceptation |
|---|---|---|---|
| P2-1 | CI step local | `scripts/run_auto_design_check.ps1` | Pipeline `analyze|verify|report` fonctionnelle |
| P2-2 | Documentation | `docs/auto-design/` | Guide d'usage + architecture + exemples |
| P2-3 | Auto-debug pathways | `designs/auto-design/auto_debug_pathways.yaml` | 3 pathways documentés : Observability, Automation, Infrastructure |

## Plan d'exécution SLM

### Phase 1 — P0 (atomic, commits séparés)

1. `feat(engine): add auto_design analyzer` — `analyzer.py`
2. `feat(engine): add auto_design generator` — `generator.py`
3. `feat(engine): add auto_design industrializer` — `industrializer.py`
4. `feat(engine): add auto_design verifier` — `verifier.py`
5. `feat(engine): add auto_design reporter` — `reporter.py`
6. `feat(scripts): add auto_design_cli` — CLI unifiée
7. `feat(templates): add auto_design runtimes` — 3 templates
8. `docs(design): add auto-design design.yaml` — motif canonique

### Phase 2 — P1 (atomic, commits séparés)

1. `docs(skill): add auto-design-readiness` — skill
2. `test(engine): add auto_design unit tests` — pytest
3. `feat(hooks): add pre-commit-auto-design-verifier` — hook

### Phase 3 — P2 (atomic, commits séparés)

1. `docs(scripts): add run_auto_design_check.ps1` — CI locale
2. `docs(auto-design): add documentation` — guide + exemples
3. `docs(design): add auto_debug_pathways.yaml` — pathways

## Critères d'Acceptation

1. `python scripts/auto_design_cli.py analyze <repo>` retourne JSON avec `auto_design_readiness` 0-100
2. `python scripts/auto_design_cli.py verify unified-design` retourne `auto_design_score >= 80`
3. `python scripts/auto_design_cli.py report --global` couvre 100% des repos `active`
4. Tous les livrables P0 sont commités et pre-commit passent
5. Skill `auto-design-readiness` documenté et invocable
6. Hook pre-commit bloque si `design.yaml` absent sur repo `active`

## Références

- **INTENT** : `INTENTS/INTENT-AUTO-DESIGN-AUFHEBUNG-20260929.md`
- **Design** : `designs/auto-design/design.yaml`
- **ADR** : `ADR/ADR-2026-09-29-auto-design-aufhebung.md`
- **Repo PoC** : `gerivdb/AUTO-DEV` (100% opérationnel)
