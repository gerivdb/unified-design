---
type: META-DESIGN
status: active
version: "2.1.0"
date: "2026-07-15"
intent_hash: 0xMDU_UNIFIED_DESIGN_20260715
---

# META-DESIGN — Unified Design Atlas

> **Le Gentil** — L'atlas global des invariants architecturaux de l'écosystème gerivdb

## 1. Vision

Le **Méta-Design (MDU)** est la **constitution architecturale** de l'écosystème gerivdb. Il définit les invariants topo-logiques qui gouvernent l'interaction entre les couches, les patterns, et les agents.

### Le Principe Fondamental

> **Tout système conscient doit être observable, orchestrable, optimisable, et valifiable.**

Les quatre piliers du MDU forment un ensemble fermé de propriétés invariants:

```
┌──────────────────────────────────────────────────────────────┐
│                    META-DESIGN ATLAS                         │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────┐  ┌─────────────────┐  ┌────────────┐ │
│  │   SONAR-DRIVEN  │  │ TRIADIC COMPOUND│  │ MORPHOHDL  │ │
│  │      DESIGN     │  │       EYE       │  │   GROWTH   │ │
│  │  (Observabilité)│  │   (Orchestration│  │(Optimisation│ │
│  └─────────────────┘  │      Agents)    │  │   Matérielle)│ │
│                        └─────────────────┘  └────────────┘ │
│                                   │                         │
│                                   ▼                         │
│                    ┌─────────────────────────┐              │
│                    │      CONNARD DESIGN     │              │
│                    │     (Contrôle Qualité)  │              │
│                    └─────────────────────────┘              │
│                                   │                         │
│                                   ▼                         │
│                  ┌─────────────────────────────┐            │
│                  │     CI/CD / PLIX SUITE      │            │
│                  │   (Intégration en production)            │
│                  └─────────────────────────────┘            │
└──────────────────────────────────────────────────────────────┘
```

## 2. Les Quatre Piliers

### 2.1 Sonar-Driven Design (SDD) — Observabilité

**Rôle** : Écoute active du système via émission cyclique d'impulsions (pings).

**Invariants** :
- **Ping/Echo** : Message minimal avec ID unique + timestamp → réponse avec métadonnées
- **Sonar Map** : Structure partagée cartographiant l'état du système en temps réel
- **PRF** : Pulse Repetition Frequency — fréquence d'émission des pings
- **Latence P99** : ≤ 45ms pour toute opération critique
- **Puissance** : ≤ 12W par inférence

**Agents associés** : NEXUS (push métriques), ECOYSTEM (alertes), BRAIN (bus partagé)

### 2.2 Triadic Compound Eye (TCE) — Architecture d'Agents

**Rôle** : Orchestration cognitive via architectures en triade (Mixture of Experts).

**Invariants** :
- **Triade C-E-Obs** : Communication → Exécution → Observation (cycle complet)
- **Swarm Intelligence** : Agents autonomes qui évoluent via feedback
- **Mémoire Hiérarchique** : NEXUS comme mémoire principale, HERMES comme mémoire secondaire
- **HITL Gate** : Toute modification critique passe par Human-in-the-Loop

**Agents associés** : FLUENCE (orchestration), CANDIDATOR (gestion), KRONOS (qualification), IRIS (capteurs)

### 2.3 MorphoHDL Anamorphic Growth (MAG) — Optimisation Matérielle

**Rôle** : Croissance de circuits ternaires via anamorphose adaptative.

**Invariants** :
- **Croissance Expérimentale** : Les circuits apprennent et s'adaptent
- **Base 243 (3^5)** : Structure ternaire native pour l'inférence
- **RVBA** : Répartition des canaux de couleur sémantique
- **O(1) Index** : Accès constant via index ternaire

**Agents associés** : LADYBIRD (attention), PIANO (opérateur T), KEEL (encodage)

### 2.4 Connard Design (CD) — Contrôle Qualité Exécutoire

**Rôle** : Dissipateur d'entropie qui élimine les designs qui gaspillent de l'énergie.

**Invariants** :
- **Héritage** : Profondeur ≤ 3 niveaux
- **Latence P99** : ≤ 45ms
- **Puissance** : ≤ 12W/inférence
- **Roast Automatique** : Feedback négatif constructif
- **Wall of Shame** : Liste des violations graves

**Agents associés** : CoPaw (qualité), SABRE (sécurité), Alfred (mémoire)

## 3. Règles Transversales

### 3.1 Règle de Composition

> **Un composant ne doit jamais dépendre de plus de 3 niveaux d'abstraction supérieure.**

