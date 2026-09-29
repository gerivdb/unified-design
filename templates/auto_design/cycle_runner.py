"""Template: cycle_runner.py — execute auto-design mediation cycle."""

from __future__ import annotations

import sys
from pathlib import Path


def run_cycle(repo_root: Path) -> int:
    design = repo_root / "design.yaml"
    if not design.exists():
        print(f"ALERT: design.yaml missing in {repo_root}", file=sys.stderr)
        return 1
    print(f"CYCLE OK: {repo_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run_cycle(Path(".").resolve()))
