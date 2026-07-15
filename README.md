# Unified Design (MDU)

> **Le Gentil** — L'atlas global des invariants architecturaux de l'écosystème gerivdb

## Vision

Le **Méta-Design (MDU)** est la **constitution architecturale** de l'écosystème gerivdb. Il définit les invariants topo-logiques qui gouvernent l'interaction entre les couches, les patterns, et les agents.

## Les Quatre Piliers

| Pilier | Abbr | Rôle | Couleur |
|--------|------|------|---------|
| Sonar-Driven Design | SDD | Observabilité | #4CAF50 |
| Triadic Compound Eye | TCE | Orchestration Agents | #2196F3 |
| MorphoHDL Anamorphic Growth | MAG | Optimisation Matérielle | #9C27B0 |
| Connard Design | CD | Contrôle Qualité | #F44336 |

## Structure

```
unified-design/
├── meta-design.yaml            # Schéma de validation YAML v2
├── atoms/                      # Design atoms réutilisables
│   ├── latency-bound.yaml
│   ├── power-capped.yaml
│   ├── b243-vector.yaml        # NOUVEAU : Vecteur ternaire 3^5=243
│   └── strate-registry.yaml    # NOUVEAU : Classification strates
├── loops/                      # Patterns de boucles documentés
│   ├── virtuous-cycle.yaml
│   └── deadlock-pattern.yaml
├── loop_engine/                # Détection et simulation de boucles
│   ├── detector.py             # Module de détection de cycles
│   ├── check_loops.py          # Wrapper CLI
│   └── simulate.py             # Simulateur d'impact (Phase 3)
├── loop_engine/patterns/       # Bibliothèque de patterns
│   ├── virtuous-cycle.yaml
│   └── deadlock-pattern.yaml
├── generator/                  # Scripts d'industrialisation
│   ├── create_design.py        # Générateur de dépôt de design
│   └── validate_inheritance.py # Validateur d'héritage
├── pipelines/                  # Pipelines KIVA-CLI
│   └── mdu-validation.yaml     # Pipeline validation MDU
├── docs/                       # Documentation détaillée
├── ADR/                        # Documents décisionnels
│   └── ADR-019-phase3-incremental.md
├── README.md                   # Ce fichier
└── REPO.yaml                   # Métadonnées du repository
```

## CLI Unified Design (Phase 3)

```bash
# Créer un design avec héritage multiple
unified-design create mon-design \
  --parent GOVERNANCE-HUB \
  --parent REPO-STANDARDS \
  --capability latency-bound

# Simuler l'impact d'un design
unified-design simulate --design mon-design.yaml

# Valider complètement
unified-design validate --root L0-CANON --strict

# Visualiser le graphe
unified-design visualize --format png --output graph.png
```

## CI/CD KIVA-CLI

Le pipeline KIVA-CLI (`./pipelines/mdu-validation.yaml`) remplace GitHub Actions :

| Step | Commande | Description |
|------|----------|-------------|
| 1 | `kiva run mdu-validation` | Validation YAML complète |
| 2 | `loop_engine/check_loops.py` | Détection de boucles |
| 3 | `loop_engine/simulate.py` | Simulation d'impact |
| 4 | `generator/validate_inheritance.py` | Validation héritage |

Exécution manuelle :
```bash
# Pipeline complet
kiva run pipeline mdu-validation-pipeline

# Ou directement
python loop_engine/check_loops.py --path . --output report/loop_check.json
python loop_engine/simulate.py meta-design.yaml --output report/simulation.json
```

## Méthodologie : Créer un design hérité

### 1. Comprendre le méta-design

Lisez `meta-design.yaml` pour identifier :
- Les **capacités** disponibles dans `capabilities/`.
- Les **règles** de validation dans `design_rules/`.
- Les **boucles** connues dans `loops/`.

### 2. Générer un nouveau design

