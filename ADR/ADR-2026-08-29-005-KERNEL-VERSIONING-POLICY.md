---
type: ADR
status: proposed
date: "2026-08-29"
intent_hash: 0xADR_KERNEL_VERSIONING_POLICY_20260829
---

# ADR-2026-08-29-005: Kernel Versioning Policy

## Status
Proposed

## Context
The LLUX resolution required replacing `gemv_ternary_f32` (v1.0.0, domain: ternary) with `gemv_f32` (v2.0.0, domain: general_f32). This was done ad-hoc without:
- Version bump protocol
- Fixture migration plan
- Cross-repo notification
- Domain contract update

## Decision
All kernels must follow **Semantic Versioning with Domain Contracts**:

## Versioning Rules

### Version Format
`MAJOR.MINOR.PATCH` per SemVer 2.0.0

### Version Bump Rules
| Change Type | Version Bump | Domain Change | Fixture Migration |
|-------------|--------------|---------------|-------------------|
| Bug fix, no domain change | PATCH | No | No |
| New feature, same domain | MINOR | No | No |
| Domain generalization | MAJOR | Yes (superset) | Required |
| Domain specialization | MAJOR | Yes (subset) | Required |
| Breaking API change | MAJOR | Any | Required |

### Domain Change Rules
- **Generalization** (e.g., `ternary` → `general_f32`): MAJOR bump, must prove `new_domain ⊇ old_domain`
- **Specialization** (e.g., `general_f32` → `q4_0`): MAJOR bump, must document data loss
- **Same domain**: MINOR or PATCH per SemVer

### Fixture Migration Protocol
When kernel domain changes:
1. **Identify affected fixtures** via `fixtures.yaml` consumers
2. **Generate new fixtures** via generator scripts
3. **Update `fixtures.yaml`** with new checksums
3. **Run `kg-l-type-guard`** to verify new domain subsumption
4. **Update `domain_links.json`** with new kernel domain
5. **Update `CHANGELOG.md`** with migration notes

### Registry Updates
All changes must update:
1. `KG-L/kernels.yaml` — kernel entry with new version, domain, supersedes
2. `KG-L/fixtures.yaml` — fixture checksums, consumers, generators
3. `KG-L/exports/domain_links.json` — kernel domain, intent_hash
4. `CHANGELOG.md` — human-readable summary

### Supersession Protocol
When kernel A supersedes kernel B:
1. A's `supersedes` includes B
2. B's `status` = `deprecated`, `superseded_by` = A
3. B's `updated_at` = now
4. Fixtures referencing B updated to reference A
5. `CHANGELOG.md` documents migration path

### Cross-Repo Notification
On kernel bump:
1. `kg-l kernel bump` triggers `fixtures.yaml` migration
2. `kg-l kernel bump` updates `domain_links.json`
3. CI posts notification to affected repos (LLUX, CTULU, PIANO)
4. Consumers have 7 days to adapt before deprecated kernel removed

### Registry Format
```yaml
# KG-L/kernels.yaml
kernels:
  - name: gemv_f32
    version: "2.0.0"
    domain: general_f32
    status: active
    supersedes: [gemv_ternary_f32]
    intent_hash: 0xKERNEL_GEMV_F32_20260829
    fixtures: [q40_block, q243_runnable]
    simd: SSE4.2
    unroll: 4
    description: "General GEMV f32 kernel..."
    created_at: "2026-08-29T00:00:00Z"
    updated_at: "2026-08-29T00:00:00Z"
    created_by: "kg-l-kernel-versioner"
```

## Enforcement
- **Pre-commit**: `kg-l-type-guard` verifies new kernel domain subsumes all data domains
- **CI**: `kg-l kernel validate --strict` runs on PR
- **Release**: `kg-l kernel bump` requires `--intent-hash` and `--description`

## References
- `KG-L/kernels.yaml` — Kernel registry
- `KG-L/fixtures.yaml` — Fixture registry
- `KG-L/exports/domain_links.json` — Domain ontology

## IntentHash
**0xADR_KERNEL_VERSIONING_POLICY_20260829**