---
type: TASK
version: "1.0.0"
date: "2026-09-29"
status: proposed
intent_hash: 0xTASK_CRM_TECH_DEBT_WORKFLOW_20260929
parent_epic: EPIC-CRM-TECH-DEBT-20260929.md
task_id: TASK-CRM-005
priority: P1
assignee: L0-CANON
repo: gerivdb/unified-design
---

# TASK — CRM Tech Debt Workflow

## Objectif

Créer `crm/workflow.py` pour orchestrer le cycle complet : détection → scoring → génération → notification.

## Critères d’acceptation

1. `workflow.py` orchestre les étapes P0/P1
2. Intègre `analyzer.py`, `generator.py`, `notifier.py`
3. Gère les erreurs et fallbacks
4. Tests d’intégration

## Livrable

`crm/workflow.py`

## Références

- **PRD** : `PRD-CRM-TECH-DEBT-20260929.md`
- **MOC** : `MOC-CRM-TECH-DEBT-20260929.md`
