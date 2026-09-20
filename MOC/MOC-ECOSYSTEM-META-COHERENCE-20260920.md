---
type: MOC
version: "1.0.0"
date: "2026-09-20"
status: active
intent_hash: 0xMOC_ECOSYSTEM_META_COHERENCE_20260920
---

# MOC — ECOSYSTEM-META-COHERENCE

> Carte de contenu pour les documents de gouvernance du design `ecosystem-meta-coherence` dans `unified-design`.

## PRD-MOC

- `PRD/PRD-MOC-ECOSYSTEM-META-COHERENCE-20260920.md` — Spécification et livrables ecosystem-meta-coherence

## Design

- `designs/ecosystem-meta-coherence/design.yaml` — Design Think/Do/Check pour corrections structurelles et causales

## Atom

- `atoms/ecosystem-meta-coherence-gate.md` — Atom enforceable

## Primitive

- `primitives/ecosystem-meta-coherence.yaml` — Primitive réutilisable

## Skills

- `skills/ecosystem-meta-coherence-analyzer/SKILL.md` — Analyse TALEX des frictions
- `skills/dryrun-causal-auditor/SKILL.md` — Vérification prod-ready

## Workflows

- `workflows/dryrun-causal-audit.md` — Dryrun causal audit
- `workflows/structural-fix-pipeline.md` — Structural fix pipeline

## Citizen

- `citizens/meta-coherence-auditor/citizen.yaml` — Citoyen auditeur

## Pipeline

- `pipelines/mdu-validation.yaml` — Pipeline CI MDU

## Références croisées

| Document | Relation |
|---|---|
| `INTENT-2026-09-19-SAFE-ACTION-PATTERN.md` | Intent parent |
| `ADR-2026-09-19-SAFE-ACTION-PATTERN.md` | ADR backing |
| `META-DESIGN.md` | Enregistrement design + atom + workflows + skills |
| `meta-design.yaml` | Enregistrement schema |
| `meta-coherence` | Design parent (détection écarts cross-repo) |
| `chain-fluidity` | Design parent (fluidité chaînes Think→Do→Check) |
| `safe-action-pattern` | Design parent (patron universel d'action) |
| `friction-analyzer` | Design source (runner TALEX) |

## Livrables

| ID | Livrable | Chemin cible | Statut |
|---|---|---|---|
| L1 | Design `ecosystem-meta-coherence` | `designs/ecosystem-meta-coherence/design.yaml` | 🟢 Commité |
| L2 | Atom `ecosystem-meta-coherence-gate` | `atoms/ecosystem-meta-coherence-gate.md` | 🟢 Commité |
| L3 | Primitive `ecosystem-meta-coherence` | `primitives/ecosystem-meta-coherence.yaml` | 🟢 Commité |
| L4 | Skill `ecosystem-meta-coherence-analyzer` | `skills/ecosystem-meta-coherence-analyzer/SKILL.md` | 🟢 Commité |
| L5 | Skill `dryrun-causal-auditor` | `skills/dryrun-causal-auditor/SKILL.md` | 🟢 Commité |
| L6 | Workflow `dryrun-causal-audit` | `workflows/dryrun-causal-audit.md` | 🟢 Commité |
| L7 | Workflow `structural-fix-pipeline` | `workflows/structural-fix-pipeline.md` | 🟢 Commité |
| L8 | Citizen `meta-coherence-auditor` | `citizens/meta-coherence-auditor/citizen.yaml` | 🟢 Commité |
| L9 | Pipeline `mdu-validation` | `pipelines/mdu-validation.yaml` | 🟢 Commité |
| L10 | Mise à jour `META-DESIGN.md` | `META-DESIGN.md` | 🟢 Commité |
| L11 | Mise à jour `meta-design.yaml` | `meta-design.yaml` | 🟢 Commité |
| L12 | Mise à jour catalogues | `catalog/*.yaml` | 🟢 Commité |

## Blocages

| Blocage | Description |
|---|---|
| Aucun | Tous les livrables sont implémentés et validés |

## Proof-of-Life

- [x] 2026-09-20T04:00:00+02:00 — Création MOC ECOSYSTEM-META-COHERENCE
