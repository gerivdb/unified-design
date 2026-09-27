---
type: DESIGN
version: "1.0.0"
intent_hash: 0xDESIGN_BRANCH_TAXONOMY_GATE_20260922
date: "2026-09-22"
status: proposed
layer: L0
source: PRD-MOC-BRANCH-TAXONOMY-ENFORCEMENT-20260922
---

# Branch Taxonomy Gate

## Principe

> Le pattern de branche est un critère de passage écrit. Sa non-conformité doit être
> détectée avant le push, pas après. ALFRED est un gardien, pas un chroniqueur.

Ce design applique les éléments G3 et G7 de `GATES_HIERARCHIQUES.md` :
- **G3** (Gates explicites) : chaque phase se termine par une décision continue / ajuster / rollback
- **G7** (Veilleur ≠ gardien) : la détection ALFRED est non-bloquante, mais le point de décision doit être tracé

## Règles

| # | Règle |
|---|-------|
| 1 | Pattern canonique : `type/jurisdiction-slug-id` |
| 2 | Exemple : `feat/gov-hub-registry-20260921` |
| 3 | Toute branche non conforme est BLOQUÉE en pré-push |
| 4 | Le message d'erreur indique le pattern attendu et un exemple |
| 5 | La branche `main` et `dev` sont exemptées |

## Pattern

```powershell
$branchPattern = '^[a-z]+/[a-z0-9-]+-[a-z0-9-]+-\d+$'
if ($CurrentBranch -notmatch $branchPattern -and $CurrentBranch -notin @("main", "dev")) {
    Write-BrgsLog "BLOCKED: Branch taxonomy mismatch in $RepoName" "ERR"
    Write-Host "`n  Branch: $CurrentBranch"
    Write-Host "  Pattern attendu: type/jurisdiction-slug-id"
    Write-Host "  Exemple: feat/env2-lxc-network-001"
    Write-Host "`n  Fix: git checkout -b feat/<jurisdiction>-<slug>-<id>`n"
    exit 1
}
Write-BrgsLog "Guard 6 — Branch taxonomy validated ($CurrentBranch)" "OK"
```

## Application

- `.githooks/pre-push.ps1` : ajouter Guard 6 après Guard 5
- `multi-repo-governance.yaml` : déclarer `allowed_branch_prefixes` par repo
- Session closeout : vérifier la taxonomie avant de déclarer la session terminée

## Anti-patterns

- Détecter la non-conformité après le push (post-push)
- Autoriser `--no-verify` comme contournement systématique
- Pattern de branche sans jurisdiction (ex: `feat/registry-001`)

## Références

- Design L0 : `GATES_HIERARCHIQUES.md` (0xDESIGN_GATES_HIERARCHIQUES_20260823)
- ADR : ADR-2026-09-19-001-stash-audit-periodic
- PRD-MOC : PRD-MOC-BRANCH-TAXONOMY-ENFORCEMENT-20260922
- ALFRED : `multi-repo-governance.yaml` branch_routing
