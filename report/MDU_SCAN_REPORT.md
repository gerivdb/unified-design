# MDU Multi-Strate Scan Report

## Résumé

| Strate | Repos | Design Candidates | Atomes potentiels |
|--------|-------|-------------------|-------------------|
| L0-CANON | 4 | 1 (GOVERNANCE-HUB) | - |
| L1-CAUSALITY | 13 | 0 | 2 (TOPOS, ECOYSTEM) |
| L3-EMERGENCE | 28 | 8 (TINA, IRIS, CITIZENS, MIMIR, STYX, INTENT-ENCODER, racines, strix) | 2 (ARGUS, triadic-compound-eye) |
| L4-TOOLS | 45 | 2 (TQL, VERSES) | 7 (Gitnote, KALA, PIANO, REPO-STANDARDS, sonar-driven-design, triadic-compound-eye) |
| L5-ARCHIVE | 14 | 0 | 1 (RESILIENCE) |

## Atomes extraits de REPO-STANDARDS

Analyse du fichier `meta-design.yaml` de REPO-STANDARDS :

| Atome | Valeur | Source |
|-------|--------|--------|
| `latency-bound` | max_p99_ms: 45 | pipelines.design_validation |
| `power-capped` | max_power_w: 12 | constraints.thermal |
| `memory-capped` | max_ram_gb: 24, cache_ratio: 0.8 | constraints.memory |
| `thermal-capped` | max_temp_c: 70 | constraints.thermal |
| `strate-governance` | clusters avec budgets | clusters.* |
| `pipeline-validation` | design_validation pipeline | pipelines.design_validation |
| `adr-lifecycle` | adr_lifecycle pipeline | pipelines.adr_lifecycle |

## Atomes extraits de TOPOS (L1-INFRA)

Analyse des fichiers `repo-manifest.yaml` et `STRATE_REGISTRY.yaml` :

| Atome | Description | Source |
|-------|-------------|--------|
| `b243-vector` | Vecteur ternaire 3^5=243 dimensions | repo-manifest.yaml |
| `strate-registry` | Classification L0-L5 des dépôts | STRATE_REGISTRY.yaml |
| `topology-sot` | Source of truth des dépendances | repo-manifest.yaml |
| `citizen-registry` | Registre des citoyens (agents) | repo-manifest.yaml |
| `swarm-config` | Configuration swarm | repo-manifest.yaml |

## Atomes extraits de TINA (L3-CITIZENS)

| Atome | Description | Source |
|-------|-------------|--------|
| `sandbox-isolation` | Isolation NeSy via CubeSandbox | TINA |
| `formal-verification` | Preuves formelles Z3 | TINA |
| `ontology-audit` | Cohérence N/N+1/N+2 | TINA |
| `auto-correction` | Détection friction + correction | TINA |
| `citizen-routing` | Routage citoyens via CITIZENS.yaml | TINA |

## Atomes extraits de IRIS (L3-CITIZENS)

| Atome | Description | Source |
|-------|-------------|--------|
| `friction-based-governance` | Gouvernance par friction + auto-correction | IRIS |

## Atomes extraits de CITIZENS (L3-CITIZENS)

| Atome | Description | Source |
|-------|-------------|--------|
| `citizen-registry` | Registre canonique des citoyens | CITIZENS |

## Atomes extraits de MIMIR (L3-CITIZENS)

| Atome | Description | Source |
|-------|-------------|--------|
| `memory-curator` | Mémoire longue durée + IntentHash | MIMIR |

## Atomes extraits de STYX (L3-CITIZENS)

| Atome | Description | Source |
|-------|-------------|--------|
| `hitl-expulsion-governance` | Gouvernance HITL pour verdicts d'expulsion irréversibles | STYX |

## Atomes extraits de INTENT-ENCODER/racines/strix (L3-CITIZENS)

| Atome | Description | Source |
|-------|-------------|--------|
| `friction-governance` | Pattern générique de gouvernance par friction + auto-correction | INTENT-ENCODER, racines, strix |

## Atomes extraits de TQL (L4-TOOLS)

| Atome | Description | Source |
|-------|-------------|--------|
| `ternary-query` | Langage requête fractal Think-Do-Check | TQL |
| `fractal-recursion` | Récursion auto-similaire | TQL |
| `think-do-check` | 9 phases cognitives | TQL |

