---
type: ADR
status: proposed
date: "2026-07-31"
intent_hash: 0xADR_037_TDD_AIRAIN_LAW_20260731
---

# ADR-037: Loi d'Airain TDD (No Test No Code)

## Context

Les agents produisent du code de production sans avoir écrit de test qui échoue au préalable, menant à du code non testé et des bugs en production (source: "Graph of Loops" L4 - Superpowers).

## Decision

Imposer une contrainte radicale: **No Test, No Code**.

- L'agent a l'interdiction de produire du code de production sans avoir écrit un test qui échoue au préalable
- Si du code de production existe avant le test: **"Delete means delete"** (on supprime et on recommence)
- Gate enforcement: pre-commit / pre-push / CI
- Couverture minimale: 85%

## Implementation

Nouvel atom: `ATOM-053-tdd-airain-law`
- Capability: `tdd-airain-law` (enforce_test_first: true, delete_on_violation: true, violation_action: delete_and_restart)
- Hérite de: `test-handler-first`, `test-windows-tcp`, `atomic-commit`
- Nouvelles design_rules: `tdd-airain-law-enforced` (check: test_first_or_delete)
- Module loop_engine: `tdd_airain_gate.py` (TDDAirainGate)

## Consequences

### Positive
- Garantie absolue: tout code prod a un test qui a échoué avant
- Élimine le pattern "test after"
- Delete means delete = pas de dette technique cachée
- Coverage threshold enforceable en CI

### Negative
- Vélocité initiale réduite (courbe d'apprentissage)
- Frustration possible agents (suppression travail)
- Nécessite outillage détection violation fiable

## References

- Graph of Loops, Section 5: "La Loi d'Airain du TDD (L4 - Superpowers)"
- ATOM-053-tdd-airain-law.yaml
- loop_engine/tdd_airain_gate.py