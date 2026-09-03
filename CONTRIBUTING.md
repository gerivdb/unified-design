# Contributing to unified-design

Thank you for your interest in contributing to unified-design, the Meta-Design
Repository (MDU) for the gerivdb ecosystem.

## Standards Compliance

This repository follows **RSS-v2.3** (Repo Structure Standard) with **CRITICAL**
profile and `rss_depth=4`. All contributions must maintain structural compliance.

### Pre-commit Hooks

The following hooks run on every commit:

- **ASCII Fixer** (`ascii-fixer`) — Auto-corrects non-ASCII characters
- **GATE-6 ASCII Validator** (`gate-6`) — Validates ASCII-only source
- **KIVA-CLI Pipeline** (`kiva-pipeline-unified-design`) — Runs MDU validation

Install hooks:
```bash
pre-commit install
```

## Development Workflow

1. Fork and clone the repository
2. Create a feature branch: `git checkout -b feat/your-feature`
3. Make changes following RSS-v2.3 structure
4. Run validation: `python scripts/compliance_scanner.py --repo unified-design --strict`
5. Commit with conventional commits: `feat(scope): description`
6. Push and open a PR

## Structure Requirements

### Directories (RSS-v2.3 CRITICAL profile)

| Directory | Required | Purpose |
|-----------|----------|---------|
| `ADR/` | ✅ | Architecture Decision Records |
| `CROSSLINKS/` | ✅ | Inter-repo bridges |
| `EPICS/` | ✅ | Epics with `EPICS-000-index.md` |
| `INTENTS/` | ✅ | Intents with `INTENTS-000-index.md` |
| `PRD/` | ✅ | PRDs with `PRD-000-index.md` |
| `REPORTS/` | ✅ | Reports |
| `schemas/` | ✅ | Validation schemas |
| `standards/` | ✅ | Standards documents |
| `templates/` | ✅ | Templates |
| `config/` | ✅ | Configuration (`settings.yaml`, `schema.json`) |
| `docs/` | ✅ | Documentation (`adr/`, `guides/`, `api/`, `architecture/`, `reports/`) |
| `scripts/` | ✅ | Scripts (`setup/`, `deploy/`, `utils/`) |
| `tests/` | ✅ | Tests (`unit/`, `integration/`, `e2e/`, `fixtures/`) |
| `tools/` | ✅ | Tools (`build/`, `deploy/`, `monitoring/`, `generators/`) |
| `src/` | ✅ | Source code (`core/`, `cli/`, `engines/`, `mcp/`, `generators/`) |

### Files (RSS-v2.3 CRITICAL profile)

| File | Required | Purpose |
|------|----------|---------|
| `README.md` | ✅ | Project entry point |
| `REPO.yaml` | ✅ | Repository metadata |
| `citizens.yaml` | ✅ | AI session context (RSS-v2.3) |
| `ONTOLOGY_DECLARATION.yaml` | ✅ | Ontology concepts (RSS-v2.3) |
| `.rssignore` | ✅ | RSS ignore patterns |
| `CHANGELOG.md` | ✅ | Keep-a-Changelog format |
| `LICENSE` | ✅ | Apache-2.0 |
| `CONTRIBUTING.md` | ✅ | This file |
| `SECURITY.md` | ✅ | Security policy |
| `CODEOWNERS` | ✅ | Code ownership |
| `NOTICES.md` | ✅ | Third-party notices |

## Validation

Before submitting a PR, run:

```bash
# Full compliance check
python scripts/compliance_scanner.py --repo unified-design --strict

# RSS lint (if available)
python scripts/rss_lint.py --repo unified-design --strict

# Ontology term gate (for governance docs)
python $GOV/scripts/ontology_term_gate.py <your-doc>.md --strict
```

## Code Style

- **ASCII only** in source files (enforced by GATE-6)
- **Conventional Commits** for all commit messages
- **Type hints** in Python code
- **Zig 0.15 API** for Zig code (no 0.14 APIs)

## Questions?

Open an issue or contact the maintainers via CODEOWNERS.