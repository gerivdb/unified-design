---
name: session-boot-skill
description: >
  Exécute les checks BOOT/CLOSEOUT de session.
  Wrapper skill de session_boot.py pour exposition cross-repo.
version: "1.0.0"
status: active
layer: L0
intent_hash: 0xSKILL_SESSION_BOOT_20260920
triggers:
  - "session boot checks"
  - "session closeout"
  - "boot sequence"
inputs:
  - type: mode
    description: "Mode : check (5sexter/talex/wazaa) ou closeout"
  - type: push
    description: "Push optionnel après closeout"
outputs:
  - type: check_results
    description: "Résultats des checks"
  - type: commit_msg
    description: "Message de commit (closeout)"
  - type: push_status
    description: "Statut du push"
tools:
  - python
  - git
artifacts:
  - path: reports/session-boot-*.json
    format: json
governance:
  adr: ADR-2026-09-19-SAFE-ACTION-PATTERN
  design: session-boot-design
  atom: ecosystem-meta-coherence-gate
---

# Skill : Session Boot

## Description

Exécute les checks BOOT/CLOSEOUT de session. Wrapper skill de `session_boot.py` pour exposition cross-repo.

## When to use

- Début de session multi-repo
- Fin de session multi-repo
- Avant tout commit/push

## Process

### ÉTAPE-1 — Boot checks
Exécuter les checks BOOT :
- TALEX checklist
- WAZAA realtime snapshot
- BOOT-5sexter auto-discovery quick scan

### ÉTAPE-2 — Travail
Travail de session (implémentation, corrections, etc.).

### ÉTAPE-3 — Closeout
- Vérifier le statut git
- Auto-commit des changements valides
- Push optionnel vers origin/main

## Usage

```bash
# Checks seulement
python -m unified-design.skills.session-boot-skill --check all

# Closeout avec push
python -m unified-design.skills.session-boot-skill --closeout --push
```

## Anti-patterns

- Session sans boot
- Session sans closeout
- Auto-commit sans vérification des changements

## References

- **Design** : `designs/session-boot-design/design.yaml`
- **Primitive** : `primitives/session-boot-primitive.yaml`
- **Script** : `scripts/session_boot.py`
- **Workflow** : `workflows/workflow-session-boot-closeout.md`
