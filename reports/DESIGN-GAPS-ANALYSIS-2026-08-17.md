# Unified-Design Repository — Design Gaps Analysis Report

**Repository:** `gerivdb/unified-design`  
**Local Path:** `D:\DO\WEB\TOOLS\L0-CANON\unified-design`  
**Analysis Date:** 2026-08-17  
**Analyst:** Kilo (automated audit)  

---

## 1. Repository Structure Overview

```
unified-design/
├── .github/workflows/
│   └── design-validation.yml          # GitHub Actions workflow (⚠️ ADR-024 VIOLATION)
├── .kiva/pipelines/
│   └── unified-design.yaml            # KIVA-CLI sovereign pipeline (5 steps)
├── .pre-commit-config.yaml            # Only ASCII fixer + GATE-6 (no schema validation)
├── ADR/                               # 30 ADRs (ADR-012 to ADR-041)
├── CROSSLINKS/
│   └── talex-unified-graph.md         # Only 1 crosslink (9 declared in REPO.yaml)
├── META-DESIGN.md                     # Generated documentation
├── ONTOLOGY_MAP.md                    # ONTOLOGY ↔ MDU mapping
├── PRD/                               # PRDs for gaps
├── REPO.yaml                          # Repo declaration
├── atoms/                             # ~197 atom YAML/MD files
├── atoms_registry.yaml                # 165 entries (some with backslashes, duplicates)
├── api/                               # OpenAPI specs
├── conventions/                       # 16 convention domains
├── designs/                           # 68 design files (duplicates + nested)
│   ├── *.yaml                         # Root-level designs
│   ├── */design.yaml                  # Nested instance designs
│   └── symptom/zombie-symptom/        # Template + instance with placeholder syntax
├── docs/                              # Documentation
├── engine/                            # Runtime engines
├── generated-designs/                 # 3 generated instances
├── loop_engine/                       # DAG/loop detection runtime
├── meta-design.yaml                   # MDU v2.1.0 executable schema
├── package.json
├── pipelines/
├── ports/                             # 6 port schemas + registry
├── reports/                           # Session reports
├── schemas/                           # 6 JSON Schema files + 2 YAML schemas
│   ├── meta-design.schema.json        # draft-07
│   ├── design.schema.json             # draft-2020-12
│   ├── registry.schema.json           # draft-2020-12 (duplicate of registry-schema.yaml)
│   ├── registry-schema.yaml           # draft-2020-12 (JSON content in .yaml file)
│   ├── artifact-quality.schema.json   # draft-2020-12
│   ├── artifact-quality.schema.yaml   # draft-2020-12 (JSON content in .yaml file)
│   └── ports/*.json                   # 6 port contracts
├── scripts/                           # 65+ validation/maintenance scripts
├── tools/                             # Generation tools
└── workflows/
```

---

## 2. Key Files Analyzed

| File | Type | Status |
|------|------|--------|
| `meta-design.yaml` | Executable schema | v2.1.0, active, 365 lines |
| `schemas/meta-design.schema.json` | JSON Schema | draft-07, `additionalProperties: false` |
| `schemas/design.schema.json` | JSON Schema | draft-2020-12 |
| `schemas/registry.schema.json` | JSON Schema | draft-2020-12 |
| `schemas/registry-schema.yaml` | JSON Schema in YAML | draft-2020-12 |
| `schemas/artifact-quality.schema.json` | JSON Schema | draft-2020-12 |
| `schemas/artifact-quality.schema.yaml` | JSON Schema in YAML | draft-2020-12 |
| `atoms_registry.yaml` | Registry | 165 entries |
| `designs/*.yaml` | Design instances | ~30 root-level |
| `designs/*/design.yaml` | Design instances | ~30 nested |
| `.kiva/pipelines/unified-design.yaml` | CI pipeline | 5 steps |
| `.github/workflows/design-validation.yml` | CI workflow | GitHub Actions |
| `.pre-commit-config.yaml` | Git hooks | 2 hooks only |

---

## 3. Specific Design Gaps Found

### GAP-1: Schema Validation Inconsistencies

**Severity:** P0 — Breaking validation across schemas

#### 1.1 Mixed JSON Schema Draft Versions
- `schemas/meta-design.schema.json` uses **draft-07** (`http://json-schema.org/draft-07/schema#`)
- `schemas/design.schema.json` uses **draft-2020-12** (`https://json-schema.org/draft/2020-12/schema`)
- `schemas/registry.schema.json` uses **draft-2020-12**

