# Workflow : Dryrun Causal Audit

## Objectif
Vérifier qu'un livrable ou un ensemble de livrables est prod-ready opérationnel à 100% avant toute implémentation ou merge.

## Déclencheur
- Avant toute implémentation de design/atom/ADR
- Avant tout merge vers `main`
- Après toute session de correction structurelle

## Étapes

### ÉTAPE-1 — Présence
Vérifier que tous les fichiers attendus existent physiquement.
- Design YAML
- Atom Markdown
- ADR avec frontmatter
- META-DESIGN.md enregistrement
- meta-design.yaml enregistrement

### ÉTAPE-2 — Validité YAML
Parser chaque YAML avec `yaml.safe_load()`.
- Si erreur → STOP
- Si valide → continuer

### ÉTAPE-3 — Frontmatter
Vérifier le frontmatter de chaque document de gouvernance (INTENT, PRD-MOC, MOC, ADR).
- Champs requis présents
- Format valide

### ÉTAPE-4 — Validation MDU
Exécuter `validate_designs.py --strict` sur le design cible.
- Exit 0 → PASS
- Exit 1 → STOP

### ÉTAPE-5 — Hooks
Vérifier que les pre-commit hooks passent.
- `design-validate`
- `branch-taxonomy-check`
- `ascii-fixer`

### ÉTAPE-6 — Cross-references
Vérifier que les références croisées sont cohérentes.
- `depends_on` résolus
- `inherits` résolus
- `cross_references` valides

### ÉTAPE-7 — Merge
Vérifier que le merge sur `main` est possible.
- `git status -sb`
- `git log --oneline -3`
- `git branch`

## Sortie
 Rapport dryrun avec verdict :
- ✅ Prod-ready opérationnel 100%
- ⚠️ Warnings non bloquants
- ❌ STOP — gaps critiques

## Journalisation
```
[DRYRUN] session=<SESSION> design=<DESIGN> verdict=<PASS|WARN|STOP>
[DRYRUN] checks=<N> passed=<M> failed=<K>
```
