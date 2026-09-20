# Workflow MDU Daily Sync

**IntentHash** : `0xWORKFLOW_MDU_DAILY_SYNC_20260921`  
**Statut** : active  
**Date** : 2026-09-21

## Objectif

Maintenir la cohérence du MDU (meta-design.yaml, catalogues, arborescence physique) au quotidien.

## Procédure

### Étape 1 — Lint préventif

```bash
python tools/mdu-lint.py --strict
```

- Si exit 0 : continuer
- Si exit 1 : corriger les écarts critiques avant toute autre action
- Si exit 2 : avertissements non bloquants, logger et continuer

### Étape 2 — Sync dry-run

```bash
python scripts/sync-mdu-catalog.py --all --dry-run
```

- Analyser le rapport JSON
- Si `total_changed > 0` : continuer Étape 3
- Si `total_changed == 0` : nothing to do, terminer

### Étape 3 — Sync effective

```bash
python scripts/sync-mdu-catalog.py --all
```

- Vérifier les fichiers modifiés
- Committer les changements si nécessaire

### Étape 4 — Validation post-sync

```bash
python tools/mdu-lint.py --strict
```

- Si exit 0 : sync validée
- Si exit 1 : rollback + investiguer

## Intégration

- **Session boot** : exécuter Étape 1 + Étape 2 automatiquement
- **Pre-push** : exécuter Étape 1 obligatoirement
- **Pre-commit** : exécuter `tools/mdu-lint.py --strict`

## Références

- `PRD-MOC-MDU-DAILY-SYNC-20260921.md`
- `MOC-MDU-DAILY-SYNC-20260921.md`
- `ADR-2026-09-21-010-MDU-DAILY-SYNC.md`
