#!/usr/bin/env python3
"""metacoherence_gate — Enforces THINK/DO/CHECK meta-coherence for unified-design.

Usage:
    python metacoherence_gate.py --check designs/
    python metacoherence_gate.py --audit-period 30d
    python metacoherence_gate.py --strict

Exit codes:
    0 = meta-coherence OK
    1 = violations found
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from datetime import datetime, timedelta

import yaml

UNIFIED_DESIGN_ROOT = Path(__file__).resolve().parent.parent


def _rel(path: Path) -> str:
    try:
        return str(path.relative_to(UNIFIED_DESIGN_ROOT))
    except ValueError:
        return str(path)


def load_design(path: Path) -> dict:
    path = path.resolve()
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    if text.startswith("---"):
        parts = text.split("---", 2)
        yaml_text = parts[1] if len(parts) >= 3 and parts[1].strip() else text
    else:
        yaml_text = text
    return yaml.safe_load(yaml_text) or {}


def check_implementation_contract(design_path: Path) -> tuple[bool, str]:
    design = load_design(design_path)
    contract = design.get("implementation_contract")
    if not contract:
        return False, "missing implementation_contract"
    
    repo_root = Path(contract.get("repo_root", ""))
    if not repo_root.exists():
        return False, f"repo_root does not exist: {repo_root}"
    
    artifacts = contract.get("artifacts", [])
    missing = []
    for art in artifacts:
        path = repo_root / art.get("path", "")
        if not path.exists():
            missing.append(f"artifact not found: {art.get('path')}")
    
    if missing:
        return False, "; ".join(missing)
    return True, "OK"


def check_proof_of_life(design_path: Path, audit_period: timedelta) -> tuple[bool, str]:
    design = load_design(design_path)
    proof_of_life = design.get("proof_of_life", [])
    if not proof_of_life:
        return False, "missing proof_of_life"
    
    now = datetime.now()
    for entry in proof_of_life:
        if isinstance(entry, str) and entry.startswith("["):
            try:
                timestamp_str = entry.split("—")[0].strip("[]")
                timestamp = datetime.fromisoformat(timestamp_str)
                if now - timestamp <= audit_period:
                    return True, "OK"
            except (ValueError, IndexError):
                continue
    
    return False, f"no proof-of-life within last {audit_period.days} days"


def check_design(design_path: Path, audit_period: timedelta) -> dict:
    name = design_path.parent.name
    contract_ok, contract_msg = check_implementation_contract(design_path)
    proof_ok, proof_msg = check_proof_of_life(design_path, audit_period)
    
    return {
        "design": name,
        "path": _rel(design_path),
        "implementation_contract": contract_ok,
        "contract_msg": contract_msg,
        "proof_of_life": proof_ok,
        "proof_msg": proof_msg,
        "meta_coherent": contract_ok and proof_ok,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Enforce meta-coherence gate")
    parser.add_argument("--check", default="designs/", help="Designs directory to check")
    parser.add_argument("--audit-period", default="30d", help="Audit period (e.g., 30d)")
    parser.add_argument("--strict", action="store_true", help="Fail on any violation")
    args = parser.parse_args()
    
    period_str = args.audit_period
    if period_str.endswith("d"):
        audit_period = timedelta(days=int(period_str[:-1]))
    else:
        audit_period = timedelta(days=30)
    
    designs_dir = Path(args.check)
    if not designs_dir.exists():
        print(f"[FAIL] Designs directory not found: {designs_dir}", file=sys.stderr)
        return 1
    
    design_files = sorted(set(designs_dir.rglob("design.yaml")))
    if not design_files:
        print("[FAIL] No designs found", file=sys.stderr)
        return 1
    
    results = []
    violations = 0
    for design_path in design_files:
        result = check_design(design_path, audit_period)
        results.append(result)
        if not result["meta_coherent"]:
            violations += 1
    
    for r in results:
        status = "OK" if r["meta_coherent"] else "FAIL"
        print(f"[{status}] {r['design']}: contract={r['implementation_contract']} proof={r['proof_of_life']}")
    
    total = len(results)
    ok = total - violations
    print(f"\n{ok}/{total} designs meta-coherent")
    
    if violations > 0:
        print("\nViolations:")
        for r in results:
            if not r["meta_coherent"]:
                print(f"  - {r['design']}: {r['contract_msg']}; {r['proof_msg']}")
    
    if violations > 0 and args.strict:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
