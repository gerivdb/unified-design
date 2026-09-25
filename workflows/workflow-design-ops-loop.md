# Workflow — Design Ops Loop

## Contexte

Ce workflow orchestre la boucle THINK → DO → CHECK du MDU :
perception des besoins, exécution des corrections, validation du réel.

## Déclencheur

- Session boot (BOOT-1)
- Pre-push validation
- Post-merge drift check
- Manuel via `python tools/design-ops-loop.py`

## Procédure

### THINK

1. **Scan besoins** — collecter les signaux :
   - Frictions TALEX (`REPORTS/REPORT-TALEX-FRICTION-*.md`)
   - Drift MDU (`tools/mdu-lint.py --warn-only`)
   - Gaps ontologiques (`scripts/ontology_term_gate.py`)
   - Retours utilisateurs (`issues/`, `discussions/`)

2. **Classifier** — prioriser par impact/effort :
   - P0 = bloqueur métacohérence
   - P1 = amélioration structurelle
   - P2 = polish

3. **Planifier** — générer le plan d’actions atomiques :
   - 1 action = 1 commit ≤ 3 fichiers
   - Dépendances explicitées (`depends_on`)

### DO

4. **Exécuter** — implémenter chaque action atomique :
   - Respecter le contrat MDU (design, primitive, skill, citizen, workflow)
   - Valider après chaque commit (`validate_designs.py --strict`)
   - Mettre à jour `meta-design.yaml` et catalogues

5. **Traçabilité** — horodater chaque action :
   - Preuve d’exécution dans `REPORTS/`
   - Cross-références dans `design.yaml`

### CHECK

6. **Audit** — vérifier la métacohérence :
   - `python tools/mdu-lint.py --strict`
   - `python scripts/sync-mdu-catalog.py --dry-run`
   - `python scripts/validate_designs.py --strict`

7. **Rapport** — générer `reports/design-ops-loop-<timestamp>.json` :
   ```json
   {
     "think": {"frictions": 0, "gaps": 0, "priorities": []},
     "do": {"actions": 0, "commits": 0, "files": 0},
     "check": {"drift": 0, "violations": 0, "status": "PASS"}
   }
   ```

8. **Closeout** — si `PASS` :
   - Mettre à jour les indexes PRD/MOC
   - Promouvoir les atoms en `active`
   - Archiver le rapport

## Sortie

- `reports/design-ops-loop-<timestamp>.json`
- Exit 0 = PASS, Exit 1 = FAIL

## Références

- **Design** : `designs/design-ops-loop/design.yaml`
- **Primitive** : `primitives/design-ops-loop-primitive.yaml`
- **Skill** : `skills/design-ops-loop-skill/SKILL.md`
- **PRD-MOC** : `PRD-MOC-DESIGN-OPS-LOOP-20260920.md`
