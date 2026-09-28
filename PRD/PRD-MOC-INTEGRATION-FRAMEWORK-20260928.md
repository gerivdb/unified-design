---
type: PRD-MOC
version: "1.0.0"
date: "2026-09-28"
status: approved
intent_hash: 0xPRD_MOC_INTEGRATION_FRAMEWORK_20260928
author: gerivdb
source_repo: gerivdb/unified-design
source_path: PRD/PRD-MOC-INTEGRATION-FRAMEWORK-20260928.md
parent_doc: PRD-MOC-UNIFIED-DESIGN-CONSUMERS-REGISTRY-20260928.md
related_adr: ADR-2026-09-19-SAFE-ACTION-PATTERN.md
related_intent: INTENT-2026-09-19-SAFE-ACTION-PATTERN.md
related_moc: MOC-INTEGRATION-FRAMEWORK-20260928.md
governance:
  strate: L0-CANON
  profil: master
  rss_depth: 0
---

# PRD-MOC — INTEGRATION FRAMEWORK : pattern d'intégration réutilisable consumer/design

> **Parent** : PRD-MOC-UNIFIED-DESIGN-CONSUMERS-REGISTRY-20260928.md
> **Périmètre** : création d'un framework d'intégration réutilisable pour appliquer les designs `unified-design` dans les repos consumers.

---

## 1. Contexte et évaluation d'utilité

### Constat

| Métrique | Valeur | Statut |
|----------|--------|--------|
| Designs déclarés | 126 | ✅ |
| Implémentations standalone | 126 | ✅ |
| Intégrations fonctionnelles | 1/126 (KIVA-CLI safe-action-pattern) | ⚠️ |
| Consumers avec hook pre-commit | 14/14 | ✅ |
| Tests unitaires intégration | 2 (KIVA-CLI seulement) | ⚠️ |

**Problème** : Les 126 implémentations existent comme modules standalone dans `PRD/` des consumers, mais ne sont pas importées/utilisées dans le code métier. Les designs sont déclarés mais pas appliqués.

### Évaluation d'utilité

| Composant | Utilité | Impact | Effort | Justification |
|-----------|---------|--------|--------|---------------|
| Framework d'intégration réutilisable | ⭐⭐⭐⭐⭐ | P0 | Moyen | Évite de réinventer l'intégration pour chaque consumer/design |
| Pattern d'injection design → consumer | ⭐⭐⭐⭐⭐ | P0 | Faible | Rend les designs enforceable |
| Tests d'intégration standardisés | ⭐⭐⭐⭐ | P1 | Faible | Vérifie que le design est bien appliqué |
| Documentation d'intégration | ⭐⭐⭐ | P1 | Faible | Guide les consumers |

**Verdict** : Framework d'intégration = P0. Effort moyen, valeur critique. Sans framework, chaque intégration est un one-off qui ne scale pas.

---

## 2. Mission

Créer un framework d'intégration réutilisable qui standardise l'application des designs `unified-design` dans les repos consumers.

---

## 3. Livrables

| ID | Livrable | Chemin cible | Type |
|---|---|---|---|
| L1 | Design `integration-framework` | `designs/integration-framework/design.yaml` | Créer |
| L2 | Primitive `integration-framework-primitive` | `primitives/integration-framework-primitive.yaml` | Créer |
| L3 | Module Python réutilisable | `tools/integration_framework.py` | Créer |
| L4 | Template d'intégration | `templates/integration-template.py` | Créer |
| L5 | Tests du framework | `tests/test_integration_framework.py` | Créer |
| L6 | Documentation | `docs/integration-framework.md` | Créer |
| L7 | Mise à jour `meta-design.yaml` | `meta-design.yaml` | Modifier |

---

## 4. Architecture du framework

### 4.1 Couches

