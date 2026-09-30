"""Pre-commit hook: bloque si promotion manquée sur document proposed."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    proposed_docs = []
    for path in REPO_ROOT.glob("**/*.md"):
        if any(part.startswith(".") for part in path.parts):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if "status: proposed" in text and "Proof-of-Life" in text and "[x]" in text:
            proposed_docs.append(str(path))
    if proposed_docs:
        print(f"ALERT: {len(proposed_docs)} proposed docs with Proof-of-Life should be promoted:", file=sys.stderr)
        for doc in proposed_docs:
            print(f"  - {doc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
