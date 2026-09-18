---
type: PRD-MOC
version: "1.0"
date: "2026-09-18"
intent_hash: 0xPRD_MOC_CODEDB_E5620_DESIGN_20260918
governance: gerivdb/REPO-STANDARDS
status: proposed
strate: L0-CANONICAL
profil: TOOL
rss_depth: 4
---

# PRD-MOC-CODEDB-E5620-DESIGN — Design codeDB pour Xeon E5620

**Repo** : `gerivdb/unified-design` (designs/codedb-e5620) | **Strate** : L0-CANONICAL | **Profil** : TOOL  
**Rôle** : Document d’intégration du design codeDB-E5620 dans l’écosystème HERMES/FLEX/INFX  
**Source** : `design.yaml` + audit cross-repo 2026-09-18

---

## Objectif

- **Consommer dynamiquement** le design YAML `design.yaml` dans HERMES
- **Ingérer les faits hardware** E5620 dans `facts.db` HERMES
- **Propager vers KG-L** via `trust_propagator.py` et `kg_l_bridge.py`
- **Alimenter FLEX** avec les contraintes NUMA/cache/affinité

---

## Design YAML source

`D:\DO\WEB\TOOLS\L0-CANON\unified-design\designs\codedb-e5620\design.yaml`

### Extraits clés

```yaml
cpu:
  model: Xeon E5620
  cores: 8
  threads: 16
  instruction_set: SSE4.2
  cache:
    l3_size_kb: 12288
    line_size_bytes: 64
  numa:
    nodes: 2
    cores_per_node: 4

constraints:
  alignment_bytes: 64
  cache_blocking_kb: 4096
  cpu_only: true
```

---

## Intégration HERMES

### Tâche E — Ingestion design YAML codeDB-E5620

**Fichiers** :
- `tools/codedb_design_reader.py` (création)
- `tools/codedb_e5620_ingestor.py` (modification : `ingest_from_design()`)
- `tests/test_codedb_design_reader.py` (création)

**Critères d’acceptation** :
- [ ] `design.yaml` lu sans erreur
- [ ] Faits ingérés avec `source: "codedb-e5620-design"`
- [ ] `ingest_from_design()` remplace `ingest_default_e5620_patterns()`

---

## Intégration FLEX

### Contraintes hardware propagées

| Contrainte | Valeur | Usage FLEX |
|---|---|---|
| `alignment_bytes` | 64 | Buffer alignment dans `affinity.zig` |
| `cache_blocking_kb` | 4096 | Cache slicing stride dans `cache.zig` |
| `numa.nodes` | 2 | Pool NUMA dans `numa.zig` |
| `cpu_only` | true | Désactivation GPU dans `thermal.zig` |

**Référence** : `PRD/PRD-MOC-FLEX-ENV2-TOPOLOGY-HARMONY.md`

---

## Intégration INFX

### Faits hardware dans le tore

| Fait | Usage INFX |
|---|---|
| `cache.l3_size_kb = 12288` | Taille hot memory 1.7 KB / warm 54 KB |
| `numa.nodes = 2` | Affinité triplets par nœud |
| `instruction_set = SSE4.2` | Contrainte compilation Zig `-Dcpu=westmere` |

**Référence** : `PRD-MOC/archives/infx/v0.5/PRD-MOC-v0.5-TOROIDAL-MEMORY-LAYOUT.md`

---

## Intégration WAZAA

### Canaux concernés

| Channel | Direction | Payload |
|---|---|---|
| `L4-TOOLS/CodeDB/index/updated` | CodeDB → WAZAA | `repo_path`, `files_indexed`, `duration_ms` |
| `L4-TOOLS/CodeDB/search/query` | CodeDB → WAZAA | `query`, `results_count`, `latency_ms` |

**Référence** : `channels/channels.index.yaml`

---

## Critères de succès globaux

- [ ] `design.yaml` consommé dynamiquement par HERMES
- [ ] Faits hardware ingérés dans `facts.db` avec `source: "codedb-e5620-design"`
- [ ] Contraintes propagées vers FLEX (alignment, cache blocking, NUMA)
- [ ] Faits hardware propagés vers KG-L `domain_links.json`
- [ ] Canaux WAZAA `CodeDB/*` opérationnels

---

## Références

- `D:\DO\WEB\TOOLS\L0-CANON\unified-design\designs\codedb-e5620\design.yaml` — Design source
- `PRD-MOC-HERMES-INTEGRATION-TOROIDAL-E5620.md` — Intégration HERMES
- `PRD/PRD-MOC-FLEX-ENV2-TOPOLOGY-HARMONY.md` — Intégration FLEX
- `PRD-MOC/archives/infx/v0.5/PRD-MOC-v0.5-TOROIDAL-MEMORY-LAYOUT.md` — Intégration INFX
- `channels/channels.index.yaml` — Canaux WAZAA

---

*PRD-MOC-CODEDB-E5620-DESIGN — Profil TOOL, Strate L0-CANONICAL, RSS Depth 4*

## Proof-of-Life
- [x] 2026-09-18T19:12:00+02:00 — PRD-MOC créé : design codeDB-E5620
- [ ] 2026-09-18T19:12:00+02:00 — Tâche E : ingestion design YAML codeDB
