---
type: ADR
status: proposed
date: "2026-08-29"
intent_hash: 0xADR_CAUSAL_RESOLUTION_METHODOLOGY_20260829
---

# ADR-2026-08-29-001: Causal Resolution Methodology

## Status
Proposed

## Context
The "silent fail" in LLUX 7B .q243 inference revealed a systemic ontological mismatch:
- **Data domain**: Q4_0 quantization (continuous values `scale × (nibble - 8)`)
- **Kernel domain**: Ternary only (expected {-1, 0, 1})
- **Fallback**: `@Vector(4, f32)` on potentially unaligned data → Undefined Behavior → silent hang

The resolution was not a simple bug fix but a **causal realignment** of domains.

## Decision
Adopt **Causal-First Development Methodology** as the standard for all ecosystem development:

### 7 Principles
1. **Domain First** — Ontology precedes implementation. `domain_links.json` declares contracts `kernel.domain ⊇ data.domain` before any code.
2. **UB as First-Class Risk** — Undefined Behavior is the primary architectural risk. Tooling: `kg-l-type-guard`, `ctulu-zig-debug-adapter`, `ctulu-zig-fmt-auto`.
3. **Trace as Mirror** — `std.debug.print` is a mandatory mirror, not optional debug. Without traces, compiler optimizes UB into silent hang.
4. **Kernel Versioning** — Kernels are versioned domain contracts. Replacement = domain generalization + fixture migration + cross-repo traceability.
4. **Format as Gate** — Format is a gate, not style. Auto-fix loop mandatory (`ctulu-zig-fmt-auto`).
5. **Zombie Prevention** — Zombie processes are build correctness risks. Pre-build hook mandatory (`ctulu-auto-cleanup-hook`).
6. **Causal Traceability** — Every commit carries causal lineage: `intent_hash` → `domain_links.json` → `CAUSAL_DIFF.md`.

### Causal Dev Loop (7 Steps)
1. **Intent → Domain Links** — `domain_links.json` declares `data.domain`, `kernel.domain`, `intent_hash`
2. **KG-L Type Guard** (pre-commit) — Verifies `kernel.domain ⊇ data.domain`
3. **CTULU Zig Validator** (`--strict --auto-fix`) — Build + Warnings 0 + Format auto-fix
4. **CTULU Auto Cleanup** (pre-build) — Kill zombies, free locks
5. **Live Debug** — `ctulu-zig-debug-adapter` (DWARF/CodeView live, breakpoints, watch `@Vector`)
6. **Causal Diff** (post-commit) — Generates `CAUSAL_DIFF.md` + `intent_hash`
7. **Kernel Versioner + Fixture Registry** — Bump version, update fixtures.yaml, link cross-repo

## Consequences
- All new development must follow the Causal Dev Loop
- All kernels must be registered in `KG-L/kernels.yaml` with domain contracts
- All fixtures must be registered in `KG-L/fixtures.yaml` with checksums
- All commits must include `intent_hash` in commit message
- Pre-commit must run `kg-l-type-guard` and `zig_validator --strict --auto-fix`
- Pre-build must run `ctulu-auto-cleanup-hook`
- Post-commit must generate `CAUSAL_DIFF.md`

## References
- LLUX Design v2.0.0: `L0-CANON/unified-design/designs/llux/design.yaml`
- Causal Resolution Report: `0xCAUSAL_RESOLUTION_LLUX_Q40_GEMV_20260829`
- Domain Links: `KG-L/exports/domain_links.json` (IntentHash: `0xINTENT_Q243_NATIVE_INFERENCE_20260825_UPDATED`)

## IntentHash
**0xADR_CAUSAL_RESOLUTION_METHODOLOGY_20260829**