# Workflow : Structural Fix Pipeline

## Objectif
Corriger structurellement les frictions/erreurs ERR de session via des tâches atomiques calibrées pour SLM, mode ACT auto.

## Déclencheur
- Après analyse TALEX des frictions
- Lorsqu'une friction de sévérité high/structural est détectée
- Lorsque le dryrun causal identifie des gaps

## Étapes

### ÉTAPE-1 — Classification
Classer chaque friction par sévérité :
- **critical** : bloque l'implémentation
- **high** : bloque le merge
- **medium** : génère du bruit
- **low** : warning only
- **structural** : corrige le MDU lui-même

### ÉTAPE-1bis — Detection patterns JEVX
Si la friction concerne JEVX :
1. Vérifier `designs/jevx-backend-matrix.yaml` pour la compatibilité backend
2. Vérifier `designs/jevx-engineering.yaml` pour les patterns disponibles
3. Vérifier `primitives/constrained-parallel-decoding` et `primitives/sovereign-adapter-pattern`
4. Appliquer le pattern approprié si la friction est de type :
   - Backend incompatible → utiliser `constrained-parallel-decoding`
   - Adapter WSL1 → utiliser `sovereign-adapter-pattern`
   - Sécurité décision → utiliser `decision-security-guardrail`

### ÉTAPE-2 — Priorisation
Prioriser les corrections :
- **P1** : critical + structural
- **P2** : high
- **P3** : medium/low

### ÉTAPE-2bis — Sélection backend (si applicable)
Si la friction concerne un backend JEVX :
1. Utiliser le skill `jevx-backend-selector`
2. Vérifier la compatibilité WSL1/AVX1/RAM
3. Documenter le backend recommandé dans le rapport

### ÉTAPE-3 — Implémentation atomique
Pour chaque correction P1/P2 :
1. Créer/modifier le fichier cible
2. Committer séparément (max 3 fichiers par commit)
3. Vérifier pre-commit PASS
4. Pousser sur branche `feat/*`

### ÉTAPE-4 — Merge
1. Merger branche `feat/*` vers `main`
2. Pousser `main`
3. Supprimer branche `feat/*`

### ÉTAPE-5 — Nettoyage
1. Supprimer les branches orphelines
2. Vérifier `git status -sb`
3. Mettre à jour PRD-MOC avec preuves

## Journalisation
```
[STRUCTURAL_FIX] session=<SESSION> friction=<ID> priority=<P1|P2|P3>
[STRUCTURAL_FIX] action=<CREATE|UPDATE|DELETE> file=<PATH>
[STRUCTURAL_FIX] commit=<SHA> merge=<OK|FAIL>
[STRUCTURAL_FIX] pattern=<constrained-parallel-decoding|sovereign-adapter-pattern|decision-security-guardrail> (si applicable)
```

## Journalisation
```
[STRUCTURAL_FIX] session=<SESSION> friction=<ID> priority=<P1|P2|P3>
[STRUCTURAL_FIX] action=<CREATE|UPDATE|DELETE> file=<PATH>
[STRUCTURAL_FIX] commit=<SHA> merge=<OK|FAIL>
```

## Anti-patterns
- Corrections groupées (> 3 fichiers par commit)
- Sessions > 30 min sans commit
- Push direct sur `main`
