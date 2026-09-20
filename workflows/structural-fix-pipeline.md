# Workflow — Structural Fix Pipeline

**IntentHash** : `0xWORKFLOW_STRUCTURAL_FIX_PIPELINE_20260920`
**Pipeline** : `pipeline-friction-analysis-to-fix`
**Skill** : `ecosystem-meta-coherence-analyzer`

---

## Déclencheur

Après détection de frictions de session via TALEX.

## Étapes

### ÉTAPE-1 — Détection
Détecter les frictions de session via TALEX.
### ÉTAPE-2 — Classification

Classer les frictions par sévérité (critical/high/medium/low/structural).

### ÉTAPE-2bis — Detection patterns JEVX

Si la friction concerne JEVX :
1. Vérifier `designs/jevx-backend-matrix.yaml` pour la compatibilité backend
2. Vérifier `designs/jevx-engineering.yaml` pour les patterns disponibles
3. Vérifier `primitives/constrained-parallel-decoding` et `primitives/sovereign-adapter-pattern`
4. Appliquer le pattern approprié si la friction est de type :
   - Backend incompatible → utiliser `constrained-parallel-decoding`
   - Adapter WSL1 → utiliser `sovereign-adapter-pattern`
   - Sécurité décision → utiliser `decision-security-guardrail`

### ÉTAPE-3 — Priorisation

Prioriser les corrections (P1/P2/P3).
### ÉTAPE-4 — Implémentation
Implémenter les corrections via tâches atomiques SLM/ACT auto.

### ÉTAPE-5 — Validation
Valider que les corrections ont résolu les frictions.

### ÉTAPE-6 — Enregistrement
Enregistrer les preuves dans VOLTX.

## Sortie

- `reports/talex-friction-analysis-*.json` : rapport TALEX
- `reports/talex-session-friction-analysis-*.md` : rapport Markdown
- Preuves horodatées dans VOLTX

## Anti-patterns

- Analyser sans dryrun préalable
- Implémenter sans validation TALEX
- Corrections groupées (> 3 fichiers par commit)
- Oublier la traçabilité causale
