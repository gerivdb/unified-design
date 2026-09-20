---
name: mdu-integrity-checker
description: Vérifie la cohérence du MDU (meta-design.yaml, catalogues, arborescence physique). Utilise tools/mdu-lint.py et scripts/sync-mdu-catalog.py. Utiliser pour audit MDU, pre-commit check, detection doublons IDs, chemins manquants, consumers vides.
version: 1.0.0
intent_hash: 0xSKILL_MDU_INTEGRITY_CHECKER_20260921
---

# MDU Integrity Checker

Skill de vérification de la cohérence structurelle du Meta-Design Universe (MDU).

## Mission

Vérifier, avant tout push ou commit, que `meta-design.yaml`, les catalogues et l'arborescence physique sont mutuellement cohérents.

## Règles

- Unicité des IDs dans `meta-design.yaml` et `catalog/*.yaml`
- Existence des chemins référencés
- Complétude des index (`atoms.index.yaml`, `designs.index.yaml`, etc.)
- Canonicalité : pas de doublon `.yaml` racine vs `dossier/design.yaml`
- Harmonisation des `status` (`ACTIVE`, `DRAFT`, `STANDARD`, `DEPRECATED`)
- `consumers: []` non vide (traçabilité descendante)

## Utilisation

### Lint structurel

```bash
python tools/mdu-lint.py --strict
```

Exit codes :
- `0` : conforme
- `1` : erreurs critiques (doublons IDs, chemins manquants)
- `2` : avertissements (statuts non harmonisés, consumers vides)

### Sync catalogues

```bash
python scripts/sync-mdu-catalog.py --all --dry-run
python scripts/sync-mdu-catalog.py --designs
python scripts/sync-mdu-catalog.py --atoms
```

### Workflow recommandé

1. Lancer `tools/mdu-lint.py --strict` avant tout commit
2. Si échec : corriger les écarts critiques
3. Lancer `scripts/sync-mdu-catalog.py --all --dry-run` pour vérifier la sync
4. Si `--dry-run` montre des changements : lancer sans `--dry-run` pour appliquer
5. Relancer `tools/mdu-lint.py --strict` après sync

## Intégration

- **Pre-commit** : `tools/mdu-lint.py --strict` (bloque si exit 1)
- **Session boot** : `scripts/sync-mdu-catalog.py --all --dry-run`
- **Pipeline** : `pipelines/pipeline-mdu-validation.yaml`

## Dépendances

- `meta-design.yaml` (source de vérité)
- `catalog/*.yaml` (indexes)
- `designs/`, `atoms/`, `pipelines/`, `workflows/`, `primitives/`, `skills/`, `citizens/` (arborescence physique)

## Références

- PRD-MOC : `PRD-MOC-MDU-INTEGRITY-CHECKER-20260921.md`
- ADR : `ADR-2026-09-21-001-MDU-INTEGRITY-CHECKER.md`
- ADR : `ADR-2026-09-19-SAFE-ACTION-PATTERN`
