#!/usr/bin/env python3
"""Consumer Integration Usage — vérifie que les modules d'intégration sont utilisés dans le code métier."""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any


def check_usage(repo_root: Path, design: str) -> dict[str, Any]:
    """Vérifie que le design est importé dans le code métier."""
    repo_root = Path(repo_root)
    hits = []
    for py in repo_root.rglob("*.py"):
        text = py.read_text(encoding="utf-8", errors="ignore")
        if design in text:
            hits.append(str(py))
    return {
        "design": design,
        "repo": str(repo_root),
        "imports": len(hits),
        "files": hits[:10],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Consumer Integration Usage checker")
    parser.add_argument("repo", type=Path)
    parser.add_argument("design")
    args = parser.parse_args()
    result = check_usage(args.repo, args.design)
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
