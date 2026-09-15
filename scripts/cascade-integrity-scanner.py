#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cascade Integrity Scanner - wrapper pour CTULU/tools/cascade-integrity-scanner.

Delegue l'execution a la version canonique dans CTULU.
Permet l'appel local depuis unified-design sans duplication.

Usage:
    python scripts/cascade-integrity-scanner.py [--repo ROOT] [--json]

IntentHash: 0xCASCADE_INTEGRITY_SCANNER_20260915
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

CTULU_TOOL = Path(__file__).resolve().parent.parent.parent.parent.parent.parent / "WEB" / "TOOLS" / "L4-TOOLS" / "CTULU" / "tools" / "cascade-integrity-scanner" / "cascade-integrity-scanner.py"


def main(argv: list[str] | None = None) -> int:
    if not CTULU_TOOL.exists():
        print(f"[CASCADE_INTEGRITY] FATAL: outil CTULU introuvable ({CTULU_TOOL})", file=sys.stderr)
        return 2
    scope = Path(__file__).resolve().parent.parent
    cmd = [sys.executable, str(CTULU_TOOL), "--repo", str(scope)] + (argv or [])
    try:
        proc = subprocess.run(cmd, check=False)
        return proc.returncode
    except OSError as exc:
        print(f"[CASCADE_INTEGRITY] FATAL: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
