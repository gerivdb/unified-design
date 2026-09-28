#!/usr/bin/env python3
"""
Documentation Audit — vérifie la cohérence de la documentation unified-design.

Usage:
    python docs_audit.py
    python docs_audit.py --json-out reports/docs-audit.json
"""

import argparse
import json
import re
import sys
from pathlib import Path
from datetime import datetime, timezone

UNIFIED_DESIGN_ROOT = Path("D:/DO/WEB/TOOLS/L0-CANON/unified-design")


def find_prd_mocs() -> list:
    """Find all PRD-MOC files."""
    return list((UNIFIED_DESIGN_ROOT / "PRD").glob("PRD-MOC-*.md"))


def find_mocs() -> list:
    """Find all MOC files."""
    return list((UNIFIED_DESIGN_ROOT / "MOC").glob("MOC-*.md"))


def find_scripts() -> list:
    """Find all automation scripts."""
    return list((UNIFIED_DESIGN_ROOT / "scripts").glob("*.py"))


def find_tests() -> list:
    """Find all test files."""
    return list((UNIFIED_DESIGN_ROOT / "tests").glob("test_*.py"))


def check_prd_moc_references(prd_moc: Path) -> dict:
    """Check if PRD-MOC has required references."""
    content = prd_moc.read_text(encoding="utf-8")
    refs = {
        "framework": "PRD-MOC-INTEGRATION-FRAMEWORK" in content,
        "registry": "PRD-MOC-UNIFIED-DESIGN-CONSUMERS-REGISTRY" in content,
        "ci": "PRD-MOC-CROSS-REPO-CI-PIPELINE" in content,
        "traceability": "PRD-MOC-ADR-DESIGN-INTEGRATION-TRACEABILITY" in content,
        "usage": "PRD-MOC-CONSUMER-INTEGRATION-USAGE" in content,
        "auto_promote": "PRD-MOC-AUTO-PROMOTE" in content,
    }
    return refs


def check_moc_references(moc: Path) -> dict:
    """Check if MOC has required references."""
    content = moc.read_text(encoding="utf-8")
    refs = {
        "framework": "PRD-MOC-INTEGRATION-FRAMEWORK" in content or "MOC-INTEGRATION-FRAMEWORK" in content,
        "registry": "PRD-MOC-UNIFIED-DESIGN-CONSUMERS-REGISTRY" in content or "MOC-UNIFIED-DESIGN-CONSUMERS-REGISTRY" in content,
        "ci": "PRD-MOC-CROSS-REPO-CI-PIPELINE" in content or "MOC-CROSS-REPO-CI-PIPELINE" in content,
        "traceability": "PRD-MOC-ADR-DESIGN-INTEGRATION-TRACEABILITY" in content or "MOC-ADR-DESIGN-INTEGRATION-TRACEABILITY" in content,
        "usage": "PRD-MOC-CONSUMER-INTEGRATION-USAGE" in content or "MOC-CONSUMER-INTEGRATION-USAGE" in content,
        "auto_promote": "PRD-MOC-AUTO-PROMOTE" in content or "MOC-AUTO-PROMOTE" in content,
    }
    return refs


def main():
    parser = argparse.ArgumentParser(description="Documentation Audit")
    parser.add_argument("--json-out", help="Output JSON report path")
    args = parser.parse_args()

    prd_mocs = find_prd_mocs()
    mocs = find_mocs()
    scripts = find_scripts()
    tests = find_tests()

    results = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "prd_moc_count": len(prd_mocs),
        "moc_count": len(mocs),
        "script_count": len(scripts),
        "test_count": len(tests),
        "prd_mocs": [],
        "mocs": [],
        "scripts": [],
        "tests": [],
        "summary": {
            "prd_moc_missing_refs": 0,
            "moc_missing_refs": 0,
            "scripts_without_tests": 0,
        }
    }

    # Check PRD-MOCs
    for prd_moc in prd_mocs:
        refs = check_prd_moc_references(prd_moc)
        missing = [k for k, v in refs.items() if not v]
        results["prd_mocs"].append({
            "file": prd_moc.name,
            "references": refs,
            "missing": missing,
        })
        results["summary"]["prd_moc_missing_refs"] += len(missing)

    # Check MOCs
    for moc in mocs:
        refs = check_moc_references(moc)
        missing = [k for k, v in refs.items() if not v]
        results["mocs"].append({
            "file": moc.name,
            "references": refs,
            "missing": missing,
        })
        results["summary"]["moc_missing_refs"] += len(missing)

    # Check scripts
    script_names = {s.stem for s in scripts}
    for script in scripts:
        stem = script.stem
        expected_test = f"test_{stem}.py"
        has_test = expected_test in {t.name for t in tests}
        results["scripts"].append({
            "file": script.name,
            "has_test": has_test,
            "test_file": expected_test if has_test else None,
        })
        if not has_test:
            results["summary"]["scripts_without_tests"] += 1

    # Check tests
    for test in tests:
        results["tests"].append({
            "file": test.name,
        })

    # Summary
    print(f"\n=== Documentation Audit ===")
    print(f"PRD-MOCs: {len(prd_mocs)}")
    print(f"MOCs: {len(mocs)}")
    print(f"Scripts: {len(scripts)}")
    print(f"Tests: {len(tests)}")
    print(f"PRD-MOC missing refs: {results['summary']['prd_moc_missing_refs']}")
    print(f"MOC missing refs: {results['summary']['moc_missing_refs']}")
    print(f"Scripts without tests: {results['summary']['scripts_without_tests']}")

    if results["summary"]["prd_moc_missing_refs"] > 0:
        print(f"\nPRD-MOC with missing references:")
        for prd in results["prd_mocs"]:
            if prd["missing"]:
                print(f"  {prd['file']}: missing {prd['missing']}")

    if results["summary"]["moc_missing_refs"] > 0:
        print(f"\nMOC with missing references:")
        for moc in results["mocs"]:
            if moc["missing"]:
                print(f"  {moc['file']}: missing {moc['missing']}")

    if results["summary"]["scripts_without_tests"] > 0:
        print(f"\nScripts without tests:")
        for script in results["scripts"]:
            if not script["has_test"]:
                print(f"  {script['file']}")

    if args.json_out:
        report_path = Path(args.json_out)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
        print(f"\nReport saved to: {args.json_out}")

    sys.exit(0)


if __name__ == "__main__":
    main()
