---
type: ADR
status: proposed
date: "2026-07-31"
intent_hash: 0xADR_035_BEADS_SQL_MEMORY_20260731
---

# ADR-035: Beads SQL Versioned Memory (Replace Markdown TODO)

## Context

L'usage de fichiers `.md` (comme `claw.md` ou `design.md`) pour la mémoire d'agent ne permet pas la persistance profonde ni la requêtabilité structurée (source: "Graph of Loops" L1 - Beads).

## Decision

Remplacer les listes de tâches Markdown par un **graphe réel sur SQL versionné** (SQLite + WAL).

- Stockage: SQLite avec mode WAL pour concurrence
- Compression: zlib ~70% ratio sur le content JSON
- Persistance profonde: insights survivent aux resets contexte + rotation comptes
- Interface query: SQL natif pour analyses complexes
- Graphe relationnel complet: nœuds (insights) + arêtes (relations sémantiques)

## Implementation

Nouvel atom: `ATOM-051-beads-sql-memory`
- Capability: `beads-sql-memory` (storage_backend: sqlite+wal, compression_ratio: 0.70)
- Hérite de: `memory-curator`, `wal-compaction`, `sovereign-vector-memory`
- Nouvelles design_rules: `beads-sql-memory-persistence` (check: sql_memory_survival)
- Module loop_engine: `beads_sql_store.py`

## Consequences

### Positive
- Survie garantie: context_reset + account_rotation
- Compression 70% = économie coûts API futurs
- Requêtabilité SQL complète (agrégations, parcours graphe)
- ACID + WAL = concurrence sûre multi-agents

### Negative
- Complexité vs fichiers Markdown
- Migration existant nécessaire
- Dépendance SQLite/WAL

## References

- Graph of Loops, Section 3: "Mémoire par SQL versionné vs Markdown (L1 - Beads)"
- ATOM-051-beads-sql-memory.yaml
- loop_engine/beads_sql_store.py