# ARTIFACT QUALITY GUARD - Validation automatique de la clarte des artefacts

## Objectif

Executer les probes P-101..P-109 sur tout artefact de gouvernance avant commit. 
Bloquer le commit si une probe obligatoire echoue. Logger les non-conformites dans WAL.

## Activation

Hook pre-commit : `.githooks/pre-commit`
Script : `scripts/validate_artifact_quality.py`
Schema : `schemas/artifact-quality.schema.json`

## Regles

1. P-106 et P-107 sont des **gates obligatoires** : echec = blocage du commit.
2. P-108 et P-109 sont des **warnings** : echec = commit autorise mais logged dans WAL.
3. P-101..P-105 sont des **probes de qualite** : echec = warning.
4. Toute non-conformite est tracee par NEXUS avec IntentHash.

## Processus

1. Auteur modifie un artefact.
2. Pre-commit execute `validate_artifact_quality.py`.
3. Le script valide P-101..P-109.
4. Si P-106 ou P-107 echoue -> commit bloque.
5. Si P-108 ou P-109 echoue -> warning + WAL log.
6. MOX peut reexecuter les probes en post-commit.

## References

- `PRD-MOC-N243-ARTIFACT-WRITING-STANDARDS-2026-08-05.md`
- `artifact-quality.schema.json`
- `ARTIFACT_WRITING_STANDARDS.md`
