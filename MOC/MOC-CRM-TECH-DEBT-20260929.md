---
type: MOC
version: "1.0.0"
date: "2026-09-29"
status: draft
intent_hash: 0xMOC_CRM_TECH_DEBT_20260929
parent_prd: PRD-CRM-TECH-DEBT-20260929.md
pole_id: POLE-MEMORY-001
owner: L0-CANON
repo: gerivdb/unified-design
---

# MOC — CRM Tech Debt Management

## Objectif

Mettre en œuvre le PRD `PRD-CRM-TECH-DEBT-20260929.md` :
- **P0** : registry, scoring, génération CRM
- **P1** : notification, workflow, tests

## État d'avancement

### P0 — Essentiel

| ID | Livrable | Chemin cible | Statut |
|---|---|---|---|
| P0-1 | Registry dette | `crm/tech_debt_registry.yaml` | ⬜ |
| P0-2 | Scoring dette | `engine/auto_design/analyzer.py` | ⬜ |
| P0-3 | Génération CRM | `engine/auto_design/generator.py` | ⬜ |

### P1 — Important

| ID | Livrable | Chemin cible | Statut |
|---|---|---|---|
| P1-1 | Notification | `crm/notifier.py` | ⬜ |
| P1-2 | Workflow | `crm/workflow.py` | ⬜ |
| P1-3 | Tests | `tests/test_crm_tech_debt.py` | ⬜ |

## Plan d'exécution SLM

### Phase 1 — P0 (3 livrables, ~3h)

1. `feat(crm): add tech_debt_registry.yaml` — Registry centralisé
2. `feat(analyzer): add tech debt scoring` — `_score_tech_debt()`
3. `feat(generator): add CRM task generation` — `generate_crm_tasks()`

### Phase 2 — P1 (3 livrables, ~3h)

4. `feat(crm): add notifier.py` — Notifications CRM
5. `feat(crm): add workflow.py` — Workflow end-to-end
6. `test(crm): add test_crm_tech_debt.py` — 10 tests

## Critères d'Acceptation

1. `tech_debt_registry.yaml` agrège la dette cross-repo
2. `_score_tech_debt()` retourne score 0-100
3. `generate_crm_tasks()` crée des tickets CRM
4. `notifier.py` envoie des notifications
5. `workflow.py` orchestre le cycle complet
6. Tests : 10/10 passent

## Références

- **PRD** : `PRD-CRM-TECH-DEBT-20260929.md`
- **INTENT** : `INTENT-CRM-TECH-DEBT-20260929.md`
- **ADR** : `ADR-CRM-TECH-DEBT-20260929.md`
- **EPIC** : `EPICS/EPIC-CRM-TECH-DEBT-20260929.md`