```
┌─────────────────────────────────────────────────────────────┐
│                     CONSUMER CODEBASE                        │
│  (KIVA-CLI, ECOS-CLI, ARGUS, CTULU, etc.)                   │
└─────────────────────────────────────────────────────────────┘
                            ▲
                            │ import
                            │
┌─────────────────────────────────────────────────────────────┐
│              INTEGRATION FRAMEWORK (ce PRD-MOC)              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ DesignGate  │  │ DesignOps   │  │ DesignTest  │         │
│  │ (safe-      │  │ Loop        │  │ Harness     │         │
│  │  action)    │  │ (THINK/DO/  │  │ (pytest)    │         │
│  │             │  │  CHECK)     │  │             │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│         ▲                 ▲                 ▲               │
│         │                 │                 │               │
│  ┌──────┴──────┐  ┌──────┴──────┐  ┌──────┴──────┐        │
│  │ Design      │  │ Design      │  │ Design      │        │
│  │ Registry    │  │ Injector    │  │ Validator   │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
└─────────────────────────────────────────────────────────────┘
                            ▲
                            │ depends_on
                            │
┌─────────────────────────────────────────────────────────────┐
│              UNIFIED-DESIGN REPOSITORY                       │
│  (designs/, primitives/, atoms/, skills/)                    │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 Interfaces

```python
# 1. DesignGate — applique un design comme gate pré-action
class DesignGate:
    def __init__(self, design_name: str, config: dict): ...
    def verify(self, context: dict) -> bool: ...
    def get_violations(self) -> list[Violation]: ...

# 2. DesignOpsLoop — applique la boucle THINK/DO/CHECK
class DesignOpsLoop:
    def think(self, input: dict) -> Thought: ...
    def do(self, thought: Thought) -> ActionResult: ...
    def check(self, result: ActionResult) -> CheckResult: ...

# 3. DesignInjector — injecte un design dans le codebase consumer
class DesignInjector:
    def inject(self, design_name: str, target_path: Path) -> None: ...
    def verify_injection(self, design_name: str, target_path: Path) -> bool: ...

# 4. DesignTestHarness — tests d'intégration standardisés
class DesignTestHarness:
    def test_design_enforcement(self, design_name: str) -> TestResult: ...
    def test_design_behavior(self, design_name: str, scenario: dict) -> TestResult: ...
```

---

## 5. Tâches

### Phase A — Design et primitive
1. `designs/integration-framework/design.yaml` : design du framework
2. `primitives/integration-framework-primitive.yaml` : primitive réutilisable

### Phase B — Implémentation
3. `tools/integration_framework.py` : module principal
4. `templates/integration-template.py` : template pour consumers
5. `tests/test_integration_framework.py` : tests du framework

### Phase C — Documentation et enregistrement
6. `docs/integration-framework.md` : documentation
7. Mise à jour `meta-design.yaml`

---

## 6. Critères d'acceptation

- [ ] Design `integration-framework` créé et validé
- [ ] Primitive créée et référencée dans `meta-design.yaml`
- [ ] Module Python fonctionnel avec tests passants
- [ ] Template d'intégration utilisable par un consumer
- [ ] Documentation complète
- [ ] Aucune violation DAG

---

## 7. Proof-of-Life

- [ ] 2026-09-28T06:00:00+02:00 — Création design `integration-framework`
- [ ] 2026-09-28T06:00:00+02:00 — Création primitive `integration-framework-primitive`
- [ ] 2026-09-28T06:00:00+02:00 — Création module `tools/integration_framework.py`
- [ ] 2026-09-28T06:00:00+02:00 — Création template `templates/integration-template.py`
- [ ] 2026-09-28T06:00:00+02:00 — Création tests `tests/test_integration_framework.py`
- [ ] 2026-09-28T06:00:00+02:00 — Création documentation `docs/integration-framework.md`
- [ ] 2026-09-28T06:00:00+02:00 — Mise à jour `meta-design.yaml`

---

## 8. Références

- **Designs** : `designs/safe-action-pattern.yaml`, `designs/design-ops-loop/design.yaml`
- **Primitives** : `primitives/safe-action-gate-primitive.yaml`, `primitives/design-ops-loop-primitive.yaml`
- **Consumers** : KIVA-CLI, ECOS-CLI, ARGUS, CTULU
- **POC** : `D:\DO\WEB\TOOLS\L1-INFRA\KIVA-CLI\kiva_cli\safe_action_integration.py`

---

*Generated by governance-doc-writer skill — Pattern C*
