#!/usr/bin/env python3
"""
Enregistrement atomique des artefacts manquants dans les catalogues unified-design.
Calibré SLM : une passe = un catalogue, idempotent, vérification post-écriture.
"""

import yaml
from pathlib import Path

REPO = Path(r"D:\DO\WEB\TOOLS\L0-CANON\unified-design")
TODAY = "2026-09-20"

# Artefacts manquants identifiés par l'audit
ARTIFACTS = [
    # Designs
    {
        "catalog": "designs.index.yaml",
        "entry": {
            "id": "ecosystem-meta-coherence",
            "source_path": "designs/ecosystem-meta-coherence/design.yaml",
            "source_repo": "unified-design",
            "status": "active",
            "type": "design",
            "updated": TODAY,
        },
    },
    {
        "catalog": "designs.index.yaml",
        "entry": {
            "id": "jevx",
            "source_path": "designs/jevx.yaml",
            "source_repo": "unified-design",
            "status": "active",
            "type": "design",
            "updated": TODAY,
        },
    },
    {
        "catalog": "designs.index.yaml",
        "entry": {
            "id": "jevx-engineering",
            "source_path": "designs/jevx-engineering.yaml",
            "source_repo": "unified-design",
            "status": "active",
            "type": "design",
            "updated": TODAY,
        },
    },
    # Atoms
    {
        "catalog": "atoms.index.yaml",
        "entry": {
            "id": "ecosystem-meta-coherence-gate",
            "source_path": "atoms/ecosystem-meta-coherence-gate.md",
            "source_repo": "unified-design",
            "status": "active",
            "type": "atom",
            "updated": TODAY,
        },
    },
    {
        "catalog": "atoms.index.yaml",
        "entry": {
            "id": "typed-decision-api",
            "source_path": "atoms/typed-decision-api.yaml",
            "source_repo": "unified-design",
            "status": "active",
            "type": "atom",
            "updated": TODAY,
        },
    },
    # Pipeline
    {
        "catalog": "pipelines.index.yaml",
        "entry": {
            "id": "mdu-validation",
            "source_path": "pipelines/mdu-validation.yaml",
            "source_repo": "unified-design",
            "status": "active",
            "type": "pipeline",
            "updated": TODAY,
        },
    },
    # Workflows
    {
        "catalog": "workflows.index.yaml",
        "entry": {
            "id": "dryrun-causal-audit",
            "source_path": "workflows/dryrun-causal-audit.md",
            "source_repo": "unified-design",
            "status": "active",
            "type": "workflow",
            "updated": TODAY,
        },
    },
    {
        "catalog": "workflows.index.yaml",
        "entry": {
            "id": "structural-fix-pipeline",
            "source_path": "workflows/structural-fix-pipeline.md",
            "source_repo": "unified-design",
            "status": "active",
            "type": "workflow",
            "updated": TODAY,
        },
    },
]


def load_catalog(path: Path):
    if not path.exists():
        return {"entries": []}
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data if data else {"entries": []}


def save_catalog(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False, default_flow_style=False)


def register_artifact(artifact: dict) -> bool:
    catalog_path = REPO / "catalog" / artifact["catalog"]
    data = load_catalog(catalog_path)
    entries = data.setdefault("entries", [])

    entry = artifact["entry"]
    key = (entry["id"].lower(), entry["source_path"].lower())

    # Idempotent : vérifier si déjà présent
    for existing in entries:
        if (existing.get("id", "").lower(), existing.get("source_path", "").lower()) == key:
            return False

    entries.append(entry)
    save_catalog(catalog_path, data)
    return True


def main():
    print("=" * 80)
    print("ENREGISTREMENT ARTEFACTS MANQUANTS — unified-design")
    print("=" * 80)

    registered = []
    skipped = []

    for artifact in ARTIFACTS:
        catalog_name = artifact["catalog"]
        entry_id = artifact["entry"]["id"]
        source_path = artifact["entry"]["source_path"]

        try:
            added = register_artifact(artifact)
            if added:
                registered.append(f"{catalog_name}: {entry_id} -> {source_path}")
                print(f"  [AJOUTÉ] {catalog_name}: {entry_id}")
            else:
                skipped.append(f"{catalog_name}: {entry_id}")
                print(f"  [DÉJÀ PRÉSENT] {catalog_name}: {entry_id}")
        except Exception as e:
            print(f"  [ERREUR] {catalog_name}: {entry_id} -> {e}")

    print()
    print("=" * 80)
    print("RÉSUMÉ")
    print("=" * 80)
    print(f"  Ajoutés: {len(registered)}")
    print(f"  Déjà présents: {len(skipped)}")
    print(f"  Total traités: {len(ARTIFACTS)}")

    if registered:
        print()
        print("Détails des ajouts:")
        for r in registered:
            print(f"  - {r}")


if __name__ == "__main__":
    main()