Si la profondeur dépendance > 3 → le composant est "déchetable" → Wall of Shame.

### 3.2 Règle de Latence

> **Toute opération critique doit avoir une latence P99 ≤ 45ms.**

Si latence > 45ms → roast automatique + alerte NEXUS.

### 3.3 Règle de Puissance

> **Chaque inférence ne doit pas dépasser 12W.**

Si puissance > 12W → optimisation forcée par PIANO.

### 3.4 Règle d'Observation

> **Tout système critique doit être observable via ping/echo.**

Si système non observable → ajout de probes Sonar.

### 3.5 Règle de Validation

> **Toute modification doit passer par le validateur Connard.**

Commandes :
```bash
gerivdb connard validate <path>
gerivdb connard roast <path>
gerivdb connard watch <path>
```

## 4. Architecture de Gouvernance

```
┌─────────────────────────────────────────────────────────────────────┐
│                        L0 - CANONICAL LAYERS                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────┐   │
│  │   GOVERNANCE    │  │    ONTOLOGY     │  │      BRAIN          │   │
│  │      HUB        │  │                 │  │                     │   │
│  │ (Règles, ADR,   │  │ (Dictionnaire,  │  │ (Mémoire cognitive, │   │
│  │  Registres)     │  │  Ontologies)    │  │  MessageBus)        │   │
│  └─────────────────┘  └─────────────────┘  └─────────────────────┘   │
│                                                                       │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────┐   │
│  │   UNIFIED       │  │    CONNARD      │  │     NEXUS           │   │
│  │   DESIGN        │  │    DESIGN       │  │                     │   │
│  │ (MDU - Meta-    │  │ (Validation,    │  │ (Orchestration,     │   │
│  │  Design Atlas)  │  │  Roast, Wall)   │  │  WAL, Métriques)    │   │
│  └─────────────────┘  └─────────────────┘  └─────────────────────┘   │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

## 5. Guide Pratique — Créer un Design MDU

### Étape 1 — Vérifier l'existence d'un ADR

Avant de créer un nouveau design, vérifiez si un ADR existant couvre la décision :

```bash
# Lire le registre ADR
cat gerivdb/GOVERNANCE-HUB/ADR/ADR-*.md | grep -i "<concept>"
```

Si un ADR **accepted** existe → continuer. Si absent → créer l'ADR d'abord.

### Étape 2 — Identifier les atomes parents

Consultez le registre des atomes dans `unified-design/atoms/` :

```yaml
# Exemple : créer un design PLIX v2
inherits:
  - plix-codec      # Codec binaire ternaire
  - gpu-decoder     # Décodage GPU NVDEC
  - ternary-query   # Requête ternaire
  - b243-vector     # Vecteur base 243
```

### Étape 3 — Définir les capacités

Spécifiez les capacités avec leurs paramètres :

```yaml
capabilities:
  - name: plix-codec
    parameters:
      codecs: [mirror_lens, clusterwave, piano_runtime, verses_resolver]
      registry: schema_registry
      gpu_decode: nvdec_wrapper
      sync_pipeline: required
      mcp_server: required
      clients: [tina_client, brain_client]
```

### Étape 4 — Valider localement

Utilisez le pipeline KIVA :

```bash
# Validation du design
python unified-design/generator/validate_inheritance.py
python unified-design/loop_engine/check_loops.py
python tools/connard-validator/connard_validator.py <path>
```

### Étape 5 — Commiter et pousser

```bash
git add design.yaml
git commit -m "feat(design): add <nom> design.yaml with <atomes> inheritance"
git push origin main
```

## 6. Atomes Disponibles

### L2-PLATFORM (18 atomes)

| Nom | Description | Parents |
|-----|-------------|---------|
| `plix-codec` | Codec PLIX v2 | ternary-query, b243-vector |
| `gpu-decoder` | Décodage GPU NVDEC | — |
| `ternary-query` | Requête ternaire | — |
| `b243-vector` | Vecteur base 243 | — |
| `auto-dev-cycle` | Cycle de développement auto | — |
| `psy-citizen-governance` | Gouvernance psy-citoyenne | — |

### L3-CITIZENS (18 atomes)

| Nom | Description | Parents |
|-----|-------------|---------|
| `hitl-expulsion-governance` | Gouvernance expulsion HITL | — |
| `friction-governance` | Gouvernance par friction | — |
| `memory-curator` | Curateur de mémoire | — |
| `citizen-registry` | Registre des citoyens | — |

### L4-TOOLS (18 atomes)

| Nom | Description | Parents |
|-----|-------------|---------|
| `stratum-relay` | Relais de strate | — |
| `pattern-citizen` | Pattern citoyen | — |
| `cognitive-sot` | Cognitive SOT | — |
| `think-do-check` | Cycle penser-faire-vérifier | — |
| `fractal-recursion` | Récursion fractal | — |

## 7. Validation — Pipeline KIVA

### CI/CD Workflow

Le workflow GitHub Actions (`.github/workflows/ci.yml`) inclut :

```yaml
- name: Connard Validator
  run: python tools/connard-validator/connard_validator.py .

