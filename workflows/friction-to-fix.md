# Workflow — Friction to Fix

**IntentHash** : `0xWORKFLOW_FRICTION_TO_FIX_20260920`
**Pipeline** : `pipeline-friction-analysis-to-fix`
**Skill** : `ecosystem-meta-coherence-analyzer`

---

## Déclencheur

Détection d'une friction de session via TALEX.

## Étapes

### ÉTAPE-1 — Détection
Détecter les frictions via TALEX.

### ÉTAPE-2 — Classification
Classer par sévérité (critical/high/medium/low/structural).

### ÉTAPE-3 — Priorisation
Prioriser P1/P2/P3.

### ÉTAPE-4 — Implémentation
Implémenter corrections via tâches atomiques SLM/ACT auto.

### ÉTAPE-5 — Validation
Valider que les corrections ont résolu les frictions.

### ÉTAPE-6 — Enregistrement
Enregistrer les preuves dans VOLTX.

## Sortie

- Rapport TALEX
- Liste des corrections appliquées
- Preuves horodatées

## Anti-patterns

- Analyser sans dryrun préalable
- Implémenter sans validation TALEX
- Corrections groupées (> 3 fichiers par commit)
- Oublier la traçabilité causale
