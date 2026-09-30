#!/usr/bin/env python3
"""
validate_consumer_designs.py — Pre-commit hook pour vérifier que les designs
consommés par un repo sont bien implémentés.

Usage:
    python validate_consumer_designs.py --designs <design1,design2,...>
    python validate_consumer_designs.py --meta-design <meta-design.yaml>
"""

from pathlib import Path
from datetime import datetime, timezone
import json
import sys
import argparse


def load_meta_design(meta_design_path: Path) -> dict:
    """Charge meta-design.yaml et retourne la mapping consumer -> designs."""
    import yaml
    with open(meta_design_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data


def check_consumer_designs(consumer: str, designs: list, repo_root: Path) -> dict:
    """Vérifie que les designs consommés sont implémentés."""
    results = {
        "consumer": consumer,
        "designs_checked": len(designs),
        "implemented": 0,
        "missing": 0,
        "details": [],
    }

    for design in designs:
        impl_file = design.replace("-", "_") + ".py"
        found = list(repo_root.glob(f"**/{impl_file}"))
        prd_moc = list(repo_root.glob(f"**/PRD-MOC-*{design.upper().replace('-', '_')}*CONSUMER*.md"))

        if found and prd_moc:
            results["implemented"] += 1
            results["details"].append({
                "design": design,
                "status": "IMPLEMENTED",
                "impl_path": str(found[0]),
                "prd_moc_path": str(prd_moc[0]),
            })
        else:
            results["missing"] += 1
            results["details"].append({
                "design": design,
                "status": "MISSING",
                "impl_path": str(found[0]) if found else None,
                "prd_moc_path": str(prd_moc[0]) if prd_moc else None,
            })

    return results


def main():
    parser = argparse.ArgumentParser(description="Validate consumer designs")
    parser.add_argument("--designs", help="Comma-separated list of designs")
    parser.add_argument("--meta-design", help="Path to meta-design.yaml")
    parser.add_argument("--consumer", default="UNKNOWN", help="Consumer repo name")
    parser.add_argument("--repo-root", default=".", help="Repo root path")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()

    if args.meta_design:
        meta = load_meta_design(Path(args.meta_design))
        consumer_designs = meta.get("consumers", {}).get(args.consumer, [])
        if not consumer_designs:
            print(f"[VALIDATE] No designs declared for consumer {args.consumer}")
            sys.exit(0)
        designs = consumer_designs
    elif args.designs:
        designs = [d.strip() for d in args.designs.split(",")]
    else:
        print("[VALIDATE] No designs specified")
        sys.exit(1)

    results = check_consumer_designs(args.consumer, designs, repo_root)

    print(f"[VALIDATE] Consumer: {args.consumer}")
    print(f"[VALIDATE] Designs checked: {results['designs_checked']}")
    print(f"[VALIDATE] Implemented: {results['implemented']}")
    print(f"[VALIDATE] Missing: {results['missing']}")

    if results["missing"] > 0:
        print("[VALIDATE] FAILED: Missing implementations detected")
        for detail in results["details"]:
            if detail["status"] == "MISSING":
                print(f"  - {detail['design']}: impl={detail['impl_path']}, prd_moc={detail['prd_moc_path']}")
        sys.exit(1)
    else:
        print("[VALIDATE] PASSED: All designs implemented")
        sys.exit(0)


if __name__ == "__main__":
    main()
