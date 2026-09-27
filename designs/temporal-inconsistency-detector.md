---
name: temporal-inconsistency-detector
description: "Pattern de détection des incohérences temporelles entre documents successifs d'un projet (Objective.txt vs Dryrun, PRD-MOC vs MOC, etc.). Résout par chronologie en retenant l'état le plus récent."
version: "1.0.0"
status: active
layer: L4
type: pattern
profile: STANDARD
intent_hash: 0xDESIGN_TEMPORAL_INCONSISTENCY_DETECTOR_20260922
adr: ADR-2026-09-22-001-temporal-inconsistency-detector
---

# temporal-inconsistency-detector

## Definition

Pattern de détection des incohérences temporelles entre documents successifs d'un projet. Résout par chronologie en retenant l'état le plus récent.

## Problem

Les documents de projet (Objective.txt, PRD-MOC, MOC, designs) évoluent dans le temps. Quand un document ancien contredit un document récent, il y a incohérence temporelle.

Exemple :
- Objective.txt (2026-09-22T00:00) : L1, L8, L9 bloqués
- Dryrun (2026-09-22T02:25) : L1, L8, L9 ✅

## Solution

### 1. Timestamp extraction

```yaml
# Extraire les timestamps des documents
objective:
  timestamp: "2026-09-22T00:00:00+02:00"
  state: L1=blocked, L8=blocked, L9=blocked

dryrun:
  timestamp: "2026-09-22T02:25:00+02:00"
  state: L1=done, L8=done, L9=done
```

### 2. Chronological resolution

```python
def resolve_temporal_inconsistency(docs):
    # Trier par timestamp décroissant
    sorted_docs = sorted(docs, key=lambda d: d.timestamp, reverse=True)
    # Retenir l'état le plus récent
    latest = sorted_docs[0]
    return latest.state
```

### 3. Audit trail

```yaml
inconsistency_detected:
  - doc_a: Objective.txt
    timestamp: "2026-09-22T00:00:00+02:00"
    state: blocked
  - doc_b: Dryrun
    timestamp: "2026-09-22T02:25:00+02:00"
    state: done
resolution:
  method: chronological
  retained: Dryrun
  reason: "Dryrun is posterior to Objective.txt"
```

## Implementation

- Script : `scripts/temporal-inconsistency-detector.py`
- Integration : pre-commit hook, CI pipeline
- Output : `reports/temporal-inconsistency-<date>.yaml`

## Benefits

- Élimine E2 (incohérence temporelle)
- Garantit la cohérence des documents
- Améliore la traçabilité décisionnelle

## IntentHash

0xDESIGN_TEMPORAL_INCONSISTENCY_DETECTOR_20260922
