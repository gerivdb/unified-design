---
type: TASK
version: "1.0.0"
date: "2026-09-29"
status: proposed
intent_hash: 0xTASK_CRM_TECH_DEBT_GENERATION_20260929
parent_epic: EPIC-CRM-TECH-DEBT-20260929.md
task_id: TASK-CRM-003
priority: P0
assignee: L0-CANON
repo: gerivdb/unified-design
---

# TASK — CRM Tech Debt Generation

## Objectif

Ajouter `generate_crm_tasks()` à `engine/auto_design/generator.py` pour créer des tickets CRM exploitables.

## Critères d’acceptation

1. `generate_crm_tasks()` prend un item de registry scoré
2. Crée un ticket CRM avec métadonnées
3. Compatible avec templates `templates/auto_design/`
4. Tests unitaires

## Livrable

`engine/auto_design/generator.py` modifié

## Références

- **PRD** : `PRD-CRM-TECH-DEBT-20260929.md`
- **MOC** : `MOC-CRM-TECH-DEBT-20260929.md`
