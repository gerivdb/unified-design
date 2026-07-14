---
type: META-DESIGN
status: active
version: "1.0.0"
date: "2026-07-15"
intent_hash: 0xMDU_UNIFIED_DESIGN_20260715
---

# META-DESIGN — Unified Design Atlas

> **Le Gentil** — L'atlas global des invariants architecturaux de l'écosystème gerivdb

## 1. Vision

Le **Méta-Design (MDU)** est la **constitution architecturale** de l'écosystème gerivdb. Il définit les invariants topo-logiques qui gouvernent l'interaction entre les couches, les patterns, et les agents.

### Le Principe Fondamental

> **Tout système conscient doit être observable, orchestrable, optimisable, et validifiable.**

Les quatre piliers du MDU forment un ensemble fermé de propriétés invariants:

```
┌──────────────────────────────────────────────────────────────┐
│                    META-DESIGN ATLAS                         │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────┐  ┌─────────────────┐  ┌────────────┐ │
│  │   SONAR-DRIVEN  │  │ TRIADIC COMPOUND│  │ MORPHOHDL  │ │
│  │      DESIGN     │  │       EYE       │  │   GROWTH   │ │
│  │  (Observabilité)│  │   (Orchestration│  │(Optimisation│ │
│  └─────────────────┘  │      Agents)    │  │   Matérielle)│ │
│                        └─────────────────┘  └────────────┘ │
│                                   │                         │
│                                   ▼                         │
│                    ┌─────────────────────────┐              │
│                    │      CONNARD DESIGN     │              │
│                    │     (Contrôle Qualité)  │              │
│                    └─────────────────────────┘              │
│                                   │                         │
│                                   ▼                         │
│                  ┌─────────────────────────────┐            │
│                  │     CI/CD / PLIX SUITE      │            │
│                  │   (Intégration en production)            │
│                  └─────────────────────────────┘            │
└──────────────────────────────────────────────────────────────┘
```

## 2. Les Quatre Piliers

### 2.1 Sonar-Driven Design (SDD) — Observabilité

**Rôle** : Écoute active du système via émission cyclique d'impulsions (pings).

**Invariants** :
- **Ping/Echo** : Message minimal avec ID unique + timestamp → réponse avec métadonnées
- **Sonar Map** : Structure partagée cartographiant l'état du système en temps réel
- **PRF** : Pulse Repetition Frequency — fréquence d'émission des pings
- **Latence P99** : ≤ 45ms pour toute opération critique
- **Puissance** : ≤ 12W par inférence

**Agents associés** : NEXUS (push métriques), ECOYSTEM (alertes), BRAIN (bus partagé)

### 2.2 Triadic Compound Eye (TCE) — Architecture d'Agents

**Rôle** : Orchestration cognitive via architectures en triade (Mixture of Experts).

**Invariants** :
- **Triade C-E-Obs** : Communication → Exécution → Observation (cycle complet)
- **Swarm Intelligence** : Agents autonomes qui évoluent via feedback
- **Mémoire Hiérarchique** : NEXUS comme mémoire principale, HERMES comme mémoire secondaire
- **HITL Gate** : Toute modification critique passe par Human-in-the-Loop

**Agents associés** : FLUENCE (orchestration), CANDIDATOR (gestion), KRONOS (qualification), IRIS (capteurs)

### 2.3 MorphoHDL Anamorphic Growth (MAG) — Optimisation Matérielle

**Rôle** : Croissance de circuits ternaires via anamorphose adaptative.

**Invariants** :
- **Croissance Expérimentale** : Les circuits apprennent et s'adaptent
- **Base 243 (3^5)** : Structure ternaire native pour l'inférence
- **RVBA** : Répartition des canaux de couleur sémantique
- **O(1) Index** : Accès constant via index ternaire

**Agents associés** : LADYBIRD (attention), PIANO (opérateur T), KEEL (encodage)

### 2.4 Connard Design (CD) — Contrôle Qualité Exécutoire

**Rôle** : Dissipateur d'entropie qui élimine les designs qui gaspillent de l'énergie.

**Invariants** :
- **Héritage** : Profondeur ≤ 3 niveaux
- **Latence P99** : ≤ 45ms
- **Puissance** : ≤ 12W/inférence
- **Roast Automatique** : Feedback négatif constructif
- **Wall of Shame** : Liste des violations graves

**Agents associés** : CoPaw (qualité), SABRE (sécurité), Alfred (mémoire)

## 3. Règles Transversales

### 3.1 Règle de Composition

> **Un composant ne doit jamais dépendre de plus de 3 niveaux d'abstraction supérieure.**

Si la profondeur dépendance > 3 → le composant est "déchetable" → Wall of Shame.

### 3.2 Règle de Latence

> **Toute opération critique doit avoir une latence P99 ≤ 45ms.**

Si latence > 45ms → roast automatique + alerte NEXUS.

### 3.3 Règle de Puissance

> **Chaque inférence ne doit pas dépasser 12W.**

Si puissance > 12W → optimisation forcée par PIANO.

### 3.4 Règle de Observation

> **Tout système critique doit être observable via ping/echo.**

Si système non observable → ajout de probes Sonar.

### 3.5 Règle de Validation

> **Toute modification doit passer par le validateur Connard.**

Commandes :
```bash
gerivdb connard validate <path>
gerivdb connard roast <path>
gerivdb connard watch <path>
```

## 4. Architecture de Gouvernance

```
┌─────────────────────────────────────────────────────────────────────┐
│                        L0 - CANONICAL LAYERS                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────┐   │
│  │   GOVERNANCE    │  │    ONTOLOGY     │  │      BRAIN          │   │
│  │      HUB        │  │                 │  │                     │   │
│  │ (Règles, ADR,   │  │ (Dictionnaire,  │  │ (Mémoire cognitive, │   │
│  │  Registres)     │  │  Ontologies)    │  │  MessageBus)        │   │
│  └─────────────────┘  └─────────────────┘  └─────────────────────┘   │
│                                                                       │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────┐   │
│  │   UNIFIED       │  │    CONNARD      │  │     NEXUS           │   │
│  │   DESIGN        │  │    DESIGN       │  │                     │   │
│  │ (MDU - Meta-    │  │ (Validation,    │  │ (Orchestration,     │   │
│  │  Design Atlas)  │  │  Roast, Wall)   │  │  WAL, Métriques)    │   │
│  └─────────────────┘  └─────────────────┘  └─────────────────────┘   │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

## 5. Validation

Le MDU est validé par :

1. **ADR-012** — Protocol de validation métacognitive
2. **meta-design.yaml** — Schéma de validation YAML
3. **gerivdb meta validate** — Commande CLI

## 6. Références

- **ADR** : ADR-012-meta-design-validation-protocol
- **ADR** : ADR-2026-06-28-001-logical-architecture-n1-n4
- **ADR** : ADR-CONNARD-001-connard-design-protocol
- **INTENT** : INT-CONNARD-001
- **EPIC** : EPIC-CONNARD-001

## 7. Changements

| Version | Date | Description |
|---------|------|-------------|
| 1.0.0 | 2026-07-15 | Version initiale — Migration depuis REPO-STANDARDS |