**Impact:** Different validators may interpret `required`, `additionalProperties`, and `unevaluatedProperties` differently. A validator that defaults to draft-07 behavior for `meta-design.schema.json` will not support `if/then/else` or `$defs` introduced in later drafts.

**Example:**
```json
// meta-design.schema.json (draft-07)
"$schema": "http://json-schema.org/draft-07/schema#"

// design.schema.json (draft-2020-12)
"$schema": "https://json-schema.org/draft/2020-12/schema"
```

#### 1.2 JSON Schema Content in `.yaml` Files
- `schemas/registry-schema.yaml` contains raw JSON Schema (not YAML)
- `schemas/artifact-quality.schema.yaml` contains raw JSON Schema (not YAML)

**Impact:** These files are misleadingly named. They are not valid YAML documents with YAML-native schema definitions — they are JSON Schema documents stored in `.yaml` containers. Any YAML-aware tooling will parse them as YAML (which happens to work for JSON), but the intent is unclear.

**Example:**
```yaml
# schemas/registry-schema.yaml — actually JSON Schema content
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  ...
}
```

#### 1.3 `additionalProperties: false` Blocks Extensions
- `meta-design.schema.json` has `additionalProperties: false` at the root level
- This caused CI failures when MOC-2/OCP added `designs`, `complexity_gates`, `consumers`, `profile`, `port_id` fields

**Evidence from commit history:**
```
ac1fa2e fix: corrige 6 lacunes P0 unified-design (schema, validator, status) (#61)
31509bc fix(schema): remove couche_gouvernance from meta-design schema (lacune #1)
```

#### 1.4 Inconsistent `intent_hash` Patterns
- `meta-design.schema.json`: `"^0x[a-zA-Z0-9_]+$"` (no hyphens)
- `design.schema.json`: `"^0x[a-zA-Z0-9_-]+$"` (allows hyphens)
- `artifact-quality.schema.json`: `"^0x[A-Z0-9_]{8,}$"` (requires uppercase, min 8 chars)

**Impact:** An `intent_hash` like `0xTINA-Plix-CONNECTOR-20260715` would pass `design.schema.json` but fail `meta-design.schema.json`.

#### 1.5 Missing Required Fields in Design Files
- `design.schema.json` requires `design_version`, `layer`, `status`, `intent_hash`
- `designs/moc-governance.yaml` is missing `design_version`
- `designs/fractal-recursion.yaml` is missing `design_version`
- `designs/buzz-persistent-state.yaml` uses `layer: L1` (inconsistent with `L0-L4` pattern)

---

### GAP-2: Missing Cross-Repo Design References

**Severity:** P1 — Broken or missing cross-repo links

#### 2.1 CROSSLINKS Underpopulated
- `REPO.yaml` declares 9 crosslinks: GOVERNANCE-HUB, REPO-STANDARDS, ONTOLOGY, MOX, LLUX, NEXUS, TOPOS, PLIX, connard-design
- `CROSSLINKS/` directory contains **only 1 file**: `talex-unified-graph.md`

**Missing crosslinks:**
- GOVERNANCE-HUB → `GOVERNANCE-HUB/known_repositories.yaml`
- REPO-STANDARDS → `REPO-STANDARDS/REPO.yaml`
- ONTOLOGY → `ONTOLOGY/ONTOLOGY.yaml`
- MOX → `MOX/builtin/`
- LLUX → `LLUX/llux_openapi.yaml`
- NEXUS → `NEXUS/nexus-core/`
- TOPOS → `TOPOS/registry/repos.json`
- PLIX → `PLIX/plix-codec/`
- connard-design → `connard-design/connard.yaml`

#### 2.2 Broken Crosslink References
- `CROSSLINKS/talex-unified-graph.md` references `src/talex/core/unified_graph.py` and `src/talex/readers/__init__.py::EcosystemReader._read_unified_design` in `gerivdb/TALEX`
- TALEX is listed as L4-TOOLS but the actual repo `gerivdb/TALEX` is **not in `known_repositories.yaml`** (inactive/uncloned per `ecos-cli-launcher-multirepo.md`)

