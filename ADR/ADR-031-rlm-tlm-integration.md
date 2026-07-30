---
type: ADR
status: proposed
date: "2026-07-28"
intent_hash: 0xRLM_TLM_SYNERGY_20260727
---

<<<<<<< HEAD
# ADR-031 -- Integration RLM <-> TLM via KIX

## Contexte

La famille RLM (7 services + noyau 243) couvre l'execution/decision operationnelle. La famille TLM (TRIX, UAE, BLO, KG/SPIDX, PLIX, CTULU) apporte la structure/causalite narrative. L'architecture est close mais non enrichie mutuellement.

## Decision

Officialiser l'integration RLM <-> TLM via KIX comme pont d'orchestration unifie.

### Interfaces standardisees (contrat v1.0)

| RLM Service | TLM Service | Endpoint RLM | Endpoint TLM | Schema |
|-------------|-------------|--------------|--------------|--------|
| RLM-GRAPH | TRIX/UAE | POST /dependencies/tlm | GET /dependencies/graph | DependencyGraph-v1 |
| RLM-SECURE | TRIX/UAE | POST /scan/tlm | POST /scan | NarrativeArchetype-v1 |
| RLM-INCIDENT | TRIX/SELINA | POST /incidents/tlm | POST /sentry/webhook | IncidentNarrative-v1 |
| RLM-CONFIG | UAE/TRIX | GET /config?scope=tlm | POST /config | TLMConfig-v1 |
| KIX | TRIX/PLIX/UAE | GET /runners/tlm, POST /vote | -- | Runner-v1 |

### Extension KIX

- GET /runners/tlm : liste services TLM (ports 8789, 8788, 8790, 8791, 8792)
- Vote ternaire etendu aux actions critiques TLM (restart TRIX, deploy PLIX)
- SERVICE_MAP + TLM_SERVICE_MAP distincts, dual_role pour TRIX/PLIX

### Schemas de donnees partages

- DependencyGraph-v1 : nodes (id, type, stride, phi_cps), edges (source, target, relation, metadata)
- NarrativeArchetype-v1 : archetype, version, stages, coherence_rules, content
- IncidentNarrative-v1 : incident_id, narrative_break, story_id, coherence_score, tlm_playbook
- TLMConfig-v1 : phi_cps_threshold, narrative_coherence_min, archetype_library, stride_max, bdcp_mode

## Consequences

Positives : Enrichissement mutuel sans duplication, resilience partagee (TLM structure + RLM vote), KIX comme single pane of glass

Risques : Versioning contrats, latence cross-service (< 10 ms cible), gouvernance evolution (breaking changes -> vote ternaire KIX)

## Plan d'implementation
=======
# ADR-031 -- Intgration RLM <-> TLM via KIX

## Contexte

La famille RLM (7 services + noyau 243) couvre l'excution/dcision oprationnelle. La famille TLM (TRIX, UAE, BLO, KG/SPIDX, PLIX, CTULU) apporte la structure/causalit narrative. L'architecture est close mais non enrichie mutuellement.

## Dcision

Officialiser l'intgration RLM <-> TLM via KIX comme pont d'orchestration unifi.

### Interfaces standardises (contrat v1.0)

| RLM Service | TLM Service | Endpoint RLM | Endpoint TLM | Schma |
|-------------|-------------|--------------|--------------|--------|
| RLM-GRAPH | TRIX/UAE | `POST /dependencies/tlm` | `GET /dependencies/graph` | `DependencyGraph-v1` |
| RLM-SECURE | TRIX/UAE | `POST /scan/tlm` | `POST /scan` | `NarrativeArchetype-v1` |
| RLM-INCIDENT | TRIX/SELINA | `POST /incidents/tlm` | `POST /sentry/webhook` | `IncidentNarrative-v1` |
| RLM-CONFIG | UAE/TRIX | `GET /config?scope=tlm` | `POST /config` | `TLMConfig-v1` |
| KIX | TRIX/PLIX/UAE | `GET /runners/tlm`, `POST /vote` | -- | `Runner-v1` |

### Extension KIX

- `GET /runners/tlm` : liste services TLM (ports 8789, 8788, 8790, 8791, 8792)
- Vote ternaire tendu aux actions critiques TLM (restart TRIX, deploy PLIX)
- `SERVICE_MAP` + `TLM_SERVICE_MAP` distincts, `dual_role` pour TRIX/PLIX

### Schmas de donnes partags

- `DependencyGraph-v1` : nuds (id, type, stride, phi_cps), edges (source, target, relation, metadata)
- `NarrativeArchetype-v1` : archetype, version, stages, coherence_rules, content
- `IncidentNarrative-v1` : incident_id, narrative_break, story_id, coherence_score, tlm_playbook
- `TLMConfig-v1` : phi_cps_threshold, narrative_coherence_min, archetype_library, stride_max, bdcp_mode

## Consquences

- **Positives** : Enrichissement mutuel sans duplication, rsilience partage (TLM structure + RLM vote), KIX comme single pane of glass
- **Risques** : Versioning contrats, latence cross-service (< 10 ms cible), gouvernance volution (breaking changes -> vote ternaire KIX)

## Plan d'implmentation
>>>>>>> 88da000 (feat(ge): implement DAG-3 Graph Engineering design with CTULU L4 master intent)

1.  Mapping interfaces (RLM_TLM_INTERFACE_MAPPING.md)
2.  Extension KIX registry + endpoints TLM
3.  ADR-031 officialisation (ce document)
<<<<<<< HEAD
4.  Tests cross-RLM-TLM (pipeline deploy, scan archetype, incident narratif)

## Statut

**Propose** -- En attente de validation MDU pour passage a `accepted`.

## References

- IntentHash : 0xRLM_TLM_SYNERGY_20260727
- Mapping detaille : D:\DO\WEB\TOOLS\L4-TOOLS\RLM_TLM_INTERFACE_MAPPING.md
- KIX service.py : D:\DO\WEB\TOOLS\L4-TOOLS\KIX\service.py
=======
4.  Tests cross-RLM-TLM (pipeline deploy, scan archtype, incident narratif)

## Statut

**Propos** -- En attente de validation MDU pour passage  `accepted`.

## Rfrences

- IntentHash : `0xRLM_TLM_SYNERGY_20260727`
- Mapping dtaill : `D:\DO\WEB\TOOLS\L4-TOOLS\RLM_TLM_INTERFACE_MAPPING.md`
- KIX service.py : `D:\DO\WEB\TOOLS\L4-TOOLS\KIX\service.py`
>>>>>>> 88da000 (feat(ge): implement DAG-3 Graph Engineering design with CTULU L4 master intent)
