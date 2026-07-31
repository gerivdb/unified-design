#!/usr/bin/env python3
"""CFMI scanner wrapper for KIVA-CLI pipeline."""
import sys
from pathlib import Path

sys.path.insert(0, "D:/DO/WEB/TOOLS/L1-INFRA/FLUENCE")

from plix.governance import scan_gates

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
result = scan_gates(root)
print(result)