#### 2.3 Non-Standard Repo Names in Design Instances
- `designs/symptom/zombie-symptom/instances/process-zombie-proliferation/symptom.yaml` uses:
  - `GeriCode/L2` (should be `gerivdb/GERIBOOKING` or `gerivdb/BRAIN`)
  - `KIX/L2` (not a standard repo name)
  - `TRIX/L4` (should be `gerivdb/TRIX`)
  - `KIVA-CLI/L1` (should be `gerivdb/KIVA-CLI`)

**Impact:** These names don't match the `known_repositories.yaml` naming convention (`gerivdb/<REPO>`), breaking any tool that resolves cross-repo references.

#### 2.4 Duplicate ADR Reference
- `meta-design.yaml` lines 347-348: `ADR-2026-07-30-004` appears **twice** in the `references` array

```yaml
references:
  - ADR-2026-07-30-004   # line 347
  - ADR-2026-07-30-004   # line 348 (duplicate)
```

---

### GAP-3: Atom/Stem Normalization Issues

**Severity:** P1 — Registry integrity compromised

#### 3.1 Mixed Path Separators
- `atoms_registry.yaml` uses **forward slashes** for most entries: `atoms/GOVERNANCE/mox-meta-coherence.yaml`
- But uses **Windows backslashes** for methodology entries: `atoms/methodology\INDEX.md`, `atoms/methodology\c\ATOM-001-c-memory-management.md`

**Impact:** On Linux/macOS, backslash paths are invalid. Any cross-platform validation will fail for 25+ entries.

**Example:**
```yaml
# Valid
- path: atoms/GOVERNANCE/mox-meta-coherence.yaml

# Invalid on non-Windows
- path: atoms/methodology\INDEX.md
- path: atoms/methodology\c\ATOM-001-c-memory-management.md
```

#### 3.2 Duplicate `depends_on` Entries
- `atoms/methodology/git/ATOM-045-git-arbiter-health-probe.md`: `ATOM-045` listed twice
- `atoms/methodology/git/ATOM-046-wic-branch-prefix-validation.md`: `ATOM-046` listed twice
- `atoms/methodology/git/ATOM-047-git-cleanup-remote-deletion-api.md`: `ATOM-047` listed twice
- `atoms/methodology/git/ATOM-048-vibe-git-graph-coherence-metric.md`: `ATOM-048` listed twice
- `atoms/methodology/git/ATOM-049-clusterwave-path-auto-resolver.md`: `ATOM-049` listed twice
- `atoms/methodology/git/ATOM-050-duplicate-commit-detector.md`: `ATOM-050` listed twice
- `atoms/methodology/git/ATOM-051-repo-locator-validator.md`: `ATOM-051` listed twice

**Impact:** Circular self-references in `depends_on` create false dependency cycles.

#### 3.3 Inconsistent Hash Formats
- Most hashes are lowercase: `b4d574dec3c0`, `089fbc53d8dc`
- Some are mixed/uppercase: `2EF20FF52435` (ATOM-042), `1866ad6e83ac`
- Hash lengths vary: 6 chars (`b4d574`), 10 chars (`089fbc53d8`), 12 chars (`2EF20FF52435`)

**Impact:** The `registry.schema.json` requires `^[a-fA-F0-9]{6,64}$` which allows mixed case, but the inconsistency makes hash comparison unreliable.

#### 3.4 Missing Atom Files
- `atoms_registry.yaml` references `ATOM-052-artifact-lifecycle-zones.md` but the actual file is `atoms/ATOM-052-artifact-lifecycle-zones.md` (exists)
- `atoms_registry.yaml` references `ATOM-042-REPOSITORY-CENSUS.md` with `depends_on: [ATOM-042]` — self-referential

---

### GAP-4: Template vs Instance Drift

**Severity:** P1 — Generated designs don't match schema

#### 4.1 Zombie-Symptom Template Uses Placeholders
- `designs/symptom/zombie-symptom/template/symptom.yaml` contains placeholder syntax:
  - `name: <symptom_name>`
  - `intent_hash: 0x<SLUG_MAJUSCULES>`
  - `category: <system_health | cross_repo | runtime | governance>`
  - `repos_target: [<repo/L>]`

**Impact:** These files would fail `design.schema.json` validation because `<symptom_name>` doesn't match `^[a-z0-9-]+$` and `<SLUG_MAJUSCULES>` doesn't match `^0x[a-zA-Z0-9_-]+$`.

#### 4.2 Instance Drifts from Template
- `designs/symptom/zombie-symptom/instances/process-zombie-proliferation/symptom.yaml` adds fields not in the template:
  - `symptom: |` (multi-line string)
  - `indicators:` (new section)
  - `impact:` (modified from template)
  - `implementation_mapping:` (new section)

