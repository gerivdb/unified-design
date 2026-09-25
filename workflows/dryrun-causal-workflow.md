---
name: dryrun-causal-workflow
description: "Workflow de dry-run causal pour vérifier que le graphe de dépendances d'un projet reflète l'état réel du code et des commits, pas seulement le texte des documents. Détecte les incohérences temporelles et les résout par chronologie."
version: "1.0.0"
status: active
layer: L4
type: workflow
profile: STANDARD
intent_hash: 0xWORKFLOW_DRYRUN_CAUSAL_20260922
---

# dryrun-causal-workflow

## Definition

Workflow de dry-run causal pour vérifier que le graphe de dépendances d'un projet reflète l'état réel du code et des commits.

## Steps

### 1. Filtration propre

Exclure le bruit :
- Listes de commits brutes
- Détails syntaxe PowerShell
- Timestamps, hashs
- Formules de conclusion

### 2. Extraction concepts ontologiques

Extraire les concepts du projet :
- Gouvernance
- Pipelines
- Designs
- Skills
- Citizens

### 3. Construction knowledge graph causal

Construire le graphe :
- Nœuds : concepts, designs, commits
- Arcs : dépendances, implémentations, validations

### 4. Dry-run par scénarios

Exécuter les scénarios :
- Push branche non conforme
- Commande absente du PATH
- Design/code désynchronisé
- Cross-repo fantôme

### 5. Reconciliation temporelle

Détecter les incohérences temporelles :
- Comparer les timestamps des documents
- Retenir l'état le plus récent
- Documenter la résolution

## Implementation

- Script : `scripts/run-dryrun-causal.ps1`
- Report : `reports/REPORT-<PROJECT>-DRYRUN-CAUSAL-<DATE>.md`
- Integration : CI pipeline, fin de session

## Benefits

- Garantit la cohérence projet/documents
- Détecte les incohérences temporelles
- Améliore la traçabilité décisionnelle

## IntentHash

0xWORKFLOW_DRYRUN_CAUSAL_20260922
