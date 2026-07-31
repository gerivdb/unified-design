---
type: ADR
status: proposed
date: "2026-07-31"
intent_hash: 0xADR_036_EXIT_INTERCEPTOR_20260731
---

# ADR-036: Exit Interceptor / Stop Hook (Cross-Model Validation)

## Context

Un agent peut "noter ses propres devoirs" et valider ses propres bugs en terminant sa session sans revue externe (source: "Graph of Loops" L5).

## Decision

Introduire un **intercepteur de sortie (Stop Hook)** qui bloque la commande `exit`/`finish` de l'agent tant qu'un second modèle (OpenAI Codex par défaut) n'a pas signé un fichier de révision (`review.md`) sur le disque.

- Blocage à la tentative de sortie
- Validation croisée obligatoire (anti-auto-validation)
- Artefact signé: `review.md` avec signature SHA256 (non-répudiation)
- Timeout: 300s par défaut

## Implementation

Nouvel atom: `ATOM-052-exit-interceptor`
- Capability: `exit-interceptor` (block_on_exit: true, validator_model: openai-codex)
- Hérite de: `hitl-gate`, `ext-code-reviewer`, `constitutional-filter`
- Nouvelles design_rules: `exit-interceptor-mandatory` (check: cross_model_validation_on_exit)
- Module loop_engine: `exit_interceptor.py` (ExitInterceptor + ExitInterceptorHook)

## Consequences

### Positive
- Élimine l'auto-validation (self-review prevention)
- Traçabilité: review.md signé = audit trail
- Flexibilité: validateur configurable (Codex, GPT-4, Claude, custom)
- Intégrable comme hook pre-exit dans tout cycle de vie agent

### Negative
- Latence ajoutée à la fin de session (max 300s)
- Dépendance modèle externe (disponibilité, coûts)
- Complexité: nécessite hook runtime dans l'agent

## References

- Graph of Loops, Section 4: "L'intercepteur de sortie ou Stop Hook (L5)"
- ATOM-052-exit-interceptor.yaml
- loop_engine/exit_interceptor.py