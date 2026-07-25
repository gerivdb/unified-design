---
type: GUI
version: 1.0.0
status: active
intent_hash: 0xATOM_037_TINA_SPECIFICATION
---

# ATOM-037 : TINA Specification

## Définition

TINA (Trusted Intelligent Neurosymbolic Architecture) est le **langage machine interne** du MDU. Il permet les échanges denses entre experts dans le canal machine.

## Caractéristiques

- **Notation symbolique** : mathématique, IR, pseudo-code C/Zig/ASM
- **Graphes, tenseurs, schémas de registres**
- **Compilable/exécutable** par le moteur TINA

## Stratum

TINA est un dépôt de **L3-CITIZENS** :

```yaml
# From known_repositories.yaml
- name: TINA
  entity_type: REPO
  full_name: gerivdb/TINA
  local_path: D:\DO\WEB\TOOLS\L3-CITIZENS\TINA
  layer: L3_CITIZENS
  role: Tina
```

## Composants

### Sandbox Éphémères

Isolation NeSy avec CubeSandbox :

- Engine : CubeSandbox
- Lifespan : ephemeral
- Namespaces : [pid, mnt, net, user]
- Cleanup : automatic

### Vérification Formelle

Proofs Z3 pour invariants :

- Solver : Z3
- Invariants : [strata_consistency, bdcp]

### Audit Ontologique

Cohérence connaissances N/N+1/N+2 :

- Strata : [N, N+1, N+2]
- Coverage : 95%
- Max time : 30000ms

### Auto-correction

Système intelligent de correction :

- Detector : friction_detector
- Corrector : post_implement_check

### Citizen Routing

Routing des citoyens :

- Registry : CITIZENS.yaml
- Fallback : Kilo Agent
- Steps : [BDCP, match, execute]

## Usage

### Vérifier la cohérence des strates

```bash
python scripts/ontology_audit_brain_docs.py
```

### Vérification Z3

```bash
python scripts/formal_verification_z3.py
```

## Format de base

```tina
# Déclaration d'entité
ENTITY: LoopEngineering
  PREREQ: [ATOM-025, ATOM-035]
  ACTION: create_convention
  VERIFY: ontology_anchor
  EXIT: ATOM-035_complete

# Règles d'invariant
INVARIANT: strata_consistency
  WHEN: layer_change
  THEN: verify_ontology_match

# Pattern de boucle
LOOP: mdu_cycle
  PHASES: [think, do, check]
  EXIT: convergence OR max_iterations
```

## Références

- [TINA](https://github.com/gerivdb/TINA) — Langage machine interne
- [design.yaml](D:\DO\WEB\TOOLS\L3-CITIZENS\TINA\design.yaml) — Spécification
- [ATOM-035](ATOM-035-ONTOLOGY_ANCHORING.md) — Ancrage requis

## Référence ADR

- **ADR** : ADR-2026-07-17-003-TINA-SPECIFICATION
- **IntentHash** : 0xATOM_037_TINA_SPECIFICATION_20260717
- **Dépôt** : gerivdb/GOVERNANCE-HUB
- **Statut ADR** : proposed
- **Màj requise si** : statut ADR → deprecated ou superseded