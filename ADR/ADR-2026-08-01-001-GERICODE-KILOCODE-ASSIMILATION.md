---
type: ADR
status: proposed
date: "2026-08-01"
intent_hash: 0xGERICODE_ASSIMILATION_20260801
---

# ADR-2026-08-01-001-GERICODE-KILOCODE-ASSIMILATION
## Assimilation of GeriCode into Kilocode-VSIX Ecosystem

### 1. Context
GeriCode is currently a monolithic Node.js/VS Code extension located in 
`D:\DO\WEB\TOOLS\L2-PLATFORM\GeriCode`. It implements a Bat-Family themed 
communication interface with ECOS CLI integration but does not conform to 
Kilicode governance standards in several critical areas:

- Missing front-matter with `intent_hash`, `layer`, `slotWeight`
- No ADR backing for architectural decisions
- Monolithic architecture preventing modular skill reuse
- Absent inclusion in `pattern-router.md`
- No registry entry in `REGISTRY.yaml`
- Uses non-canonical strate `L2-PLATFORM` instead of `L3-CITIZENS`

### 2. Decision
It is decided to assimilate GeriCode into the Kilocode-VSIX ecosystem by:

1. **Governing via ADR**: Create this ADR to document the assimilation strategy
2. **Front-matter Alignment**: Add `_kilo` object with `intent_hash`, `layer`, `slotWeight`, etc. to `package.json`
3. **Architectural Refactor**: Split monolithic `extension.ts` into modular skills:
   - `bat-family-chat`
   - `ecos-cli-bridge` 
   - `quality-check-runner`
4. **Pattern Router Updates**: Add routing keywords for GeriCode operations
5. **Registry Update**: Add `GeriCode-L3` entry to `REGISTRY.yaml`
6. **CI Validation**: Extend `ci-validation-local.sh` to validate GeriCode manifests
7. **Strate Renaming**: Rename `L2-PLATFORM` to `L3-CITIZENS` in canonical directories

### 3. Consequences
- **Positive**: 
  - Full compliance with Kilicode sovereign governance policies
  - Enables cross-repo tooling and automated maintenance
  - Facilitates transverse skill handling (`pr-review-resolver`, `close-loop-detector`)
  - Maintains architectural consistency across `L3-CITIZENS` ecosystem

- **Negative/Impact**:
  - Breaking change for existing GeriCode extension users
  - Requires migration of existing functionality to new modular structure
  - Temporary loss of Bat-Family thematic elements during transition

### 4. Alternatives Considered
- **Maintain Separate Project**: Continue GeriCode as standalone VSIX outside Kilicode governance
- **Partial Integration**: Keep monolith but add minimal compliance patches
- **Reject Integration**: Decline assimilation and document as external project

All alternatives were rejected because they prevent the strategic goal of unified cross-repo governance and create technical debt.

### 5. Related Decisions
- ADR-2026-07-28-020-CTULU-TRIX-ECOS-CLI-ORCHESTRATION  
- ADR-2026-06-28-001-MASSIVE-DECOMPOSITION  
- Governance Governance-Gate (ADR-2026-06-07)

---

*Status: proposed*  
*Decision-Date: 2026-08-01*  
*Tags: governance, integration, refactor, assimilation*

