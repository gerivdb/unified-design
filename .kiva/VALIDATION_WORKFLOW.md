# MDU Validation Workflow - KIVA-CLI Based

Ce workflow utilise **KIVA-CLI** pour la validation atomique du MDU.

## Usage avec KIVA-CLI

### Validation complète
```bash
# Depuis le répertoire unified-design
kiva validate --path . --check loops --check atoms --check inheritance

# Ou avec les scripts Python
python loop_engine/check_loops.py --path . --max-depth 5 --output report/loop_check.json
python generator/validate_inheritance.py meta-design.yaml
```

### Validation atomique par fichier
```bash
# Valider un atome
python generator/validate_inheritance.py atoms/latency-bound.yaml

# Valider un loop
python loop_engine/check_loops.py --path . --max-depth 3
```

### Génération d'un nouveau design
```bash
# Créer un design avec KIVA-CLI
python generator/create_design.py mon-nouveau-design \
  --parent GOVERNANCE-HUB \
  --capability latency-bound \
  --capability power-capped
```

## Pipeline KIVA-CLI

Le MDU suit le pattern KIVA-CLI pour les validations :

| Step | Commande | Description |
|------|----------|-------------|
| 1 | `kiva fetch` | Récupère l'état du dépôt |
| 2 | `kiva validate --check loops` | Détecte les boucles |
| 3 | `kiva validate --check atoms` | Valide les atomes YAML |
| 4 | `kiva validate --check inheritance` | Vérifie l'héritage |
| 5 | `kiva commit` | Commit atomique si OK |

## Fichiers de workflow

- `scripts/kiva-validate.py` - Wrapper KIVA-CLI pour validation
- `scripts/kiva-commit.py` - Commit atomique avec KIVA-CLI
- `scripts/kiva-merge.py` - Merge avec vérification KIVA-CLI