---
type: INTENT
version: "1.0.0"
date: "2026-09-29"
status: proposed
intent_hash: 0xINTENT_CRM_TECH_DEBT_20260929
parent_intent: INTENT-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md
pole_id: POLE-MEMORY-001
owner: L0-CANON
repo: gerivdb/unified-design
---

# INTENT — CRM Tech Debt Management

## Objectif

Transformer `TASKS/` d'un dossier de tâches plainte en système CRM de gestion de la dette technique, intégré à `auto-design` et exploitable par tout l'écosystème.

## Contexte

- `TASKS/` contient 15 tâches auto-design, mais sans suivi de dette, sans notification, sans workflow de résolution.
- `auto-design` sait scorer la maturité, mais pas la dette technique.
- L'écosystème multi-repo (`unified-design`, `ARGUS`, `CTULU`, `KG-L`, etc.) nécessite une vue agrégée de la dette.

## Décisions

1. Registry centralisé `crm/tech_debt_registry.yaml` pour agréger la dette cross-repo
2. Scoring dette dans `analyzer.py` : `_score_tech_debt()`
3. Génération CRM dans `generator.py` : `generate_crm_tasks()`
4. Notification dans `verifier.py` : hook vers `crm/notifier.py`
5. Workflow end-to-end : détection → scoring → génération → notification → PR → merge

## Livrables

| ID | Livrable | Fichier | Priorité |
|---|---|---|---|
| L1 | Registry dette | `crm/tech_debt_registry.yaml` | P0 |
| L2 | Scoring dette | `analyzer.py` | P0 |
| L3 | Génération CRM | `generator.py` | P0 |
| L4 | Notification | `crm/notifier.py` | P1 |
| L5 | Workflow | `crm/workflow.py` | P1 |
| L6 | Tests | `tests/test_crm_tech_debt.py` | P1 |

## Proof-of-Life

- [ ] 2026-09-29T21:00:00+02:00 — INTENT créé
- [ ] 2026-09-29T21:05:00+02:00 — PRD créé
- [ ] 2026-09-29T21:10:00+02:00 — MOC créé
- [ ] 2026-09-29T21:15:00+02:00 — ADR créé
- [ ] 2026-09-29T21:20:00+02:00 — EPIC créé
- [ ] 2026-09-29T21:25:00+02:00 — TASKs créés
- [ ] 2026-09-29T21:30:00+02:00 — Implémentation terminée
- [ ] 2026-09-29T21:35:00+02:00 — Tests passés

## Références

- **PRD** : `PRD/PRD-CRM-TECH-DEBT-20260929.md`
- **MOC** : `MOC/MOC-CRM-TECH-DEBT-20260929.md`
- **ADR** : `ADR/ADR-CRM-TECH-DEBT-20260929.md`
- **EPIC** : `EPICS/EPIC-CRM-TECH-DEBT-20260929.md`
