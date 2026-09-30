#!/usr/bin/env python3
"""codedb_design_reader.py — lit le design YAML codeDB-E5620 et retourne les faits hardware."""
from __future__ import annotations

import yaml
from pathlib import Path
from typing import Any


def read_design(design_path: Path) -> dict[str, Any]:
    """Lit le design YAML et retourne les faits hardware."""
    with open(design_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return {
        "cpu": data.get("cpu", {}),
        "constraints": data.get("constraints", {}),
        "source": str(design_path),
    }


def main() -> int:
    design = Path(__file__).resolve().parent.parent / "designs" / "codedb-e5620" / "design.yaml"
    facts = read_design(design)
    print(facts)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
