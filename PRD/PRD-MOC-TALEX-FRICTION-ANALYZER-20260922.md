---
type: PRD-MOC
version: "1.0.0"
status: approved
date: "2026-09-22"
intent_hash: 0xPRD_MOC_TALEX_FRICTION_ANALYZER_20260922
jurisdiction: unified-design
slug: talex-friction-analyzer
---

# PRD-MOC — TALEX Friction Analyzer

## Pourquoi

Les frictions de session (ERR-001 → ERR-010) sont détectées tardivement, corrigées manuellement, et peu tracées. Ce PRD-MOC crée le pipeline causal `friction → root cause → fix → proof` pour automatiser la prévention et la résolution structurelle.

## Quoi

 Artefacts :
- `designs/talex-friction-analyzer/design.yaml`
- `primitives/talex-friction-analyzer-primitive.yaml`
- `atoms/ATOM-TALEX-FRICTION-ANALYZER.md`
- `skills/talex-friction-analyzer/SKILL.md`
- `workflows/workflow-talex-friction-analysis.md`
- `tools/talex_friction_analyzer.py`
- Citizen `talex-friction-analyzer-citizen`

## Comment

1. Scanner `REPORTS/REPORT-TALEX-FRICTION-*.md`
2. Classifier P0/P1/P2
3. Analyser causes racines
4. Générer corrections atomiques
5. Appliquer + vérifier + enregistrer preuves

## Validation

- `python tools/talex_friction_analyzer.py --strict`
- `python scripts/validate_designs.py --strict`
- Pre-commit hooks passent

## Référence ADR

- **ADR** : ADR-2026-09-22-001-TALEX-FRICTION-ANALYZER
- **IntentHash** : 0xPRD_MOC_TALEX_FRICTION_ANALYZER_20260922
- **Dépôt** : gerivdb/unified-design
- **Statut ADR** : proposed
- **Màj requise si** : statut ADR passe à deprecated ou superseded

## Proof-of-Life

```
[TALEX] friction-analyzer: design=OK primitive=OK atom=OK skill=OK workflow=OK tool=OK
[TALEX] PRD-MOC-TALEX-FRICTION-ANALYZER-20260922: created=2026-09-22
[TALEX] MOC-TALEX-FRICTION-ANALYZER-20260922: created=2026-09-22
[TALEX] citizen: talex-friction-analyzer-citizen: created=2026-09-22
```
