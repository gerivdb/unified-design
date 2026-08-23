---
type: GUI
version: 1.0.0
status: active
intent_hash: 0xATOM_032_SIX_ORGANS
---

# ATOM-032 : Les Six Organes

Pour tourner, une boucle MDU doit disposer de :

## 1. Automations

Scripts, hooks, CI :
- `.githooks/` : hooks pré-commit, pré-push, post-merge
- `.github/workflows/` : pipelines CI/CD
- `scripts/` : outils d'automatisation

## 2. Worktrees

Isolation Git par branche :
- `feat/`, `fix/`, `release/`
- Branches temporaires pour review
- Isolation des changements

## 3. Skills

Connaissance permanente :
- `unified-design/conventions/` : conventions codifiées
- `ATOM-*.md` : atomes de design
- `ADR-*.md` : décisions architecturales

## 4. Connectors

Interfaces externes :
- API GitHub (REST/GraphQL)
- MCP (Model Context Protocol)
- `curl` pour appels HTTP
- SSH pour accès distant

## 5. Sub-agents

Rôles MDU :
- 9 experts (Poincaré, Maxwell, Musk, LeCun, Karpathy, Steinberger, Hassani, Bellard, Gardien)
- Avocat du Diable (Critic)
- Gardien (validation)
- HOTL (Human-in-the-Loop)

> Note AXE-0 (PRD-MOC-GEN-009) : "HOTL" ici = gate de validation humaine =
> niveau **A0 (HITL)** de `ONTOLOGY/concepts/autonomy-ladder.md`.

## 6. Mémoire

État hors-contexte :
- `.mdu/checkpoint.json` : état de session
- `design.context` : configuration courante
- `.mdu_deploy_kit/` : artefacts de déploiement

## Tableau de correspondance

| Organe | Implémentation MDU |
|--------|---------------------|
| Automations | `.githooks/`, CI, `scripts/` |
| Worktrees | Branches `feat/`, `fix/`, `release/` |
| Skills | `unified-design/conventions/` |
| Connectors | `curl`, API GitHub, SSH |
| Sub-agents | 9 experts + Avocat du Diable + Gardien |
| Mémoire | `.mdu/checkpoint.json`, `.mdu_deploy_kit/` |

## Règles d'interaction

- Chaque organe a un rôle clair
- Les organes communiquent via des canaux standardisés
- La mémoire est persistante et versionnée
- Les sub-agents peuvent être remplacés sans rupture