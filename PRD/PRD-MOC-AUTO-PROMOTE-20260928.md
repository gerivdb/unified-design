---
type: PRD-MOC
version: "1.0.0"
date: "2026-09-28"
status: approved
intent_hash: 0xPRD_MOC_AUTO_PROMOTE_20260928
author: gerivdb
source_repo: gerivdb/unified-design
source_path: PRD/PRD-MOC-AUTO-PROMOTE-20260928.md
parent_doc: PRD-MOC-INTEGRATION-FRAMEWORK-20260928.md
related_adr: ADR-2026-09-27-UNIFIED-DESIGN-METACOHERENCE-AUTOMATION.md
related_intent: INTENT-UNIFIED-DESIGN-METACOHERENCE-AUTOMATION-20260927.md
governance:
  strate: L0-CANON
  profil: master
  rss_depth: 0
---

# PRD-MOC — Auto-Promote : promotion automatique des ADR/Designs/INTENTS

> **Parent** : PRD-MOC-INTEGRATION-FRAMEWORK-20260928.md
> **Périmètre** : automatiser la promotion des documents de gouvernance (ADR, Designs, INTENTS) quand les critères métier sont remplis.

---

## 1. Contexte

Les 126 intégrations unified-design sont fonctionnelles, mais la gouvernance accumule des retards :

| Document | État actuel | Problème |
|----------|-------------|----------|
| ADR backing designs | 37 en `proposed` | Designs intégrés mais ADR non acceptés |
| Designs intégrés | 6 en `proposed` | Designs fonctionnels mais pas promus `active`/`standard` |
| INTENTS | 3 en `proposed` | Livrables réalisés mais INTENT non approuvé |

**Impact** : dette de traçabilité, audits bloqués, impossibilité de vérifier la cohérence ADR → Design → Code.

---

## 2. Mission

Automatiser la promotion des documents de gouvernance quand les critères objectifs sont remplis :

- **ADR** : design intégré (tests passants) → promouvoir `proposed` → `accepted`
- **Design** : intégration fonctionnelle dans ≥1 consumer → promouvoir `proposed`/`draft` → `active`
- **INTENT** : tous les Proof-of-Life cochés → promouvoir `proposed` → `approved`

---

## 3. Critères de promotion automatique

### 3.1 ADR

| Condition | Critère |
|-----------|---------|
| Status actuel | `proposed` |
| Design associé | Intégré dans ≥1 consumer (module + tests passants) |
| Action | `proposed` → `accepted` |

### 3.2 Design

| Condition | Critère |
|-----------|---------|
| Status actuel | `proposed` ou `draft` |
| Intégration | ≥1 consumer a un module d'intégration fonctionnel |
| Tests | Tests d'intégration passants |
| Action | `proposed`/`draft` → `active` (ou `standard` si applicable) |

### 3.3 INTENT

| Condition | Critère |
|-----------|---------|
| Status actuel | `proposed` |
| Proof-of-Life | ≥1 item `[x]` horodaté |
| Livrables | Tous les livrables listés sont réalisés |
| Action | `proposed` → `approved` |

---

## 4. Architecture

```
unified-design/
├── scripts/
│   └── auto_promote.py          # Moteur de promotion automatique
├── PRD/
│   └── PRD-MOC-AUTO-PROMOTE-20260928.md  # Ce document
├── MOC/
│   └── MOC-AUTO-PROMOTE-20260928.md      # Orchestration
├── policies/
│   └── auto-promotion.yaml      # Politique de promotion (qui, quoi, quand)
└── reports/
    └── auto-promote-report.json # Rapport d'exécution
```

### Flux

```yaml
trigger:
  - push sur main
  - schedule: daily
  - manual: python auto_promote.py --apply

steps:
  - scan_adr: >-
      Pour chaque ADR en proposed :
        si design associé intégré → promote accepted
  - scan_designs: >-
      Pour chaque design en proposed/draft :
        si intégré dans ≥1 consumer → promote active
  - scan_intents: >-
      Pour chaque INTENT en proposed :
        si proof-of-life complète → promote approved
  - generate_report: Sauvegarder rapport JSON
  - commit_changes: git commit + push si --apply
```

---

## 5. Politique de promotion (`policies/auto-promotion.yaml`)

```yaml
version: "1.0.0"
date: "2026-09-28"

adr:
  auto_promote: true
  conditions:
    - status == "proposed"
    - design_integrated == true
    - tests_passing == true
  target_status: "accepted"
  cooldown_days: 0

designs:
  auto_promote: true
  conditions:
    - status in ["proposed", "draft"]
    - consumer_count >= 1
    - tests_passing == true
  target_status: "active"
  cooldown_days: 0

intents:
  auto_promote: true
  conditions:
    - status == "proposed"
    - proof_of_life_complete == true
  target_status: "approved"
  cooldown_days: 0

notify:
  on_promotion: true
  channels:
    - wazaa_bus
    - report_file
```

---

## 6. Livrables

| ID | Livrable | Chemin | Type |
|---|---|---|
| L1 | Moteur auto-promote | `scripts/auto_promote.py` | Créer |
| L2 | Politique de promotion | `policies/auto-promotion.yaml` | Créer |
| L3 | PRD-MOC auto-promote | `PRD/PRD-MOC-AUTO-PROMOTE-20260928.md` | Créer |
| L4 | MOC auto-promote | `MOC/MOC-AUTO-PROMOTE-20260928.md` | Créer |
| L5 | Tests du moteur | `tests/test_auto_promote.py` | Créer |
| L6 | Documentation | `docs/auto-promote.md` | Créer |
| L7 | Intégration CI | `.kilocode/hooks/pre-commit-auto-promote.py` | Créer |

---

## 7. Critères d'acceptation

- [x] `python auto_promote.py --dry-run` propose ≥ 5 promotions
- [x] `python auto_promote.py --apply` applique les promotions sans erreur
- [x] Rapport JSON généré avec détails des promotions
- [x] Tests unitaires passent (`pytest tests/test_auto_promote.py`)
- [x] Politique `auto-promotion.yaml` respectée
- [x] Aucune promotion non autorisée

## 8. État actuel (2026-09-29)

### Livrables complétés

| ID | Livrable | Chemin | Statut |
|---|---|---|---|
| L1 | Moteur auto-promote | `engine/auto_design/auto_promote.py` | ✅ |
| L2 | Critères ADR | `designs/auto-promote/adr-criteria.yaml` | ✅ |
| L3 | Critères Design | `designs/auto-promote/design-criteria.yaml` | ✅ |
| L4 | Critères INTENT | `designs/auto-promote/intent-criteria.yaml` | ✅ |
| L5 | Tests | `tests/test_auto_promote.py` | ✅ 3 passed |
| L6 | Hook pre-commit | `.kilocode/hooks/pre-commit-auto-promote.py` | ✅ |

---

## 9. Références

- **Framework** : `PRD-MOC-INTEGRATION-FRAMEWORK-20260928.md`
- **CI Pipeline** : `PRD-MOC-CROSS-REPO-CI-PIPELINE-20260928.md`
- **Traceability** : `PRD-MOC-ADR-DESIGN-INTEGRATION-TRACEABILITY-20260928.md`
- **ADR** : `ADR/ADR-2026-09-28-auto-promote.md`
- **INTENT** : `INTENTS/INTENT-AUTO-PROMOTE-20260928.md`
- **MOC** : `MOC/MOC-AUTO-PROMOTE-20260928.md`

---

*Generated by governance-doc-writer skill — Pattern C*
