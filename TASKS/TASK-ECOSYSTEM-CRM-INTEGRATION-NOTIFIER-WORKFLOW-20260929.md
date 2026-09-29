---
type: TASK
version: "1.0.0"
date: "2026-09-29"
status: proposed
intent_hash: 0xTASK_ECOSYSTEM_CRM_NOTIFIER_WORKFLOW_20260929
parent_epic: EPIC-ECOSYSTEM-CRM-INTEGRATION-20260929.md
task_id: TASK-ECOSYSTEM-CRM-003
priority: P1
assignee: L0-CANON
repo: gerivdb/unified-design
---

# TASK — Ecosystem CRM Notifier + Workflow

## Objectif

Créer `crm/notifier.py` et `crm/workflow.py` pour notifications et workflow end-to-end.

## Critères d’acceptation

1. `notifier.py` notifie les repos cibles
2. `workflow.py` orchestre détection → scoring → génération → notification
3. Fallback local si ARGUS/CTULU indisponibles
4. Tests d’intégration

## Livrable

`crm/notifier.py`, `crm/workflow.py`

## Références

- **PRD** : `PRD-ECOSYSTEM-CRM-INTEGRATION-20260929.md`
- **MOC** : `MOC-ECOSYSTEM-CRM-INTEGRATION-20260929.md`
