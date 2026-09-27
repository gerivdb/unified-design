---
type: MOC
version: "1.0.0"
status: approved
date: "2026-09-22"
intent_hash: 0xMOC_TALEX_FRICTION_ANALYZER_20260922
jurisdiction: unified-design
slug: talex-friction-analyzer
---

# MOC — TALEX Friction Analyzer

## Contexte

Ce MOC orchestre la détection, classification, analyse causale et résolution des frictions TALEX pour `unified-design`.

## Portée

- Toutes les frictions de session sur `unified-design`
- Intégration avec `meta-coherence-auditor` citizen
- Pipeline `pipeline-friction-analysis-to-fix`

## Artefacts liés

| Type | ID | Path |
|------|-----|------|
| Design | `talex-friction-analyzer` | `designs/talex-friction-analyzer/design.yaml` |
| Primitive | `talex-friction-analyzer-primitive` | `primitives/talex-friction-analyzer-primitive.yaml` |
| Atom | `ATOM-TALEX-FRICTION-ANALYZER` | `atoms/ATOM-TALEX-FRICTION-ANALYZER.md` |
| Skill | `talex-friction-analyzer` | `skills/talex-friction-analyzer/SKILL.md` |
| Workflow | `workflow-talex-friction-analysis` | `workflows/workflow-talex-friction-analysis.md` |
| Tool | `talex_friction_analyzer.py` | `tools/talex_friction_analyzer.py` |
| Citizen | `talex-friction-analyzer-citizen` | `citizens/talex-friction-analyzer-citizen/citizen.yaml` |
| PRD-MOC | `PRD-MOC-TALEX-FRICTION-ANALYZER-20260922` | `PRD/PRD-MOC-TALEX-FRICTION-ANALYZER-20260922.md` |

## Workflow

1. **Collecte** : Scanner `REPORTS/REPORT-TALEX-FRICTION-*.md`
2. **Classification** : P0/P1/P2
3. **Analyse causale** : 5 Pourquoi
4. **Correction** : tâches atomiques
5. **Vérification** : pre-commit + tests
6. **Preuve** : enregistrement VOLTX

## Référence ADR

- **ADR** : ADR-2026-09-22-001-TALEX-FRICTION-ANALYZER
- **IntentHash** : 0xMOC_TALEX_FRICTION_ANALYZER_20260922
- **Dépôt** : gerivdb/unified-design
- **Statut ADR** : proposed
- **Màj requise si** : statut ADR passe à deprecated ou superseded
