---
type: PRD
version: "1.0.0"
date: "2026-09-29"
status: implemented
intent_hash: 0xPRD_CRM_TECH_DEBT_20260929
parent_intent: INTENT-CRM-TECH-DEBT-20260929.md
pole_id: POLE-MEMORY-001
owner: L0-CANON
repo: gerivdb/unified-design
---

# PRD — CRM Tech Debt Management

## Objectif

Transformer `TASKS/` en système CRM de gestion de la dette technique, intégré à `auto-design` et exploitable par tout l'écosystème.

## Périmètre

### P0 — Essentiel

| ID | Livrable | Chemin cible | Critère d'acceptation |
|---|---|---|---|
| P0-1 | Registry dette | `crm/tech_debt_registry.yaml` | Agrège la dette cross-repo |
| P0-2 | Scoring dette | `engine/auto_design/analyzer.py` | `_score_tech_debt()` retourne score 0-100 |
| P0-3 | Génération CRM | `engine/auto_design/generator.py` | `generate_crm_tasks()` crée des tickets CRM |

### P1 — Important

| ID | Livrable | Chemin cible | Critère d'acceptation |
|---|---|---|---|
| P1-1 | Notification | `crm/notifier.py` | Envoie notifications CRM |
| P1-2 | Workflow | `crm/workflow.py` | Orchestre détection → scoring → génération → notification |
| P1-3 | Tests | `tests/test_crm_tech_debt.py` | 10 tests couvrant P0/P1 |

## État d'avancement réel (dry-run causal 2026-09-30)

### P0 — Essentiel (IMPLÉMENTÉ)

| ID | Livrable | Chemin cible | Critère d'acceptation | Statut |
|---|---|---|---|---|
| P0-1 | Registry dette | `crm/tech_debt_registry.yaml` | Agrège la dette cross-repo | ✅ Implémenté |
| P0-2 | Scoring dette | `engine/auto_design/analyzer.py` | `_score_conventional_commit_adherence()` retourne score 0-100 | ✅ Implémenté |
| P0-3 | Génération CRM | `engine/auto_design/generator.py` | `generate_commit_message()` crée des messages conventionnels | ✅ Implémenté |

### P1 — Important (IMPLÉMENTÉ)

| ID | Livrable | Chemin cible | Critère d'acceptation | Statut |
|---|---|---|---|---|
| P1-1 | Notification | `crm/notifier.py` | Envoie notifications CRM | ✅ Implémenté |
| P1-2 | Workflow | `crm/workflow.py` | Orchestre détection → scoring → génération → notification | ✅ Implémenté |
| P1-3 | Tests | `tests/test_crm_tech_debt.py` | 10 tests couvrant P0/P1 | ✅ Implémenté |

## Architecture cible

```
unified-design/
├── crm/
│   ├── tech_debt_registry.yaml    # Registry centralisé
│   ├── notifier.py                # Notifications CRM
│   └── workflow.py                # Workflow dette
└── engine/
    └── auto_design/
        ├── analyzer.py            # + _score_tech_debt()
        └── generator.py           # + generate_crm_tasks()
```

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
2. `_score_tech_debt()` retourne score 0-100 cohérent avec l'écosystème
3. `generate_crm_tasks()` crée des tickets CRM exploitables
4. `notifier.py` envoie des notifications
5. `workflow.py` orchestre le cycle complet
6. Tests : 10/10 passent

## Références

- **INTENT** : `INTENT-CRM-TECH-DEBT-20260929.md`
- **MOC** : `MOC-CRM-TECH-DEBT-20260929.md`
- **ADR** : `ADR-CRM-TECH-DEBT-20260929.md`
- **EPIC** : `EPICS/EPIC-CRM-TECH-DEBT-20260929.md`
