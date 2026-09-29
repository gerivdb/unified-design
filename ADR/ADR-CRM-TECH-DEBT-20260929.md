---
type: ADR
version: "1.0.0"
date: "2026-09-29"
status: proposed
intent_hash: 0xADR_CRM_TECH_DEBT_20260929
parent_intent: INTENT-CRM-TECH-DEBT-20260929.md
pole_id: POLE-MEMORY-001
owner: L0-CANON
repo: gerivdb/unified-design
---

# ADR — CRM Tech Debt Registry as Cross-Repo Ledger

## Contexte

`TASKS/` est un dossier de tâches plainte sans agrégation, scoring ni workflow. La dette technique cross-repo (`unified-design`, `ARGUS`, `CTULU`, `KG-L`, etc.) n’est pas centralisée, donc non visible, non notifiée, non résolue.

## Décision

Introduire un registry CRM dédié à la dette technique, avec scoring intégré à `auto-design` et workflow end-to-end.

## Options

| # | Option | Description |
|---|---|---|
| 1 | Aucune | Laisser `TASKS/` comme dossier plainte |
| 2 | Registry YAML + hook `auto-design` | Centraliser la dette, scorer, générer, notifier |

## Décision

Option 2.

## Conséquences

- `crm/tech_debt_registry.yaml` devient la source de vérité de la dette technique
- `analyzer.py` expose `_score_tech_debt()`
- `generator.py` expose `generate_crm_tasks()`
- `crm/notifier.py` notifie vers les repos cibles
- `crm/workflow.py` orchestre le cycle complet

## Rationale

- Dette technique multi-repo nécessite une vue agrégée
- `auto-design` est le point d’entrée naturel pour scoring/génération
- YAML simple, lisible, versionné, compatible BDCP

## Références

- **PRD** : `PRD-CRM-TECH-DEBT-20260929.md`
- **INTENT** : `INTENT-CRM-TECH-DEBT-20260929.md`
- **MOC** : `MOC-CRM-TECH-DEBT-20260929.md`
