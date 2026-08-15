---
type: ADR
status: proposed
date: "2026-08-15"
intent_hash: 0xADR_GOVERNANCE_HUB_BRANCH_RENAME_GOVERNANCE_20260815
author: gerivdb
source_repo: gerivdb/GOVERNANCE-HUB
source_path: ADR/ADR-2026-08-15-002-BRANCH-RENAME-GOVERNANCE.md
---

# ADR-2026-08-15-002 - Branch Rename Governance

## Contexte

L'audit du 2026-08-15 a révélé que la branche `feat/adr-0100-base243-meta-substrate` a été **rebaptisée** sans trace ni avertissement. Le nom original suggérait un contenu (ADR-0100) qui n'était plus présent dans la branche. Ceci a créé :

1. Une confusion lors de l'audit (2 heures perdues à vérifier le contenu)
2. Un risque d'oubli du travail réel (5 commits sur ADR-004/0101/INTENT-022/PRD-144/EPIC-236)
3. Une impossibilité de tracker l'historique via les noms de branche

## Problème

Aucune règle ne gouverne le renommage de branches git dans l'écosystème. Un agent peut rebaptiser une branche sans laisser de trace dans le WAL, sans mettre à jour les références, et sans créer de PR pour le nouveau nom.

## Décision

### Règles

| Règle | Description |
|-------|-------------|
| **R-BRG-001** | Interdiction de renommer une branche sans créer de PR ou de document de traçabilité |
| **R-BRG-002** | Toute branche renommée doit avoir son ancien nom documenté dans le message de commit initial de la nouvelle branche |
| **R-BRG-003** | Le WAL (NEXUS) doit enregistrer l'événement `branch_renamed` avec `old_name` et `new_name` |
| **R-BRG-004** | Les branches dont le nom contient un ADR/PRD/EPIC/INTENT number doivent correspondre au contenu (pas de rebaptisation silencieuse) |
| **R-BRG-005** | Si une branche est renommée, la branche originale doit être supprimée sur tous les remotes dans les 24h |

### Implementation

```yaml
# unified-design/atoms/branch-rename-governance.yaml
name: branch-rename-governance
version: 1.0.0
rules:
  - id: R-BRG-001
    trigger: git branch -m old_name new_name
    action: require_pr_or_documentation
  - id: R-BRG-002
    trigger: new_branch_first_commit
    action: include_old_name_in_commit_message
  - id: R-BRG-003
    trigger: branch_renamed
    action: log_to_wal_nexus
  - id: R-BRG-004
    trigger: branch_name_contains_number
    action: validate_content_matches_number
  - id: R-BRG-005
    trigger: branch_renamed
    action: delete_old_branch_on_all_remotes_within_24h
```

### Hook pre-commit

```bash
#!/usr/bin/env bash
# .githooks/pre-commit-branch-rename-check
# Bloque les renommages silencieux

BRANCH_NAME=$(git rev-parse --abbrev-ref HEAD)
if [[ $BRANCH_NAME =~ ^(feat|fix|docs|chore)/adr-[0-9]+ ]]; then
    ADR_NUM=$(echo $BRANCH_NAME | grep -oP 'adr-[0-9]+' | head -1)
    ADR_FILE=$(find ADR/ -name "ADR-${ADR_NUM}-*.md" | head -1)
    if [ -z "$ADR_FILE" ]; then
        echo "BLOCKED: Branch name references ADR-${ADR_NUM} but file does not exist"
        exit 1
    fi
fi
```

### Skills associés

| Skill | Description |
|-------|-------------|
| `branch-rename-governance` | Vérifie la conformité des renommages, log dans WAL |
| `governance-doc-writer` | Crée le document de traçabilité lors d'un renommage |

## Conséquences

- **Positif** : Traçabilité complète des renommages
- **Positif** : Cohérence entre nom de branche et contenu
- **Négatif** : Légère overhead administratif pour les renommages légitimes
- **Négatif** : Nécessite une éducation des agents

## Alternatives écartées

| Alternative | Raison |
|-------------|--------|
| Interdiction totale de renommer | Trop restrictif, les renommages sont parfois nécessaires |
| Confiance sans vérification | A conduit à l'incident du 2026-08-15 |

## Validation

- **Spécification** : Ce ADR + PRD MOC `PRD-MOC-GOVERNANCE-HUB-GIT-GRAPH-RECOVERY-2026-08-15.md`
- **Preuve** : Incident 2026-08-15 - branche `feat/adr-0100-base243-meta-substrate` rebaptisée sans trace
- **RSS-v2.3** : Conforme

## Référence

- **PRD MOC** : `PRD-MOC-GOVERNANCE-HUB-GIT-GRAPH-RECOVERY-2026-08-15.md`
- **IntentHash** : `0xADR_GOVERNANCE_HUB_BRANCH_RENAME_GOVERNANCE_20260815`
- **Dépôt** : gerivdb/unified-design
- **Statut ADR** : proposed

