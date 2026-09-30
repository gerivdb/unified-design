---
type: ADR
status: proposed
date: "2026-09-29"
intent_hash: 0xADR_AUTO_DESIGN_ARGUS_CTULU_JEVX_20260929
---

# ADR — Auto-Design : intégration ARGUS, CTULU et JEVX pour la validation sémantique et la gestion automatique des commits

## Contexte

`auto-design` dispose d'une architecture complète (analyzer, generator, industrializer, verifier, auto_promote, CLI, hooks). Cependant, il raisonne en **autonomie locale** et n'exploite pas les capacités existantes d'**ARGUS** (couche N+2 de détection), **CTULU** (couche N+3 d'orchestration et traçabilité) et **JEVX** (couche de projection/synchronisation).

Cette isolation crée des gaps critiques :
- **Pas de validation sémantique** des bridges et cross-refs (seul un comptage de fichiers est fait)
- **Pas de traçabilité** cross-repo des designs déployés
- **Pas de gestion automatique des commits** (conventional commits, atomic commits, auto-commit)
- **Pas de projection** des designs vers des formats consommables (TALEX, CURX)

## Décision

Intégrer ARGUS, CTULU et JEVX comme **dépendances fonctionnelles** d'`auto-design` via des appels CLI `--json` et imports Python directs.

### ARGUS — Validateur sémantique N+2

| Intégration | Fichier ARGUS | Mécanisme |
|---|---|---|
| Bridge validation | `scanners/bridge_check.py` | `scan_repo()` → JSON |
| Crossref validation | `scanners/crossref_check.py` | `scan_repo()` → JSON |
| Meta-coherence gate | `PRD/ecosystem_meta_coherence.py` | `verify_meta_coherence()` |
| Component classification | `runners/nodex.py` | `NodexRunnerEffective()._execute()` |

### CTULU — Moteur d'exécution N+3

| Intégration | Fichier CTULU | Mécanisme |
|---|---|---|
| Trace graph | `tools/traceability/trace_graph.py` | `build_and_save()` |
| Trace validator | `tools/traceability/trace_validator.py` | `TraceabilityValidator().validate()` |
| Trace drift | `tools/traceability/trace_drift.py` | `DriftDetector().scan()` |
| Commit monitor | `tools/trix-box/trix-commit-monitor.py` | `--commit`, `--status` |
| Git workflow | `tools/trix-box/trix-git-workflow.py` | `commit_atomic()`, `push_safe()` |
| Pre-commit guard | `tools/trix-box/trix-pre-commit-guard.py` | `check_staged_json()` |
| Governance synthesizer | `tools/vibe-governance-synthesizer/` | `PromptParser.parse()` + `synthesizer.py` |

### JEVX — Projection/synchronisation

| Intégration | Rôle | Mécanisme |
|---|---|---|
| Design projection | `design.yaml` → TALEX/CURX/narratives | Templates Jinja2 |
| Sync validation | Cohérence `unified-design/designs/` ↔ repos cibles | Hook post-deploy |
| Consumer validation | Conformité aux attentes consommateurs | JEVX validation gate |

## Conséquences

### Techniques

1. **Dépendances externes** : `auto-design` dépend de ARGUS et CTULU comme librairies Python
2. **Performance** : scanners ARGUS ajoutent ~1-2s par validation (timeout 120s)
3. **Robustesse** : fallback local si ARGUS/CTULU indisponibles
4. **Versionning** : nécessite un contrat d'interface stable entre les repos

### Organisationnelles

1. **Couplage fort** : `auto-design` ne peut pas évoluer indépendamment d'ARGUS/CTULU
2. **Responsabilité partagée** : bugs dans ARGUS/CTULU impactent `auto-design`
3. **Documentation** : nécessite une documentation d'intégration cross-repo

### Économiques

1. **ROI immédiat** : +80% détection bridges, +100% cross-refs, traçabilité 100%
2. **Coût de maintenance** : +1j/semestre pour suivre les évolutions ARGUS/CTULU
3. **Risque** : si ARGUS/CTULU évoluent sans coordination, `auto-design` casse

## Alternatives écartées

| Alternative | Raison du rejet |
|---|---|
| Réimplémenter bridge_check dans auto-design | Duplication, maintenance double, perte de la sémantique ARGUS |
| Créer un nouveau scanner dédié | ARGUS existe déjà, il faut l'exploiter pas le recréer |
| Intégration via API REST | Overhead, complexité, pas de gain par rapport à imports Python |
| Intégration via fichiers plats | Pas de validation temps réel, risque de désync |

## Références

- **INTENT** : `INTENT-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md`
- **PRD** : `PRD-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md`
- **MOC** : `MOC-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md`
- **Repo ARGUS** : `gerivdb/ARGUS`
- **Repo CTULU** : `gerivdb/CTULU`
- **Repo JEVX** : mécanisme intégré à CTULU/TALEX
- **Repo KG-L** : `gerivdb/KG-L`

## Màj requise si

- Statut ADR passe à `deprecated` ou `superseded`
- ARGUS/CTULU/JEVX changent d'architecture de façon incompatible
- Nouveau pattern d'intégration cross-repo émerge (ex: API REST unifiée)