**Impact:** No schema validates these instance-specific fields, creating a validation blind spot.

#### 4.3 Root-Level vs Nested Design Drift
Multiple designs exist in **two locations** with completely different structures:

| Design | Root-level (`designs/*.yaml`) | Nested (`designs/*/design.yaml`) |
|--------|------------------------------|----------------------------------|
| `moc-governance` | 44 lines, full schema | 5 lines, minimal |
| `plix` | 30+ lines, full schema | 5 lines, minimal |
| `llux` | 20+ lines, full schema | 5 lines, minimal |
| `fractal-recursion` | 19 lines, full schema | 5 lines, minimal |

**Example — `moc-governance`:**
```yaml
# designs/moc-governance.yaml (44 lines)
name: moc-governance
version: 1.0.0
status: active
layer: L0-L4
intent_hash: 0xmoc_governance_design_20260801
inherits: [fractal-recursion, ouroboros]
depends_on: [ATOM-045-git-arbiter-health-probe, ...]
bridges: [...]
capabilities: [...]
components: [...]
constraints: [...]

# designs/moc-governance/design.yaml (5 lines)
name: moc-governance
version: 1.0.0
status: active
profile: STANDARD
consumers: []
```

**Impact:** `design.schema.json` would reject the nested 5-line `design.yaml` because it lacks `layer`, `intent_hash` (in proper format), and `design_version`. The root-level `moc-governance.yaml` would be rejected because it lacks `design_version`.

#### 4.4 Generated-Design Inheritance Mismatch
- `generated-designs/tina-plix-connector/design.yaml` declares:
  ```yaml
  inherits:
    - plix-codec        # Does not exist as a design
    - sandbox-isolation  # Does not exist as a design
    - citizen-routing    # Does not exist as a design
  ```
- Actual design files are named: `plix.yaml`, `sandbox-isolation.yaml`, `citizen-routing.yaml`

**Impact:** Inheritance validation fails silently because there's no check that inherited designs actually exist.

---

### GAP-5: YAML/JSON Syntax Validation Gaps

**Severity:** P1 — Invalid files pass current validation

#### 5.1 Placeholder Syntax in Templates
- `designs/symptom/zombie-symptom/template/*.yaml` contains `<...>` placeholders
- These files are matched by the GitHub Actions workflow glob `designs/**` but would fail schema validation

#### 5.2 `validate_yaml.py` is Frontmatter-Only
- `scripts/validate_yaml.py` only checks for YAML frontmatter presence and required keys
- It does **not** validate against JSON Schema
- It does **not** validate YAML syntax beyond frontmatter extraction

**Impact:** Invalid YAML structures can pass the current validation pipeline.

#### 5.3 No Hash Consistency Validation
- `atoms_registry.yaml` stores SHA1 hashes for each atom file
- No script validates that the stored hash matches the actual file content
- `scripts/validate_atom_registry.py` exists but is **not in the KIVA-CLI pipeline**

#### 5.4 Multi-Doc YAML Not Fully Handled
- `designs/buzz-persistent-state.yaml` contains multi-line strings with embedded newlines
- The GitHub Actions workflow uses `yaml.safe_load_all()` but `validate_yaml.py` uses `yaml.safe_load()` (single doc)

---

### GAP-6: Missing Governance Hooks for Design Docs

**Severity:** P0 — Direct ADR-024 violation + incomplete validation

#### 6.1 GitHub Actions Workflow — ADR-024 VIOLATION
- `.github/workflows/design-validation.yml` uses **GitHub Actions**
- **ADR-024** explicitly forbids GitHub Actions for CI/validation:
  > CI, validation, merge, synchronisation → exclusivement via outils locaux : KIVA-CLI / ECOS-CLI
  > Mode BDCP permanent : ne jamais suggérer de basculer en mode FREE pour push git ou CI

**Evidence from recent session report:**
```
~20:29 | Échec GitHub Actions : account locked due to a billing issue | gh pr checks 60
~20:30 | Bascule vers CI locale KIVA-CLI | kiva ci run unified-design
```

**Impact:** The GitHub Actions workflow is non-functional (billing lock) and violates the sovereign CI policy. It should be removed.

#### 6.2 No Pre-Commit Schema Validation Hook
- `.pre-commit-config.yaml` only has:
  - `ascii-fixer` (auto-correction)
  - `gate-6` (ASCII validator)
