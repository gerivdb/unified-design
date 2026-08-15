---
type: ADR
status: proposed
date: "2026-08-15"
intent_hash: 0xADR_GOVERNANCE_HUB_PR_LIFECYCLE_GATE_20260815
author: gerivdb
source_repo: gerivdb/GOVERNANCE-HUB
source_path: ADR/ADR-2026-08-15-001-PR-LIFECYCLE-GATE.md
---

# ADR-2026-08-15-001 - PR Lifecycle Gate Obligatoire

## Contexte

L'audit du 2026-08-15 sur `gerivdb/GOVERNANCE-HUB` a révélé que la PR #84 (`feat/epic-257-ternary-state-mapper`) a été fermée sans merge, entraînant la perte apparente de 11 commits. En réalité, ces commits étaient des DUPLICATS déjà présents dans `main` via d'autres PRs. Cependant, l'absence de garde-fou automatique a créé :

1. Une branche orpheline de 6 semaines
2. 13 stashes liés à cette branche
3. Un travail de nettoyage de 4 heures
4. Un risque de perte réelle si les commits n'avaient pas été dupliqués

## Problème

Aucun mécanisme ne surveille les PRs orphelines (fermées sans merge) ni ne déclenche d'alerte lorsqu'une branche feature diverge de `main` pendant plus de 7 jours.

## Décision

Implémenter un **PR Lifecycle Gate** obligatoire dans `unified-design` :

### Règles

| Règle | Description |
|-------|-------------|
| **R-PRLG-001** | Toute PR ouverte depuis > 14 jours sans activité -> alerte automatique |
| **R-PRLG-002** | Toute PR fermée non mergée -> vérifier si le travail est récupérable ailleurs |
| **R-PRLG-003** | Toute branche `feature/*` sans PR ouverte depuis > 7 jours -> alerte |
| **R-PRLG-004** | Toute branche `feature/*` dont le dernier commit date de > 14 jours -> suggestion de suppression |
| **R-PRLG-005** | Les stashes liés à des branches supprimées doivent être inspectés avant suppression |

### Implementation

```yaml
# unified-design/atoms/pr-lifecycle-gate.yaml
name: pr-lifecycle-gate
version: 1.0.0
rules:
  - id: R-PRLG-001
    trigger: pr_age > 14d AND pr.status = open
    action: alert_owner + comment_on_pr
  - id: R-PRLG-002
    trigger: pr.status = closed AND pr.merged = false
    action: scan_other_branches_for_duplicate_work
  - id: R-PRLG-003
    trigger: branch.prefix = feature/ AND branch.has_open_pr = false AND branch.age > 7d
    action: alert_owner + suggest_pr_or_delete
  - id: R-PRLG-004
    trigger: branch.prefix = feature/ AND branch.last_commit_age > 14d
    action: suggest_deletion_after_7d_grace
  - id: R-PRLG-005
    trigger: stash.referenced_branch NOT IN active_branches
    action: flag_for_audit_before_drop
```

### Skills associés

| Skill | Description |
|-------|-------------|
| `pr-lifecycle-gate` | Scan quotidien des PRs et branches, application des règles R-PRLG-001 à 005 |
| `branch-content-analyzer` | Vérifie si le contenu d'une branche est déjà dans `main` avant suppression |
| `kilo-worktree-reconciler` | Réconcilie les worktrees Agent Manager avec les branches git |

### Workflows

| Workflow | Déclencheur | Action |
|----------|-------------|--------|
| `pr-lifecycle-gate-daily.yml` | Schedule quotidien 04:00 UTC | Scan toutes les PRs ouvertes, appliquer règles |
| `pr-lifecycle-gate-post-session.yml` | Post-session KiloCode | Vérifier les branches créées pendant la session |

## Conséquences

- **Positif** : Les PRs orphelines sont détectées avant d'accumuler des mois de divergence
- **Positif** : Le travail en double est détecté et signalé
- **Négatif** : Nécessite un citoyen dédié ou un workflow automatisé
- **Négatif** : Peut générer des alertes excessives si les seuils sont trop bas

## Alternatives écartées

| Alternative | Raison |
|-------------|--------|
| Suppression automatique des PRs > 14 jours | Trop risqué, risque de perdre du travail en cours |
| Alerte manuelle uniquement | Pas suffisant, les agents IA oublient |
| Garder toutes les branches | Pollution du graphe git, confusion |

## Validation

- **Spécification** : Ce ADR + PRD MOC `PRD-MOC-GOVERNANCE-HUB-GIT-GRAPH-RECOVERY-2026-08-15.md`
- **Preuve** : Session 2026-08-15 a identifié 12 branches divergentes, 13 stashes, 1 branche orpheline de 6 semaines
- **RSS-v2.3** : Conforme

## Référence

- **PRD MOC** : `PRD-MOC-GOVERNANCE-HUB-GIT-GRAPH-RECOVERY-2026-08-15.md`
- **IntentHash** : `0xADR_GOVERNANCE_HUB_PR_LIFECYCLE_GATE_20260815`
- **Dépôt** : gerivdb/unified-design
- **Statut ADR** : proposed

