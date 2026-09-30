---
type: PRD
version: "1.0.0"
date: "2026-09-29"
status: implemented
intent_hash: 0xPRD_ECOSYSTEM_CRM_INTEGRATION_20260929
parent_intent: INTENT-ECOSYSTEM-CRM-INTEGRATION-20260929.md
pole_id: POLE-MEMORY-001
owner: L0-CANON
repo: gerivdb/unified-design
---

# PRD — Ecosystem CRM Integration

## Objectif

Intégrer la CRM tech debt à tout l’écosystème `gerivdb` pour que chaque repo puisse déclarer, scorer et résoudre sa dette technique via `unified-design`.

## Périmètre

### P0 — Essentiel

| ID | Livrable | Chemin cible | Critère d'acceptation |
|---|---|---|---|
| P0-1 | Registry | `crm/tech_debt_registry.yaml` | Agrège la dette cross-repo |
| P0-2 | API publique | `engine/auto_design/analyzer.py`, `generator.py` | Scoring + génération CRM |
| P0-3 | Docs | `INTENT`, `PRD`, `MOC`, `ADR`, `EPIC`, `TASKS` | Gouvernance complète |

### P1 — Important

| ID | Livrable | Chemin cible | Critère d'acceptation |
|---|---|---|---|
| P1-1 | Notifications | `crm/notifier.py` | Notifie les repos cibles |
| P1-2 | Workflow | `crm/workflow.py` | Orchestre détection → scoring → génération → notification |
| P1-3 | Tests | `tests/test_crm_tech_debt.py` | 10 tests passent |

## Architecture cible

```
unified-design/
├── crm/
│   ├── tech_debt_registry.yaml
│   ├── notifier.py
│   └── workflow.py
├── engine/
│   └── auto_design/
│       ├── analyzer.py (+ _score_tech_debt)
│       └── generator.py (+ generate_crm_tasks)
└── tests/
    └── test_crm_tech_debt.py
```

## Plan d'exécution SLM

### Phase 1 — P0

1. Registry + docs
2. API publique
3. Tests P0

### Phase 2 — P1

4. Notifier + workflow
5. Tests P1

## Critères d'Acceptation

1. Registry agrège la dette cross-repo
2. API publique fonctionnelle
3. Tests : 10/10 passent
4. Docs complètes

## Références

- **INTENT** : `INTENT-ECOSYSTEM-CRM-INTEGRATION-20260929.md`
- **MOC** : `MOC-ECOSYSTEM-CRM-INTEGRATION-20260929.md`
- **ADR** : `ADR-ECOSYSTEM-CRM-INTEGRATION-20260929.md`
