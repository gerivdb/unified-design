---
type: ADR
status: proposed
date: "2026-07-15"
intent_hash: 0xADR_019_PHASE3_INCREMENTAL_20260715
---

# ADR-019 — Phase 3 : Incrémentalité, Héritage avancé, Loop Engineering Systémique

## Contexte

Le MDU (MetaCluster Design Unified) a atteint la Phase 2 avec succès :
- Méta-design v2 avec capacités et détection de boucles
- Extraction des patterns constitutionnels de GOVERNANCE-HUB
- Générateur industrialisé
- Scan multi-strates L0-L4

Cependant, pour une adoption à grande échelle, nous avons besoin de :
1. **Incrémentalité** : Les designs doivent pouvoir évoluer sans casser les descendants
2. **Héritage multiple** : Un design peut hériter de plusieurs parents
3. **Loop Engineering** : Outil de simulation prédictive des boucles
4. **Industrialisation KIVA-CLI** : Pipeline CI/CD autonome

## Décision

Implémenter la Phase 3 avec les composants suivants :

### 1. Schéma étendu `design.yaml`

Ajout des champs :
- `design_version` : Versionnement sémantique (major/minor/patch)
- `deprecated_capabilities` : Liste des capacités à déprécier
- `priority_resolution` : Stratégie de résolution des conflits
- `deprecation_period_days` : Période de transition (défaut: 90j)

### 2. Simulateur de boucles (`loop_engine/simulate.py`)

Fonctionnalités :
- Prédiction des cycles créés par un nouveau design
- Détection des conflits de capacités
- Calcul du score d'incrémentalité (0-100)
- Suggestions de remediation

### 3. Bibliothèque de patterns (`loop_engine/patterns/`)

Patterns documentés :
- `virtuous-cycle.yaml` : Boucles autorégulatrices
- `deadlock-pattern.yaml` : Boucles bloquantes

### 4. Pipeline KIVA-CLI (`pipelines/mdu-validation.yaml`)

7 étapes :
1. Pré-flight (vérification structure)
2. Validation YAML
3. Détection de boucles
4. Validation de l'héritage
5. Simulation MDU
6. Génération du rapport
7. Alertes HITL

## Conséquences

### Positives
- **Prédictibilité** : Les impacts sont anticipés avant création
- **Sécurité** : Les conflits sont détectés automatiquement
- **Scalabilité** : L'héritage multiple permet des designs plus expressifs
- **Autonomie** : KIVA-CLI remplace GitHub Actions pour une validation locale

### Risques
- **Complexité** : L'héritage multiple peut être difficile à comprendre
- **Performance** : La simulation ajoute une étape de vérification
- **Maintenance** : Les patterns de boucles doivent être maintenus

## Alternatives considérées

1. **Rester sur GitHub Actions** — Rejeté : besoin d'autonomie locale
2. **Héritage simple uniquement** — Rejeté : insuffisant pour les designs complexes
3. **Pas de simulateur** — Rejeté : perte de prédictibilité

## Références

- ADR-016-loop-engine
- ADR-CONNARD-001-connard-design-protocol
- ADR-2026-06-28-001-logical-architecture-n1-n4
- INTENT-016: MetaCluster Unified Design (MDU) Magistral
- EPIC-001: Conversation Mastery

## Statut

- **Date** : 2026-07-15
- **Statut** : proposed
- **Prochaine étape** : Revues par l'équipe architecturale