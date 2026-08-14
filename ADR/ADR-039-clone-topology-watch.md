---
type: ADR
version: "1.0.0"
status: proposed
date: "2026-08-15"
intent_hash: 0xADR_CLONE_TOPOLOGY_WATCH_20260815
---

# ADR-039 - Clone Topology Watch

## Problem Statement

Before implementing continuous topological surveillance, clones illegitimes could be created undetected in D:\DO\WEB\TOOLS\L* and C:\DevTools. Two clones of GOVERNANCE-HUB were detected in L1-INFRA and C:\DevTools, demonstrating the absence of a daemon/watch filesystem comparing disk topology to SOT (known_repositories.yaml, ECOSROOT.json, TOPOS/topology.yaml, STRATE_REGISTRY.yaml, ONTOLOGY.yaml).

## Design

### Principle Established

A continuous topology-watch service monitors the filesystem for illegitimate clones, plain directories, stratum violations, and path deviations. Detection is based on SOT comparison and ontological classification.

### Key Rules

1. `clone-topology-watch.py` scans D:\DO\WEB\TOOLS\L* and C:\DevTools
2. Entities are classified using ONTOLOGY concepts: git_worktree, kilo_worktree, plain_directory, clone_legitimate, clone_illegitimate
3. Violations R-TOP-001 to R-TOP-006 are detected and reported
4. Effects are reversible (RSI): scan, quarantine, block, alert
5. POOP cycle: @day=scan, @twilight=verify, @night=quarantine
6. Pre-commit hook blocks commits with topology violations

### Enforcement Mechanisms

- `clone-topology-watch.py` main service (L4 REPO-STANDARDS)
- `topos_clone_validator.py` TOPOS validation (L1b)
- `strate-watcher.py` extended detection (L1b)
- `.githooks/pre-commit-topology-watch.py` blocking hook (L4)
- `rss_bulk_scan.py` integrated scan (L4)

### Consequences

- Continuous detection of illegitimate clones and plain directories
- Reversible quarantine system for clones
- Integration with NEXUS WAL for traceability
- Integration with TALEX for notifications
- Compliance with BDCP mode (no network egress)

## Alternatives Considered

1. Manual monitoring (insufficient scale)
2. CI-only detection (delayed feedback)
3. Daemon-only without hooks (bypassable)
4. Topology-watch with hooks + daemon (chosen solution)

## Implementation Status

- Script created: REPO-STANDARDS/scripts/clone-topology-watch.py
- TOPOS tools created: tools/topos_clone_validator.py
- RSS updated: rss_bulk_scan.py includes C:\DevTools
- Pre-commit hook: .githooks/pre-commit-topology-watch.py
- Tests: 12 passing
- Documentation: docs/clone-topology-watch.md

## Reference ADR

- **ADR** : ADR-039-clone-topology-watch
- **IntentHash** : 0xADR_CLONE_TOPOLOGY_WATCH_20260815
- **Statut ADR** : proposed
- **Màj requise si** : statut ADR passe a deprecated ou superseded
