---
type: PRD-MOC
version: "1.0.0"
date: "2026-09-22"
status: approved
intent_hash: 0xPRD_MOC_STRUCTURAL_COHERENCE_20260922
author: gerivdb
source_repo: gerivdb/unified-design
parent_doc: PRD-MOC-JEVX-MDU-INTEGRATION-FIX-20260922.md
related_adr: ADR-0111-JEVX-SOVEREIGN-OVERLAY.md
related_intent: INTENT-JEVX-SOVEREIGN-OVERLAY.md
related_moc: MOC-JEVX-MDU-INTEGRATION-FIX-20260922.md
ontology:
  concepts:
    - git-lock-guardian
    - temporal-inconsistency-detector
    - cross-repo-reference-validator
    - ontology-dedup-auditor
    - design-code-sync
    - catalog-consumer-auditor
    - dry-run-causal
    - jevx-mdu-integration-fix
  repo: gerivdb/ONTOLOGY
---

# PRD-MOC — Structural Coherence

> **Parent** : PRD-MOC-JEVX-MDU-INTEGRATION-FIX-20260922.md
> **Périmètre** : patterns et pipelines de cohérence structurelle déduits de l'analyse TALEX des frictions de session.
> **Coordination transverse** : voir MOC JEVX §3 (livrables, dépendances).

---

## 1. Objectif

Éliminer structurellement les frictions et erreurs récurrentes identifiées par TALEX :
- E1 : git `index.lock` bloquant
- E2 : incohérences temporelles entre documents
- E3 : références cross-repo fantômes
- E4 : doublons ontologiques
- E5/E6/E9 : désynchronisations design/code
- E8 : consumers de catalogue manquants
- E10 : PRD-MOC/MOC non synchronisés

## 2. Livrables assignés

| ID | Livrable | Chemin cible | Type | Statut |
|---|---|---|---|---|
| L13 | Pattern `git-lock-guardian` | `designs/git-lock-guardian.md` | Créer | ✅ |
| L14 | Pattern `temporal-inconsistency-detector` | `designs/temporal-inconsistency-detector.md` | Créer | ✅ |
| L15 | Pattern `cross-repo-reference-validator` | `designs/cross-repo-reference-validator.md` | Créer | ✅ |
| L16 | Pipeline `structural-coherence-pipeline` | `pipelines/structural-coherence-pipeline.yaml` | Créer | ✅ |
| L17 | Workflow `dryrun-causal-workflow` | `workflows/dryrun-causal-workflow.md` | Créer | ✅ |
| L18 | Rapport TALEX friction analysis | `reports/REPORT-TALEX-FRICTION-ANALYSIS-20260922.md` | Créer | ✅ |
| L19 | Pattern `ontology-dedup-auditor` | `designs/ontology-dedup-auditor.md` | Créer | ✅ |
| L20 | Pattern `design-code-sync` | `designs/design-code-sync.md` | Créer | ✅ |
| L21 | Pattern `catalog-consumer-auditor` | `designs/catalog-consumer-auditor.md` | Créer | ✅ |

## 3. Tâches

### Phase A — Patterns P1

1. **L13** : `designs/git-lock-guardian.md` — détecter et nettoyer les `index.lock` avant commit.
2. **L14** : `designs/temporal-inconsistency-detector.md` — détecter les incohérences temporelles entre documents.
3. **L15** : `designs/cross-repo-reference-validator.md` — valider les références cross-repo contre la SOT.

### Phase B — Pipeline et workflow P1

4. **L16** : `pipelines/structural-coherence-pipeline.yaml` — agréger tous les checks de cohérence structurelle.
5. **L17** : `workflows/dryrun-causal-workflow.md` — pérenniser la méthodologie de dry-run causal.

### Phase C — Patterns P2

6. **L19** : `designs/ontology-dedup-auditor.md` — détecter et fusionner les doublons ontologiques.
7. **L20** : `designs/design-code-sync.md` — vérifier la synchronisation design/code.
8. **L21** : `designs/catalog-consumer-auditor.md` — vérifier que les consumers sont documentés.

## 4. Contraintes

- **SLM** : tâches atomiques, < 3 fichiers par commit
- **Validation** : `python scripts/validate_designs.py --strict` sur tous les nouveaux designs
- **Ontologie** : chaque pattern/workflow/pipeline doit référencer des concepts ONTOLOGY
- **Preuves** : Proof-of-Life horodatées pour chaque livrable

## 5. Plan de commits proposé

| Commit | Fichiers | Description |
|---|---|---|
| `feat(patterns): add git-lock-guardian` | `designs/git-lock-guardian.md` | L13 |
| `feat(patterns): add temporal-inconsistency-detector` | `designs/temporal-inconsistency-detector.md` | L14 |
| `feat(patterns): add cross-repo-reference-validator` | `designs/cross-repo-reference-validator.md` | L15 |
| `feat(pipeline): add structural-coherence-pipeline` | `pipelines/structural-coherence-pipeline.yaml` | L16 |
| `feat(workflow): add dryrun-causal-workflow` | `workflows/dryrun-causal-workflow.md` | L17 |
| `feat(report): add TALEX friction analysis` | `reports/REPORT-TALEX-FRICTION-ANALYSIS-20260922.md` | L18 |
| `feat(patterns): add ontology-dedup-auditor` | `designs/ontology-dedup-auditor.md` | L19 |
| `feat(patterns): add design-code-sync` | `designs/design-code-sync.md` | L20 |
| `feat(patterns): add catalog-consumer-auditor` | `designs/catalog-consumer-auditor.md` | L21 |

## 6. Adossement (PF2)

- **Implémentation** : ce PRD-MOC, exécuté par agent Kilo session suivante
- **Vérificateur** : `python scripts/validate_designs.py --strict` ; hooks pre-commit (`design-validate`, `frontmatter-guardian`, `check-yaml`)
- **Propriétaire** : gerivdb / GOVERNANCE-HUB N+4

## 7. Critères d'acceptation

1. Tous les designs/pipelines/workflows passent `validate_designs.py --strict`.
2. Chaque pattern/workflow/pipeline référence des concepts ONTOLOGY.
3. Le pipeline `structural-coherence-pipeline` couvre tous les checks E1-E10.
4. Le workflow `dryrun-causal-workflow` est documenté et réutilisable.
5. Le rapport TALEX friction analysis est créé et validé.
6. Les Proof-of-Life sont horodatés et documentés.

## 8. Proof-of-Life

- [x] 2026-09-22T03:11:05+02:00 — Création PRD-MOC Structural Coherence
- [x] 2026-09-22T03:11:05+02:00 — Patterns L13-L15 créés et validés
- [x] 2026-09-22T03:11:05+02:00 — Pipeline L16 et workflow L17 créés
- [x] 2026-09-22T03:11:05+02:00 — Rapport TALEX L18 créé
- [ ] 2026-09-22T03:11:05+02:00 — Patterns L19-L21 à créer
