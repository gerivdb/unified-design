---
name: design-code-sync
description: "Pattern de vérification de la synchronisation entre les designs YAML et le code implémenté. Détecte les décalages d'entrypoint, de hardware_profile, de configuration et de sémantique."
version: "1.0.0"
status: active
layer: L4
type: pattern
profile: STANDARD
intent_hash: 0xDESIGN_DESIGN_CODE_SYNC_20260922
adr: ADR-2026-09-22-004-design-code-sync
---

# design-code-sync

## Definition

Pattern de vérification de la synchronisation entre les designs YAML et le code implémenté.

## Problem

Les designs décrivent un comportement théorique qui peut désynchroniser du code réel :

Exemples :
- `entrypoint: src/server.ts` dans `jevx.yaml` mais `src/index.ts` dans `package.json`
- `max_queue: 64` dans `jevx.yaml` mais compteur `waiting` dans `engine.ts`
- `hardware_profile` ambigu dans `jevx.yaml`

## Solution

### 1. Entrypoint verification

```bash
# Vérifier que l'entrypoint du design existe dans le repo
design_entrypoint=$(yq '.components[0].entrypoint' designs/jevx.yaml)
git ls-tree HEAD $design_entrypoint || BLOCK
```

### 2. Configuration sync

```bash
# Vérifier que les paramètres du design correspondent au code
design_max_inflight=$(yq '.constraints[0].max_inflight' designs/jevx.yaml)
code_max_inflight=$(grep -o 'maxInflight: [0-9]*' src/config.ts)
if [ "$design_max_inflight" != "$code_max_inflight" ]; then WARN; fi
```

### 3. Hardware profile validation

```bash
# Vérifier que le hardware_profile est conforme
yq '.hardware_profile' designs/jevx.yaml | validate_schema hardware_schema.yaml
```

## Implementation

- Script : `scripts/design-code-sync.py`
- Integration : pre-commit hook, CI pipeline
- Targets : `designs/*.yaml`, `designs/**/*.yaml`

## Benefits

- Élimine E5/E6/E9 (désynchronisations design/code)
- Améliore la fiabilité des designs
- Réduit les incohérences documentation/implémentation

## IntentHash

0xDESIGN_DESIGN_CODE_SYNC_20260922
