---
name: ontology-dedup-auditor
description: "Pattern de détection et de fusion des doublons ontologiques dans les déclarations de concepts. Vérifie l'unicité des `id` et des `intent_hash` dans ONTOLOGY_DECLARATION.yaml et les fichiers de concepts."
version: "1.0.0"
status: active
layer: L4
type: pattern
profile: STANDARD
intent_hash: 0xDESIGN_ONTOLOGY_DEDUP_AUDITOR_20260922
adr: ADR-2026-09-22-003-ontology-dedup-auditor
---

# ontology-dedup-auditor

## Definition

Pattern de détection et de fusion des doublons ontologiques dans les déclarations de concepts.

## Problem

Les imports manuels ou automatisés de concepts peuvent créer des doublons :
- Même `id` déclaré plusieurs fois
- Même `intent_hash` répété
- Concepts sémantiquement identiques mais syntaxiquement différents

Exemple : `jev_variant` et `comparative_study` déclarés deux fois dans `JEVX/ONTOLOGY_DECLARATION.yaml`.

## Solution

### 1. Uniqueness check

```python
def check_duplicates(concepts):
    ids = [c['id'] for c in concepts]
    hashes = [c['intent_hash'] for c in concepts]
    
    duplicates = {
        'ids': [id for id in set(ids) if ids.count(id) > 1],
        'hashes': [h for h in set(hashes) if hashes.count(h) > 1]
    }
    return duplicates
```

### 2. Auto-merge

```python
def merge_duplicates(concepts):
    unique = {}
    for concept in concepts:
        key = concept['id']
        if key in unique:
            # Fusionner les métadonnées
            unique[key].update(concept)
        else:
            unique[key] = concept
    return list(unique.values())
```

### 3. Audit report

```yaml
ontology_dedup_report:
  duplicates_found: 2
  merged:
    - id: "jev_variant"
    - id: "comparative_study"
  action: MERGED
```

## Implementation

- Script : `scripts/ontology-dedup-auditor.py`
- Integration : pre-commit hook, CI pipeline
- Targets : `ONTOLOGY_DECLARATION.yaml`, `concepts/**/*.md`

## Benefits

- Élimine E4 (doublons ontologiques)
- Améliore la qualité de l'ontologie
- Réduit la pollution conceptuelle

## IntentHash

0xDESIGN_ONTOLOGY_DEDUP_AUDITOR_20260922