## Atomes extraits de VERSES (L4-TOOLS)

| Atome | Description | Source |
|-------|-------------|--------|
| `verses-generation` | Génération contrainte de vers | VERSES |

## Nouveaux design.yaml créés

Les `design.yaml` suivants ont été créés pour ancrer les dépôts dans le MDU :

1. **TINA** (`D:\DO\WEB\TOOLS\L3-CITIZENS\TINA\design.yaml`) — 5 atomes hérités
2. **IRIS** (`D:\DO\WEB\TOOLS\L3-CITIZENS\IRIS\design.yaml`) — 3 atomes hérités
3. **CITIZENS** (`D:\DO\WEB\TOOLS\L3-CITIZENS\CITIZENS\design.yaml`) — 2 atomes hérités
4. **MIMIR** (`D:\DO\WEB\TOOLS\L3-CITIZENS\MIMIR\design.yaml`) — 2 atomes hérités
5. **STYX** (`D:\DO\WEB\TOOLS\L3-CITIZENS\STYX\design.yaml`) — 2 atomes hérités
6. **INTENT-ENCODER** (`D:\DO\WEB\TOOLS\L3-CITIZENS\INTENT-ENCODER\design.yaml`) — 2 atomes hérités
7. **racines** (`D:\DO\WEB\TOOLS\L3-CITIZENS\racines\design.yaml`) — 2 atomes hérités
8. **strix** (`D:\DO\WEB\TOOLS\L3-CITIZENS\strix\design.yaml`) — 2 atomes hérités
9. **TQL** (`D:\DO\WEB\TOOLS\L4-TOOLS\TQL\design.yaml`) — 3 atomes hérités
10. **VERSES** (`D:\DO\WEB\TOOLS\L4-TOOLS\VERSES\design.yaml`) — 1 atome hérité

## Dépôts analysés

### REPO-STANDARDS (L4-TOOLS)
- **design.yaml** : Non présent
- **REPO.yaml** : Présent - crosslink vers unified-design
- **ONTOLOGY_DECLARATION.yaml** : Présent - concepts MDU
- **meta-design.yaml** : Présent - schéma exécutable MDU

### TOPOS (L1-INFRA)
- **repo-manifest.yaml** : Présent - manifeste canonique
- **STRATE_REGISTRY.yaml** : Présent - registre strates
- **CITIZENS.yaml** : Présent - registre agents
- **SWARM.yaml** : Présent - configuration swarm

## Fichiers générés / modifiés

- `report/loop_check.json` - Résultats de la détection de boucles
- `report/scan_l1.json` - Scan de la strate L1
- `report/scan_l3.json` - Scan de la strate L3
- `report/scan_l4.json` - Scan de la strate L4
- `report/scan_l5.json` - Scan de la strate L5
- `atoms/b243-vector.yaml` - Atome ternaire
- `atoms/strate-registry.yaml` - Classification des strates
- `atoms/friction-based-governance.yaml` - Gouvernance par friction (IRIS/TINA)
- `atoms/friction-governance.yaml` - Pattern friction générique
- `atoms/hitl-expulsion-governance.yaml` - Gouvernance HITL expulsion (STYX)
- `atoms/memory-curator.yaml` - Mémoire longue durée (MIMIR)
- `atoms/citizen-registry.yaml` - Registre citoyens (CITIZENS)
- `atoms/verses-generation.yaml` - Génération de vers (VERSES)
- `generated-designs/test-multi-inherit/design.yaml` - Design test héritage multiple
- `generated-designs/test-conflict-inherit/design.yaml` - Design test conflit
- `L3-CITIZENS/TINA/design.yaml` - Design TINA
- `L3-CITIZENS/IRIS/design.yaml` - Design IRIS
- `L3-CITIZENS/CITIZENS/design.yaml` - Design CITIZENS
- `L3-CITIZENS/MIMIR/design.yaml` - Design MIMIR
- `L3-CITIZENS/STYX/design.yaml` - Design STYX
- `L3-CITIZENS/INTENT-ENCODER/design.yaml` - Design INTENT-ENCODER
- `L3-CITIZENS/racines/design.yaml` - Design racines
- `L3-CITIZENS/strix/design.yaml` - Design strix
- `L4-TOOLS/TQL/design.yaml` - Design TQL
- `L4-TOOLS/VERSES/design.yaml` - Design VERSES