---
intent_hash: 0xINTENT_REPO_RELATIONS_CARTOGRAPHY_V1
status: proposed
priority: P1
---

# INTENT — Cartographie et modélisation des relations inter-dépôts de l'écosystème gerivdb

> **Contexte** : `unified-design` dispose des atomes pour modéliser les relations entre repos (`cross-repo-flow`, `structural-relations`, `sync-orchestrator`, `registry-sync`, `multi-repo-audit`, `registry-consistency-sentinel`), mais il n'existe **aucune cartographie appliquée** de l'écosystème réel (~119 repos dans `known_repositories.yaml`). Cet intent propose de combler ce gap en créant un registre de relations inter-dépôts exhaustif, maintenu et validé.

---

## 1. Contexte & Motivation

### 1.1 État observé

- `unified-design` définit **comment** modéliser les relations inter-dépôts via 6 atomes dédiés.
- `known_repositories.yaml` recense **119 repos** réels, répartis sur 11 strates/couches.
- Aucun fichier de `unified-design` n'applique ces atomes à l'ensemble des repos pour produire une cartographie exploitable.
- L'ATOM-042 mentionne *“225 repos”* alors que la SOT en contient 119 : le chiffre est obsolète ou anticipé, créant un risque de décision sur des données inventées.

### 1.2 Problématique

Sans cartographie formelle :
- Les dépendances implicites entre repos ne sont pas détectables automatiquement.
- Les cycles (`PRIMUS -> CTULU -> PRIMUS`) ne peuvent être prévenus que réactivement.
- Les drift cross-repo (désynchronisation de `known_repositories.yaml` vs `TOPOS/registry/repos.json`) restent des incidents au lieu d'être des alerts.
- L'impact d'une modification dans un repo N+1 sur les repos N+2/N+3/N+4 reste manuel.
- Les 12 repos structurants (SOT, memory_role, rôle canonique) ne sont pas distingués des repos ordinaires, empêchant toute priorisation de gouvernance.

### 1.3 Repos structurants cibles

Les repos suivants sont identifiés comme **structurants** (`memory_role`, rôle SOT/canonique, ou `ternary_role` gouvernance) et doivent être traités en priorité dans la cartographie :

| Repo | Layer | memory_role | Rôle structurant |
|---|---|---|---|
| GOVERNANCE-HUB | L0_CANON | governance | SOT execution, registres, règles |
| NEXUS | L0_CANON | — | Mega-SOT, registre des registres |
| ONTOLOGY | L0_CANON | ontology | SOT sémantique, dictionnaire |
| unified-design | L0_CANON | meta_design | Atlas invariants architecturaux |
| HERMES | L0_CONSTITUTIONAL | orchestrator | SOT mémoire hiérarchique |
| VOLTX | L0_CANON | conversational_memory | Vault Orchestrator Root |
| BRAIN | L0_CANON | cognitive_memory | Couche IA, agents cognitifs |
| TOPOS | L1b_INFRA | topology | Registre canonique ENV |
| N243 | L4_TOOLS | memory_gate | Méta-orchestrateur ternaire |
| WAZAA | L3_CITIZENS | event_bus | Event bus |
| VERSES | L4-TOOLS | ontological_memory | Ontologie / VERSES sync |
| INFX | L4-TOOLS | toroidal_interface | Interface toroïdale |
| TIMX | L2_PLATFORM | — | TIMeline Event eXtractor / Feature Store |

**Règle** : ces 13 repos doivent avoir **tous leurs flux documentés** dans `repo-relations/` avant tout autre repo de leur strate respective.

### 1.4 ARGUS — statut SOT et intégration

