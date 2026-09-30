"""JEVX projection templates for auto-design.

Projects design.yaml into TALEX/CURX narratives.
"""

from __future__ import annotations

import yaml
from pathlib import Path
from typing import Any


def load_design(repo_root: Path) -> dict[str, Any]:
    design = repo_root / "design.yaml"
    if not design.exists():
        return {}
    try:
        return yaml.safe_load(design.read_text(encoding="utf-8")) or {}
    except Exception:
        return {}


def project_talex(repo_root: Path) -> str:
    design = load_design(repo_root)
    name = design.get("name", repo_root.name)
    components = design.get("auto_design", {}).get("components", [])
    return "\n".join([
        f"# TALEX projection for {name}",
        f"components: {len(components)}",
        "pathways: observability, automation, infrastructure",
    ])


def project_curx(repo_root: Path) -> str:
    design = load_design(repo_root)
    name = design.get("name", repo_root.name)
    intent_hash = design.get("intent_hash", "0xUNKNOWN")
    return "\n".join([
        f"# CURX projection for {name}",
        f"intent_hash: {intent_hash}",
        "validation: pending",
    ])


def project_narrative(repo_root: Path) -> str:
    design = load_design(repo_root)
    name = design.get("name", repo_root.name)
    components = design.get("auto_design", {}).get("components", [])
    lines = [f"# Narrative for {name}"]
    for component in components[:10]:
        lines.append(f"- {component}: operational")
    return "\n".join(lines)
