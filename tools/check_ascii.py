#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_ascii.py — GATE-6 ASCII Validator wrapper.

Wrapper around ascii_fix.py --check for pre-commit hook compatibility.
Exit code 0 = all ASCII, 1 = non-ASCII found.
"""

import subprocess
import sys
from pathlib import Path

ASCII_FIX = Path(__file__).parent / "ascii_fix.py"


def main() -> int:
    if not ASCII_FIX.exists():
        print(f"[ERROR] {ASCII_FIX} not found", file=sys.stderr)
        return 1

    result = subprocess.run(
        [sys.executable, str(ASCII_FIX), "--check"],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent,
    )

    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

    return result.returncode


if __name__ == "__main__":
    sys.exit(main())