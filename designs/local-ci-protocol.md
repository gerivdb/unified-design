---
name: local-ci-protocol
description: Protocole CI 100% local pour l'écosystème Kilo. Pas de GitHub Actions. Utilise des scripts PowerShell, des skills locaux, et des watchers pour valider les sessions, les worktrees, et les règles.
version: 1.0.0
intent_hash: 0xDESIGN_LOCAL_CI_PROTOCOL_20260810
type: design
layer: L3
repo: gerivdb/GeriCode
---

# Local CI Protocol

## Objectif
Remplacer GitHub Actions par un pipeline CI 100% local, exécuté par PowerShell et des watchers Kilo.

## Architecture

```
+------------------------------------------+
|           LOCAL CI ORCHESTRATOR          |
|         (PowerShell + Kilo Skills)       |
+------------------------------------------+
                     |
         +----------+----------+
         |                     |
         v                     v
    +-----------+         +-----------+
    | VALIDATE  |         |  AUDIT    |
    |  JSON     |         | WORKTREE  |
    +-----------+         +-----------+
         |                     |
         v                     v
    +-----------+         +-----------+
    | powershell|         | kilo-wt   |
    | -json-safe|         | -audit    |
    +-----------+         +-----------+
```

## Workflows locaux

| Workflow | Déclencheur | Action |
|----------|-------------|--------|
| `post-session-local-validation` | post-session | Valide JSON + worktrees + processus |
| `kilo-worktree-audit` | schedule:daily | Audit complet kilo worktrees |

## Exécution

### Manuel
```powershell
# Valider après session
.\kilo\workflows\post-session-local-validation\run.ps1

# Auditer quotidiennement
.\kilo\workflows\kilo-worktree-audit\run.ps1
```

### Automatique
```powershell
# Watcher post-session
.\kilo\orchestrator\scripts\callback-watcher.ps1 -Action post-session-local-validation

# Watcher quotidien
.\kilo\orchestrator\scripts\callback-watcher.ps1 -Schedule daily -Action kilo-worktree-audit
```

## Interdictions
- [KO] Aucun `.github/workflows/`
- [KO] Aucun appel à `gh` pour des workflows
- [KO] Aucune dépendance à GitHub Actions
- [OK] Tout est local, PowerShell, et skills Kilo

## Référence ADR
- **ADR** : ADR-2026-08-10-008-LOCAL_CI_PROTOCOL
- **IntentHash** : 0xDESIGN_LOCAL_CI_PROTOCOL_20260810
- **Dépôt** : gerivdb/GeriCode
- **Statut ADR** : proposed
