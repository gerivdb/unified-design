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
│   └── power-capped.yaml
├── loops/                      # Patterns de boucles documentés
│   ├── virtuous-cycle.yaml
│   └── deadlock-pattern.yaml
├── generator/                  # Scripts d'industrialisation
│   ├── create_design.py
│   └── validate_inheritance.py
├── docs/                       # Documentation détaillée
├── README.md                   # Ce fichier
└── REPO.yaml                   # Métadonnées du repository
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
  --parent morphohdl-anamorphic-growth \
  --capability latency-bound \
  --capability power-capped
```

Cela génère un fichier `generated-designs/mon-nouveau-design/design.yaml` contenant :
- Les paramètres hérités du parent.
- Les capacités sélectionnées avec leurs paramètres par défaut.
- Une checklist des boucles potentielles à vérifier.

### 3. Valider l'héritage et détecter les boucles

```bash
python generator/validate_inheritance.py generated-designs/mon-nouveau-design/design.yaml
```

Le validateur vérifie :
- L'**acyclicité** du graphe d'héritage.
- L'**absence de conflits** entre capacités (ex: `latency-bound <= 1ms` + `power-capped <= 1W`).

### 4. Déployer

Une fois validé, le `design.yaml` peut être déployé dans un nouveau dépôt ou intégré à un existant.

## Validation

```bash
gerivdb meta validate
gerivdb connard validate
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
