# src/ — Source Code Structure (RSS-v2.3 rss_depth=4)

This directory is the **target structure** for unified-design source code,
following RSS-v2.3 CRITICAL profile with `rss_depth=4`.

## Structure

```
src/
├── core/           # Core business logic (atoms, schemas, meta-design)
├── cli/            # CLI interfaces
├── engines/        # Engine implementations (trix, rlm, piano, llux, etc.)
├── mcp/            # MCP protocol implementations (future)
└── generators/     # Code/artifact generators
```

## Migration Plan (Non-Destructive)

**Current state**: 12+ engine-like directories at repo root:
- `engine/`, `generator/`, `loop_engine/`, `trix/`, `rlm/`, `piano/`, `llux/`, `gateway/`, `spidx/`, `triade/`, `runners/`, `loops/`

**Target**: Move contents into `src/engines/` and `src/generators/` with
appropriate namespacing. This is a **future migration** (out of scope
for current PRD-MOC-GEN-032) to avoid breaking existing imports.

**Strategy**:
1. Create `src/` structure (✅ done)
2. Document migration in this README
3. Migrate incrementally per engine with compatibility layers
4. Update imports and CI/CD

## Timeline

- Phase 4 (current): Structure created
- Phase 5+: Incremental migration per engine (separate PRDs)

## References

- RSS-v2.3 §4.2 (Structure niveau par niveau)
- PRD-MOC-GEN-032-unified-design-rss-v2-compliance-restructuring-2026-09-03.md