- **Missing:** JSON Schema validation for `meta-design.yaml`, `designs/*.yaml`, `atoms_registry.yaml`
- **Missing:** KIVA-CLI pipeline invocation (`kiva pipeline run unified-design`)

**Impact:** Invalid changes can be committed without schema validation, relying only on the KIVA-CLI pipeline run manually or in CI.

#### 6.3 No OCP/Auto-Discovery Check
- PRD-MOC-MDU-GAPS-2026-08-16.md defines MOC-2 rule: `meta-design.yaml` must be auto-generated
- `.kiva/pipelines/unified-design.yaml` does **not** include a step to verify `meta-design.yaml` matches the auto-generated version
- `scripts/validate_meta_design.py` validates against the schema but doesn't check if the file is stale

**Impact:** `meta-design.yaml` can diverge from the source manifests without detection.

#### 6.4 No Cross-Repo Reference Validation
- No hook or CI step validates that cross-references in `CROSSLINKS/`, `ONTOLOGY_MAP.md`, and `designs/*.yaml` point to existing repos/files
- `designs/symptom/zombie-symptom/instances/process-zombie-proliferation/symptom.yaml` references `ONTOLOGY/ONTOLOGY.yaml` but no check verifies this file exists

#### 6.5 No Design Instance Consistency Check
- No validation that `designs/*.yaml` and `designs/*/design.yaml` are consistent
- No detection of orphaned nested `design.yaml` files or orphaned root-level designs

---

## 4. Impact on Dependent Repos

