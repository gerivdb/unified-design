---
name: catalog-consumer-auditor
description: "Pattern de vérification que les consumers des designs et pipelines sont documentés dans les catalogues. Détecte les entrées de catalogue sans consumers et les consumers non catalogués."
version: "1.0.0"
status: active
layer: L4
type: pattern
profile: STANDARD
intent_hash: 0xDESIGN_CATALOG_CONSUMER_AUDITOR_20260922
adr: ADR-2026-09-22-005-catalog-consumer-auditor
---

# catalog-consumer-auditor

## Definition

Pattern de vérification que les consumers des designs et pipelines sont documentés dans les catalogues.

## Problem

Les catalogues (`designs.index.yaml`, `pipelines.index.yaml`) peuvent avoir des entrées sans `consumers` documentés, ou des designs/pipelines avec consumers non listés dans les catalogues.

Exemple : `jevx.yaml` a des consumers (`KIX`, `ROOTX`, `TALEX`, `VOLTX`, `KG-CAUSAL`) mais `catalog/designs.index.yaml` les avait omis.

## Solution

### 1. Catalog completeness check

```yaml
# Pour chaque entrée de catalogue
entry:
  name: jevx
  consumers: []  # EMPTY - PROBLEM
  action: BLOCK
```

### 2. Design consumer extraction

```yaml
# Extraire les consumers du design
design_consumers:
  - gerivdb/KIX
  - gerivdb/ROOTX
  - gerivdb/TALEX
  - gerivdb/VOLTX
  - gerivdb/KG-CAUSAL
```

### 3. Reconciliation

```yaml
# Réconcilier catalogue vs design
catalog_consumers: []
design_consumers: [KIX, ROOTX, TALEX, VOLTX, KG-CAUSAL]
missing_in_catalog: [KIX, ROOTX, TALEX, VOLTX, KG-CAUSAL]
action: UPDATE_CATALOG
```

## Implementation

- Script : `scripts/catalog-consumer-auditor.py`
- Integration : pre-commit hook, CI pipeline
- Targets : `catalog/designs.index.yaml`, `catalog/pipelines.index.yaml`

## Benefits

- Élimine E8 (consumers manquants)
- Améliore la documentation
- Renforce la traçabilité des dépendances

## IntentHash

0xDESIGN_CATALOG_CONSUMER_AUDITOR_20260922
