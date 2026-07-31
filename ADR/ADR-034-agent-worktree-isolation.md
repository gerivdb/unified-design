---
type: ADR
status: proposed
date: "2026-07-31"
intent_hash: 0xADR_034_AGENT_WORKTREE_ISO_20260731
---

# ADR-034: Agent Worktree Isolation (Git Worktree per Agent)

## Context

Faire tourner plusieurs agents en parallèle dans un seul dépôt provoque des collisions de fichiers (source: "Graph of Loops" G2).

## Decision

Chaque nœud du graphe reçoit son propre **worktree Git**. Le système effectue un *dry-run* (test à blanc) avant la fusion finale ; si le code ne s'applique pas proprement, il avorte l'opération pour éviter de laisser le dépôt dans un état instable.

## Implementation

Nouvel atom: `ATOM-050-agent-worktree-isolation`
- Capability: `worktree-isolation` (dry_run_enabled: true, abort_on_conflict: true, max_parallel_worktrees: 8)
- Hérite de: `gated-boot-sequence`, `constitutional-sot`
- Nouvelles design_rules: `worktree-isolation-enforced` (check: agent_worktree_isolation)
- Module loop_engine: `worktree_orchestrator.py`

## Consequences

### Positive
- Isolation physique complète entre agents parallèles
- Dry-run garantit merge propre avant fusion réelle
- Nettoyage automatique (cleanup_on_complete: true)
- Scalable jusqu'à 8 worktrees parallèles

### Negative
- Overhead disque (worktrees multiples)
- Complexité orchestration (branche par agent)
- Nécessite git 2.5+ (worktree support)

## References

- Graph of Loops, Section 2: "L'isolation physique par git worktree (G2)"
- ATOM-050-agent-worktree-isolation.yaml
- loop_engine/worktree_orchestrator.py