`ARGUS` existe localement (`D:\DO\WEB\TOOLS\L1-INFRA\ARGUS\`) et sur GitHub (`gerivdb/ARGUS`). C'est un repo **actif** (3 commits récents, remote `origin` configuré), mais il **n'est pas dans `known_repositories.yaml`**.

ARGUS est déclaré **indispensable** à l'écosystème car :
- Il est le `scanner` de référence pour détecter les gaps, ghosts, orphans et drifts cross-repo.
- Il est référencé dans de nombreux atomes MDU (`ATOM-054`, `ATOM-055`, `ATOM-056`, `registry-consistency-sentinel`, `multi-repo-audit`).
- Il est le moteur de `BOOT-5bis` (cohérence registre tripartite) et `selina_sync.py`.
- Il possède son propre `atoms_registry.yaml` et `SKILL.md`, démontrant sa maturité.

**Décision** : ARGUS est ajouté à la SOT avec les attributs suivants :
- `layer: L1_CAUSALITY`
- `status: ACTIVE`
- `entity_type: REPO`
- `role: Scanner/gap detector — détection GAP/GHOST/ORPHAN/DRIFT/COLLISION cross-repo`
- `memory_role: ecosystem_scanner`
- `local_path: D:\DO\WEB\TOOLS\L1-INFRA\ARGUS`

Toute cartographie de relations inclut ARGUS comme **repo structurant de niveau P1**.

---

## 2. Cartographie du MDU Existant (Confrontation)

### 2.1 Atomes et patterns déjà disponibles

| Atome / Design | Rôle | Couverture actuelle |
|---|---|---|
| `atoms/cross-repo-flow.yaml` | Pattern `provider -> consumers`, contrat, validation, détection de cycles | Définit le contrat, pas les instances |
| `atoms/structural-relations.yaml` | 8 kinds : `opposes`, `complements`, `inherits`, `requires`, `blocks`, `stabilizes`, `supersedes`, `evolves_to` | Définit les sémantiques, pas les instances |
| `atoms/sync-orchestrator.yaml` | Synchronisation cross-repo : pull/push/drift/rollback | Pattern générique, pas de config par repo |
| `atoms/registry-sync.yaml` | Sync des registres entre repos | Pattern, pas d'instance appliquée |
| `atoms/multi-repo-audit.yaml` | Audit cross-repo avec gardes anti-zombie | Pattern, pas de scheduling |
| `atoms/registry-consistency-sentinel.yaml` | Détection d'incohérences entre registres | Pattern, pas d'instance appliquée |

### 2.2 Gap identifié

Le MDU fournit les **briques de modélisation**, mais pas la **modélisation elle-même**. C'est l'équivalent d'avoir un langage de schéma XML sans aucun document XML instancié.

### 2.3 Flux prioritaires à instancier en Phase 1

Les flux suivants sont **obligatoires** en v0.1 et doivent être les premiers fichiers créés dans `repo-relations/flows/` :

| Provider | Consumer | Type de flux | Contrat |
|---|---|---|---|
| GOVERNANCE-HUB | unified-design | Extraction MDU | `known_repositories.yaml`, `multi-repo-governance.yaml` |
| GOVERNANCE-HUB | NEXUS | Registre des registres | `OrgansRegistry.yaml`, `BRIDGES.yaml` |
| GOVERNANCE-HUB | TOPOS | Topologie ENV | `TOPOS/registry/repos.json` |
| GOVERNANCE-HUB | ECOS-CLI | CLI multi-repo | `known_repositories.yaml` |
| GOVERNANCE-HUB | KIVA-CLI | Validation souveraine | `known_repositories.yaml` |
| NEXUS | ARGUS | Sentinelle de cohérence | `registry/` |
| NEXUS | KG-L | Graphe causal | `KG-L/exports/` |
| ONTOLOGY | VERSES | Sync ontologique | `ONTOLOGY/concepts/` |
| ONTOLOGY | KG-L | Termes ontologiques | `ontology_anchors.jsonl` |
| unified-design | NEXUS | Atomes MDU | `atoms/`, `designs/` |
| unified-design | REPO-STANDARDS | Standards macro | `META-DESIGN.md` |
| TOPOS | ECOS-CLI | Registry ENV | `topology.yaml` |
| TOPOS | KIVA-CLI | Topologie projets | `TOPOS/registry/` |
| BRAIN | FLUENCE | Orchestration cognitive | `BRAIN/agents/` |
| BRAIN | WAZAA | Event bus | MessageBus |
| KIVA | KIVA-CLI | Runtime CLI | `KIVA/` |
| KIVA | TRIX | Runtime Zig | `TRIX/` |
| TIMX | LLUX | Feature Store — signatures temporelles | `TIMX/tools/perimeter-awareness/*.py` |
| TIMX | RLM-243 | Feature Store — features vectorielles | `TIMX/tools/perimeter-awareness/*.py` |
| TIMX | TALEX | Feature Store — timeline events | `TIMX/tools/perimeter-awareness/*.py` |
| CTULU | WAZAA | Pipeline events | `CTULU/pipelines/` |
| BatMCP | SKILLS | Skills MCP | `SKILLS/` |
| REPO-STANDARDS | GOVERNANCE-HUB | Standards governance | `REPO-STANDARDS/governance/` |

**Règle de priorité** : N+1 → N+2 → N+3 → N+4. Les repos L0-CANON/L0_CONSTITUTIONAL sont instanciés avant les strates inférieures.

---

## 3. Décision

Créer et maintenir un **registre des relations inter-dépôts** dans `unified-design`, structuré comme suit :

```
unified-design/
├── repo-relations/
│   ├── registry.yaml          # Vue d'ensemble : tous les flows par repo
│   ├── layers/
│   │   ├── L0-CANON.yaml      # Relations intra-L0
│   │   ├── L1-INFRA.yaml
│   │   ├── L2-PLATFORM.yaml
│   │   ├── L3-CITIZENS.yaml
│   │   ├── L4-TOOLS.yaml
│   │   ├── L5-ARCHIVE.yaml
│   │   └── L6-WORK.yaml
│   ├── flows/                 # Un fichier par flow significatif
│   │   ├── governance-hub -> unified-design.yaml
│   │   ├── topy -> ... etc.
│   └── README.md
```

### 3.1 Structure d'un flow

Chaque fichier dans `flows/` utilise le schéma `cross-repo-flow.yaml` :

```yaml
cross_repo_flow:
  name: governance-hub -> unified-design
  provider: GOVERNANCE-HUB
  consumers:
    - unified-design
  contract:
    interface: file
    format: yaml
    path: known_repositories.yaml
    version: "1.0"
  validation:
    - provider_registered
    - consumer_registered
    - no_cycle
  wal_logging: required
  inherits: [cross-repo-flow]
```

### 3.2 Structure de `registry.yaml`

```yaml
registry_version: "1.0.0"
generated_at_utc: "2026-09-21T20:14:30Z"
source_of_truth: GOVERNANCE-HUB/known_repositories.yaml
total_repos: 121
total_flows: 23

flows:
  - file: layers/L0-CANON.yaml
    repos_count: 8
    flows_count: <N>
  - file: layers/L1-INFRA.yaml
    repos_count: <N>
    flows_count: <N>
  # ...

structural_relations:
  - file: layers/structural-overview.yaml
    kinds:
      - requires
      - blocks
      - stabilizes
      - complements
      - opposes
      - supersedes
      - evolves_to
```

### 3.3 Règles de maintenance

1. **Tout nouveau repo** ajouté dans `known_repositories.yaml` DOIT avoir ses relations documentées dans `repo-relations/` avant d'être déclaré `ACTIVE`.
2. **Toute modification de contrat** entre deux repos DOIT être tracée dans le fichier de flow correspondant et loggée dans le WAL.
3. **Validation CI** : `gerivdb design validate` DOIT vérifier que tous les repos `ACTIVE` de la SOT ont au moins un flux documenté ou une annotation explicite `standalone: true`.
4. **Cycle detection** : le loop_engine MDU DOIT exécuter un DFS sur `repo-relations/registry.yaml` avant tout merge touchant `known_repositories.yaml` ou `repo-relations/`.

---

## 4. Livrables atomiques

| # | Livrable | Fichier cible | Action | Priorité |
|---|----------|---------------|--------|----------|
| 1 | Ajout ARGUS à la SOT | `known_repositories.yaml` | Edit | P0 (prérequis) |
| 2 | Registre initial L0 structurant | `repo-relations/layers/L0-CANON.yaml` | Write | P0 |
| 3 | Flux GOVERNANCE-HUB → NEXUS | `repo-relations/flows/govhub-nexus.yaml` | Write | P0 |
| 4 | Flux GOVERNANCE-HUB → unified-design | `repo-relations/flows/govhub-unified-design.yaml` | Write | P0 |
| 5 | Flux GOVERNANCE-HUB → TOPOS | `repo-relations/flows/govhub-topos.yaml` | Write | P0 |
| 6 | Flux GOVERNANCE-HUB → ECOS-CLI | `repo-relations/flows/govhub-ecos-cli.yaml` | Write | P0 |
| 7 | Flux GOVERNANCE-HUB → KIVA-CLI | `repo-relations/flows/govhub-kiva-cli.yaml` | Write | P0 |
| 8 | Flux ONTOLOGY → VERSES | `repo-relations/flows/ontology-verses.yaml` | Write | P1 |
| 9 | Flux ONTOLOGY → KG-L | `repo-relations/flows/ontology-kgl.yaml` | Write | P1 |
| 10 | Flux unified-design → REPO-STANDARDS | `repo-relations/flows/unified-design-repo-standards.yaml` | Write | P1 |
| 11 | Flux NEXUS → ARGUS | `repo-relations/flows/nexus-argus.yaml` | Write | P1 |
| 12 | Flux BRAIN → FLUENCE | `repo-relations/flows/brain-fluence.yaml` | Write | P1 |
| 13 | Flux BRAIN → WAZAA | `repo-relations/flows/brain-wazaa.yaml` | Write | P1 |
| 14 | Flux KIVA → KIVA-CLI | `repo-relations/flows/kiva-kiva-cli.yaml` | Write | P1 |
| 15 | Flux KIVA → TRIX | `repo-relations/flows/kiva-trix.yaml` | Write | P1 |
| 16 | Flux TIMX → LLUX | `repo-relations/flows/timx-llux.yaml` | Write | P1 |
| 17 | Flux TIMX → RLM-243 | `repo-relations/flows/timx-rlm243.yaml` | Write | P1 |
| 18 | Flux TIMX → TALEX | `repo-relations/flows/timx-talex.yaml` | Write | P1 |
| 19 | Flux BatMCP → SKILLS | `repo-relations/flows/batmcp-skills.yaml` | Write | P2 |
| 20 | Registres par strate | `repo-relations/layers/*.yaml` | Write | P2 |
| 21 | Vue d'ensemble | `repo-relations/registry.yaml` | Write | P2 |
| 22 | README | `repo-relations/README.md` | Write | P2 |
| 23 | Mise à jour ATOM-042 | `atoms/ATOM-042-REPOSITORY-CENSUS.md` | Edit | P1 |
| 24 | Validation CI | `.kiva/pipelines/unified-design.yaml` | Edit | P1 |
| 25 | Hook pre-commit | `.githooks/pre-commit` | Edit | P1 |

---

## 5. Plan d'implémentation

### Phase 1 — Extraction (v0.1, cet intent)
1. **Ajouter ARGUS et TIMX à `known_repositories.yaml`** avec leurs attributs respectifs.
2. Lire `known_repositories.yaml` et extraire les 121 repos avec leur `layer`, `role`, `crosslinks`, `status`, `memory_role`.
3. Pour chaque strate, identifier les flux connus :
   - Flux de gouvernance : `GOVERNANCE-HUB` → tous les repos (via `known_repositories.yaml`, `multi-repo-governance.yaml`)
   - Flux de design : `unified-design` → repos consommateurs de designs (`designs/*.yaml`)
   - Flux de sync : `TOPOS` ↔ `ECOS-CLI` ↔ tous les repos
   - Flux de skill : `SKILLS` → agents/outils
   - Flux de données : `KG-L` / `VERSES` / `ONTOLOGY` → consommateurs
   - Flux de scan : `ARGUS` → `NEXUS` / `GOVERNANCE-HUB` / `KG-L`
   - Flux de feature store : `TIMX` → `LLUX` / `RLM-243` / `TALEX`
4. Instancier en priorité les 21 flux obligatoires listés en section 2.3, en commençant par les 13 repos structurants.
5. Pour les repos sans relation documentée, ajouter `standalone: true` avec justification.

### Phase 2 — Validation (v0.2)
1. Ajouter la CI `gerivdb design validate` sur `repo-relations/`.
2. Ajouter le check `cycle_detection` sur le registre.
3. Publier un rapport `REPORT-REPO-RELATIONS-AUDIT-YYYY-MM-DD.md`.

### Phase 3 — Automatisation (v1.0)
1. Connecter `repo-relations/registry.yaml` à `known_repositories.yaml` via un script de sync.
2. Détecter automatiquement les nouveaux repos orphelins de flux documenté.
3. Intégrer au `session-boot-sequence` BOOT-5bis.

---

## 6. Critères d'acceptation

- [ ] `ARGUS` est ajouté à `known_repositories.yaml` avec `layer: L1_CAUSALITY`, `status: ACTIVE`, `role`, `local_path` et `memory_role: ecosystem_scanner`.
- [ ] Les 12 repos structurants listés en section 1.3 ont tous leurs flux documentés dans `repo-relations/flows/`.
- [ ] Les 18 flux obligatoires listés en section 2.3 sont instanciés et validés.
- [ ] `repo-relations/registry.yaml` existe et référence 100% des repos `ACTIVE` de `known_repositories.yaml`.
- [ ] Aucun cycle détecté dans `structural_relations` (kinds `requires`, `blocks`, `inherits`, `supersedes`, `evolves_to`).
- [ ] Chaque repo `ACTIVE` a soit un flux documenté, soit `standalone: true` justifié.
- [ ] `gerivdb design validate --strict` passe sur l'ensemble de `repo-relations/`.
- [ ] ATOM-042 est mis à jour : chiffre exact de repos SOT (119 + 1 si ARGUS ajouté), mention explicite d'ARGUS.
- [ ] Le registre est linked depuis `META-DESIGN.md` section “References”.
- [ ] Les `memory_role` sont documentés dans `repo-relations/registry.yaml` pour chaque repo structurant.

---

## 7. Références croisées

- `unified-design/atoms/cross-repo-flow.yaml` — pattern de base
- `unified-design/atoms/structural-relations.yaml` — kinds de relations
- `unified-design/atoms/sync-orchestrator.yaml` — sync cross-repo
- `unified-design/atoms/registry-sync.yaml` — sync des registres
- `unified-design/atoms/multi-repo-audit.yaml` — audit cross-repo
- `unified-design/atoms/registry-consistency-sentinel.yaml` — sentinelle de cohérence
- `GOVERNANCE-HUB/known_repositories.yaml` — source de vérité des repos
- `GOVERNANCE-HUB/BRIDGES.yaml` — connexions inter-repos
- `GOVERNANCE-HUB/TOPOS/registry/repos.json` — registre détaillé
- `D:\DO\WEB\TOOLS\L1-INFRA\ARGUS\` — repo ARGUS (scanner cross-repo)
- `ATOM-042-REPOSITORY-CENSUS` — documentation du gap précédent
- ADR-029 (`cross-repo-flows`) — décision d'ajout des atomes de flux
- ADR-018 (`governance-hub-mdu-extraction`) — extraction MDU de GOVERNANCE-HUB

---

## 8. Ontologie / Terms

| Terme | Définition | Source |
|-------|-----------|--------|
| `cross_repo_flow` | Flux orienté `provider -> consumers` avec contrat, validation et WAL | `atoms/cross-repo-flow.yaml` |
| `structural_relations` | Relations horizontales entre nodes MDU : 8 kinds | `atoms/structural-relations.yaml` |
| `registry.yaml` | Vue agrégée de tous les flows par strate | Ce document |
| `standalone` | Repo sans flux documenté vers un autre repo | Ce document |
| `cycle_detection` | DFS sur le graphe de flows pour interdire les cycles | `atoms/cross-repo-flow.yaml` |
