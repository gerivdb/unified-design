# META-DESIGN.md — Meta-Design Atlas v2.1.0

> **Version** : 2.1.0 | **Date** : 2026-07-15 | **Statut** : ACTIF

---

## Table des matières

1. [Vue d'ensemble](#vue-densemble)
2. [Architecture des piliers](#architecture-des-piliers)
3. [Validation](#validation)
4. [Atoms catalogués](#atoms-catalogués)
5. [Références](#références)

---

## Vue d'ensemble

Le **Meta-Design (MDU)** est l'atlas des invariants architecturaux de l'écosystème gerivdb. Il définit :

- Les **piliers** de conception (SDD, TCE, MAG, CD)
- Les **règles transversales** de validation
- Les **atoms** réutilisables (patterns fondamentaux)
- Le **protocole de validation** via le CLI `gerivdb design validate`

---

## Architecture des piliers

### Sonar-Driven Design (SDD)

**Rôle** : Observabilité

| Invariant | Description | Limite |
|-----------|-------------|--------|
| Ping/Echo | Message minimal avec ID unique + timestamp | - |
| Sonar Map | Structure partagée d'état temps réel | - |
| PRF | Pulse Repetition Frequency | - |
| Latence P99 | Temps de réponse 99e centile | ≤ 45ms |
| Puissance | Consommation énergétique | ≤ 12W |

### Triadic Compound Eye (TCE)

**Rôle** : Orchestration Agents

| Invariant | Description |
|-----------|-------------|
| Triade C-E-Obs | Communication → Exécution → Observation |
| Swarm Intelligence | Agents autonomes évolutifs |
| HITL Gate | Validation humaine pour modifications critiques |

### MorphoHDL Anamorphic Growth (MAG)

**Rôle** : Optimisation Matérielle

| Invariant | Description |
|-----------|-------------|
| Croissance Expérimentale | Circuits adaptatifs |
| Base 243 | Structure ternaire native 3⁵ |
| RVBA | Canaux de couleur sémantique |
| O(1) Index | Accès constant via index ternaire |

### Connard Design (CD)

**Rôle** : Contrôle Qualité

| Invariant | Description | Limite |
|-----------|-------------|--------|
| Héritage | Profondeur d'abstraction | ≤ 3 niveaux |
| Latence P99 | Temps de réponse | ≤ 45ms |
| Puissance | Consommation | ≤ 12W |
| Roast Automatique | Feedback négatif constructif | - |

---

## Validation

### CLI Design Validate

Le CLI `gerivdb design validate` fournit une interface unifiée pour valider les fichiers `design.yaml` et leurs atomes associés.

#### Usage

```bash
# Validation rapide (pass sur warnings)
gerivdb design validate

# Validation stricte (échoue sur warnings)
gerivdb design validate --strict

# Validation d'un chemin spécifique
gerivdb design validate /path/to/repo

# Sortie JSON pour CI/CD
gerivdb design validate --output json

# Combinaison
gerivdb design validate --strict --output json
```

#### Checks exécutés

| Check | Source | Seuil critique |
|-------|--------|----------------|
| inheritance_depth | connard-validator | > 3 niveaux |
| latency_p99 | connard-validator | > 45ms |
| power_w | connard-validator | > 12W |
| git_policy | connard-validator | violation politique |
| semantic_loops | loop_engine | deadlock_pattern |

#### Sortie texte

```
✓ inheritance_depth: 2 (OK)
✓ latency_p99: 32ms (OK)
✓ power_w: 8W (OK)
✓ git_policy: OK on branch 'main'
✓ semantic_loops: No cycles detected

[PASS] Design validation passed
```

#### Sortie JSON

```json
{
  "path": "/path/to/repo",
  "checks": [
    {"name": "inheritance_depth", "passed": true, "value": 2},
    {"name": "latency_p99", "passed": true, "value": 32},
    {"name": "power_w", "passed": true, "value": 8},
    {"name": "git_policy", "passed": true, "value": "OK"},
    {"name": "semantic_loops", "passed": true, "cycles": 0}
  ],
  "passed": true
}
```

### Intégration CI/CD

#### GitHub Actions

```yaml
- name: Validate Design
  run: |
    python -m tools.connard-validator.gerivdb_design_validate \
      --output json --strict
```

#### Pre-commit Hook

```yaml
- repo: local
  hooks:
    - id: design-validate
      name: Validate design.yaml
      entry: python -m tools.connard-validator.gerivdb_design_validate
      language: python
      pass_filenames: false
```

---

## Atoms catalogués

### L0-CANON

| Atom | Type | Description |
|------|------|-------------|
| constitutional-sot | Registry | Source de vérité constitutionnelle |
| stratified-repository-registry | Registry | Registre des dépôts par strate |
| ternary-governance | Rule | Règles de gouvernance ternaire |
| gated-boot-sequence | Procedure | Séquence de boot avec gates |
| absolute-rules-enforcement | Rule | Enforcement des règles absolues |
| adr-prd-epics-intents | Registry | Registre ADR/PRD/EPIC/INTENT |

### L1-INFRA (nouveaux)

| Atom | Type | Description |
|------|------|-------------|
| TOPOS_CITIZENS | Registry | Citoyens (agents) pour validation TOPOS |
| TOPOS_STRATE_REGISTRY | Registry | Registre des strates L0-L5 |
| TOPOS_SWARM | Config | Configuration coordination swarming |
| TOPOS_TOPOLOGY | Graph | Topologie des dépôts |
| GATEWAY_CONFIG | Config | Configuration principale du gateway |
| BDCP_CONFIG | Config | Configuration BDCP - Behind CDP |
| BOOT_SEQUENCE | Procedure | Séquence canonique de boot LLM |
| GATE_RSS_V1 | Config | Gate RSS v1 pour validation HITL |
| MORPHISM_MAP_SCHEMA | Schema | Schéma de morphism map |

---

## Références

- **ADR-013** : Meta-Design Validation Protocol
- **ADR-016** : Unified Design Loop Detection Engine
- **ADR-CONNARD-001** : Connard Design Protocol
- **meta-design.yaml** : Schéma de validation YAML

---

## Changements

| Version | Date | Description |
|---------|------|-------------|
| 2.1.0 | 2026-07-15 | Ajout CLI design validate, nouveaux atoms L1-INFRA |
| 2.0.0 | 2026-07-15 | Migration vers unified-design repo |
| 1.0.0 | 2026-06-29 | Version initiale |

---

## Référence ADR

- **ADR** : ADR-2026-07-15-001-MDU-L1-INFRA-EXTENSION
- **IntentHash** : 0xMDU_L1_INFRA_EXT_20260715
- **Dépôt** : gerivdb/unified-design
- **Statut ADR** : proposed
- **Màj requise si** : statut ADR → deprecated ou superseded
## Cas pratique — Test boucle MDU (2026-07-15)

Problème: Concevoir le connecteur TINA-PLIX-CONNECTOR en mode équipe horizontale.

Résultat:
- Équipe générée: personae/teams/generated-tina-plix-connector.yaml
- Verses: VERSES/generated/tina-plix-connector/
- Validation: PASS
- Gain: instanciation dynamique vs équipe pré-câblée statique
