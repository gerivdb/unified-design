# DESIGN-FLEX-001 — FLEX Harmony Topology Engine

| Property | Value |
|----------|-------|
| **Design ID** | DESIGN-FLEX-001 |
| **Name** | FLEX Harmony Topology Engine |
| **Repo** | FLEX |
| **Layer** | L4-TOOLS |
| **Version** | 1.0.0 |
| **Status** | PROPOSED |
| **Description** | Moteur d'harmonie topos-code-matériel pour ENV2. Détection NUMA, affinité CPU, optimisation cache, surveillance thermique. |
| **Capabilities** | numa-detection, affinity-scheduling, cache-optimization, thermal-monitoring, topology-mapping |
| **Dependencies** | TRIX (runtime Zig), KIVA (orchestration), BRAIN (cognitive mapping), ZIG-RUNTIME (compilation) |
| **Atoms** | ATOM-FLEX-NUMA-DETECT, ATOM-FLEX-AFFINITY-SET, ATOM-FLEX-CACHE-SLICE, ATOM-FLEX-THERMAL-MONITOR |
| **SOT Reference** | `gerivdb/FLEX/spec/FLEX-SPEC.md` |
| **Validation** | `kiva ci run flex` (pipeline in FLEX repo) |
| **MDU Layer** | N+3 (Action/Orchestration matérielle) |

## Atoms

| Atom ID | Name | Description |
|---------|------|-------------|
| ATOM-FLEX-NUMA-DETECT | NUMA Detection | Détection runtime topologie mémoire |
| ATOM-FLEX-AFFINITY-SET | Affinity Set | Allocation threads à pools NUMA |
| ATOM-FLEX-CACHE-SLICE | Cache Slice | Découpage workloads en slices cache-friendly |
| ATOM-FLEX-THERMAL-MONITOR | Thermal Monitor | Surveillance température, alertes, throttling |
| ATOM-FLEX-TOPO-GEN | Topos Generator | Génération/maintenance Topos ENV2.md |

## Dependencies

| Repo | Type | Interface |
|------|------|-----------|
| TRIX | Consumer | FLEX configure runners Zig avant exécution |
| KIVA | Consumer | KIVA consulte FLEX avant chaque run |
| BRAIN | Consumer | BRAIN mappe mathèmes -> pools NUMA |
| GOVERNANCE-HUB | Producer | FLEX déclare ses concepts ontologiques |
| TOPOS | Consumer | FLEX enrichit TOPOS/topology.yaml avec NUMA |
| NEXUS | Consumer | FLEX écrit WAL pour chaque configuration |
| ZIG-RUNTIME | Producer | FLEX consomme les binaires Zig souverains |
| REPO-STANDARDS | Producer | FLEX suit RSS-v2, déclare designs |

## Validation

- Compilation Zig 0.15.2 : OK
- Tests unitaires : OK
- RSS-v2 TOOL profile : conforme
- META-DESIGN : DESIGN-FLEX-001 ajouté
