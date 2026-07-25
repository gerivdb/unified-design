---
type: README
version: 2.0.0
status: active
intent_hash: 0xREADME_UNIFIED_20260725
---

# Unified Design — Conventions SOTA MDU

Ce dépôt contient les **conventions de développement standardisées** pour l'écosystème MDU (gerivdb).

## Architecture (DAG ASCII)

```
unified-design/
├── ADR/                    # Architecture Decision Records
├── atoms/                  # ATOMs SOTA (165 entrées)
│   ├── methodology/        # Git, Python, Rust, Universal
│   └── ATOM-*.md / *.yaml
├── conventions/            # Conventions SOTA par domaine
│   ├── commit/             # Conventional Commits
│   ├── versioning/         # SemVer + Changelog
│   ├── lint/               # Code Quality
│   ├── ci/                 # Minimal CI
│   ├── loop/               # Loop Engineering
│   ├── maker-checker/      # Double validation
│   ├── default-fail/       # Sécurité par défaut
│   ├── evidence/           # Évidence requise
│   ├── trix/               # TRIX Architecture
│   ├── autoresearch/       # Bilevel Autoresearch
│   ├── movements/          # Five Movements
│   ├── organs/             # Six Organes
│   ├── topos/              # TOPOS Merge
│   ├── anti-patterns/      # Anti-patterns interdits
│   ├── ontology/           # ATOM-035 Ontology Anchoring
│   ├── verses/             # ATOM-036 VERSES Mapping
│   ├── tina/               # ATOM-037 TINA Specification
│   ├── tql/                # ATOM-038 TQL Interface Contract
│   └── design-seeker/      # ATOM-039/040 Design Seeker
├── docs/                   # Documentation
│   ├── META-DESIGN.md      # Vue d'ensemble MDU
│   └── README-full.md      # Documentation complète (archive)
├── scripts/                # Outils utilitaires
│   ├── validate_meta_design.py   # Validation schema JSON
│   ├── extract_atom_deps.py      # Extraction deps ATOM
│   ├── post_merge_cleanup.py     # Nettoyage post-merge
│   ├── cleanup_merged_branches.py
│   └── sync-scripts.sh           # Sync vers autres repos
├── schemas/                # Schémas JSON Schema
│   └── meta-design.schema.json
├── atoms_registry.yaml     # Registry ATOMs (165 entrées, 28 avec deps)
├── meta-design.yaml        # Schéma MDU v2 (validé par CI)
├── DAG.md                  # Dépendances ATOMs/ADRs
└── workflows/              # Templates CI/CD
    └── ci-template.yml
```

## Commandes de maintenance

```bash
# Validation schema meta-design
python scripts/validate_meta_design.py --schema schemas/meta-design.schema.json meta-design.yaml

# Extraction dépendances ATOM
python scripts/extract_atom_deps.py --dry-run   # Preview
python scripts/extract_atom_deps.py --write     # Mise à jour registry

# Nettoyage post-merge (alias git cleanup-repo)
git cleanup-repo
python scripts/post_merge_cleanup.py --repo .
python scripts/cleanup_merged_branches.py

# Sync scripts vers autres repos
bash scripts/sync-scripts.sh --dry-run
bash scripts/sync-scripts.sh

# Sync via KIVA-CLI (CI locale)
cd ../KIVA-CLI && kiva ci run
```

## Liens

- **Documentation complète** : `docs/README-full.md`
- **Registry ATOMs** : `atoms_registry.yaml` (165 entrées, 28 avec dépendances)
- **Schéma MDU** : `schemas/meta-design.schema.json`
- **DAG détaillé** : `DAG.md`
- **ADR index** : `ADR/ADR-INDEX.md`
- **Conventions** : `conventions/`

## Adoption dans un nouveau repo

1. Copier `conventions/` et `scripts/`
2. Installer hooks : `git config core.hooksPath .githooks`
3. Configurer CI : copier `.github/workflows/ci.yml`
4. Ajouter templates : `.github/PULL_REQUEST_TEMPLATE.md`, etc.

---

*Écosystème gerivdb — L0-CANON / unified-design — Industrialisé via KIVA-CLI*