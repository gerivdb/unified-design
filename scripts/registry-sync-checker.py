#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Registry Sync Checker - wrapper pour CTULU/tools/registry_sync_checker.

Delegue l'execution a la version canonique dans CTULU.
Permet l'appel local depuis unified-design sans duplication.

Usage:
    python scripts/registry-sync-checker.py [--json] [--registry PATH] [--kix PATH] [--sot PATH]

IntentHash: 0xREGISTRY_SYNC_CHECKER_20260824
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

CTULU_TOOL = Path(__file__).resolve().parent.parent.parent.parent.parent.parent / "WEB" / "TOOLS" / "L4-TOOLS" / "CTULU" / "tools" / "registry_sync_checker" / "src" / "checker.py"


def main(argv: list[str] | None = None) -> int:
    if not CTULU_TOOL.exists():
        print(f"[REGISTRY_SYNC] FATAL: outil CTULU introuvable ({CTULU_TOOL})", file=sys.stderr)
        return 2
    cmd = [sys.executable, str(CTULU_TOOL)] + (argv or [])
    try:
        proc = subprocess.run(cmd, check=False)
        return proc.returncode
    except OSError as exc:
        print(f"[REGISTRY_SYNC] FATAL: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
