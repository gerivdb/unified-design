---
type: INTENT
version: "1.0.0"
date: "2026-09-19"
status: proposed
intent_hash: 0xINTENT_SAFE_ACTION_PATTERN_20260919
parent_prd: null
repo: "gerivdb/unified-design"
layer: "L0"
author: gerivdb
source_repo: gerivdb/unified-design
source_path: INTENTS/INTENT-2026-09-19-SAFE-ACTION-PATTERN.md
---

# INTENT — Intégration de PATRON-0 comme micro-design d'action universelle dans le MDU

> **Contexte** : Cet intent synthétise l'analyse d'extraction du design PATRON-0 (patron universel de toute action sûre en environnement incertain — 7 fonctions + 3 états + 1 invariant + 4 gènes) et propose son intégration comme design/atom/ADR dans le Meta-Design Unifié (MDU) de `unified-design`. Il documente la confrontation avec le MDU existant, les gaps identifiés, la proposition d'architecture cible, les livrables atomiques, le plan de commits, et les critères d'acceptation.

---

## 1. Contexte & Motivation

### 1.1 PATRON-0 — L'extraction

PATRON-0 est un **design universel** extrait de la traversée de rue, réinstancié sur le dev IA. Il formalise ce que toute action irréversible en environnement incertain exige :

```
[PROJECT]  1. PERCEVOIR      (multi-source, ordonné, redondant)
           2. ÉVALUER        (multi-axes, indépendants)
           3. SE_MODÉLISER   (capacité propre + incertitude propre)
           4. RÉSERVER       (marge de sûreté / plan de repli)
           5. VALIDER        (gate : les 4 précédents sont-ils suffisants ?)

[PROGRESS] 6. AGIR           (engagement, irréversible)
              + MONITORER    (invariants tenus pendant l'action)

[BILAN]    7. VALIDER_RÉEL   (succès constaté dans le monde, pas prédit)
              + ENREGISTRER  (mémoire → héritage)
```

**Invariant central** : *le succès n'est jamais déclaré avant la fin réelle de l'action.*

**4 gènes universels** :
1. **Pluralité** — une seule source de perception est toujours insuffisante
2. **Auto-modèle** — l'agent doit modéliser sa propre capacité et son incertitude
3. **Réserve** — toute action engage une marge (rollback, budget, plan de repli)
4. **Validation réelle** — le succès n'existe que constaté, jamais prédit

### 1.2 Le MDU comme cadre d'intégration

Le Meta-Design Unifié (`unified-design`) est l'atlas des invariants architecturaux de l'écosystème gerivdb. Il contient déjà :

- **Think/Do/Check Consciousness** (`ATOM-THINK-DO-CHECK-CONSCIOUSNESS`, `INTENT-ECOSYSTEM-CONSCIOUSNESS-THINK-DO-CHECK-2026-09-17`)
- **Gate Layers** (`ATOM-GATE-LAYERS`) — barrière de contrôle à 4 couches
- **External Verification Mandatory** (`ATOM-EXTERNAL-VERIFICATION-MANDATORY`) — "l'agent ne se relit pas"
- **Stop Condition** (`ATOM-STOP-CONDITION`) — condition d'arrêt explicite pour boucles
- **Confidence Threshold** (`ATOM-CONFIDENCE-THRESHOLD`) — seuil 0.6
- **Independent Sources Rule** (`ATOM-INDEPENDENT-SOURCES-RULE`) — 2 sources indépendantes
- **U-Model Agent-Ready Data** (`ATOM-UMODEL-AGENT-READY-DATA`) — modèle de données agent-ready
- **Delta Check** (`ATOM-DELTA-CHECK`) — vérification incrémentale
- **Carry Forward Principle** (`ATOM-CARRY-FORWARD-PRINCIPLE`) — travail valide reporté
- **Delivery Engine** (`designs/delivery-engine.yaml`) — workflow de delivery mutualisé
- **Chain Engineering** (`designs/chain-engineering.yaml`) — chaînage résilient
- **Approval Readiness** (`designs/approval-readiness.yaml`) — gate de validation avant merge

**Problématique** : Ces concepts existent dispersés. PATRON-0 les agrège en un **patron d'action universel** enforceable, avec une machine d'état explicite (PROJECT → PROGRESS → BILAN), une checklist de 7 fonctions, un invariant central, et des anti-patrons documentés.

