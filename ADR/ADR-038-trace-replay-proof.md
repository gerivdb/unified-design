---
type: ADR
status: proposed
date: "2026-07-31"
intent_hash: 0xADR_038_TRACE_REPLAY_PROOF_20260731
---

# ADR-038: Preuve par Re-exécution de Trace (Trace Replay Verification)

## Context

Les corrections d'agents sont difficiles à valider: comment prouver qu'une défaillance a vraiment disparu sans rejouer l'exécution exacte ? (source: "Graph of Loops" L6 - Workshop).

## Decision

Capturer une exécution réelle de l'agent, puis rejouer **exactement la même trace** contre le code modifié sur un démon local. Les assertions de l'agent sont lues via SQL sur une base de traces locale pour prouver que les défaillances ont disparu avant de passer les voyants au vert.

- Capture: trace complète (appels fonctions, retours, exceptions, I/O, timing)
- Stockage: SQLite + WAL (schema: trace_sessions, trace_events, trace_assertions)
- Replay: exécution déterministe de la même commande
- Vérification: assertions SQL sur trace rejouée (exact_trace_match + all_assertions_pass)
- Preuve: artefact `REPLAY_PROOF.json` généré

## Implementation

Nouvel atom: `ATOM-054-trace-replay-proof`
- Capability: `trace-replay-proof` (capture_mode: full_trace, replay_target: local_daemon, verification_method: sql_assertions)
- Hérite de: `wal-reconciler`, `phi-opt-recovery`, `deterministic-replay`
- Nouvelles design_rules: `trace-replay-verification` (check: replay_assertions_pass)
- Module loop_engine: `trace_replay.py` (TraceDatabase, TraceCapture, TraceReplayer)

## Consequences

### Positive
- Preuve mathématique de correction (replay déterministe)
- Assertions SQL = queries vérifiables, auditable
- Détection régressions exactes (mismatch trace = alerte)
- Artefact de preuve pour compliance/audit

### Negative
- Overhead capture (tracing sys.settrace = ralentissement ~10-50%)
- Stockage traces volumineux (WAL + compression nécessaire)
- Complexité replay déterministe (environnement, seeds, temps)
- Faux positifs si non-déterminisme environnement

## References

- Graph of Loops, Section 6: "Preuve par re-exécution de trace (L6 - Workshop)"
- ATOM-054-trace-replay-proof.yaml
- loop_engine/trace_replay.py