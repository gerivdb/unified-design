---
type: ADR
version: "1.0.0"
status: proposed
date: "2026-07-31"
intent_hash: 0xCLONE_GOVERNANCE_20260731
---

# ADR-032 - Clone Governance

## Problem Statement

Before implementing formal governance, duplicate repositories could be created across strata, which led to inconsistencies and wasted resources. The case of ECOS-CLI showed a duplicate instance in L4-TOOLS while the canonical version remained in L1-INFRA. The case of KIVA-CLI shows a similar duplicate at L4-TOOLS/KIVA-CLI vs L1-INFRA/KIVA-CLI.

## Design

### Principle Established

Each repository must have exactly one canonical path defined in `known_repositories.yaml`. Any duplicate instance across strata is illegitimate and must be detected and resolved.

### Key Rules

1. `do_not_create: true` blocks automatic cloning of protected repositories
2. Canonical paths are defined in `known_repositories.yaml`
3. Cross-strata duplication is prohibited
4. All violations must be documented in ADR's `violations_documented` section

### Enforcement Mechanisms

- Pre-commit hook validates no duplicates exist
- CI pipeline runs `scan_strates.py` for duplicate detection
- Violations are automatically documented in ADR's violations_documented section

### Violation Example

The ECOS-CLI case was resolved by removing the duplicate from L4-TOOLS and preserving the canonical L1-INFRA/ECOS-CLI repository.

## Consequences

- Enforces single source of truth for all repositories
- Prevents fragmentation across layers
- Provides automatic detection mechanism
- Requires explicit approval for any cross-strata integration

## Alternatives Considered

1. Manual monitoring (insufficient scale)
2. Ignoring duplicates (risk of inconsistency)
3. Centralized validation with scan_strates.py (chosen solution)

## Implementation Status

- Design document created: designs/clone-governance.yaml
- ADR created: ADR-032-clone-governance.md
- CI validation hook planned: check_no_duplicates

## Reference ADR

- **ADR** : ADR-032-clone-governance
- **IntentHash** : 0xCLONE_GOVERNANCE_20260731
- **Depot** : gerivdb/GOVERNANCE-HUB
- **Statut ADR** : proposed
- **Maj requise si** : statut ADR -> deprecated ou superseded