---

## 2. Cartographie du MDU Existant (Confrontation)

### 2.1 Designs cognition / conscience existants

| Design | Version | Couverture actuelle |
|---|---|---|
| `consciousness` | 3.0.0 | État subjectif premier, agrégation de 26 tests d'intégration, 34 checks cross-repo, 6 tests ACT |
| `ecosystem-consciousness` | 1.0.0 | Conscience écosystémique ternaire Think/Do/Check, méthodologie quinquepartite |
| `approval-readiness` | 1.0.0 | Gate de validation : A0/A1/A2/A3, Proof-of-Life obligatoire |
| `delivery-engine` | 1.0.0 | Workflow de delivery mutualisé : build/test/package/audit |
| `chain-engineering` | 1.0.0 | Méta-design de chaînage : loop-engineering, circuit-breaker, conflict-resolver |
| `meta-coherence` | 2.0 | Cohérence multi-échelle cross-repo, 12 pathologies, ARGUS opérationnel |
| `context-engineering` | 1.0.0 | 5 critères : Relevance, Sufficiency, Isolation, Economy, Provenance |
| `agent-engineering-maturity` | 1.0.0 | Hiérarchie Prompt → Context → Harness → Loop → Graph → Specification |

### 2.2 Atoms méthodologiques existants

| Atom | Couverture actuelle |
|---|---|
| `ATOM-GATE-LAYERS` | Barrière de contrôle à 4 couches (L1 technique, L2 architecture, L3 gouvernance, L4 humain) |
| `ATOM-EXTERNAL-VERIFICATION-MANDATORY` | "L'agent ne se relit pas" — vérification externe obligatoire |
| `ATOM-STOP-CONDITION` | Condition d'arrêt explicite pour toute boucle d'ingénierie |
| `ATOM-CONFIDENCE-THRESHOLD` | Seuil de confiance 0.6 minimum pour décision/validation |
| `ATOM-INDEPENDENT-SOURCES-RULE` | 2 sources indépendantes requises pour décision critique |
| `ATOM-UMODEL-AGENT-READY-DATA` | Modèle de données unifié Alibaba UModel : 4 piliers Agent-Ready |
| `ATOM-DELTA-CHECK` | Delta Check : écart entre attendu et réel |
| `ATOM-CARRY-FORWARD-PRINCIPLE` | Carry Forward : travail valide reporté d'un run à l'autre |
| `ATOM-REJECT-WORK-PRINCIPLE` | Reject Work : rejet préférable à accommodation |
| `ATOM-DEEP-MIND-CO-SCIENTIST-RELIABILITY` | Fiabilité agents DeepMind Co-Scientist : vérification déterministe |

### 2.3 Gaps identifiés (ce que PATRON-0 apporte de nouveau)

| Gap PATRON-0 | État MDU actuel | Impact |
|---|---|---|
| **Machine d'état PROJECT → PROGRESS → BILAN** avec gate obligatoire | Think/Do/Check existe mais pas la transition formalisée comme gate pré-action | Actions engagées sans validation complète → échecs |
| **7 fonctions atomiques d'action** (PERCEVOIR → ÉVALUER → SE_MODÉLISER → RÉSERVER → VALIDER → AGIR+MONITORER → VALIDER_RÉEL+ENREGISTRER) | Concepts dispersés, pas agrégés en checklist enforceable | Pas de vérification mécanique que toutes les fonctions ont été remplies |
| **Fonction 3 — SE_MODÉLISER** (auto-modèle + incertitude propre) | Partiellement couvert par `umodel-agent-ready-data` | Obligation explicite pour l'agent de modéliser sa propre incertitude |
| **Invariant central** : *le succès n'est jamais déclaré avant la fin réelle* | Implicite dans `approval-readiness` (AR1 : [x] sans preuve = []) | Élévation au rang de loi génétique du MDU |
| **4 gènes universels** formalisés comme gènes de survie | Dispersés | Couche ontologique nouvelle : "ce ne sont pas des conventions, ce sont des gènes" |
| **Table des anti-patrons** (gène manquant → pathologie) | Absente | Outil de gouvernance nouveau : mapping défaillance → pathologie → correction |

