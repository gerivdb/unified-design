# Skill — TALEX Friction Analyzer

## Description

Skill d'analyse des frictions TALEX pour détecter, classifier et résoudre les erreurs système de manière causale et automatisée.

## Déclencheur

- Fin de session multi-repo
- Après tout incident/erreur système
- Lorsque le PRD/MOC demande une analyse TALEX

## Procédure

### 1. Collecte

- Scanner `REPORTS/REPORT-TALEX-FRICTION-*.md`
- Extraire les tableaux de frictions (#, Erreur, Fréquence, Impact, Cause racine)
- Agréger par type d'erreur

### 2. Classification

- **P0** : Bloquant métacohérence
- **P1** : Amélioration structurelle
- **P2** : Polish

### 3. Analyse causale

- Pour chaque friction P0/P1 :
  - Identifier la cause racine
  - Déduire l'action corrective atomique
  - Évaluer l'impact de la correction

### 4. Génération de correctifs

- Créer les artefacts manquants (design, primitive, atom, skill, workflow, script)
- Mettre à jour `meta-design.yaml` et catalogues
- Générer le rapport `REPORTS/REPORT-TALEX-FRICTION-ANALYSIS-<timestamp>.md`

### 5. Vérification

- `python tools/talex_friction_analyzer.py --strict`
- `python scripts/validate_designs.py --strict`
- Pre-commit hooks passent

## Sortie

- `REPORTS/REPORT-TALEX-FRICTION-ANALYSIS-<timestamp>.md`
- Actions correctives par lot atomique

## Références

- **Design** : `designs/talex-friction-analyzer/design.yaml`
- **Primitive** : `primitives/talex-friction-analyzer-primitive.yaml`
- **Atom** : `atoms/ATOM-TALEX-FRICTION-ANALYZER.md`
- **Workflow** : `workflows/workflow-talex-friction-analysis.md`
- **Outil** : `tools/talex_friction_analyzer.py`
