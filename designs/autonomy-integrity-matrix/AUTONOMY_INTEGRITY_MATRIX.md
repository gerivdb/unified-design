---
name: autonomy-integrity-matrix
description: Politique de resolution des references fantomes declaree par niveau AUTONOMY_LADDER (A0-A3). Rend le comportement du RIG verifiable au lieu d'implicite.
version: 1.0.0
intent_hash: 0xDESIGN_AUTONOMY_INTEGRITY_MATRIX_20260823
type: design
layer: L0
repo: gerivdb/unified-design
---

# DESIGN -- AUTONOMY INTEGRITY MATRIX

## Principe

Le niveau d'autonomie (AXE-0, `ONTOLOGY/concepts/autonomy-ladder.md`) determine
la politique de traitement des references fantomes detectees par le RIG.
La politique est **declaree ici**, implementee dans `check-ref-integrity.ps1`,
resolue au runtime via `hotl_resolve.ps1`. Design d'abord, code ensuite.

## La matrice

| Niveau | Etat integrite | Politique | Comportement RIG |
|--------|----------------|-----------|------------------|
| A0 (HITL) | fantomes > 0 | Bloquant | exit 1 -- commit bloque, correction avant action |
| A1 (HOTL actif) | fantomes > 0 | Bloquant + alerte temps reel | exit 1 + alerte supervision |
| A2 (HOTL passif) | fantomes > 0 | Non bloquant + **journalise** | exit 0 + warning + append `rig_phantoms.log` |
| A3 (HOTL inactif) | fantomes > 0 | Differe + journalise | exit 0 + append `rig_phantoms.log` (queue) |
| Tous | 0 fantome | Vert | exit 0 |

Journal des fantomes : `GOVERNANCE-HUB/RUNTIME/rig_phantoms.log` (JSONL,
append-only, meme format que corrections_journal avec `action":"detected"`).

## Bornes explicites

1. **Un scan ne declenche jamais de rollback.** Le rollback automatique est
   reserve aux MUTATIONS (voir `hotl_checkpoint.ps1` / `hotl_rollback.ps1`).
   "Critique" en A3 ne s'applique donc pas aux findings de scan : ils sont
   diffuses et journalises, point.
2. La monotonie herite : la politique appliquee est celle du niveau EFFECTIF
   resolu (`min(global, override)`), jamais un niveau local expansif.
3. Le defaut fail-safe reste A2 : un RIG sans resolver accessible alerte et
   journalise, il ne bloque jamais sur incertitude de niveau.

## Delta d'implementation declare (honnêtete)

Au moment de l'adoption de ce design, le code existant couvre A0/A1/A2-exit
mais ne journalise pas les fantomes. Le delta suivant est requis pour que le
design ne devienne pas lui-meme une friction "contrat ecrit, adossement absent" :

- [ ] `check-ref-integrity.ps1` : append des fantomes a `RUNTIME/rig_phantoms.log`
      en A2 et A3 (une ligne JSONL par finding)

## Verification

| Test | Attendu |
|------|---------|
| repo sans fantome | exit 0 quel que soit le niveau |
| fantome + A2 | exit 0 + row journal present |
| fantome + A3 | exit 0 + row journal present |
| fantome + A1 (SOT elevee) | exit 1 |

## Relations

- Depend de : AUTONOMY_LADDER (`ONTOLOGY/concepts/autonomy-ladder.md`)
- Consomme par : RIG, BOOT-5, hooks post-wiring (design hotl-wiring)
- Connected to : AUTO_DEBUG_INTENTS (`GOVERNANCE-HUB/INTENTS/INTENT-AUTONOM-DEBUG-001.md`)
- Complete : CONTRACT_TRACEABILITY (les detections journalisees alimentent
  les corrections tracees)

## AUTO-DEBUG Extension

Ce design étend AUTONOMY_INTEGRITY_MATRIX pour intégrer la stratégie AUTO-DEBUG :

| INTENT | AutonomOps Property | Autonomy Level | Design Dependency |
|--------|---------------------|----------------|-------------------|
| KIVA-FEEDBACK | hasDecisionFramework | A1 | DESIGN-AUTONOMY-003 |
| CURX-OPTIMIZER | hasSelfHealing | A2 | DESIGN-AUTONOMY-004 |
| CITIZENS-CIRCUIT | hasAutonomyLevel | A3 | DESIGN-AUTONOMY-005 |
| AUTO-ALERTER | hasDecisionFramework | A1 | DESIGN-AUTONOMY-002 |

### Intégration avec AUTO-DISCOVERY

```bash
# Hook pre-commit avec auto-discovery
python GOVERNANCE-HUB/scripts/auto_discovery_engine.py --mode quick
```

### Mapping des Run IDs

- RUN-001 à RUN-012 : Implémentation des INTENTS AUTO-DEBUG
- RUN-013 à RUN-025 : Phase 2 AutonomOps

## Voir aussi

- `designs/contract-traceability/CONTRACT_TRACEABILITY.md`
- `PRD-MOC-GEN-009` sections 2.3, 4.2 (GOVERNANCE-HUB)
