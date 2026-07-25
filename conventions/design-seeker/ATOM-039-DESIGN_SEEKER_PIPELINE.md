---
type: GUI
version: 1.0.0
status: active
intent_hash: 0xATOM_039_DESIGN_SEEKER_PIPELINE
---

# ATOM-039 : Design-Seeker Pipeline

## Définition

Méta-outil d'analyse des designs existants qui détecte, extrait et durcit les designs implicites dans l'écosystème gerivdb/*.

## Pipeline en 5 phases

```
[ONTOLOGY / TQL] ──── Scan ────┐
                              │
[TINA] ──── Discovery ─────────┤
                              │
[FLUENCE / UAE] ── Hunt ───────┤
                              ▼
                    ┌─────────────────┐
                    │ DESIGN-SEEKER   │
                    │ (ATOM-039)    │
                    └─────────────────┘
                              │
                    ┌─────────┼─────────┐
                    ▼         ▼         ▼
               [Scan TQL] [Discovery TINA] [Hunt UAE/FLUENCE]
                    │         │         │
                    ▼         ▼         ▼
             Concepts non    Écarts     Workflows
             documentés     formels    orphelins
                    │         │         │
                    └─────────┼─────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │ HARDEN (CTULU /│
                    │ VERSES)        │
                    └─────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │ REPORT (STYX → │
                    │ NEXUS WAL)     │
                    └─────────────────┘
```

## Règles associées

### Règle D1 — Scan (TQL)
- Interroger l'ONTOLOGY pour identifier les concepts non documentés
- Requête type : `SELECT workflow WHERE EXISTS_IN_CODE=true AND DOCUMENTED_IN_DESIGN=false`

### Règle D2 — Discovery (TINA)
- Vérifier la cohérence formelle des designs
- Détecter les écarts entre code et spécifications

### Règle D3 — Hunt (FLUENCE/UAE)
- Prioriser les découvertes par score d'attention
- Orchestrer les sondes distribuées (voir ATOM-040)

### Règle D4 — Harden (CTULU/VERSES)
- Valider les appels système (CTULU)
- Générer des designs durcis (VERSES)

### Règle D5 — Report (STYX)
- Publier les résultats dans le WAL NEXUS
- Produire `design_gaps_report.json` conforme au schéma

## Fallback local (Hassani Pattern)

Si FLUENCE est hors ligne :
- Les agents locaux continuent de scanner
- Résultats stockés dans `.seeker/local_report.json`
- FLUENCE consolide à sa reconnexion

## Exemple de scan MVP

```bash
python scripts/design_seeker_mvp.py --repo unified-design --output report.json
```

## Références

- [TQL](conventions/tql/ATOM-038-TQL_INTERFACE_CONTRACT.md) — Interface de requête
- [TINA](conventions/tina/ATOM-037-TINA_SPECIFICATION.md) — Vérification formelle
- [ATOM-040](conventions/design-seeker/ATOM-040-DISTRIBUTED_SEEKER_AGENTS.md) — Agents distribués

## Référence ADR

- **ADR** : ADR-2026-07-17-006-DESIGN-SEEKER
- **IntentHash** : 0xATOM_039_DESIGN_SEEKER_PIPELINE_20260717
- **Dépôt** : gerivdb/GOVERNANCE-HUB
- **Statut ADR** : proposed
- **Màj requise si** : statut ADR → deprecated ou superseded