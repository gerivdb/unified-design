# Automation Targets — Meta Aggregation Report

**Scopes**: 1
**KG Engines**: 120 targets
**Total targets**: 127
**Existing**: 4
**Missing**: 3
**Patterns**: 2

## Scopes

### unified-design

- **Path**: `D:\DO\WEB\TOOLS\L0-CANON\unified-design`
- **Targets**: 7 (existing: 4, missing: 3)
- **Patterns**: 2

**Missing items**:
- SKILL: `registry-sync-checker`
- PRIMITIVE: `registry-sync-checker`
- ROUTINE: `registry-sync-checker`

## KG Engines

### KG_L

- **Count**: 115
- ✅ **CONCEPT**: garde_fou
- ✅ **CONCEPT**: gguf
- ✅ **CONCEPT**: q243
- ✅ **CONCEPT**: piano_diff
- ✅ **CONCEPT**: kbin
- ✅ **CONCEPT**: llux_native
- ✅ **CONCEPT**: ternary_weights
- ✅ **CONCEPT**: transport_ptx1
- ✅ **CONCEPT**: i2_s
- ✅ **CONCEPT**: empirical_spec_port

### VOLTX

- **Count**: 4
- ✅ **CONCEPT**: VERSES
- ✅ **BRIDGE**: VOLTX <-> KG-L
- ✅ **ROUTINE**: verses_versioning
- ✅ **BRIDGE**: KG-L <-> VOLTX bridge

### VERSES

- **Count**: 1
- ✅ **CONCEPT**: verse-discipline

### Non-Overlap Analysis

| Engine | Unique | Overlap |
|--------|--------|---------|
| KG-L | 115 | 0 with VOLTX |
| VOLTX | 4 | 0 with VERSES |
| VERSES | 1 | 0 with KG-L |

## Recommendations

1. [SCOPE] SKILL: `registry-sync-checker`
2. [SCOPE] PRIMITIVE: `registry-sync-checker`
3. [SCOPE] ROUTINE: `registry-sync-checker`
