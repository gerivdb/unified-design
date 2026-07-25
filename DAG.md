# META-DESIGN DAG

```text
unified-design/
├── ADR/
│   ├── ADR-014-git-policy.md
│   ├── ADR-016-loop-engine.md
│   ├── ADR-018-governance-hub-mdu-extraction.md
│   ├── ADR-019-phase3-incremental.md
│   ├── ADR-027-wazaa-mdc-integration.md
│   ├── ADR-028-design-principles.md
│   └── ADR-029-cross-repo-flows.md
├── atoms/
│   ├── ATOM-042-REPOSITORY-CENSUS.md
│   ├── methodology/
│   │   ├── git/
│   │   ├── python/
│   │   ├── rust/
│   │   └── universal/
│   ├── build-pipeline.yaml
│   ├── ci-pipeline.yaml
│   ├── cluster-federation.yaml
│   ├── cognitive-bridge.yaml
│   ├── cognitive-bus.yaml
│   ├── cross-repo-flow.yaml
│   ├── design-principle.yaml
│   ├── dip.yaml
│   ├── git-remote-safety.yaml
│   ├── governance-gate-script.yaml
│   ├── mcp-fix-diagnostics.yaml
│   ├── multi-repo-audit.yaml
│   ├── registry-driven-orchestration.yaml
│   ├── security-fabric.yaml
│   ├── skill-orchestration.yaml
│   ├── srp.yaml
│   └── yagni.yaml
├── conventions/
│   ├── anti-patterns/
│   ├── ci/
│   ├── commit/
│   ├── default-fail/
│   ├── evidence/
│   ├── loop/
│   ├── maker-checker/
│   ├── organs/
│   ├── topos/
│   ├── trix/
│   └── verses/
├── docs/
│   ├── GIT_BRANCH_CONVENTION.md
│   ├── LAYER_STRUCTURE.md
│   ├── META-DESIGN.md
│   └── README.md
├── EPICS/
├── PRD/
├── scripts/
│   └── design_seeker_mvp.py
├── tools/
│   └── ascii_fix.py
└── workflows/
    └── ci-template.yml
```

Liens clés :
- ADR-028 → atoms/design-principle.yaml
- ADR-029 → atoms/cross-repo-flow.yaml
- ADR-016 → loop_engine/
- ADR-018 → governance-hub extraction
- atoms/ci-pipeline.yaml → workflows/ci-template.yml
- atoms/build-pipeline.yaml → scripts/design_seeker_mvp.py
