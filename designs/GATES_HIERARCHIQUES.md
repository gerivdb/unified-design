---
type: DESIGN
version: "1.0.0"
date: 2026-08-23
status: accepted
intent_hash: 0xDESIGN_GATES_HIERARCHIQUES_20260823
design_id: U-C6
layer: L0
source: INTENT V3.0 (GATE-0..7, sous-gates 6a/6b/6c), INTENT infra (GATE-INFRA-0..6)
---

# GATES_HIERARCHIQUES.md — Patron de gouvernance des opérations risquées

## Principe

> **Aucune opération de masse ne s'exécute sans baseline mesurée avant, gates explicites
> pendant, et un test de sortie symbolique qui prouve la réussite.**

## Le patron en 7 éléments

| # | Élément | Règle |
|---|---------|-------|
| G1 | **Checkpoint** | Tag git avant toute mutation (`pre-<operation>-<date>`) |
| G2 | **Baseline** | L'outil de mesure existe ET tourne sur l'état initial avant la première mutation (« on ne déplace rien sans l'outil qui mesure ») |
| G3 | **Gates explicites** | Chaque phase se termine par une décision continue / ajuster / rollback, avec critères de passage écrits à l'avance |
| G4 | **Sous-gates** | Aucun segment de travail ne dépasse ~2h sans point de décision |
| G5 | **Rollback disponible** | À chaque gate, la commande de retour arrière est connue et testée |
| G6 | **Test de sortie symbolique** | Un livrable concret, idéalement un artefact qui a échoué avant, prouve la réussite (ex: commit SOT ARGUS) |
| G7 | **Veilleur ≠ gardien** | La détection continue est non-bloquante ; seuls les points de décision bloquent |

## Anti-patterns

- Phase « monolithique » sans gate interne
- Critères de gate définis après l'exécution
- Contournement (`--no-verify`) plutôt qu'arbitrage tracé
- Métrique de succès = « fini » au lieu d'un état mesuré

## Applications documentées

- INTENT V3.0 : restructuration artefacts (gates 0-7, sous-gates 6a-c)
- INTENT infra : bootstrap/Arbiter (gates INFRA-0-6, test de sortie = commit SOT)
