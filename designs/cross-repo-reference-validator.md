---
name: cross-repo-reference-validator
description: "Pattern de validation des références cross-repo dans les designs, PRD-MOC et MOC. Vérifie que chaque référence vers un repo, un fichier ou un concept existe bien dans la SOT avant acceptation."
version: "1.0.0"
status: active
layer: L4
type: pattern
profile: STANDARD
intent_hash: 0xDESIGN_CROSS_REPO_REFERENCE_VALIDATOR_20260922
adr: ADR-2026-09-22-002-cross-repo-reference-validator
---

# cross-repo-reference-validator

## Definition

Pattern de validation des références cross-repo dans les designs, PRD-MOC et MOC. Vérifie que chaque référence vers un repo, un fichier ou un concept existe bien dans la SOT avant acceptation.

## Problem

Les documents font des références à des repos, fichiers ou concepts qui n'existent pas ou ont été renommés/supprimés.

Exemples :
- `gerivdb/CLM` référencé dans `JEVX/SCOPE.yaml` mais absent de `known_repositories.yaml`
- `src/server.ts` référencé dans `designs/jevx.yaml` mais absent du repo JEVX
- `kg-causal` référencé dans `depends_on` mais non résolu dans le MDU

## Solution

### 1. SOT-first validation

```yaml
# Pour chaque référence cross-repo
reference:
  type: repo
  target: gerivdb/CLM
  validation:
    - check: known_repositories.yaml
      result: NOT_FOUND
    - action: BLOCK
```

### 2. File existence check

```yaml
reference:
  type: file
  target: src/server.ts
  repo: gerivdb/JEVX
  validation:
    - check: git ls-tree HEAD src/server.ts
      result: NOT_FOUND
    - action: BLOCK
```

### 3. Concept resolution

```yaml
reference:
  type: concept
  target: kg-causal
  validation:
    - check: meta-design.yaml
      result: UNRESOLVED
    - action: WARN
```

## Implementation

- Script : `scripts/cross-repo-reference-validator.py`
- Integration : pre-commit hook, CI pipeline
- SOT sources : `known_repositories.yaml`, `meta-design.yaml`, `ONTOLOGY_DECLARATION.yaml`

## Benefits

- Élimine E3 (références cross-repo fantômes)
- Améliore la fiabilité des documents
- Réduit les incohérences design/code

## IntentHash

0xDESIGN_CROSS_REPO_REFERENCE_VALIDATOR_20260922
