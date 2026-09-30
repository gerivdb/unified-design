---
type: MOC
version: "1.0.0"
date: "2026-09-28"
status: approved
intent_hash: 0xMOC_UNIFIED_DESIGN_CONSUMERS_REGISTRY_20260928
---

# MOC — Unified-Design Consumers Registry

**Repo** : `gerivdb/unified-design`  
**Strate** : L0-CANON  
**Statut** : approved  
**Date** : 2026-09-28

## Vue d'ensemble

Ce MOC orchestre le registry des consumers unified-design : 14 consumers, 9 designs, 126 intégrations.

## Composants

| Composant | Type | Chemin | Statut |
|-----------|------|--------|--------|
| `meta-design.yaml` | Registry | `meta-design.yaml` | ✅ Existe |
| `ACT-026-final-coverage-100.json` | Coverage | `ACT-026-final-coverage-100.json` | ✅ Existe |
| `PRD-MOC-UNIFIED-DESIGN-CONSUMERS-REGISTRY-20260928.md` | PRD-MOC | `PRD/PRD-MOC-UNIFIED-DESIGN-CONSUMERS-REGISTRY-20260928.md` | ✅ Existe |

## Séquence d'implémentation

### Phase 1 — Registry core (P0)

1. ✅ `meta-design.yaml` avec 9 designs × 14 consumers
2. ✅ Coverage 126/126 validée
3. ✅ PRD-MOC registry créé

### Phase 2 — Maintenance (P1)

4. Mettre à jour `meta-design.yaml` quand un nouveau design/consumer est ajouté
5. Régénérer `ACT-026-final-coverage-100.json` après chaque intégration

## Gates

| Gate | Critère | Statut |
|------|---------|--------|
| G1 — Registry à jour | `meta-design.yaml` reflète tous les designs/consumers actifs | ✅ |
| G2 — Coverage 100% | 126/126 intégrations fonctionnelles | ✅ |
| G3 — PRD-MOC à jour | `PRD-MOC-UNIFIED-DESIGN-CONSUMERS-REGISTRY-20260928.md` synchronisé | ✅ |

## Références

- PRD : `PRD/PRD-MOC-UNIFIED-DESIGN-CONSUMERS-REGISTRY-20260928.md`
- Framework : `PRD/PRD-MOC-INTEGRATION-FRAMEWORK-20260928.md`
- CI Pipeline : `PRD/PRD-MOC-CROSS-REPO-CI-PIPELINE-20260928.md`
- Traceability : `PRD/PRD-MOC-ADR-DESIGN-INTEGRATION-TRACEABILITY-20260928.md`
- Usage : `PRD/PRD-MOC-CONSUMER-INTEGRATION-USAGE-20260928.md`
- Auto-Promote : `PRD/PRD-MOC-AUTO-PROMOTE-20260928.md`