**Verdict** : PATRON-0 n'est pas un doublon. C'est une **micro-design** qui rend opérationnels les concepts macro Think/Do/Check + gate-layers + approval-readiness via une checklist d'action universelle enforceable par CI/hooks.

---

## 3. Proposition d'Intégration

### 3.1 Architecture cible

```
safe-action-pattern (L0, À CRÉER)
├── inherits:
│   ├── chain-engineering      # séquence, circuit-breaker
│   ├── delivery-engine        # AGIR + MONITORER
│   ├── approval-readiness     # VALIDER_RÉEL + Proof-of-Life
│   └── think-do-check-consciousness  # macro PROJECT/DO/BILAN
├── depends_on:
│   ├── ATOM-GATE-LAYERS               # VALIDER gate
│   ├── ATOM-EXTERNAL-VERIFICATION-MANDATORY  # VALIDER_RÉEL
│   ├── ATOM-STOP-CONDITION            # RÉSERVER
│   ├── ATOM-CONFIDENCE-THRESHOLD      # ÉVALUER
│   ├── ATOM-INDEPENDENT-SOURCES-RULE  # PERCEVOIR (pluralité)
│   ├── ATOM-UMODEL-AGENT-READY-DATA   # SE_MODÉLISER
│   ├── ATOM-DELTA-CHECK               # VALIDER_RÉEL
│   └── ATOM-CARRY-FORWARD-PRINCIPLE   # ENREGISTRER
├── states: [PROJECT, PROGRESS, BILAN]
├── functions: [PERCEVOIR, EVALUER, SE_MODELISER, RESERVER, VALIDER, AGIR+MONITORER, VALIDER_REEL+ENREGISTRER]
├── invariant: "success never declared before real end"
├── genes: [pluralite, auto-modele, reserve, validation-reelle]
├── anti_patterns: [...]
└── cross_references:
    ├── GOVERNANCE-HUB (enforces)
    ├── CTULU (orchestrates)
    ├── DevTools (executes)
    └── ARGUS (audits)
```

### 3.2 Intégration dans `meta-design.yaml`

Le design `safe-action-pattern` sera enregistré dans `meta-design.yaml` :

```yaml
designs:
  - name: safe-action-pattern
    path: designs/safe-action-pattern.yaml
    version: '1.0.0'
    intent_hash: 0xDESIGN_SAFE_ACTION_PATTERN_20260919
    consumers: []
    profile: STANDARD

governance_atoms:
  - safe-action-gate
```

### 3.3 Intégration dans `META-DESIGN.md`

Ajouts :
- Dans `Designs enregistrés` : `safe-action-pattern | 1.0.0 | Patron universel d'action : 7 fonctions + 3 états + 1 invariant`
- Dans `Atoms L0-L3` : `safe-action-gate | Atom | Gate d'action universelle : PROJECT → PROGRESS → BILAN`

---

## 4. Livrables Atomiques

| ID | Livrable | Chemin cible | Type |
|---|---|---|---|
| L1 | Design `safe-action-pattern` | `designs/safe-action-pattern.yaml` | Nouveau |
| L2 | Atom `safe-action-gate` | `atoms/safe-action-gate.md` | Nouveau |
| L3 | ADR backing | `ADR/ADR-2026-09-19-SAFE-ACTION-PATTERN.md` | Nouveau |
| L4 | Mise à jour `META-DESIGN.md` | `META-DESIGN.md` | Modification |
| L5 | Mise à jour `meta-design.yaml` | `meta-design.yaml` | Modification |

---

## 5. Plan de Commits (Atomic)

| Commit | Fichiers | Description |
|---|---|---|
| `feat(design): add safe-action-pattern` | `designs/safe-action-pattern.yaml` | Design PATRON-0 : 7 fonctions + 3 états + 1 invariant + 4 gènes |
| `feat(atom): add safe-action-gate` | `atoms/safe-action-gate.md` | Atom enforceable : states, functions, rules, anti-patterns |
| `docs(adr): add SAFE-ACTION-PATTERN ADR` | `ADR/ADR-2026-09-19-SAFE-ACTION-PATTERN.md` | ADR backing pour adoption PATRON-0 |
| `docs(meta-design): register safe-action-pattern` | `META-DESIGN.md`, `meta-design.yaml` | Enregistrement dans MDU |

---

## 6. Critères d'Acceptation

