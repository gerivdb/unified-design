---
source: unified-design
target: TALEX
type: semantic_graph_ingestion
direction: outbound
status: active
intent_hash: 0xCROSSLINK_UNIFIED_DESIGN_TALEX_20260804
---

# Crosslink unified-design -> TALEX

unified-design ingère ses `atoms/` et `design.yaml` dans le `UnifiedSemanticGraph` de TALEX.

## Cible

| Attribut | Valeur |
|----------|--------|
| **Repo** | `gerivdb/TALEX` |
| **Module** | `src/talex/core/unified_graph.py` |
| **Reader** | `src/talex/readers/__init__.py::EcosystemReader._read_unified_design` |
| **Strate** | L4-TOOLS |

## Artefacts consommés par TALEX

| Artefact unified-design | Type TALEX | EdgeKind |
|-------------------------|------------|----------|
| `design.yaml` | `SemanticNode[DESIGN]` | DEPENDS_ON / USES |
| `atoms/*.yaml` | `SemanticNode[ATOM]` | - |

## Usage

```bash
x-forge analyze repo --name unified-design --root D:\DO\WEB
x-forge analyze triangulate --target DESIGN:unified-design --root D:\DO\WEB
```

## Référence

- **Repo source** : `gerivdb/unified-design`
- **IntentHash unified-design** : `0xUNIFIED_DESIGN_ENGINE_20260801`