- name: Scan Strates
  run: python unified-design/scan_strates.py
```

### Check-list de Validation

| Check | Commande | Statut attendu |
|-------|----------|----------------|
| Pas de cycles | `check_loops.py` | 0 cycles |
| Héritage valide | `validate_inheritance.py` | No conflicts |
| Connard | `connard_validator.py` | PASS |
| Latence | Métriques P99 | ≤ 45ms |
| Puissance | Métriques | ≤ 12W |

## 8. Références ADR

| ADR | Titre | Statut |
|-----|-------|--------|
| ADR-018 | Governance Hub MDU Extraction | accepted |
| ADR-019 | Phase 3 Incremental | proposed |
| ADR-2026-06-28-001 | Logical Architecture N+1/N+4 | proposed |
| ADR-CONNARD-001 | Connard Design Protocol | proposed |
| ADR-012 | Meta-Design Validation Protocol | accepted |

## 9. Changements

| Version | Date | Description |
|---------|------|-------------|
| 2.0.0 | 2026-07-15 | Version complète — Scan L4/L5, 18 atomes, 17 designs, pipeline KIVA |
| 1.0.0 | 2026-07-15 | Version initiale — Migration depuis REPO-STANDARDS |

## 10. Exemple Concret — TINA-PLIX-CONNECTOR

Ce section documente le test workflow complet du design `TINA-PLIX-CONNECTOR`, un connecteur entre l'architecture TINA (neurosymbolique) et le codec PLIX (binaire ternaire).

### 10.1 Contexte

**Objectif** : Créer un design qui orchestre les flux de données entre l'architecture cognitive TINA et le codec binaire ternaire PLIX, en isolant les environnements d'exécution.

### 10.2 Atomes utilisés

| Atome | Rôle |
|-------|------|
| `plix-codec` | Codec binaire ternaire avec GPU decode |
| `sandbox-isolation` | Isolation des environnements via CubeSandbox |
| `citizen-routing` | Routage via CITIZENS.yaml avec fallback Kilo Agent |

### 10.3 Fichier design.yaml

```yaml
---
name: TINA-PLIX-CONNECTOR
description: Connecteur TINA ↔ PLIX - interface cognitivo-technique
version: "1.0.0"
parent: unified-design
inherits:
  - plix-codec
  - sandbox-isolation
  - citizen-routing
capabilities:
  - name: plix-codec
    parameters:
      codecs: [mirror_lens, clusterwave, piano_runtime, verses_resolver]
      registry: schema_registry
      gpu_decode: nvdec_wrapper
      sync_pipeline: required
      mcp_server: required
      clients: [tina_client, brain_client]
  - name: sandbox-isolation
    parameters:
      engine: CubeSandbox
      lifespan: ephemeral
      namespaces: [pid, mnt, net, user]
      cleanup: automatic
  - name: citizen-routing
    parameters:
      registry: CITIZENS.yaml
      fallback: Kilo Agent
      steps: [BDCP, match, execute]
stratum: L3_CITIZENS
status: active
intent_hash: 0xTINA_Plix_CONNECTOR_20260715
---
```

### 10.4 Validation exécutée

```
[OK] Inheritance check: PASS (plix-codec, sandbox-isolation, citizen-routing)
[OK] Loop check: PASS (0 cycles)
[OK] Connard validator: PASS
[OK] Push to unified-design/generated-designs/tina-plix-connector/
```

### 10.5 Résultats

- **Props** : Aucun conflit d'atomes
- **Cycles** : Aucun cycle détecté dans le graphe d'héritage
- **Push** : Design poussé avec succès vers `unified-design/generated-designs/`

Ce design sert d'exemple concret pour valider le workflow MDU complet.

## 11. Prochaines Étapes

1. **Exercer le MDU** — Créer un nouveau design concret pour tester le workflow complet (ex: orchestrateur multi-agents)
2. **Automatiser l'intégration continue** — Brancher le pipeline KIVA sur les événements de commit
3. **Ancrer les designs dans leurs dépôts** — Pousser les design.yaml dans les repos distants (TINA, IRIS, CITIZENS)