1. Le design `safe-action-pattern.yaml` parse en YAML valide, respecte le schéma `meta-design.yaml`, et passe `gerivdb design validate --strict`.
2. L'atom `safe-action-gate.md` est créé et référencé dans `META-DESIGN.md` et `meta-design.yaml`.
3. L'ADR `ADR-2026-09-19-SAFE-ACTION-PATTERN` est créée avec frontmatter valide.
4. Aucune violation DAG n'est introduite (vérifier `depends_on` et `inherits`).
5. Les pre-commit hooks (`design-validate`, `frontmatter-guardian`, `check-yaml`) passent sur l'ensemble des fichiers modifiés.
6. Le mapping PATRON-0 → MDU est documenté : chaque fonction PATRON-0 pointe vers un atom/design MDU existant.
7. Les anti-patrons PATRON-0 sont intégrés dans l'atom `safe-action-gate`.

---

## 7. Références

| Document | Emplacement |
|---|---|
| PATRON-0 source | Fourni par l'utilisateur (extraction universelle) |
| MDU | `D:\DO\WEB\TOOLS\L0-CANON\unified-design\META-DESIGN.md` |
| Meta-Design YAML | `D:\DO\WEB\TOOLS\L0-CANON\unified-design\meta-design.yaml` |
| Design chain-engineering | `D:\DO\WEB\TOOLS\L0-CANON\unified-design\designs\chain-engineering.yaml` |
| Design delivery-engine | `D:\DO\WEB\TOOLS\L0-CANON\unified-design\designs\delivery-engine.yaml` |
| Design approval-readiness | `D:\DO\WEB\TOOLS\L0-CANON\unified-design\designs\approval-readiness.yaml` |
| Atom gate-layers | `D:\DO\WEB\TOOLS\L0-CANON\unified-design\atoms\ATOM-GATE-LAYERS.md` |
| Atom external-verification-mandatory | `D:\DO\WEB\TOOLS\L0-CANON\unified-design\atoms\ATOM-EXTERNAL-VERIFICATION-MANDATORY.md` |
| Atom stop-condition | `D:\DO\WEB\TOOLS\L0-CANON\unified-design\atoms\ATOM-STOP-CONDITION.md` |
| Atom confidence-threshold | `D:\DO\WEB\TOOLS\L0-CANON\unified-design\atoms\ATOM-CONFIDENCE-THRESHOLD.md` |
| Atom independent-sources-rule | `D:\DO\WEB\TOOLS\L0-CANON\unified-design\atoms\ATOM-INDEPENDENT-SOURCES-RULE.md` |
| Atom umodel-agent-ready-data | `D:\DO\WEB\TOOLS\L0-CANON\unified-design\atoms\ATOM-UMODEL-AGENT-READY-DATA.md` |
| Atom delta-check | `D:\DO\WEB\TOOLS\L0-CANON\unified-design\atoms\ATOM-DELTA-CHECK.md` |
| Atom carry-forward-principle | `D:\DO\WEB\TOOLS\L0-CANON\unified-design\atoms\ATOM-CARRY-FORWARD-PRINCIPLE.md` |
| Atom think-do-check-consciousness | `D:\DO\WEB\TOOLS\L0-CANON\unified-design\atoms\ATOM-THINK-DO-CHECK-CONSCIOUSNESS.md` |
| Atom methodological-bon-sens | `D:\DO\WEB\TOOLS\L0-CANON\unified-design\atoms\ATOM-METHODOLOGICAL-BON-SENS.md` |
| ADR Think/Do/Check | `D:\DO\WEB\TOOLS\L0-CANON\GOVERNANCE-HUB\ADR\ADR-2026-09-12-001-THINK-DO-CHECK-ARCHITECTURE.md` |
| ADR Governance Gate | `D:\DO\WEB\TOOLS\L0-CANON\GOVERNANCE-HUB\ADR\ADR-2026-06-07-001-ADR-GOVERNANCE-GATE.md` |

---

## 8. Intentions

- [[INTENT-008]]
- [[INTENT-021]]
- [[INTENT-191]]

---

## 9. Livrables et documents subalternes

