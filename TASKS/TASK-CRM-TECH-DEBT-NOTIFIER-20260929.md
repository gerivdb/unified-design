---
type: TASK
version: "1.0.0"
date: "2026-09-29"
status: proposed
intent_hash: 0xTASK_CRM_TECH_DEBT_NOTIFIER_20260929
parent_epic: EPIC-CRM-TECH-DEBT-20260929.md
task_id: TASK-CRM-004
priority: P1
assignee: L0-CANON
repo: gerivdb/unified-design
---

# TASK — CRM Tech Debt Notifier

## Objectif

Créer `crm/notifier.py` pour notifier la dette technique vers les repos cibles.

## Critères d’acceptation

1. `notifier.py` envoie notifications CRM
2. Support multi-repo (`unified-design`, `ARGUS`, `CTULU`, etc.)
3. Fallback local si ARGUS/CTULU indisponibles
4. Tests unitaires

## Livrable

`crm/notifier.py`

## Références

- **PRD** : `PRD-CRM-TECH-DEBT-20260929.md`
- **MOC** : `MOC-CRM-TECH-DEBT-20260929.md`
