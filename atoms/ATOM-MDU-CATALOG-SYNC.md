# ATOM-MDU-CATALOG-SYNC

## Description

Atome de synchronisation catalogue MDU. Encode les règles de canonicalité, de complétude et de cohérence entre `meta-design.yaml`, les catalogues et l'arborescence physique.

## États obligatoires

| État | Nature | Gate |
|---|---|---|
| IDLE | En attente de synchronisation | SCAN |
| SCAN | Scan des artefacts physiques | CLASSIFY |
| CLASSIFY | Classification des écarts | PROPOSE |
| PROPOSE | Proposition de corrections | APPLY |
| APPLY | Application des corrections (HITL) | IDLE |

## Fonctions obligatoires

1. **SCAN_PHYSIQUE** — scan de l'arborescence physique
2. **CLASSIFY_ÉCARTS** — classification des écarts (nouveau / manquant / ambigu)
3. **PROPOSER_CORRECTIONS** — proposition de corrections atomiques
4. **VALIDER_CORRECTIONS** — validation HITL des corrections
5. **APPLIQUER_CORRECTIONS** — application des corrections validées
6. **ENREGISTRER_TRACE** — enregistrement horodaté

## Règles

1. 1 ID = 1 artefact = 1 chemin (canonicalité)
2. 100% des artefacts physiques sont catalogués (complétude)
3. `meta-design.yaml` ↔ catalogues ↔ arborescence sont cohérents
4. Toute correction est tracée et horodatée

## Anti-patterns

| Gène manquant | Pathologie |
|---|---|
| canonicalité | Doublons d'IDs, chemins ambigus |
| complétude | Artefacts orphelins non découvervables |
| cohérence | Divergence MDU / catalogues / arborescence |
| traçabilité | Corrections sans auditabilité |

## Invariant central

`meta-design.yaml`, les catalogues et l'arborescence physique sont mutuellement cohérents.

## Références

- **IntentHash** : `0xPRD_MOC_ATOM_MDU_CATALOG_SYNC_20260921`
- **Dépôt** : gerivdb/unified-design
- **Parent** : `meta-design-self-healing`, `ecosystem-meta-coherence`
