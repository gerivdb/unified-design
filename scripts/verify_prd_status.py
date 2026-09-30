#!/usr/bin/env python3
"""Verify PRD/MOC status consistency with filesystem deliverables."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


def verify_prd_status(repo_root: Path) -> dict[str, Any]:
    """Vérifie la cohérence entre statut PRD/MOC et livrables."""
    repo_root = Path(repo_root)
    inconsistencies = []
    for f in sorted(repo_root.rglob("PRD*.md")):
        text = f.read_text(encoding="utf-8")
        status = re.search(r"^status:\s*(.+)$", text, re.M)
        if not status:
            continue
        st = status.group(1).strip()
        if st in ("approved", "final", "implemented"):
            continue
        # Découverte basique des chemins déclarés
        paths = re.findall(r"`([^`]*\.(?:py|yaml|md|json))`", text)
        missing = [p for p in paths if not (repo_root / p).exists()]
        if missing:
            inconsistencies.append({
                "file": str(f),
                "status": st,
                "missing": missing,
            })
    return {
        "repo": str(repo_root),
        "inconsistencies": inconsistencies,
        "ok": len(inconsistencies) == 0,
    }


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description="Verify PRD/MOC status consistency")
    parser.add_argument("repo", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = verify_prd_status(args.repo)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Repo: {result['repo']}")
        print(f"Inconsistencies: {len(result['inconsistencies'])}")
        for item in result["inconsistencies"]:
            print(f"- {item['file']} ({item['status']})")
            for p in item["missing"]:
                print(f"  missing: {p}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
