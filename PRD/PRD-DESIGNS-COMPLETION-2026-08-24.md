---
type: PRD
version: "1.0"
date: "2026-08-24"
status: proposed
intent_hash: 0xPRD_MOC_UNIFIED_DESIGN_GOVERNANCE_AUTOCOMPLETE_20260823
citizen: "unified-design"
layer: "L0"
author: gerivdb
source_repo: gerivdb/GOVERNANCE-HUB
source_path: PRD-MOC/general/PRD-MOC-GEN-011-unified-design-governance-autocomplete-2026-08-23.md
---

# PRD — Complétion des designs unified-design (subalterne GEN-011)

> Parent : PRD-MOC-GEN-011 v2.2 (hash racine propagé ci-dessus)
> Périmètre : ce dépôt uniquement — création des 13 designs + ATOM-053 + registre + META-DESIGN.
> Coordination transverse : voir MOC §15.1 (matrice, phases, dépendances).

---

## 1. Objectif

Créer dans `unified-design` les 13 designs listés au MOC §11 (7 fonctionnels + 4 méta-designs + 2 axiomes) et combler le fantôme ATOM-053, afin que chaque pattern de gouvernance né de l'incident PIANO 2026-08-23 soit couvert par un design adossé (PF2).

## 2. Livrables assignés (IDs du MOC §15)

| ID MOC | Livrable | Chemin cible | Section MOC |
|---|---|---|---|
| 1 | Design BALISE | designs/balise-identity-freshness.yaml | 11.1 |
| 2 | Design ARGUS orphan scanner | designs/argus-orphan-scanner.yaml | 11.2 |
| 3 | Design meta-coherence (+ note anti-collision MOX) | designs/meta-coherence.yaml | 11.3 |
| 4 | Design .LIMBO transit (+ escalade HOTL) | designs/limbo-transit.yaml | 11.4 |
| 5 | Design recovery tooling | designs/recovery-tooling.yaml | 11.5 |
| 6 | Design GGUF retention | designs/gguf-probe-retention.yaml | 11.6 |
| 7 | Design KG35 migration | designs/kg35-migration.yaml | 11.7 |
| 8 | Design unforeseen lifecycle | designs/unforeseen-lifecycle.yaml | 11.8 |
| 9 | Design design-coverage scanner | designs/design-coverage-scanner.yaml | 11.9 |
| 10 | Design impense register | designs/impense-register.yaml | 11.10 |
| 11 | Design thought-commit pipeline | designs/thought-commit-pipeline.yaml | 11.11 |
| 12 | ATOM-053 workspace draft convention | atoms/ATOM-053-workspace-draft-convention.md | 12 |
| 17 | Mise a jour atoms_registry.yaml | atoms_registry.yaml | - |
| 18 | Mise a jour META-DESIGN.md | META-DESIGN.md | - |

(Livrables 19-20, designs multi-repo et meta-cluster §11.12/§11.13, complètent la liste : 13 designs au total.)

## 3. Tâches

### Phase A — Fondations axiomatiques
1. `multi-repo-fundamental.yaml` : axiomes MR1-MR6 (MOC §11.12)
2. `meta-cluster-design.yaml` : définition formelle, taxonomie couplage, cohérence graduée (MOC §11.13)

### Phase B — Gouvernance opérationnelle
3. `meta-coherence.yaml` : capabilities ARGUS + note anti-collision vs mox-meta-coherence (portée documents ≠ cross-repo structurel)
4. `limbo-transit.yaml` : zones .LIMBO + workflow + escalade HOTL (PF4/PF6)
5. `argus-orphan-scanner.yaml` : pathologies ORPHAN_FILE/WRONG_REPO/TEMP_ARTIFACT/SOT_MISMATCH
6. `balise-identity-freshness.yaml` : sous-commandes BALISE + paramètres RUNTIME

### Phase C — Méta-designs
7. `unforeseen-lifecycle.yaml` : taxonomie 6 types, grille échelle x moment, règle R, métriques TE/TF/VE/H
8. `design-coverage-scanner.yaml` : pathologies DESIGN_* + croisement incidents x designs
9. `impense-register.yaml` : deux boucles, trois lentilles, triage, auto-audit ouroboros
10. `thought-commit-pipeline.yaml` : chaîne vibe->commit, gates G0-G3, 8 cas de cascade