| ID | Type | Chemin | Statut |
|---|---|---|---|
| 1 | PRD-MOC | `PRD/PRD-MOC-SAFE-ACTION-PATTERN-20260919.md` | 🟡 Draft |
| 2 | MOC | `MOC/MOC-SAFE-ACTION-PATTERN-20260919.md` | 🟡 Draft |
| 3 | Design | `designs/safe-action-pattern.yaml` | 🟡 Draft |
| 4 | Atom | `atoms/safe-action-gate.md` | 🟡 Draft |
| 5 | ADR | `ADR/ADR-2026-09-19-SAFE-ACTION-PATTERN.md` | 🟡 Draft |
| 6 | Doc MDU | `META-DESIGN.md` | ⏳ En attente d'enregistrement |
| 7 | Schema MDU | `meta-design.yaml` | ⏳ En attente d'enregistrement |

---

## 10. Proof-of-Life

- [x] 2026-09-19T20:52:20+02:00 — Création INTENT PATRON-0 / safe-action-pattern
- [x] 2026-09-19T20:52:20+02:00 — Création PRD-MOC PATRON-0 / safe-action-pattern
- [x] 2026-09-19T20:52:20+02:00 — Création MOC PATRON-0 / safe-action-pattern
- [x] 2026-09-19T20:52:20+02:00 — Création design `safe-action-pattern.yaml`
- [x] 2026-09-19T20:52:20+02:00 — Création atom `safe-action-gate.md`
- [x] 2026-09-19T20:52:20+02:00 — Création ADR `ADR-2026-09-19-SAFE-ACTION-PATTERN.md`
- [x] 2026-09-19T20:52:20+02:00 — Mise à jour `META-DESIGN.md` et `meta-design.yaml`
- [ ] Validation CI — `gerivdb design validate --strict` PASS
- [ ] Hooks — pre-commit pass sur tous les fichiers

---

## 11. Références

| Document | Emplacement |
|---|---|
| PATRON-0 source | Fourni par l'utilisateur (extraction universelle) |
| MDU | `D:\DO\WEB\TOOLS\L0-CANON\unified-design\META-DESIGN.md` |
| Meta-Design YAML | `D:\DO\WEB\TOOLS\L0-CANON\unified-design\meta-design.yaml` |
| Design chain-engineering | `D:\DO\WEB\TOOLS\L0-CANON\unified-design\designs\chain-engineering.yaml` |
| Design delivery-engine | `D:\DO\WEB\TOOLS\L0-CANON\unified-design\designs\delivery-engine.yaml` |
| Design approval-readiness | `D:\DO\WEB\TOOLS\L0-CANON\unified-design\designs\approval-readiness.yaml` |
| Atom gate-layers | `D:\DO\WEB\TOOLS\L0-CANON\unified-design\atoms\ATOM-GATE-LAYERS.md` |
| Atom external-verification-mandatory | `D:\DO\WEB\TOOLS\L0-CANON\unified-design\atoms\ATOM-EXTERNAL-VERIFICATION-MANDATORY.md` |
| Atom stop-condition | `D:\DO\WEB\TOOLS\L0-CANON\unified-design\atoms\ATOM-STOP-CONDITION.md` |
| Atom confidence-threshold | `D:\DO\WEB\TOOLS\L0-CANON\unified-design\atoms\ATOM-CONFIDENCE-THRESHOLD.md` |
| Atom independent-sources-rule | `D:\DO\WEB\TOOLS\L0-CANON\unified-design\atoms\ATOM-INDEPENDENT-SOURCES-RULE.md` |
| Atom umodel-agent-ready-data | `D:\DO\WEB\TOOLS\L0-CANON\unified-design\atoms\ATOM-UMODEL-AGENT-READY-DATA.md` |
| Atom delta-check | `D:\DO\WEB\TOOLS\L0-CANON\unified-design\atoms\ATOM-DELTA-CHECK.md` |
| Atom carry-forward-principle | `D:\DO\WEB\TOOLS\L0-CANON\unified-design\atoms\ATOM-CARRY-FORWARD-PRINCIPLE.md` |
| Atom think-do-check-consciousness | `D:\DO\WEB\TOOLS\L0-CANON\unified-design\atoms\ATOM-THINK-DO-CHECK-CONSCIOUSNESS.md` |
| Atom methodological-bon-sens | `D:\DO\WEB\TOOLS\L0-CANON\unified-design\atoms\ATOM-METHODOLOGICAL-BON-SENS.md` |
| ADR Think/Do/Check | `D:\DO\WEB\TOOLS\L0-CANON\GOVERNANCE-HUB\ADR\ADR-2026-09-12-001-THINK-DO-CHECK-ARCHITECTURE.md` |
| ADR Governance Gate | `D:\DO\WEB\TOOLS\L0-CANON\GOVERNANCE-HUB\ADR\ADR-2026-06-07-001-ADR-GOVERNANCE-GATE.md` |

