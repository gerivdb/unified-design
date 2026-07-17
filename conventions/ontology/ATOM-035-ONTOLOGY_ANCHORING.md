---
type: GUI
version: 1.0.0
status: active
intent_hash: 0xATOM_035_ONTOLOGY_ANCHORING
---

# ATOM-035 : ONTOLOGY Anchoring

## Définition

ONTOLOGY est le **dictionnaire sémantique canonique** de l'écosystème gerivdb/*. Tout concept, règle, ou artefact du MDU doit être ancré dans ONTOLOGY pour garantir la cohérence sémantique.

## Rôle

ONTOLOGY fournit :

- **Définitions canoniques** : concepts/core/*.md
- **Schémas machine-readable** : schema/*.yaml
- **Relations inter-concepts** : relations/graph.json, hierarchies.yaml
- **Cross-references** : crossrefs/*_map.md
- **Bridges actifs** : bridges/*_bridge.md

## Règle

> **Tout concept utilisé dans les ATOMs, ADRs, ou conventions doit être défini dans ONTOLOGY.**

- Un nouvel ATOM n'est valide que si ses termes clés existent dans ONTOLOGY.
- Le fichier `ONTOLOGY_MAP.md` (dans unified-design) maintient la correspondance.
- TQL est utilisé pour interroger ONTOLOGY : `TQL> SELECT concept WHERE name = 'ATOM-035'`.

## Validation

### CHECK-1 : Existence du concept
```bash
# Vérifier si un concept existe dans ONTOLOGY
test -f "D:\DO\WEB\TOOLS\L0-CANON\ONTOLOGY/concepts/core/<concept>.md"
```

### CHECK-2 : Schéma associé
```bash
# Vérifier le schéma YAML correspondant
test -f "D:\DO\WEB\TOOLS\L0-CANON\ONTOLOGY/schema/<schema>.yaml"
```

### CHECK-3 : Cross-reference
```bash
# Vérifier la cross-reference dans BRAIN
grep -r "<concept>" "D:\DO\WEB\TOOLS\L0-CANON\ONTOLOGY/crossrefs/brain_map.md"
```

## Exemple d'application

```
CONCEPT : "Loop Engineering"
→ ONTOLOGY/concepts/core/loop_engineering.md
→ ONTOLOGY/schema/loop.yaml
→ ONTOLOGY/crossrefs/brain_map.md : Loop Engineering → loops/LoopEngineering.py
→ TQL> EXPLAIN 'loop_engineering'
```

## Règles associées

- **ATOM-036** : VERSES Mapping — les modèles d'interaction doivent être liés aux concepts ONTOLOGY
- **ATOM-038** : TQL Interface Contract — la requête doit respecter le schéma ONTOLOGY

## Références

- [ONTOLOGY](https://github.com/gerivdb/ONTOLOGY) — Dictionnaire canonique
- [ONTOLOGY.yaml](D:\DO\WEB\TOOLS\L0-CANON\ONTOLOGY\ONTOLOGY.yaml) — Spécification formelle
- [TQL README](D:\DO\WEB\TOOLS\L4-TOOLS\TQL\README.md) — Interrogation sémantique

## Référence ADR

- **ADR** : ADR-2026-07-17-001-ONTOLOGY-ANCHORING
- **IntentHash** : 0xATOM_035_ONTOLOGY_ANCHORING_20260717
- **Dépôt** : gerivdb/GOVERNANCE-HUB
- **Statut ADR** : proposed
- **Màj requise si** : statut ADR → deprecated ou superseded