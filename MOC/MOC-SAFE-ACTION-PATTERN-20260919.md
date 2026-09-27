---
type: MOC
version: "1.0.0"
date: "2026-09-22"
status: approved
intent_hash: 0xMOC_SAFE_ACTION_PATTERN_20260919
---

# MOC — SAFE-ACTION-PATTERN

> Carte de contenu pour les documents de gouvernance du pattern d'action universelle PATRON-0 dans `unified-design`.

## PRD-MOC

- `PRD/PRD-MOC-SAFE-ACTION-PATTERN-20260919.md` — Spécification et livrables PATRON-0

## Design

- `designs/safe-action-pattern.yaml` — Design PATRON-0 : 7 fonctions + 3 états + 1 invariant + 4 gènes

## Atom

- `atoms/safe-action-gate.md` — Atom enforceable : states, functions, rules, anti-patterns

## ADR

- `ADR/ADR-2026-09-19-SAFE-ACTION-PATTERN.md` — Décision architecturale backing adoption PATRON-0

## Références croisées

| Document | Relation |
|---|---|
| `INTENT-2026-09-19-SAFE-ACTION-PATTERN.md` | Intent parent |
| `META-DESIGN.md` | Enregistrement design + atom |
| `meta-design.yaml` | Enregistrement schema |
| `ATOM-THINK-DO-CHECK-CONSCIOUSNESS.md` | Dépendance macro |
| `ATOM-GATE-LAYERS.md` | Dépendance gate |
| `ATOM-EXTERNAL-VERIFICATION-MANDATORY.md` | Dépendance validation réelle |
| `ATOM-STOP-CONDITION.md` | Dépendance réserve |
| `ATOM-CONFIDENCE-THRESHOLD.md` | Dépendance évaluation |
| `ATOM-INDEPENDENT-SOURCES-RULE.md` | Dépendance perception |
| `ATOM-UMODEL-AGENT-READY-DATA.md` | Dépendance auto-modèle |
| `ATOM-DELTA-CHECK.md` | Dépendance validation réelle |
| `ATOM-CARRY-FORWARD-PRINCIPLE.md` | Dépendance enregistrement |
| `designs/chain-engineering.yaml` | Dépendance séquence |
| `designs/delivery-engine.yaml` | Dépendance exécution |
| `designs/approval-readiness.yaml` | Dépendance validation réelle |
| `designs/think-do-check-consciousness.yaml` | Dépendance conscience ternaire |

## Livrables

| ID | Livrable | Chemin cible | Statut |
|---|---|---|---|
| L1 | Design `safe-action-pattern` | `designs/safe-action-pattern.yaml` | 🟡 Draft |
| L2 | Atom `safe-action-gate` | `atoms/safe-action-gate.md` | 🟡 Draft |
| L3 | ADR backing | `ADR/ADR-2026-09-19-SAFE-ACTION-PATTERN.md` | 🟡 Draft |
| L4 | Mise à jour `META-DESIGN.md` | `META-DESIGN.md` | ⏳ En attente |
| L5 | Mise à jour `meta-design.yaml` | `meta-design.yaml` | ⏳ En attente |

## Blocages

| Blocage | Description |
|---|---|
| ADR proposé | `ADR-2026-09-19-SAFE-ACTION-PATTERN` doit être accepté pour débloquer les designs opérationnels |
| Validation CI | `gerivdb design validate --strict` doit passer sur `safe-action-pattern.yaml` |
| Hooks | Pre-commit (`design-validate`, `frontmatter-guardian`, `check-yaml`) doit passer sans blocage encoding |

## Proof-of-Life

- [x] 2026-09-19T20:52:20+02:00 — Création MOC PATRON-0 / safe-action-pattern