---

## 9. Livrables et documents subalternes

| ID | Type | Chemin | Statut |
|---|---|---|---|
| 1 | PRD-MOC | `PRD/PRD-MOC-SAFE-ACTION-PATTERN-20260919.md` | 🟡 Draft |
| 2 | MOC | `MOC/MOC-SAFE-ACTION-PATTERN-20260919.md` | 🟡 Draft |
| 3 | Design | `designs/safe-action-pattern.yaml` | 🟡 Draft |
| 4 | Atom | `atoms/safe-action-gate.md` | 🟡 Draft |
| 5 | ADR | `ADR/ADR-2026-09-19-SAFE-ACTION-PATTERN.md` | 🟡 Draft |
| 6 | Doc MDU | `META-DESIGN.md` | ⏳ En attente d'enregistrement |
| 7 | Schema MDU | `meta-design.yaml` | ⏳ En attente d'enregistrement |

---

## 10. Références

| Document | Emplacement |
|---|---|
| PATRON-0 source | Fourni par l'utilisateur (extraction universelle) |
| MDU | `D:\DO\WEB\TOOLS\L0-CANON\unified-design\META-DESIGN.md` |
| Meta-Design YAML | `D:\DO\WEB\TOOLS\L0-CANON\unified-design\meta-design.yaml` |
| Design chain-engineering | `D:\DO\WEB\TOOLS\L0-CANON\unified-design\designs\chain-engineering.yaml` |
| Design delivery-engine | `D:\DO\WEB\TOOLS\L0-CANON\unified-design\designs\delivery-engine.yaml` |
| Design approval-readiness | `D:\DO\WEB\TOOLS\L0-CANON\unified-design\designs\approval-readiness.yaml` |
| Atom gate-layers | `D:\DO\WEB\TOOLS\L0-CANON\unified-design\atoms\ATOM-GATE-LAYERS.md` |
| Atom external-verification-mandatory | `D:\DO\WEB\TOOLS\L0-CANON\unified-design\atoms\ATOM-EXTERNAL-VERIFICATION-MANDATORY.md` |
| Atom stop-condition | `D:\DO\WEB\TOOLS\L0-CANON\unified-design\atoms\ATOM-STOP-CONDITION.md` |
| Atom confidence-threshold | `D:\DO\WEB\TOOLS\L0-CANON\unified-design\atoms\ATOM-CONFIDENCE-THRESHOLD.md` |
| Atom independent-sources-rule | `D:\DO\WEB\TOOLS\L0-CANON\unified-design\atoms\ATOM-INDEPENDENT-SOURCES-RULE.md` |
| Atom umodel-agent-ready-data | `D:\DO\WEB\TOOLS\L0-CANON\unified-design\atoms\ATOM-UMODEL-AGENT-READY-DATA.md` |
| Atom delta-check | `D:\DO\WEB\TOOLS\L0-CANON\unified-design\atoms\ATOM-DELTA-CHECK.md` |
| Atom carry-forward-principle | `D:\DO\WEB\TOOLS\L0-CANON\unified-design\atoms\ATOM-CARRY-FORWARD-PRINCIPLE.md` |
| Atom think-do-check-consciousness | `D:\DO\WEB\TOOLS\L0-CANON\unified-design\atoms\ATOM-THINK-DO-CHECK-CONSCIOUSNESS.md` |
| Atom methodological-bon-sens | `D:\DO\WEB\TOOLS\L0-CANON\unified-design\atoms\ATOM-METHODOLOGICAL-BON-SENS.md` |
| ADR Think/Do/Check | `D:\DO\WEB\TOOLS\L0-CANON\GOVERNANCE-HUB\ADR\ADR-2026-09-12-001-THINK-DO-CHECK-ARCHITECTURE.md` |
| ADR Governance Gate | `D:\DO\WEB\TOOLS\L0-CANON\GOVERNANCE-HUB\ADR\ADR-2026-06-07-001-ADR-GOVERNANCE-GATE.md` |