| Dependent Repo | Impact | Gap Reference |
|----------------|--------|---------------|
| **GOVERNANCE-HUB** | `known_repositories.yaml` cross-references broken; `ONTOLOGY_MAP.md` stale | GAP-2.1, GAP-2.3 |
| **REPO-STANDARDS** | `REPO.yaml` crosslinks declared but `CROSSLINKS/` empty | GAP-2.1 |
| **ONTOLOGY** | `ONTOLOGY_MAP.md` references `ONTOLOGY.yaml` path not validated | GAP-2.2, GAP-6.4 |
| **MOX** | `REPO.yaml` lists MOX as crosslink but no CROSSLINKS entry | GAP-2.1 |
| **TALEX** | `CROSSLINKS/talex-unified-graph.md` references TALEX paths but repo is inactive | GAP-2.2 |
| **KIVA-CLI** | Pipeline `unified-design` references non-existent designs in inheritance chains | GAP-4.4 |
| **PLIX** | `generated-designs/tina-plix-connector/design.yaml` inherits from `plix-codec` (doesn't exist) | GAP-4.4 |
| **TRIX** | `process-zombie-proliferation` references `TRIX/L4` (non-standard name) | GAP-2.3 |
| **ALL repos using atoms** | `atoms_registry.yaml` has Windows backslashes breaking Linux validation | GAP-3.1 |

---

## 5. Recommended Fixes

### FIX-1: Schema Validation Inconsistencies
| Action | Target File | Priority |
|--------|-------------|----------|
| Unify all schemas to **draft-2020-12** | `schemas/meta-design.schema.json` | P0 |
| Rename `.yaml` schema files to `.json` or convert to native YAML | `schemas/registry-schema.yaml`, `schemas/artifact-quality.schema.yaml` | P1 |
| Standardize `intent_hash` pattern to `^0x[a-zA-Z0-9_-]+$` across all schemas | All schema files | P1 |
| Add `design_version` to all `designs/*.yaml` files | `designs/moc-governance.yaml`, `designs/fractal-recursion.yaml`, etc. | P1 |
| Add `layer` and `intent_hash` to all nested `designs/*/design.yaml` files | `designs/*/design.yaml` | P1 |
| Remove `additionalProperties: false` or add all expected properties | `schemas/meta-design.schema.json` | P0 |

### FIX-2: Missing Cross-Repo Design References
| Action | Target File | Priority |
|--------|-------------|----------|
| Create 8 missing CROSSLINKS files | `CROSSLINKS/*.md` | P1 |
| Verify TALEX repo existence in `known_repositories.yaml` | GOVERNANCE-HUB | P1 |
| Standardize repo names in design instances to `gerivdb/<REPO>` | `designs/symptom/zombie-symptom/instances/process-zombie-proliferation/symptom.yaml` | P1 |
| Remove duplicate `ADR-2026-07-30-004` entry | `meta-design.yaml` lines 347-348 | P0 |
| Add cross-repo reference validation script | `scripts/validate_crossrefs.py` | P2 |

### FIX-3: Atom/Stem Normalization Issues
| Action | Target File | Priority |
|--------|-------------|----------|
| Replace all backslashes with forward slashes | `atoms_registry.yaml` | P0 |
| Remove duplicate `depends_on` entries (self-references) | `atoms_registry.yaml` | P0 |
| Standardize hash format to lowercase, fixed length (12 chars) | `atoms_registry.yaml` | P1 |
| Add hash consistency validation to KIVA-CLI pipeline | `.kiva/pipelines/unified-design.yaml` | P1 |

### FIX-4: Template vs Instance Drift
| Action | Target File | Priority |
|--------|-------------|----------|
| Replace placeholder syntax with valid defaults or mark templates as excluded from validation | `designs/symptom/zombie-symptom/template/*.yaml` | P1 |
| Add schema for `symptom.yaml` instances or document allowed extensions | `schemas/symptom.schema.json` | P2 |
| Choose one canonical location for each design (root OR nested, not both) | `designs/moc-governance.yaml` + `designs/moc-governance/design.yaml` | P1 |
| Fix inheritance chains to use existing design names | `generated-designs/tina-plix-connector/design.yaml` | P0 |
| Add design consistency check to KIVA-CLI pipeline | `.kiva/pipelines/unified-design.yaml` | P2 |

### FIX-5: YAML/JSON Syntax Validation Gaps
| Action | Target File | Priority |
|--------|-------------|----------|
| Upgrade `validate_yaml.py` to validate against JSON Schema | `scripts/validate_yaml.py` | P1 |
| Add YAML syntax validation for all files (not just frontmatter) | `scripts/validate_yaml.py` | P1 |
| Add hash verification script to KIVA-CLI pipeline | `scripts/validate_atom_registry.py` → `.kiva/pipelines/unified-design.yaml` | P1 |
| Exclude template files with placeholders from validation globs | `.kiva/pipelines/unified-design.yaml`, `.github/workflows/design-validation.yml` | P1 |

### FIX-6: Missing Governance Hooks for Design Docs
| Action | Target File | Priority |
|--------|-------------|----------|
| **REMOVE** `.github/workflows/design-validation.yml` (ADR-024 violation) | `.github/workflows/design-validation.yml` | **P0** |
| Add pre-commit hook for KIVA-CLI pipeline (`kiva pipeline run unified-design`) | `.pre-commit-config.yaml` | P0 |
| Add MOC-2/OCP check: verify `meta-design.yaml` matches auto-generated version | `.kiva/pipelines/unified-design.yaml` | P1 |
| Add cross-reference validation step to KIVA-CLI pipeline | `.kiva/pipelines/unified-design.yaml` | P1 |
| Add design instance consistency check to KIVA-CLI pipeline | `.kiva/pipelines/unified-design.yaml` | P2 |

---

## 6. Summary

| Category | P0 | P1 | P2 | Total |
|----------|----|----|----|-------|
| Schema validation inconsistencies | 2 | 4 | 0 | 6 |
| Missing cross-repo design references | 1 | 3 | 1 | 5 |
| Atom/stem normalization issues | 2 | 2 | 0 | 4 |
| Template vs instance drift | 1 | 3 | 1 | 5 |
| YAML/JSON syntax validation gaps | 0 | 4 | 1 | 5 |
| Missing governance hooks | 2 | 2 | 1 | 5 |
| **Total** | **8** | **18** | **4** | **30** |

### Critical Path (P0 — Must Fix Before Next Merge)

1. **Remove `.github/workflows/design-validation.yml`** — Direct ADR-024 violation
2. **Unify JSON Schema drafts to 2020-12** — Mixed drafts cause validation divergence
3. **Remove `additionalProperties: false` from `meta-design.schema.json`** — Blocks MOC extensions
4. **Standardize `intent_hash` pattern across all schemas** — Inconsistent regex causes silent failures
5. **Replace Windows backslashes in `atoms_registry.yaml`** — Breaks Linux CI
6. **Remove duplicate `depends_on` entries** — Creates false dependency cycles
7. **Fix inheritance chains in `generated-designs/`** — References non-existent designs
8. **Add pre-commit hook for KIVA-CLI pipeline** — Current hooks don't validate schemas

---

*Report generated by Kilo automated audit — unified-design repository*
