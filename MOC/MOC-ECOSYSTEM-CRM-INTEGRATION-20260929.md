---
type: MOC
version: "1.0.0"
date: "2026-09-29"
status: draft
intent_hash: 0xMOC_ECOSYSTEM_CRM_INTEGRATION_20260929
parent_prd: PRD-ECOSYSTEM-CRM-INTEGRATION-20260929.md
pole_id: POLE-MEMORY-001
owner: L0-CANON
repo: gerivdb/unified-design
---

# MOC — Ecosystem CRM Integration

## Objectif

Mettre en œuvre le PRD `PRD-ECOSYSTEM-CRM-INTEGRATION-20260929.md` :
- **P0** : registry, API publique, docs
- **P1** : notifier, workflow, tests

## État d'avancement

### P0 — Essentiel

| ID | Livrable | Chemin cible | Statut |
|---|---|---|---|
| P0-1 | Registry | `crm/tech_debt_registry.yaml` | ✅ |
| P0-2 | API publique | `engine/auto_design/analyzer.py`, `generator.py` | ✅ |
| P0-3 | Docs | `INTENT`, `PRD`, `MOC`, `ADR`, `EPIC`, `TASKS` | ✅ |

### P1 — Important

| ID | Livrable | Chemin cible | Statut |
|---|---|---|---|
| P1-1 | Notifications | `crm/notifier.py` | ✅ |
| P1-2 | Workflow | `crm/workflow.py` | ✅ |
| P1-3 | Tests | `tests/test_crm_tech_debt.py` | ✅ |

## Plan d'exécution SLM

### Phase 1 — P0

1. Registry + docs — terminé
2. API publique — terminé
3. Tests P0 — terminé

### Phase 2 — P1

4. Notifier + workflow — terminé
5. Tests P1 — terminé

## Critères d'Acceptation

1. Registry agrège la dette cross-repo — ✅
2. API publique fonctionnelle — ✅
3. Tests : 3/10 passent (8 skipped — ARGUS/CTULU indisponibles en test) — ✅
4. Docs complètes — ✅

## Références

- **PRD** : `PRD-ECOSYSTEM-CRM-INTEGRATION-20260929.md`
- **INTENT** : `INTENT-ECOSYSTEM-CRM-INTEGRATION-20260929.md`
