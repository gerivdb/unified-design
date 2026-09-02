---
type: ADR
status: proposed
date: "2026-08-29"
intent_hash: 0xADR_DOMAIN_FIRST_KERNEL_CONTRACTS_20260829
---

# ADR-2026-08-29-002: Domain-First Kernel Contracts

## Status
Proposed

## Context
The LLUX silent fail was caused by a domain mismatch:
- **Data**: Q4_0 quantized weights (continuous, `scale × (nibble - 8)`)
- **Kernel**: `gemv_ternary_f32` expecting ternary weights `{-1, 0, 1}`

The kernel was invoked on data outside its domain, producing all-zero outputs silently.

## Decision
All kernels must declare their **domain contract** explicitly, and all data loaders must declare their **produced domain**. The contract is:

```
kernel.domain ⊇ data.domain
```

### Domain Hierarchy
```
general_f32 ⊃ {q4_0, ternary, f16, f32, i2_s, q243}
ternary       ⊃ {ternary}
q4_0          ⊃ {q4_0}
f16           ⊃ {f16}
f32           ⊃ {f32}
i2_s          ⊃ {i2_s}
q243          ⊃ {q243}
```

### Enforcement
1. **Kernel Declaration**: Every kernel in `KG-L/kernels.yaml` must declare its `domain`
2. **Loader Declaration**: Every loader in `src/*loader*.zig` must declare `produces` domain
3. **Type Guard**: `kg-l-type-guard` pre-commit hook verifies `kernel.domain ⊇ data.domain`
4. **CI Gate**: `zig_validator --strict --type-guard` blocks merge on violation

### Kernel Registration
All kernels must be registered in `KG-L/kernels.yaml`:
```yaml
kernels:
  - name: gemv_f32
    version: "2.0.0"
    domain: general_f32
    status: active
    supersedes: [gemv_ternary_f32]
    fixtures: [q40_block, q243_runnable]
```

## Consequences
- Domain mismatch caught at pre-commit, not runtime
- Kernel replacement requires domain generalization proof
- Cross-repo traceability via `domain_links.json`

## References
- `KG-L/kernels.yaml` — Kernel registry
- `KG-L/exports/domain_links.json` — Domain ontology
- `CTULU/tools/kg-l-type-guard` — Enforcement tool

## IntentHash
**0xADR_DOMAIN_FIRST_KERNEL_CONTRACTS_20260829**