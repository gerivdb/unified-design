# Zombie Symptom — Design Pattern

**Pattern ID** : `zombie-symptom`  
**Category** : `system_health`  
**Layer** : L0-CANON  
**IntentHash** : `0xZOMBIE_SYMPTOM_DESIGN_PATTERN_20260809`  
**Status** : proposed  
**Repo** : gerivdb/unified-design

---

## Problem

An ecosystem of tools/agents/runners leaves **zombie entities** after session end:
- system processes (`git.exe`, `node.exe`, `python.exe`, `zig.exe`, `cargo.exe`, `bun.exe`, `pwsh.exe`)
- orphan git worktrees
- Windows handles locking directories
- cross-repo conflicts undetected

## Abstract Solution

1. **Detection** : centralized observability of zombie entities
2. **Classification** : typology + criticality
3. **Orchestrated purge** : prioritization + safe execution
4. **Traceability** : WAL/NEXUS for each action
5. **Prevention** : before/after hooks for critical sessions

## Reuse

This pattern composes:
- `kix_orchestrator` → health endpoints
- `trix_runtime` → preflight checks
- `wal_nexus` → audit logging
- `process_zombie_hygiene` → skill/script layer

## Instances

See `instances/` for concrete implementations:
- `process-zombie-proliferation` — current ENV2 issue
