---
type: GUI
version: 1.0.0
status: active
intent_hash: 0xONTOLOGY_MAP_20260717
---

# ONTOLOGY MAP — Référentiel de correspondance concepts / artefacts MDU

Ce fichier maintient la correspondance entre les concepts de l'ONTOLOGY canonique et les artefacts du MDU (ATOMs, ADRs, conventions).

Interrogeable via TQL : `TQL> EXPLAIN 'ATOM-035'`

---

## Table de correspondance principale

| Concept ONTOLOGY | Définition | Artefact MDU | Dépôt |
|-----------------|------------|--------------|-------|
| `ontology` | Dictionnaire sémantique canonique | ONTOLOGY | L0-CANON |
| `verses` | Modèles d'interaction (double canal) | ATOM-036 | L4-TOOLS/VERSES |
| `tina` | Langage machine interne | ATOM-037 | L3-CITIZENS/TINA |
| `tql` | Interface de requête ontologique | ATOM-038 | L4-TOOLS/TQL |
| `atom` | Règle atomique de conception | ATOM-001 à ATOM-034 | L0-CANON/unified-design |
| `adr` | Décision architecturale enregistrée | ADR-*.md | L0-CANON/unified-design/ADR |
| `loop_engineering` | Mécanisme de contrôle itératif | ATOM-025 | L0-CANON/unified-design/conventions/loop |
| `maker_checker` | Double validation | ATOM-026 | L0-CANON/unified-design/conventions/maker-checker |
| `default_fail` | Sécurité par défaut | ATOM-027 | L0-CANON/unified-design/conventions/default-fail |
| `evidence_required` | Évidence tangible requise | ATOM-028 | L0-CANON/unified-design/conventions/evidence |
| `trix_architecture` | Architecture TRIX | ATOM-029 | L0-CANON/unified-design/conventions/trix |
| `bilevel_autoresearch` | Recherche automatique bicouche | ATOM-030 | L0-CANON/unified-design/conventions/autoresearch |
| `five_movements` | Cinq mouvements de débat | ATOM-031 | L0-CANON/unified-design/conventions/movements |
| `six_organs` | Six organes de gouvernance | ATOM-032 | L0-CANON/unified-design/conventions/organs |
| `topos_merge` | Fusion souveraine TOPOS | ATOM-033 | L0-CANON/unified-design/conventions/topos |
| `anti_patterns` | Anti-patterns interdits | ATOM-034 | L0-CANON/unified-design/conventions/anti-patterns |

---

## Références croisées détaillées

### ONTOLOGY → Concepts core

| Concept | Fichier | Schéma | Description |
|---------|---------|--------|-------------|
| `phi_cps` | concepts/core/phi_cps.md | schema/phi_cps.yaml | Mesure de valeur ajoutée |
| `wal` | concepts/core/wal.md | BRAIN | Write-Ahead Log |
| `ecosystem` | concepts/core/ecosystem.md | ECOS_ROOT | Ensemble des repos |
| `brain` | concepts/core/brain.md | BRAIN | Orchestrateur IA |
| `citizen` | concepts/core/citizen.md | intent_types.yaml | Agent dans le DAG |
| `blo_event` | concepts/core/blo_event.md | intent_types.yaml | Événement de cycle |
| `intent_hash` | concepts/core/intent_hash.md | intent_types.yaml | Identifiant unique |
| `issue_hash` | concepts/core/issue_hash.md | intent_types.yaml | Identifiant d'issue |
| `lifecycle_state` | concepts/core/lifecycle_state.md | lifecycle_states.yaml | État FSM |
| `fractal_pattern` | concepts/core/fractal_pattern.md | issue_ontology.yaml | Pattern fractal |

### VERSES → Personae MDU

| Persona | Rôle | Canal | Verse associé |
|---------|------|-------|---------------|
| Architecte | Conçoit la solution | Machine | `design.yaml` |
| Implémenteur | Code l'implémentation | Machine | `mdu_pipeline.py` |
| Auditeur | Vérifie la cohérence | Humain | `coherence_threshold: 0.8` |
| Décideur | Valide le résultat | Humain | `regeneration_on_drift: true` |

### TINA → Composants

| Composant | Fonction | Fichier | Vérification |
|-----------|----------|---------|--------------|
| Sandbox Éphémères | Isolation NeSy | CITIZENS.yaml | Z3 proofs |
| Vérification Formelle | Invariants | formal_verification_z3.py | Z3 solver |
| Audit Ontologique | Cohérence | ontology_audit_brain_docs.py | 95% coverage |
| Auto-correction | Corrections | post_implement_check.py | friction_detector |
| Citizen Routing | Routing | CITIZENS.yaml | [BDCP, match, execute] |

### TQL → Opérateurs cognitifs

| Opérateur | Type | Usage MDU |
|-----------|------|-----------|
| `diagnostic()` | Think | Analyse des erreurs |
| `vision()` | Think | Planification |
| `recherche()` | Think | Recherche de patterns |
| `acquis()` | Do | Collecte de faits |
| `besoin()` | Do | Validation des besoins |
| `strategie()` | Do | Définition de stratégie |
| `ecart()` | Check | Détection des écarts |
| `revision()` | Check | Revue de code |
| `alignement()` | Check | Vérification d'alignement |
| `ajustement()` | Coord | Ajustement de la stratégie |
| `deploiement()` | Coord | Déploiement |
| `controle()` | Coord | Contrôle qualité |

---

## Script de vérification

Utilisez ce script pour vérifier la cohérence entre ONTOLOGY et les ATOMs :

```bash
# Vérifier qu'un concept existe
tql "SELECT concept WHERE name = 'ATOM-035'"

# Vérifier les relations
tql "DOES 'ATOM-035' IMPLEMENT 'ontology_anchoring'?"

# Lister tous les ATOMs
tql "LIST ATOMS WHERE STATUS = 'active' AND LAYER = 'L0'"
```

---

## Mises à jour

| Version | Date | Description |
|---------|------|-------------|
| 1.0.0 | 2026-07-17 | Initialisation - ATOMs 035-038 |

---

## Référence ADR

- **ADR** : ADR-2026-07-17-005-ONTOLOGY-MAP
- **IntentHash** : 0xONTOLOGY_MAP_20260717
- **Dépôt** : gerivdb/GOVERNANCE-HUB
- **Statut ADR** : proposed
- **Màj requise si** : statut ADR → deprecated ou superseded