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

Ce MOC orchestre la détection, classification, analyse causale et résolution des frictions TALEX pour `unified-design` et l’écosystème gerivdb.

Analyse TALEX consolidée (2026-09-29) : 33 issues détectées dans 6 rapports `friction_analysis_*.json`, couvrant TALEX L4, unified-design, VEX, HERMES, SPIDX, SABRE, LOOPX, BRAIN-CLI, ARGUS, DMR, CLIP-FACTORY, COMET, BatMCP, BRAIN-DOCS, NEXUS, GOVERNANCE-HUB, KIVA-CLI, ECOS-CLI.

4 gaps ontologiques comblés dans ONTOLOGY L0 :
- `ATOM-CRM-TECH-DEBT-SCORE-20260929`
- `ATOM-CROSS-REPO-TRACEABILITY-20260929`
- `ATOM-SEVERITY-CLASSIFICATION-20260929`
- `ATOM-REPO-IDENTITY-SCHEMA-20260929`

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

## Évaluation d'utilité

| Artefact | Utilité | Impact |
|----------|---------|--------|
| `primitives/__init__.py` | Débloque l'import TALEX friction pipeline runner | P0 |
| `tools/file_writer_helper.py` | Élimine les erreurs d'encoding PowerShell (ERR-120..ERR-124) | P1 |
| `tools/fix_hitl_batch_v2.py` | Résout les références courtes de repo (ERR-SESSION-002) | P1 |
| `workflows/talex-friction-pipeline.yaml` | Structure le pipeline d'analyse TALEX | P1 |
| `schemas/REPO_IDENTITY_v1.yaml` | Garantit la cohérence SOT des repos (ERR-SESSION-003) | P1 |
| `scripts/branch-cleanup-helper.sh` | Automatise le contournement BRGS (ERR-BRGS-001) | P2 |
| ATOM `CRM Tech Debt Score` | Score de dette technique cross-repo | P1 |
| ATOM `Cross-Repo Traceability` | Traçabilité inter-repos via intent_hash | P1 |
| ATOM `Severity Classification` | Taxonomie des sévérités d'erreur | P1 |
| ATOM `Repo Identity Schema` | Schéma d'identité canonique des repos | P1 |

## Référence ADR

- **ADR** : ADR-2026-09-22-001-TALEX-FRICTION-ANALYZER
- **IntentHash** : 0xMOC_TALEX_FRICTION_ANALYZER_20260922
- **Dépôt** : gerivdb/unified-design
- **Statut ADR** : proposed
- **Màj requise si** : statut ADR passe à deprecated ou superseded
