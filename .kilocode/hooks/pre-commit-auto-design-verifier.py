"""Pre-commit hook: bloque si design.yaml absent sur repo active."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DESIGN_YAML = REPO_ROOT / "design.yaml"

if __name__ == "__main__":
    if not DESIGN_YAML.exists():
        print(f"ALERT: {DESIGN_YAML} missing for active repo {REPO_ROOT}", file=sys.stderr)
        sys.exit(1)
    sys.exit(0)
