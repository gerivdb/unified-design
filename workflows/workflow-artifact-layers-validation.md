# Workflow — Artifact Layers Validation

## Contexte

Ce workflow valide que chaque repo gerivdb respecte la structure causale standardisée en 7 layers :
`src/`, `config/`, `tools/`, `scripts/`, `tests/`, `docs/`, `markdown/`.

## Déclencheur

- Pre-push
- Pre-commit
- Manuel via `python tools/mdu-lint.py --strict`

## Procédure

1. **Scan repos** — pour chaque repo listé dans `known_repositories.yaml` :
   - Vérifier la présence des 7 dossiers obligatoires
   - Détecter les dossiers parasites hors layers

2. **Validation** — pour chaque layer manquant :
   - Signaler en erreur si `STRICT=true`
   - Signaler en warning si `STRICT=false`

3. **Rapport** — générer `reports/artifact-layers-<timestamp>.json` :
   ```json
   {
     "repo": "gerivdb/unified-design",
     "layers_present": ["src", "config", "tools", "scripts", "tests", "docs", "markdown"],
     "layers_missing": [],
     "parasitic_dirs": [],
     "status": "PASS"
   }
   ```

4. **Correctif** — si `AUTO_FIX=true` :
   - Créer les dossiers manquants
   - Déplacer les dossiers parasites vers `markdown/` ou `tools/` selon leur nature

5. **Historique** — archiver le rapport dans `reports/artifact-layers/`

## Sortie

- `reports/artifact-layers-<timestamp>.json`
- Exit 0 = PASS, Exit 1 = FAIL

## Références

- **Design** : `designs/artifact-layers-design/design.yaml`
- **Primitive** : `primitives/artifact-layers-primitive.yaml`
- **Skill** : `skills/artifact-layers-validator/SKILL.md`
- **PRD-MOC** : `PRD-MOC-ARTIFACT-LAYERS-20260920.md`
