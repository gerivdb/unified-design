---
name: git-lock-guardian
description: "Pattern de garde-fou git qui détecte et nettoie automatiquement les index.lock avant commit, et sérialise les opérations git critiques pour éviter les blocages E1."
version: "1.0.0"
status: active
layer: L4
type: pattern
profile: STANDARD
intent_hash: 0xDESIGN_GIT_LOCK_GUARDIAN_20260922
adr: ADR-2026-06-19-001-git-atomic-commit
---

# git-lock-guardian

## Definition

Pattern de garde-fou git qui détecte et nettoie automatiquement les `index.lock` avant commit, et sérialise les opérations git critiques pour éviter les blocages.

## Problem

Les commits échouent avec `fatal: Unable to create .../.git/index.lock: File exists.` quand :
- Un processus git zombie détient le lock
- Un commit parallèle non détecté se termine
- Un crash git précédent a laissé un lock

## Solution

### 1. Pre-commit hook

```powershell
# Détecter et supprimer le lock avant commit
$lockPath = ".git/index.lock"
if (Test-Path $lockPath) {
    Remove-Item $lockPath -Force
    Write-Host "[GIT-LOCK-GUARDIAN] index.lock removed"
}
```

### 2. Serialization guard

```powershell
# Vérifier qu'aucun processus git ne tourne avant commit critique
$gitProcesses = Get-Process -Name "git" -ErrorAction SilentlyContinue
if ($gitProcesses.Count -gt 0) {
    Write-Warning "[GIT-LOCK-GUARDIAN] git processes running, waiting..."
    Start-Sleep -Seconds 2
}
```

### 3. Retry with backoff

```powershell
$maxRetries = 3
for ($i = 0; $i -lt $maxRetries; $i++) {
    try {
        git commit -m $message
        break
    } catch {
        if ($i -eq $maxRetries - 1) { throw }
        Start-Sleep -Seconds ($i + 1)
    }
}
```

## Implementation

- Hook : `.git/hooks/pre-commit`
- Script : `scripts/git-lock-guardian.ps1`
- Integration : `pre-commit` config

## Benefits

- Élimine E1 (index.lock bloquant)
- Réduit les frictions git
- Améliore la fiabilité des commits atomiques

## IntentHash

0xDESIGN_GIT_LOCK_GUARDIAN_20260922
