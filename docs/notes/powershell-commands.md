---
type: NOTE
status: active
date: "2026-09-21"
intent_hash: 0xNOTE_POWERSHELL_CMDS_20260921
---

# Notes — Commandes PowerShell vs Unix

## Interdiction : commandes Unix dans PowerShell

PowerShell n'a pas les commandes Unix suivantes :

| Commande Unix | Alternative PowerShell |
|---------------|------------------------|
| `head -n 20` | `Select-Object -First 20` |
| `tail -n 20` | `Select-Object -Last 20` |
| `grep -r pattern` | `Select-String -Path ... -Pattern pattern` |
| `wc -l` | `(Get-Content ... | Measure-Object -Line).Lines` |
| `cat file` | `Get-Content file` ou `type file` |
| `ls -la` | `Get-ChildItem -Force` |
| `cp -r src dst` | `Copy-Item -Path src -Destination dst -Recurse` |
| `mv src dst` | `Move-Item -Path src -Destination dst` |
| `rm -rf dir` | `Remove-Item -Path dir -Recurse -Force` |
| `mkdir -p dir` | `New-Item -ItemType Directory -Path dir -Force` |

## Règle

**Ne jamais utiliser** de commandes Unix dans les scripts PowerShell du repo.
Toujours utiliser les cmdlets PowerShell natives.

## Référence

- TALEX friction #7 : `head` inexistant dans PowerShell
- Source : `REPORTS/REPORT-TALEX-FRICTION-SESSION-20260921.md`