### Phase D — Fonctionnel
11. `recovery-tooling.yaml` / `gguf-probe-retention.yaml` / `kg35-migration.yaml`

### Phase E — Registre et indexation
12. `atoms/ATOM-053-workspace-draft-convention.md` : contenu MOC §12
13. `atoms_registry.yaml` : entrées pour 13 designs + correction entrée ATOM-053 (path réelle)
14. `META-DESIGN.md` : table atomes + section changelog

## 4. Contraintes

- Encodage ASCII/CP1252 strict (hook pre-commit bloque U+2192 etc.)
- Chaque YAML suit le template observé (name, version, status, layer, intent_hash, inherits, depends_on, bridges, capabilities, performance/constraints si applicable)
- Commits atomiques <= 3 fichiers ; un commit par phase ou par paire de designs liés

## 5. Plan de commits proposé

| Commit | Fichiers |
|---|---|
| feat(designs): add multi-repo and meta-cluster axioms | multi-repo-fundamental, meta-cluster-design |
| feat(designs): add governance operational set | meta-coherence, limbo-transit |
| feat(designs): add scanner and balise designs | argus-orphan-scanner, balise-identity-freshness |
| feat(designs): add lifecycle meta-designs | unforeseen-lifecycle, design-coverage-scanner |
| feat(designs): add register and pipeline metas | impense-register, thought-commit-pipeline |
| feat(designs): add functional trio | recovery-tooling, gguf-probe-retention, kg35-migration |
| fix(atom): create missing ATOM-053 workspace convention | ATOM-053 file |
| chore(registry): index new designs and fix ghost entry | atoms_registry.yaml |
| docs(meta-design): reference new atoms and patterns | META-DESIGN.md |

## 6. Adossement (PF2)

- **Implémentation** : ce PRD, exécuté par agent Kilo session suivante
- **Vérificateur** : lecture croisée atoms_registry <-> disque (manuel en P1 ; automatique quand ARGUS design_coverage_scanner livré — livrable MOC 13) ; encodage via hook existant
- **Propriétaire** : gerivdb / GOVERNANCE-HUB N+4

## 7. Critères d'acceptation

