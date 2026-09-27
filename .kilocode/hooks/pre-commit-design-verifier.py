#!/usr/bin/env python3
"""pre-commit-design-verifier — Pre-commit hook for unified-design.

Blocks commits if:
- A design.yaml is missing implementation_contract
- Artifacts defined in implementation_contract are missing
- Coverage is below threshold (default 80%)

Usage:
    python .kilocode/hooks/pre-commit-design-verifier.py
    python .kilocode/hooks/pre-commit-design-verifier.py --threshold 100
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
UNIFIED_DESIGN_ROOT = SCRIPT_DIR.parent.parent


def verify_design(design_path: Path, threshold: float = 80.0) -> tuple[bool, str]:
    # Import here to avoid circular imports
    sys.path.insert(0, str(UNIFIED_DESIGN_ROOT / "scripts"))
    from design_impl_verifier import verify_design as _verify_design
    
    result = _verify_design(design_path)
    if not result.get("implemented", False):
        return False, f"not implemented (coverage={result.get('coverage_pct', 0)}%)"
    
    coverage = result.get("coverage_pct", 0.0)
    if coverage < threshold:
        return False, f"coverage {coverage}% below threshold {threshold}%"
    
    return True, "OK"


def main() -> int:
    parser = argparse.ArgumentParser(description="Pre-commit design verifier")
    parser.add_argument("--threshold", type=float, default=80.0, help="Minimum coverage percentage")
    parser.add_argument("--check", default=str(UNIFIED_DESIGN_ROOT / "designs"), help="Designs directory")
    args = parser.parse_args()
    
    designs_dir = Path(args.check)
    if not designs_dir.exists():
        print(f"[SKIP] Designs directory not found: {designs_dir}", file=sys.stderr)
        return 0
    
    # Check all design.yaml files
    design_files = sorted(set(designs_dir.rglob("design.yaml")))
    if not design_files:
        print("[SKIP] No designs found", file=sys.stderr)
        return 0
    
    failures = []
    for design_path in design_files:
        ok, msg = verify_design(design_path, args.threshold)
        if not ok:
            failures.append(f"{design_path.relative_to(UNIFIED_DESIGN_ROOT)}: {msg}")
    
    if failures:
        print("[FAIL] Pre-commit design verification failed:", file=sys.stderr)
        for failure in failures:
            print(f"  - {failure}", file=sys.stderr)
        return 1
    
    print(f"[OK] All {len(design_files)} designs pass verification (threshold={args.threshold}%)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
