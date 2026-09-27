# Workflow — TALEX Friction Analysis

## Contexte

Ce workflow orchestre l'analyse des frictions TALEX et la génération de correctifs structurés.

## Déclencheur

- Fin de session multi-repo
- Après tout incident/erreur système
- Manuel via `python tools/talex_friction_analyzer.py`

## Procédure

### Phase 1 — Collecte

1. Scanner `REPORTS/REPORT-TALEX-FRICTION-*.md`
2. Extraire les frictions par tableau
3. Agréger par type d'erreur

### Phase 2 — Classification

1. Classifier chaque friction :
   - P0 = bloquant métacohérence
   - P1 = amélioration structurelle
   - P2 = polish
2. Prioriser par impact/effort

### Phase 3 — Analyse causale

1. Pour chaque friction P0/P1 :
   - Identifier la cause racine
   - Déduire l'action corrective atomique
   - Évaluer l'impact de la correction

### Phase 4 — Génération de correctifs

1. Créer les artefacts manquants (design, primitive, atom, skill, workflow, script)
2. Mettre à jour `meta-design.yaml` et catalogues
3. Générer le rapport `REPORTS/REPORT-TALEX-FRICTION-ANALYSIS-<timestamp>.md`

### Phase 5 — Vérification

1. `python tools/talex_friction_analyzer.py --strict`
2. `python scripts/validate_designs.py --strict`
3. Pre-commit hooks passent

### Phase 6 — Closeout

1. Mettre à jour les indexes PRD/MOC
2. Archiver le rapport
3. Commit atomique

## Sortie

- `REPORTS/REPORT-TALEX-FRICTION-ANALYSIS-<timestamp>.md`
- Actions correctives par lot atomique

## Références

- **Design** : `designs/talex-friction-analyzer/design.yaml`
- **Primitive** : `primitives/talex-friction-analyzer-primitive.yaml`
- **Atom** : `atoms/ATOM-TALEX-FRICTION-ANALYZER.md`
- **Skill** : `skills/talex-friction-analyzer/SKILL.md`
- **Outil** : `tools/talex_friction_analyzer.py`