```bash
# Depuis la racine du repo unified-design
python generator/create_design.py mon-nouveau-design \
  --parent GOVERNANCE-HUB \
  --capability latency-bound \
  --capability power-capped
```

Cela génère automatiquement :
- Un fichier `design.yaml` avec les paramètres hérités
- Un fichier `REPO.yaml` avec les métadonnées du dépôt
- Un workflow CI GitHub Actions
- Un fichier `.gitignore` standard
- La structure de répertoires minimale

Options disponibles :
```
--dry-run              Affiche ce qui serait créé sans créer les fichiers
--output-dir PATH      Répertoire de sortie personnalisé
--template PATH        Chemin vers un template de dépôt à utiliser
```

### 3. Valider l'héritage et détecter les boucles

```bash
# Valider un design spécifique
python generator/validate_inheritance.py generated-designs/mon-nouveau-design/design.yaml

# Vérifier les boucles dans tout le MDU
python loop_engine/check_loops.py --path . --max-depth 5
```

Le validateur vérifie :
- L'**acyclicité** du graphe d'héritage.
- L'**absence de conflits** entre capacités (ex: `latency-bound <= 1ms` + `power-capped <= 1W`).

### 4. Déployer

Une fois validé, le `design.yaml` peut être déployé dans un nouveau dépôt ou intégré à un existant.

## Industrialisation du générateur

Le générateur `create_design.py` crée un dépôt de design complet avec :

| Élément | Description |
|---------|-------------|
| `design.yaml` | Définition du design avec héritage et capacités |
| `REPO.yaml` | Métadonnées du dépôt (path, parent, statut) |
| `.github/workflows/ci.yml` | Workflow CI de validation |
| `.gitignore` | Fichier de ignore standard |
| Structure | `atoms/`, `loops/`, `ADR/`, `docs/` |

## Validation

```bash
# Valider le meta-design
python loop_engine/check_loops.py --path .

# Valider l'héritage d'un design
python generator/validate_inheritance.py <design.yaml>
```

## Fichiers

| Fichier | Description |
|---------|-------------|
| `docs/META-DESIGN.md` | Atlas des invariants architecturaux |
| `meta-design.yaml` | Schéma de validation YAML v2 (capacités, boucles, industrialisation) |
| `atoms/*.yaml` | Design atoms réutilisables |
| `loops/*.yaml` | Patterns de boucles documentés |
| `generator/*.py` | Scripts de génération et de validation |
| `REPO.yaml` | Métadonnées du repository |
| `citizens.yaml` | Déclaration des concepts (RSS-v2) |
| `ONTOLOGY_DECLARATION.yaml` | Déclaration ontologique (RSS-v2.3) |

## Concepts clés

### Design Atoms

Les plus petites unités de design réutilisables. Exemples :
- `latency-bound` — impose une limite de latence.
- `power-capped` — impose une limite de puissance.

### Loop Engineering

Le méta-design peut analyser le graphe de dépendances et identifier les boucles de design :
- **Vertueuses** — autorégulation, documentées dans `loops/virtuous-cycle.yaml`.
- **Vicieuses** — incohérence, documentées dans `loops/deadlock-pattern.yaml`.

### Incrémentalité

Un design incrémental est un design qui peut être étendu sans redéfinir l'existant, uniquement par ajout de contraintes ou spécialisation de paramètres. Le score d'incrémentalité cible est > 80 %.

## Références

- **ADR** : [ADR-013 — Meta-Design Validation Protocol](https://github.com/gerivdb/GOVERNANCE-HUB/blob/main/ADR/ADR-013-meta-design-validation-protocol.md)
- **ADR** : [ADR-015 — Unified Design v2](https://github.com/gerivdb/GOVERNANCE-HUB/blob/main/ADR/ADR-015-unified-design-v2.md)
- ADR-2026-06-28-001 : Logical Architecture N1-N4
- ADR-CONNARD-001 : Connard Design Protocol
- RSS-v2 : Repo Structure Standard

## License

MIT
