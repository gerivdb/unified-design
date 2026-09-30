---
type: EPIC
version: "1.0.0"
date: "2026-09-29"
status: proposed
intent_hash: 0xEPIC_ECOSYSTEM_CRM_INTEGRATION_20260929
parent_prd: PRD-ECOSYSTEM-CRM-INTEGRATION-20260929.md
pole_id: POLE-MEMORY-001
owner: L0-CANON
repo: gerivdb/unified-design
---

# EPIC — Ecosystem CRM Integration

## Objectif

Livrer un système CRM de gestion de la dette technique intégré à `unified-design`, exploitable par tout l’écosystème `gerivdb`.

## Scope

### P0 — Essentiel

| ID | Livrable | Fichier | Priorité |
|---|---|---|---|
| E1 | Registry | `crm/tech_debt_registry.yaml` | P0 |
| E2 | API publique | `engine/auto_design/analyzer.py`, `generator.py` | P0 |
| E3 | Docs | `INTENT`, `PRD`, `MOC`, `ADR`, `EPIC`, `TASKS` | P0 |

### P1 — Important

| ID | Livrable | Fichier | Priorité |
|---|---|---|---|
| E4 | Notifications | `crm/notifier.py` | P1 |
| E5 | Workflow | `crm/workflow.py` | P1 |
| E6 | Tests | `tests/test_crm_tech_debt.py` | P1 |

## Critères d’Acceptation

1. Registry agrège la dette cross-repo
2. API publique fonctionnelle
3. Tests : 10/10 passent
4. Docs complètes

## Références

- **PRD** : `PRD-ECOSYSTEM-CRM-INTEGRATION-20260929.md`
- **INTENT** : `INTENT-ECOSYSTEM-CRM-INTEGRATION-20260929.md`
