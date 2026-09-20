---
name: branch-orphan-conflict-resolver
description: >
  Résout les branches orphelines et prévient les conflits cross-repo.
  Détecte les branches orphelines via reflog, analyse la saturation de contenu,
  et applique la stratégie de résolution appropriée (resurrection, absorption,
  cherry-pick, suppression). Utilise dryrun causal avant merge.
version: "1.0.0"
status: active
intent_hash: 0xSKILL_BRANCH_ORPHAN_CONFLICT_RESOLVER_20260920
layer: L0
triggers:
  - "branche orpheline"
  - "branche supprimée"
  - "conflit git"
  - "merge conflict"
  - "dryrun causal"
inputs:
  - type: repo_root
    description: "Racine du repo git"
  - type: branch_name
    description: "Nom de la branche orpheline (optionnel)"
  - type: conflict_strategy
    description: "Stratégie de résolution: resurrection | absorption | cherry-pick | delete"
outputs:
  - type: resolution_report
    description: "Rapport de résolution (JSON/Markdown)"
  - type: action_taken
    description: "Action effectuée: resurrected | absorbed | cherry_picked | deleted | skipped"
tools:
  - git
  - yaml_parser
  - validate_designs.py
  - pre-commit
artifacts:
  - path: reports/branch-orphan-resolution-*.md
    format: markdown
  - path: reports/branch-orphan-resolution-*.json
    format: json
governance:
  adr: ADR-2026-08-28-001-BRANCH-RESURRECTION-PROTOCOL
  design: branch-orphan-conflict-resolver
  atom: ATOM-053-workspace-draft-convention
  workflow: dryrun-causal-audit
---

# Skill : Branch Orphan Conflict Resolver

## Description

Résout les branches orphelines et prévient les conflits cross-repo.
Détecte les branches orphelines via reflog, analyse la saturation de contenu,
et applique la stratégie de résolution appropriée.

## When to use

- Après détection d'une branche orpheline (supprimée, non mergée)
- Avant tout merge vers `main` (dryrun causal)
- Lorsque des conflits git sont détectés
- En fin de session KiloCode (PR_LIFECYCLE_GATE)
- Lors de l'audit de branches (BOOT-3, BOOT-3bis)

## Process

### ÉTAPE-1 — Détection

1. Exécuter `git reflog | grep -i "deleted\|pruned\|branch"`
2. Lister les branches distantes mergées dans main sans PR ouverte
3. Identifier les branches orphelines

### ÉTAPE-2 — Analyse de saturation

1. Comparer les commits uniques: `git log main..<branch> --oneline`
2. Vérifier les fichiers clés sur main: `git ls-tree -r main -- <fichier>`
3. Calculer le taux de recouvrement

### ÉTAPE-3 — Stratégie de résolution

| Saturation | Action |
|-----------|--------|
| > 80% overlap | Absorption main (drop) |
| < 20% overlap | Résurrection + merge |
| 20-80% overlap | Cherry-pick manuel |

### ÉTAPE-4 — Résolution

1. **Resurrection** : `git branch <name> <sha>` + test merge `--no-commit --no-ff`
2. **Absorption** : `git show main:<file> > <file>` + `git add <file>`
3. **Cherry-pick** : `git cherry-pick <commit_sha>` avec résolution manuelle
4. **Suppression** : `git branch -d <branch>` + `git push origin --delete <branch>`

### ÉTAPE-5 — Validation

1. Exécuter dryrun causal sur les fichiers modifiés
2. Vérifier les hooks pre-commit
3. Valider la cohérence MDU

### ÉTAPE-6 — Nettoyage

1. Supprimer la branche locale et distante
2. Mettre à jour le rapport de session
3. Logger dans VOLTX

## Anti-patterns

- Supprimer une branche sans vérifier `git reflog` d'abord
- Déclarer "perdu" sans avoir tenté la resurrection
- Merge force sans test `--no-commit --no-ff`
- Résoudre les conflits en gardant la version feature quand main a le contenu canonique
- Ignorer les branches orphelines en fin de session

## Governance

- **ADR** : ADR-2026-08-28-001-BRANCH-RESURRECTION-PROTOCOL
- **Design** : branch-orphan-conflict-resolver
- **Atom** : ATOM-053-workspace-draft-convention
- **Workflow** : dryrun-causal-audit
- **Règle** : branch-resurrection-protocol.md (KiloCode)