1. Les 13 fichiers design/*.yaml existent et parsent en YAML valide
2. atoms_registry.yaml référence chaque nouveau design avec hash et description
3. Aucun DESIGN_GHOST résiduel sur l'ensemble designs + atoms (vérif manuelle croisée)
4. META-DESIGN.md liste les nouveaux patterns avec renvois
5. Pre-commit passe sans blocage encoding sur tous les fichiers

## 8. Références

- PRD-MOC-GEN-011 v2.2 (parent, toutes sections 11.x détaillées)
- artifact-structure-standard.md (REPO-STANDARDS, placement/numérotation)
- designs/moc-governance.yaml, prd-moc-progress-sync.yaml (patterns hérités)
- PRD-MOC-TDC-CONSCIOUSNESS-MASTER.md (livrables TDC additionnels)
- ADR-KG-CAUSAL-001-20260916 (ADR backing KG-CAUSAL)

---

## 9. Livrables additionnels — TDC Consciousness & méta-KG (2026-09-17)

> Ajouté par l'analyse de méta-KG du 2026-09-17 : les 13 designs initiaux couvrent la gouvernance opérationnelle, mais pas la couverture des 4 KG-engines (KG-L, VOLTX, KG-CAUSAL, VERSES) ni les carrefours Think/Do/Check.

### 9.1 Designs TDC Consciousness

| ID | Livrable | Chemin cible | Type | État | Blocage |
|---|---|---|---|---|---|
| 14 | Design `ecosystem-consciousness` | `designs/ecosystem-consciousness.yaml` | Créer | ✅ Implémenté | — |
| 15 | Design `chain-fluidity` | `designs/chain-fluidity.yaml` | Créer | 🟡 Draft | ADR gouvernance requis |
| 16 | Design `autonomy-fluidity` | `designs/autonomy-fluidity.yaml` | Créer | 🟡 Draft | ADR gouvernance requis |
| 17 | Design `conversation-aggregator` | `designs/conversation-aggregator.yaml` | Créer | 🟡 Draft | ADR gouvernance requis |
| 18 | Design `conversation-to-execution-bridge` | `designs/conversation-to-execution-bridge.yaml` | Créer | 🟡 Draft | ADR gouvernance requis |

### 9.2 Designs méta-KG

| ID | Livrable | Chemin cible | Type | État | Blocage |
|---|---|---|---|---|---|
| 19 | Design `kg-causal` | `designs/kg-causal.yaml` | Créer | 🟡 Draft | ADR `ADR-KG-CAUSAL-001-20260916` proposé |
| 20 | Design `kg-causal-engine` | `designs/kg-causal-engine.yaml` | Créer | 🟡 Draft | Dépend de `kg-causal` + ADR gouvernance |
| 21 | Design `causal-semantic-bridge` | `designs/causal-semantic-bridge.yaml` | Créer | 🟡 Draft | ADR gouvernance requis |
| 22 | Design `narrative-causal-fusion` | `designs/narrative-causal-fusion.yaml` | Créer | 🟡 Draft | ADR gouvernance requis |
| 23 | Design `meta-kg-engine` | `designs/meta-kg-engine.yaml` | Créer | 🟡 Draft | ADR gouvernance requis |
| 24 | Design `kg-causal-integration-pattern` | `designs/kg-causal-integration-pattern.yaml` | Créer | 🟡 Draft | ADR gouvernance requis |

### 9.3 Crosslinks

| ID | Livrable | Chemin cible | Type | État | Blocage |
|---|---|---|---|---|---|
| 25 | Crosslink `kg-causal-unified-graph` | `CROSSLINKS/kg-causal-unified-graph.md` | Créer | 🟡 Draft | Dépend du design `kg-causal` |
| 26 | Crosslink `voltx-unified-graph` | `CROSSLINKS/voltx-unified-graph.md` | Créer | 🟡 Draft | ADR gouvernance requis |
| 27 | Crosslink `verses-unified-graph` | `CROSSLINKS/verses-unified-graph.md` | Créer | 🟡 Draft | ADR gouvernance requis |

### 9.4 Atoms additionnels

| ID | Livrable | Chemin cible | Type | État | Blocage |
|---|---|---|---|---|---|
| 28 | Atom `kg-causal-consciousness` | `atoms/ATOM-KG-CAUSAL-CONSCIOUSNESS.md` | Créer | 🟡 Draft | Dépend du design `kg-causal` |

### 9.5 Critères d'acceptation additionnels

1. Tous les designs TDC et méta-KG existent et parsent en YAML valide.
2. `META-DESIGN.md` et `meta-design.yaml` référencent chaque nouveau design/atom/crosslink.
3. `CROSSLINKS/` contient les crosslinks pour KG-CAUSAL, VOLTX et VERSES.
4. Aucun DESIGN_GHOST ni DESIGN_GAP sur l'ensemble étendu (40 designs).
5. Pre-commit passe sans blocage encoding sur tous les nouveaux fichiers.
6. ADR `ADR-KG-CAUSAL-001-20260916` accepté pour débloquer les designs KG-CAUSAL.
7. ADR de gouvernance créé pour les designs opérationnels (chain-fluidity, autonomy-fluidity, conversation-aggregator, conversation-to-execution-bridge).

---

## Phases & preuves d'exécution (clôture 2026-08-24)

> Ajouté par l'audit de clôture GEN-011 : les livrables étaient produits mais non prouvés (réserve SUBALTERN_UNPROVEN du cascade_integrity_scanner).

- [x] **Phase A/B — 13 designs + ATOM-053 + registre + META** : vérification machine Test-Path → 13/13 designs OK, ATOM-053 présent, atoms_registry.yaml et META-DESIGN.md présents.
- [x] **Scan de couverture ARGUS** : design_coverage_scanner.py → **designs=76, H=0.9218, 0 DESIGN_GHOST / 0 DESIGN_GAP / 0 COLLISION** (57 DESIGN_ORPHAN INFO = chantier bridges résiduel tracé). Rapport JSON : ARGUS/reports/DESIGN_COVERAGE_20260824T003023Z.json.
- [x] **Intégrité cascade** : cascade_integrity_scanner.py --moc GEN-011 → ce fichier passe de SUBALTERN_UNPROVEN à prouvé (présente section).
- [x] **Section 9 ajoutée** : 14 livrables additionnels TDC + méta-KG identifiés, avec chemins, statuts et blocages gouvernance.
