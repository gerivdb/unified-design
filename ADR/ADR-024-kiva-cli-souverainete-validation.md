---
status: accepted
date: 2026-07-26
author: gerivdb
---

# ADR-024 : KIVA‑CLI comme source souveraine de validation

## Contexte
L’écosystème `gerivdb` utilise historiquement plusieurs mécanismes de validation (GitHub Actions, scripts locaux, hooks), ce qui crée une fragmentation et des divergences d’exécution. La gouvernance du méta‑design et des ATOMs nécessite un outil unique, prévisible, et exécutable localement.

## Décision
- **KIVA‑CLI est l’unique outil de validation** pour tous les dépôts de l’écosystème `gerivdb`.
- Toute validation structurante (schéma `meta-design.yaml`, registry ATOM, extractions de dépendances) **doit** être exécutée via `kiva ci run <repo>`.
- Les pipelines KIVA sont définis dans `.kiva/pipelines/<repo>.yaml` et sont la **source de vérité** pour les étapes de validation.
- **Aucun workflow CI externe (GitHub Actions, GitLab CI, Jenkins, etc.)** ne sera utilisé pour valider les artefacts de design.

## Conséquences
- Les dépôts doivent avoir un pipeline KIVA opérationnel.
- Les scripts de validation (ex: `validate_meta_design.py`, `extract_atom_deps.py`) sont appelés **uniquement** via KIVA‑CLI.
- Les hooks Git déclenchent `kiva ci run --dry-run` en local pour pré‑valider avant commit.

## Implémentation
- Créer `.kiva/pipelines/unified-design.yaml` avec les étapes :
  ```yaml
  steps:
    - name: Validate meta-design schema
      run: python scripts/validate_meta_design.py --schema schemas/meta-design.schema.json meta-design.yaml
    - name: Validate atoms registry
      run: python scripts/validate_atom_registry.py --registry atoms_registry.yaml --atoms-dir atoms
    - name: Extract atom dependencies
      run: python scripts/extract_atom_deps.py --write
  ```
- Tous les dépôts doivent avoir une structure `.kiva/pipelines/` similaire.

## Références
- `META-DESIGN.md` – section "Validation"
- `README.md` – commandes KIVA‑CLI
- `INTENT-084-atomic-commit-discipline.md` – alignement avec KIVA
