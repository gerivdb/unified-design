# META-DESIGN.md - Meta-Design Atlas v2.1.0

> **Version** : 2.1.0 | **Date** : 2026-07-15 | **Statut** : ACTIF

---

## Table des matieres

1. [Vue d'ensemble](#vue-densemble)
2. [Architecture des piliers](#architecture-des-piliers)
3. [Validation](#validation)
4. [Atoms catalogues](#atoms-catalogues)
5. [References](#references)

---

## Vue d'ensemble

Le **Meta-Design (MDU)** est l'atlas des invariants architecturaux de l'ecosysteme gerivdb. Il definit :

- Les **piliers** de conception (SDD, TCE, MAG, CD)
- Les **regles transversales** de validation
- Les **atoms** reutilisables (patterns fondamentaux)
- Le **protocole de validation** via le CLI `gerivdb design validate`

---

## Architecture des piliers

### Sonar-Driven Design (SDD)

**Role** : Observabilite

| Invariant | Description | Limite |
|-----------|-------------|--------|
| Ping/Echo | Message minimal avec ID unique + timestamp | - |
| Sonar Map | Structure partagee d'etat temps reel | - |
| PRF | Pulse Repetition Frequency | - |
| Latence P99 | Temps de reponse 99e centile | <= 45ms |
| Puissance | Consommation energetique | <= 12W |

### Triadic Compound Eye (TCE)

**Role** : Orchestration Agents

| Invariant | Description |
|-----------|-------------|
| Triade C-E-Obs | Communication -> Execution -> Observation |
| Swarm Intelligence | Agents autonomes evolutifs |
| HITL Gate | Validation humaine pour modifications critiques |

### MorphoHDL Anamorphic Growth (MAG)

**Role** : Optimisation Materielle

| Invariant | Description |
|-----------|-------------|
| Croissance Experimentale | Circuits adaptatifs |
| Base 243 | Structure ternaire native 35 |
| RVBA | Canaux de couleur semantique |
| O(1) Index | Acces constant via index ternaire |

### Connard Design (CD)

**Role** : Controle Qualite

| Invariant | Description | Limite |
|-----------|-------------|--------|
| Heritage | Profondeur d'abstraction | <= 3 niveaux |
| Latence P99 | Temps de reponse | <= 45ms |
| Puissance | Consommation | <= 12W |
| Roast Automatique | Feedback negatif constructif | - |

### .LIMBO Transit Pattern (L0-CANON)

**Role** : Transit automatique des fichiers orphelins cross-repo

| Invariant | Description |
|-----------|-------------|
| Detection | ARGUS scan identifie les orphelins (GAP/GHOST/ORPHAN) |
| Classification | Ontologie + unified-design determinent la strate/repo cible |
| Transit | Deplacement vers `.LIMBO/<strate>/<repo>/` |
| Validation | HITL confirmation avant deplacement final |
| Integration | `git mv` vers le repo cible + commit atomique |

**Structure .LIMBO** :
```
D:\DO\WEB\TOOLS\.LIMBO\
├── L0-CANON\GOVERNANCE-HUB\    ← Fichiers gouvernance
├── L1-INFRA\ARGUS\             ← Fichiers ARGUS
├── L2-PLATFORM\PLIX\           ← Fichiers PLIX
├── L4-TOOLS\PIANO\             ← Fichiers PIANO
├── temp\                       ← Artefacts temporaires (debug, optimize, etc.)
└── quarantine\                 ← Fichiers suspects a auditer
```

**Workflow ARGUS** :
1. `orphan_file_scanner.py` scanne tous les repos sous `D:\DO\WEB\TOOLS`
2. Detecte : ORPHAN_FILE, WRONG_REPO, TEMP_ARTIFACT, SOT_MISMATCH
3. Route vers `.LIMBO/<strate>/<repo>/` selon la pathologie
4. Cron `balise_limbo_cron.py` execute le transit automatique (dry-run par defaut)
5. BALISE `scan` delegue au scanner ARGUS

**Principe RSR etendu** : Un artefact = une seule localisation canonique.
Si un fichier est orphelin, il transite par `.LIMBO` avant d'etre re-affecte.

---

## Validation

### CLI Design Validate

Le CLI `gerivdb design validate` fournit une interface unifiee pour valider les fichiers `design.yaml` et leurs atomes associes.

#### Usage

```bash
# Validation rapide (pass sur warnings)
gerivdb design validate

# Validation stricte (echoue sur warnings)
gerivdb design validate --strict

# Validation d'un chemin specifique
gerivdb design validate /path/to/repo

# Sortie JSON pour CI/CD
gerivdb design validate --output json

# Combinaison
gerivdb design validate --strict --output json
```

#### Checks executes

| Check | Source | Seuil critique |
|-------|--------|----------------|
| inheritance_depth | connard-validator | > 3 niveaux |
| latency_p99 | connard-validator | > 45ms |
| power_w | connard-validator | > 12W |
| git_policy | connard-validator | violation politique |
| semantic_loops | loop_engine | deadlock_pattern |
| cognitive_complexity | connard-validator | > 15 |
| max_capabilities_per_design | connard-validator | > 8 |
| max_rules_per_atom | connard-validator | > 10 |
| max_nesting_depth | connard-validator | > 3 |

#### Sortie texte

```
OK inheritance_depth: 2 (OK)
OK latency_p99: 32ms (OK)
OK power_w: 8W (OK)
OK git_policy: OK on branch 'main'
OK semantic_loops: No cycles detected

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

### Integration CI/CD

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

## Atoms catalogues

### L0-CANON

| Atom | Type | Description | Consommateurs |
|------|------|-------------|---------------|
| constitutional-sot | Registry | Source de verite constitutionnelle | - |
| stratified-repository-registry | Registry | Registre des depots par strate | - |
| ternary-governance | Rule | Regles de gouvernance ternaire | - |
| gated-boot-sequence | Procedure | Sequence de boot avec gates | - |
| absolute-rules-enforcement | Rule | Enforcement des regles absolues | - |
| adr-prd-epics-intents | Registry | Registre ADR/PRD/EPIC/INTENT | - |

### Designs enregistres

| Design | Version | Description |
|---|---|---|
| moc-governance | 1.0.0 | MOC governance design for artifact hierarchy and session control |
| ecosystem-consciousness | 1.0.0 | Conscience écosystémique ternaire Think/Do/Check |
| methodological-bon-sens | 1.0.0 | Méthodologie quinquepartite (qui/quoi/où/quand/comment/pourquoi) |
| problem-structuring-method | 1.0.0 | Filetree problématisation : décomposition arborescente de problèmes |
| value-machine | 1.0.0 | Machine à valeur : transformation inputs -> outputs via pipeline de valeur |
| ecosystem-feedback-loop | 1.0.0 | Boucle de feedback DevTools ↔ Obsidian : technique ↔ narration |
| context-engineering | 1.0.0 | Ingénierie de contexte : fenêtres glissantes, fraîcheur, embedding |
| agent-engineering-maturity | 1.0.0 | Hiérarchie des disciplines d'ingénierie agentique 2026 (5 axes, 5 niveaux) |
| fresh-context-verifier | 1.0.0 | Fresh-Context Vérificateur : TTL, embedding drift, source integrity, cross-model agreement |
| meta-coherence | 2.0 | Principe P0 de cohérence multi-échelle et cross-repo : ARGUS détecte GAP/GHOST/DRIFT/COLLISION/ORPHAN/SHADOW/VOID/PHANTOM_PATH/UNTRACKED_MASS |
| consciousness | 3.0.0 | État subjectif premier : Think/Do/Check consciousness, MDU reflet élégant, engineering ideas integration |
| agent-observability-architecture | 1.0.0 | Observabilité agents : UModel (graphe sémantique, U-SPL), Trace Engineering (DAG causal, Event Sourcing, rejouabilité), taxonomie Log/Trajectoire/Trace, distillation multi-niveaux, triple magasin de données |
| kg-causal | 1.0.0 | Draft : graphe causal déterministe KG-CAUSAL, bloqué par ADR-KG-CAUSAL-001-20260916 proposed |
| chain-fluidity | 1.0.0 | Fluidité des chaînes Think→Do→Check : réduction des frictions, pipelines, orchestration |
| autonomy-fluidity | 1.0.0 | Fluidité d'autonomie : niveaux AXE-0, transitions A0→A3, droits d'écriture |
| conversation-aggregator | 1.0.0 | Agrégateur de conversations : Agent Manager + Buzz + sessions KiloCode |
| conversation-to-execution-bridge | 1.0.0 | Pont conversation→exécution : instructions, modèles, designs, pipelines |
| task-planning | 1.0.0 | Planification des tâches : décomposition, estimation, scheduling |
| task-chaining | 1.0.0 | Chainage des tâches : dépendances, séquences, jonctions, WAL |
| hitl-assistance | 1.0.0 | Assistance HITL : points d'escalade, décharge de dette technique |
| debt-relief | 1.0.0 | Décharge de dette technique : patterns de réduction, priorisations, métriques |
| ergonomics | 1.0.0 | Ergonomie des workflows : principes d'ergonomie, patterns d'interaction, feedback |
| operational-fluidity | 1.0.0 | Fluidité opérationnelle globale : métriques, patterns d'optimisation |
| elegance | 1.0.0 | Élégance des solutions : critères, patterns de simplicité, mesure de complexité |
| assistant-load | 1.0.0 | Charge de l'assistant : mesure, patterns de décharge, équilibre dette technique |
| kg-causal-engine | 1.0.0 | Architecture KG-CAUSAL : pipeline CLM, do-calculus, résolution conflits, flux entrants/sortants | DRAFT |
| causal-semantic-bridge | 1.0.0 | Pont KG-CAUSAL ↔ VERSES : annotation causale des concepts sémantiques | DRAFT |
| narrative-causal-fusion | 1.0.0 | Fusion VOLTX ↔ KG-CAUSAL : preuves horodatées annotées par causalité | DRAFT |
| meta-kg-engine | 1.0.0 | Méta-KG unifiée : 4 engines (KG-L, VOLTX, KG-CAUSAL, VERSES), ingestion/production/cycles | DRAFT |
| kg-causal-integration-pattern | 1.0.0 | Pattern d'intégration KG-CAUSAL → KG-L (similaire ATOM-056 ARGUS→KG-L) |
| umodel-agent-ready-data | 1.0.0 | Modèle de données unifié Alibaba UModel : 4 piliers Agent-Ready, graphe sémantique, U-SPL, MCP |
| reasoningbank-persistent-strategy | 1.0.0 | Banque de Raisonnement : distillation de traces en stratégies, compression multi-niveaux, réinjection prompts |
| deepmind-co-scientist-reliability | 1.0.0 | Fiabilité agents DeepMind Co-Scientist : vérification déterministe, fabrication 4%, 0.0% fabrication complète |
| agent-swarm-self-improving-loop | 1.0.0 | Architecture agentique auto-améliorante : loop auto-arrêtante, graphe mémoire, correction accumulée, Agent Swarm 300/4000, SKILL.md versionné |
| harness-engineering-reliable-agents | 1.0.0 | Harness Engineering : 6 couches (Contract Validator, Context Compiler, Policy Engine, State Manager, Verification Engine, Trace Recorder) ; modèle probabiliste -> exécutant déterministe |

### Atoms L0-L3 (extraits)

| Atom | Type | Description |
|---|---|---|
| ATOM-065-co-abductive-halo | Atom | Interface Co-abductive HALO (L3 - Emergence) Observation -> DIVERGE -> LEAP -> CONVERGE |

### TDC Consciousness Atoms (nouveaux)

| Atom | Type | Description |
|---|---|---|
| ATOM-THINK-DO-CHECK-CONSCIOUSNESS | Atom | Conscience ternaire Think/Do/Check de l'écosystème gerivdb |
| ATOM-METHODOLOGICAL-BON-SENS | Atom | Méthodologie quinquepartite (qui/quoi/où/quand/comment/pourquoi) |
| ATOM-EXTERNAL-VERIFICATION-MANDATORY | Atom | "L'agent ne se relit pas" : vérification externe obligatoire |
| ATOM-GATE-LAYERS | Atom | Barrière de contrôle à 4 couches (L1 technique, L2 architecture, L3 gouvernance, L4 humain) |
| ATOM-INDEPENDENT-SOURCES-RULE | Atom | 2 sources indépendantes requises pour décision critique |
| ATOM-CONFIDENCE-THRESHOLD | Atom | Seuil de confiance 0.6 minimum pour décision/validation |
| ATOM-STOP-CONDITION | Atom | Loop Engineering : condition d'arrêt explicite pour toute boucle |
| ATOM-CARRY-FORWARD-PRINCIPLE | Atom | Carry Forward : travail valide reporté, rejet documenté |
| ATOM-REJECT-WORK-PRINCIPLE | Atom | Reject Work : rejet préférable à accommodation |
| ATOM-DELTA-CHECK | Atom | Delta Check : écart entre attendu et réel |
| ATOM-META-EDIT-LOOP | Atom | Méta-boucle d'édition : vérification après chaque modification |
| ATOM-LEARNING-CURVE-EXPECTATION | Atom | Courbe d'apprentissage : évaluation avant adoption |
| ATOM-DEPLOYMENT-PATTERNS | Atom | Patterns de déploiement : blue-green, canary, rolling, immuable |
| ATOM-KG-CAUSAL-CONSCIOUSNESS | Atom | Conscience de KG-CAUSAL : graphe causal déterministe, draft bloqué par ADR proposed |
| ATOM-DETERMINISTIC-EXECUTION-LOG-CLIPPING | Atom | Vérification anti-hallucination par capture déterministe des logs d'exécution (inspiré de DeepMind Co-Scientist) |
| ATOM-UMODEL-AGENT-READY-DATA | Atom | Modèle de données unifié UModel Alibaba : 4 piliers Agent-Ready, graphe sémantique, U-SPL, MCP |
| ATOM-REASONINGBANK-PERSISTENT-STRATEGY | Atom | Banque de Raisonnement : distillation de traces en stratégies, compression multi-niveaux, réinjection prompts |
| ATOM-DEEP-MIND-CO-SCIENTIST-RELIABILITY | Atom | Fiabilité agents DeepMind Co-Scientist : vérification déterministe, fabrication 4%, 0.0% fabrication complète |
| ATOM-AGENT-SWARM-SELF-IMPROVING-LOOP | Atom | Architecture agentique auto-améliorante : loop auto-arrêtante, graphe mémoire, correction accumulée, Agent Swarm 300/4000, SKILL.md versionné |
| ATOM-HARNESS-ENGINEERING-RELIABLE-AGENTS | Atom | Harness Engineering : 6 couches (Contract Validator, Context Compiler, Policy Engine, State Manager, Verification Engine, Trace Recorder) ; modèle probabiliste -> exécutant déterministe |

### L1-INFRA (nouveaux)

| Atom | Type | Description | Consommateurs |
|------|------|-------------|---------------|
| TOPOS_CITIZENS | Registry | Citoyens (agents) pour validation TOPOS | - |
| TOPOS_STRATE_REGISTRY | Registry | Registre des strates L0-L5 | - |
| TOPOS_SWARM | Config | Configuration coordination swarming | - |
| TOPOS_TOPOLOGY | Graph | Topologie des depots | - |
| GATEWAY_CONFIG | Config | Configuration principale du gateway | - |
| BDCP_CONFIG | Config | Configuration BDCP - Behind CDP | - |
| BOOT_SEQUENCE | Procedure | Sequence canonique de boot LLM | - |
| GATE_RSS_V1 | Config | Gate RSS v1 pour validation HITL | - |
| MORPHISM_MAP_SCHEMA | Schema | Schema de morphism map | - |
| LIMBO_TRANSIT | Pattern | Zone de transit normalisee pour fichiers orphelins (ARGUS -> .LIMBO) | L0 |
| MULTI_REPO_FUNDAMENTAL | Axiome | MR1-MR6 : pas de monorepo, capacite=repo, contrats explicites, atomicite per-repo | L0 |
| META_CLUSTER | Design | Cohesion N repos : SOT unique, bridges, coherence graduee, operations cluster | L0-L1 |
| UNFORESEEN_LIFECYCLE | Pattern | Imprevus signal->institution : taxonomie, recurrence R, metriques TE/TF/VE/H | L1 |
| DESIGN_COVERAGE_SCANNER | Outil | Pathologies DESIGN_* + matrice couverture + croisement incidents x designs | L1 |
| IMPENSE_REGISTER | Pattern | Boucle prospective MDU (3 lentilles) + registre R=1 trie | L1-L4 |
| THOUGHT_COMMIT_PIPELINE | Design | Continuite vibe->INTENT->MOC->subalternes->ADR/EPIC ; gates G0-G3 ; 8 cas cascade | L0 |
| RECOVERY_TOOLING | Pattern | Recovery SQLite securisee (copie travail, integrite, vacuum) | L0 |
| GGUF_PROBE_RETENTION | Pattern | Binaires lourds hors git, probes metadata, e2e kbin | L4 |
| KG35_MIGRATION | Pattern | Migration documents inter-repos avec HITL gate et SOT update | L4 |
| WAZAA_SOCIAL_BUS | Design | Bus 3 transports + reseau social des entites (realms kilo/act, presence, inbox) | L3-fct N4 |

---

## References

- **ADR-013** : Meta-Design Validation Protocol
- **ADR-016** : Unified Design Loop Detection Engine
- **ADR-CONNARD-001** : Connard Design Protocol
- **ADR-20260823** : Orphan File Classification and .LIMBO (PRD-MOC-GEN-010)
- **meta-design.yaml** : Schema de validation YAML

---

## Changements

| Version | Date | Description |
|---------|------|-------------|
| 2.1.0 | 2026-07-15 | Ajout CLI design validate, nouveaux atoms L1-INFRA |
| 2.0.0 | 2026-07-15 | Migration vers unified-design repo |
| 1.0.0 | 2026-06-29 | Version initiale |

---

---

## Références croisées

| Repo | Relation | Document |
|------|----------|----------|
| GOVERNANCE-HUB | SOT governance, known_repositories.yaml, BRIDGES.yaml, ATOM-REGISTRY | `L0-CANON/GOVERNANCE-HUB/` |
| REPO-STANDARDS | RSS-v2.3, templates, CROSSLINKS/bridges.yaml | `L4-TOOLS/REPO-STANDARDS/` |
| ONTOLOGY | Couche sémantique, bridges/, concepts | `L0-CANON/ONTOLOGY/` |
| MOX | Context forge, PRD-MOC validation, ATOM-052/053 compliance | `L2-PLATFORM/MOX/` |
| LLUX | Proof-of-concept ATOM-052/053, artifact lifecycle | `L3-CITIZENS/LLUX/` |
| NEXUS | Mega-SOT, registre des registres, N4 governance | `L1-INFRA/NEXUS/` |
| PLIX | Codec, path-registry, inference engine | `L2-PLATFORM/PLIX/` |
| ARGUS | Meta-coherence, orphan detection, .LIMBO transit, scanners | `L1-INFRA/ARGUS/` |
| WAZAA | Bus multi-transport + reseau social entites (realms, presence, inbox) | `L4-TOOLS/WAZAA/` |
| GOVERNANCE-HUB | GEN-014 STENTOR : gate moc-close -RequireOperational, ide_open, registre fenetres (design `ide-window-lifecycle`) | `L0-CANON/GOVERNANCE-HUB/scripts/balise.ps1` |
| KG-CAUSAL | Graphe causal déterministe : pipeline CLM, do-calculus, résolution conflits, intégration KG-L | `L4-TOOLS/KG-CAUSAL/` |
| VOLTX | Vault narratif : preuves horodatées, narration gouvernance, méta-KG introspection | `L4-TOOLS/VOLTX/` |
| VERSES | Couche sémantique : concepts ONTOLOGY ↔ versets, validation frontmatter, audit versets | `L0-CANON/VERSES/` |

### Crosslinks méta-KG

| Crosslink | Source | Cible | Rôle |
|-----------|--------|-------|------|
| `CROSSLINKS/talex-unified-graph.md` | unified-design | TALEX | Ingestion designs TALEX |
| `CROSSLINKS/kg-causal-unified-graph.md` | unified-design | KG-CAUSAL | Ingestion designs KG-CAUSAL (à créer) |
| `CROSSLINKS/voltx-unified-graph.md` | unified-design | VOLTX | Ingestion designs VOLTX (à créer) |
| `CROSSLINKS/verses-unified-graph.md` | unified-design | VERSES | Ingestion designs VERSES (à créer) |

### Bridges implémentés

- **unified-design -> GOVERNANCE-HUB** : ADR-013, ATOM governance
- **unified-design -> GOVERNANCE-HUB (STENTOR)** : designs/ide-window-lifecycle.yaml -> balise.ps1 (moc-close/ide-open/fanout), RUNTIME/editor_products.yaml
- **unified-design -> REPO-STANDARDS** : META-DESIGN.md macro <-> micro cohérence
- **REPO-STANDARDS -> unified-design** : CROSSLINKS/bridges.yaml, N1 logical layer
- **REPO-STANDARDS -> MOX** : PRD-MOC template, ATOM-052/053 validation
- **REPO-STANDARDS -> LLUX** : Artifact lifecycle proof-of-concept
- **ONTOLOGY -> GOVERNANCE-HUB** : bridges/governance_hub_bridge.md (à créer)
- **ONTOLOGY -> REPO-STANDARDS** : bridges/repo_standards_bridge.md (à créer)
- **ONTOLOGY -> unified-design** : bridges/unified_design_bridge.md (à créer)
- **ONTOLOGY -> MOX** : bridges/mox_bridge.md (à créer)
- **ONTOLOGY -> LLUX** : bridges/llux_bridge.md (à créer)

## Reference ADR

- **ADR** : ADR-2026-07-15-001-MDU-L1-INFRA-EXTENSION
- **IntentHash** : 0xMDU_L1_INFRA_EXT_20260715
- **Depot** : gerivdb/unified-design
- **Statut ADR** : proposed
- **Màj requise si** : statut ADR -> deprecated ou superseded
## Cas pratique - Test boucle MDU (2026-07-15)

Probleme: Concevoir le connecteur TINA-PLIX-CONNECTOR en mode equipe horizontale.

Resultat:
- Équipe generee: personae/teams/generated-tina-plix-connector.yaml
- Verses: VERSES/generated/tina-plix-connector/
- Validation: PASS
- Gain: instanciation dynamique vs equipe pre-câblee statique

---

## Application : Structure des artefacts (U-M1 -- 2026-08-23)

Le design fractal s'applique concretement a la structure des artefacts de gouvernance.
Norme operationnelle: REPO-STANDARDS/standards/artifacts/artifact-structure-standard.md (L4).

| Principe fractal | Application artefacts |
|------------------|----------------------|
| Auto-similarite | Meme patron pour PRD/, PRD-MOC/, ADR/, EPICS/, INTENTS/, SPEC/ |
| Profondeur bornee | Max 3 niveaux |
| Declaratif | Le frontmatter porte l'information de placement (type, category) |
| Auto-indexation | Index regeneres de facon idempotente (update-artifact-index.ps1) |
| Clustering | Detection seuil >= 3 en mode suggestion ; split jamais automatique |
| HITL | L'automatisation propose, l'humain valide |

### Axiome 10 -- Repository Single Responsibility (RSR) (U-M2)

Un depot declare UN role unique dans la SOT (known_repositories.yaml).
Tout artefact heberge doit correspondre au role de son depot hote.
Extension services (INTENT infra): un service = une responsabilite unique
declaree dans services.yaml (binaire, port, endpoints explicites).

DRY inter-repos: un artefact = une seule localisation canonique.
YAGNI inter-repos: pas de stockage preventif.

Lecon ADR-028: un principe sans gate mecanique n'est pas suivi d'effet.
RSR est verifie par check-prd-structure.ps1 (croisement artefacts x roles).

- inter-repo-migration
- limbo-governance
- recovery-tooling-governance
