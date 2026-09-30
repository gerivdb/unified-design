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

Analyse TALEX consolidée (2026-09-29) : 33 issues détectées dans 6 rapports `friction_analysis_*.json`, couvrant TALEX L4, unified-design, VEX, HERMES, SPIDX, SABRE, LOOPX, BRAIN-CLI, ARGUS, DMR, CLIP-FACTORY, COMET, BatMCP, BRAIN-DOCS, NEXUS, GOVERNANCE-HUB, KIVA-CLI, ECOS-CLI.

4 gaps ontologiques comblés dans ONTOLOGY L0 :
- `ATOM-CRM-TECH-DEBT-SCORE-20260929`
- `ATOM-CROSS-REPO-TRACEABILITY-20260929`
- `ATOM-SEVERITY-CLASSIFICATION-20260929`
- `ATOM-REPO-IDENTITY-SCHEMA-20260929`

## Quoi

 Artefacts :
- `designs/talex-friction-analyzer/design.yaml`
- `primitives/talex-friction-analyzer-primitive.yaml`
- `atoms/ATOM-TALEX-FRICTION-ANALYZER.md`
- `skills/talex-friction-analyzer/SKILL.md`
- `workflows/workflow-talex-friction-analysis.md`
- `tools/talex_friction_analyzer.py`
- Citizen `talex-friction-analyzer-citizen`
- `D:\DO\WEB\TOOLS\L4-TOOLS\TALEX\primitives\__init__.py` (fix module import ERR)
- `D:\DO\WEB\TOOLS\L4-TOOLS\TALEX\tools\file_writer_helper.py` (canonical file writer, élimine ERR-120..ERR-124)
- `D:\DO\WEB\TOOLS\L4-TOOLS\TALEX\tools\fix_hitl_batch_v2.py` (INLINE_REF_MAP étendue, corrige ERR-SESSION-002)
- `D:\DO\WEB\TOOLS\L4-TOOLS\TALEX\workflows\talex-friction-pipeline.yaml` (workflow YAML structuré)
- `D:\DO\WEB\TOOLS\L0-CANON\unified-design\schemas\REPO_IDENTITY_v1.yaml` (schéma identité repo, corrige ERR-SESSION-003)
- `D:\DO\WEB\TOOLS\L0-CANON\unified-design\scripts\branch-cleanup-helper.sh` (workflow BRGS compliant, corrige ERR-BRGS-001)
- Ontologie L0 : 4 ATOMs créés (`CRM Tech Debt Score`, `Cross-Repo Traceability`, `Severity Classification`, `Repo Identity Schema`)

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
