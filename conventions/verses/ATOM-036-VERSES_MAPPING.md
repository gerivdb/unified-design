---
type: GUI
version: 1.0.0
status: active
intent_hash: 0xATOM_036_VERSES_MAPPING
---

# ATOM-036 : VERSES Mapping

## Définition

VERSES définit les **modèles d'interaction** entre agents, humains et systèmes. Il encode le pattern "Double canal" et les structures de dialogue pour les sessions MDU.

## Rôle

VERSES sert de pont entre :

- **Channel Machine** : langage symbolique, IR, code
- **Channel Humain** : langage naturel, DAG ASCII, captures d'écran

## Concepts clés

### Double Canal

```
┌─────────────────┐      ┌─────────────────┐
│   Channel       │      │   Channel       │
│   Machine       │◄────►│   Humain        │
│                 │      │                 │
│ • IR            │      │ • Langage NL    │
│ • Pseudo-code   │      │ • DAG ASCII     │
│ • Regex         │      │ • Captures UI   │
└─────────────────┘      └─────────────────┘
```

### Personae Mapping

Chaque expert dans une session MDU a une persona définie dans VERSES :

| Persona | Rôle | Canal | Verse associé |
|---------|------|-------|---------------|
| Architecte | Conçoit la solution | Machine | `design.yaml` |
| Implémenteur | Code l'implémentation | Machine | `mdu_pipeline.py` |
| Auditeur | Vérifie la cohérence | Humain | `coherence_threshold: 0.8` |
| Décideur | Valide le résultat | Humain | `regeneration_on_drift: true` |

## Structure du dépôt VERSES

```
VERSES/
├── design.yaml              # Spécification du pattern
├── personae_mapping.md      # Cartographie des personas
├── mdu_pipeline.py          # Pipeline d'exécution MDU
├── verses_topos_mapping.json # Mapping TOPOS ↔ VERSES
└── wallet.jsonl             # Historique des échanges
```

## Règles associées

### Règle V1 : Coherence Threshold

Chaque verse généré doit avoir un `coherence_threshold >= 0.8` avant d'être accepté.

### Règle V2 : Regeneration on Drift

Si un drift sémantique est détecté, les verses doivent être régénérés automatiquement.

## Intégration avec TINA

Le langage machine utilisé dans VERSES est spécifié par TINA (voir ATOM-037).

## Exemple d'application

```
Session MDU :
1. Architecte → verse : "Implémenter ATOM-036"
2. Machine → IR : [ATOM, VERSES, MAPPING, ...]
3. Implémenteur → code : atoms/036_verses_mapping.py
4. Auditeur → vérification : test_verses_coherence.py
5. Décideur → validation : merge PR
```

## Références

- [VERSES](https://github.com/gerivdb/VERSES) — Modèles d'interaction
- [design.yaml](D:\DO\WEB\TOOLS\L4-TOOLS\VERSES\design.yaml) — Spécification technique
- [ATOM-037](ATOM-037-TINA_SPECIFICATION.md) — Langage machine associé

## Référence ADR

- **ADR** : ADR-2026-07-17-002-VERSES-MAPPING
- **IntentHash** : 0xATOM_036_VERSES_MAPPING_20260717
- **Dépôt** : gerivdb/GOVERNANCE-HUB
- **Statut ADR** : proposed
- **Màj requise si** : statut ADR → deprecated ou superseded