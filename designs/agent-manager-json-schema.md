---
name: agent-manager-json-schema
description: Schéma JSON de référence pour .kilo/agent-manager.json. Garantit la structure, les types, et les contraintes de validité. Utilise ce skill quand tu dois valider, créer, ou réparer agent-manager.json.
version: 1.0.0
intent_hash: 0xDESIGN_AGENT_MANAGER_JSON_SCHEMA_20260810
type: design
layer: L3
repo: gerivdb/GeriCode
---

# Agent Manager JSON Schema

## Objectif
Définir le schéma JSON de référence pour `.kilo/agent-manager.json` afin de prévenir la corruption et garantir la cohérence.

## Structure

```json
{
  "worktrees": {
    "<worktreeId>": {
      "branch": "string",
      "path": "string (absolute Windows path)",
      "parentBranch": "string",
      "createdAt": "ISO 8601 datetime",
      "remote": "string",
      "branchOwned": "boolean",
      "label": "string (optional)"
    }
  },
  "sessions": {
    "<sessionId>": {
      "worktreeId": "string | null",
      "createdAt": "ISO 8601 datetime"
    }
  },
  "tabOrder": {
    "local": ["sessionId | pending:<uuid>"]
  },
  "worktreeOrder": ["<worktreeId>"],
  "sessionsCollapsed": "boolean"
}
```

## Contraintes

### worktrees
- `branch` : non vide, correspond à une branche git existante
- `path` : absolu, sous `.kilo/worktrees/`
- `parentBranch` : non vide
- `createdAt` : ISO 8601
- `remote` : `origin` ou autre remote valide
- `branchOwned` : boolean
- `label` : optionnel, max 50 chars

### sessions
- `worktreeId` : null ou référence valide vers `worktrees`
- `createdAt` : ISO 8601

### tabOrder
- `local` : tableau de sessionId ou `pending:<uuid>`
- Cohérent avec `sessions`

### worktreeOrder
- Tableau de worktreeId
- Sous-ensemble de `worktrees`

## Validation PowerShell

```powershell
function Test-AgentManagerJson {
    param([string]$Path)
    $obj = Get-Content $Path -Raw | ConvertFrom-Json
    $errors = @()

    # Vérifier worktrees
    foreach ($wt in $obj.worktrees.PSObject.Properties) {
        if (-not $wt.Value.branch) { $errors += "worktree $($wt.Name): branch missing" }
        if (-not (Test-Path $wt.Value.path)) { $errors += "worktree $($wt.Name): path missing" }
    }

    # Vérifier sessions
    foreach ($s in $obj.sessions.PSObject.Properties) {
        if ($s.Value.worktreeId -and -not $obj.worktrees.PSObject.Properties.Name -contains $s.Value.worktreeId) {
            $errors += "session $($s.Name): orphan worktreeId"
        }
    }

    # Vérifier worktreeOrder
    foreach ($id in $obj.worktreeOrder) {
        if (-not $obj.worktrees.PSObject.Properties.Name -contains $id) {
            $errors += "worktreeOrder: $id not in worktrees"
        }
    }

    return $errors
}
```

## Référence ADR
- **ADR** : ADR-2026-08-10-007-AGENT_MANAGER_JSON_SCHEMA
- **IntentHash** : 0xDESIGN_AGENT_MANAGER_JSON_SCHEMA_20260810
- **Dépôt** : gerivdb/GeriCode
- **Statut ADR** : proposed
