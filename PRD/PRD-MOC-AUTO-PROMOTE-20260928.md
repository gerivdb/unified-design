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

| ID | Livrable | Chemin | Type | Statut |
|---|---|---|---|---|
| L1 | Moteur auto-promote | `scripts/auto_promote.py` | Créer | ✅ |
| L2 | Critères promotion ADR | `designs/auto-promote/adr-criteria.yaml` | Créer | ✅ |
| L3 | Critères promotion Design | `designs/auto-promote/design-criteria.yaml` | Créer | ✅ |
| L4 | Critères promotion INTENT | `designs/auto-promote/intent-criteria.yaml` | Créer | ✅ |
| L5 | Tests du moteur | `tests/test_auto_promote.py` | Créer | ✅ 3 passed |
| L6 | Hook pre-commit | `.kilocode/hooks/pre-commit-auto-promote.py` | Créer | ✅ |
| L7 | CLI integrate | `scripts/auto_design_cli.py promote` | Créer | ✅ |
| L8 | CI locale | `scripts/run_auto_promote_check.ps1` | Créer | ✅ |
| L9 | Documentation | `docs/auto-promote/README.md` | Créer | ✅ |

---

## 7. Critères d'acceptation

- [x] `python scripts/auto_design_cli.py promote --dry-run` retourne JSON valide — OK (2 INTENTS promouvables détectés)
- [x] `python scripts/auto_design_cli.py promote --apply` fonctionne — OK
- [x] `python scripts/auto_promote.py --dry-run` propose ≥ 5 promotions — OK
- [x] `python scripts/auto_promote.py --apply` applique les promotions sans erreur — OK
- [x] Rapport JSON généré avec détails des promotions — OK
- [x] Tests unitaires passent (`pytest tests/test_auto_promote.py`) — OK (3/3)
- [x] Politique `auto-promotion.yaml` respectée — OK
- [x] Aucune promotion non autorisée — OK

## 8. État actuel (2026-09-30)

### État d'avancement réel (dry-run causal 2026-09-30)

| ID | Livrable | Chemin | Statut | Preuve |
|---|---|---|---|---|
| L1 | Moteur auto-promote | `scripts/auto_promote.py` | ✅ Implémenté | 369 lignes, fonctions promote_adr/design/intent |
| L2 | Critères ADR | `designs/auto-promote/adr-criteria.yaml` | ✅ Implémenté | Critères formalisés |
| L3 | Critères Design | `designs/auto-promote/design-criteria.yaml` | ✅ Implémenté | Critères formalisés |
| L4 | Critères INTENT | `designs/auto-promote/intent-criteria.yaml` | ✅ Implémenté | Critères formalisés |
| L5 | Tests | `tests/test_auto_promote.py` | ✅ Implémenté | 3 passed |
| L6 | Hook pre-commit | `.kilocode/hooks/pre-commit-auto-promote.py` | ✅ Implémenté | Hook créé |
| L7 | CLI integrate | `scripts/auto_design_cli.py promote` | ✅ Implémenté | Subcommand promote fonctionnel |
| L8 | CI locale | `scripts/run_auto_promote_check.ps1` | ✅ Implémenté | Script PowerShell créé |
| L9 | Documentation | `docs/auto-promote/README.md` | ✅ Implémenté | README complet |

### Livrables complétés

| ID | Livrable | Chemin | Statut |
|---|---|---|---|
| L1 | Moteur auto-promote | `scripts/auto_promote.py` | ✅ |
| L2 | Critères ADR | `designs/auto-promote/adr-criteria.yaml` | ✅ |
| L3 | Critères Design | `designs/auto-promote/design-criteria.yaml` | ✅ |
| L4 | Critères INTENT | `designs/auto-promote/intent-criteria.yaml` | ✅ |
| L5 | Tests | `tests/test_auto_promote.py` | ✅ 3 passed |
| L6 | Hook pre-commit | `.kilocode/hooks/pre-commit-auto-promote.py` | ✅ |
| L7 | CLI integrate | `scripts/auto_design_cli.py promote` | ✅ |
| L8 | CI locale | `scripts/run_auto_promote_check.ps1` | ✅ |
| L9 | Documentation | `docs/auto-promote/README.md` | ✅ |

---

## 9. Dry-Run Causal Validation

**Date** : 2026-09-30T04:35:37+02:00

**Résultat** : ✅ PROD READY — 100% opérationnel

```
[DRY-RUN CAUSAL] Résultats:
  Total checks: 126
  Implemented: 126 (100.0%)
  Prod ready: 126 (100.0%)
  Target: 100%
```

## 10. Proof-of-Life

- [x] 2026-09-29T06:20:00+02:00 — Moteur `auto_promote.py` créé et testé
- [x] 2026-09-29T06:25:00+02:00 — Critères YAML créés
- [x] 2026-09-29T06:30:00+02:00 — Hook pre-commit créé
- [x] 2026-09-29T06:35:00+02:00 — Tests unitaires passent (3/3)
- [x] 2026-09-29T06:40:00+02:00 — CLI `auto_design_cli.py promote` intégrée
- [x] 2026-09-30T04:02:00+02:00 — `scripts/run_auto_promote_check.ps1` créé
- [x] 2026-09-30T04:02:00+02:00 — `docs/auto-promote/README.md` créé
- [x] 2026-09-30T04:35:00+02:00 — Dry-run causal : 126/126 prod ready (100%)

## 11. Références

- **Framework** : `PRD-MOC-INTEGRATION-FRAMEWORK-20260928.md`
- **CI Pipeline** : `PRD-MOC-CROSS-REPO-CI-PIPELINE-20260928.md`
- **Traceability** : `PRD-MOC-ADR-DESIGN-INTEGRATION-TRACEABILITY-20260928.md`
- **ADR** : `ADR/ADR-2026-09-28-auto-promote.md`
- **INTENT** : `INTENTS/INTENT-AUTO-PROMOTE-20260928.md`
- **MOC** : `MOC/MOC-AUTO-PROMOTE-20260928.md`
- **Rapport validation** : `reports/ACT-VALIDATION-AUTO-PROMOTE-20260930.md`

---

*Generated by governance-doc-writer skill — Pattern C*
