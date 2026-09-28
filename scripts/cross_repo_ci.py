#!/usr/bin/env python3
"""
Cross-Repo CI Pipeline for unified-design.

Valide automatiquement que tous les consumers ont correctement intégré
les designs unified-design.

Usage:
    python cross_repo_ci.py --all
    python cross_repo_ci.py --consumer KIVA-CLI
    python cross_repo_ci.py --design safe-action-pattern
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timezone

UNIFIED_DESIGN_ROOT = Path("D:/DO/WEB/TOOLS/L0-CANON/unified-design")
CONSUMER_MAP = {
    "KIVA-CLI": Path("D:/DO/WEB/TOOLS/L1-INFRA/KIVA-CLI"),
    "ECOS-CLI": Path("D:/DO/WEB/TOOLS/L1-INFRA/ECOS-CLI"),
    "ARGUS": Path("D:/DO/WEB/TOOLS/L1-INFRA/ARGUS"),
    "CTULU": Path("D:/DO/WEB/TOOLS/L4-TOOLS/CTULU"),
    "KG-CAUSAL": Path("D:/DO/WEB/TOOLS/L4-TOOLS/KG-CAUSAL"),
    "KG-L": Path("D:/DO/WEB/TOOLS/L4-TOOLS/KG-L"),
    "KIX": Path("D:/DO/WEB/TOOLS/L2-PLATFORM/KIX"),
    "LOOPX": Path("D:/DO/WEB/TOOLS/L3-CITIZENS/LOOPX"),
    "NEXUS": Path("D:/DO/WEB/TOOLS/L1-INFRA/NEXUS"),
    "TALEX": Path("D:/DO/WEB/TOOLS/L4-TOOLS/TALEX"),
    "TRIX": Path("D:/DO/WEB/TOOLS/L4-TOOLS/TRIX"),
    "VERSES": Path("D:/DO/WEB/TOOLS/L4-TOOLS/VERSES"),
    "VOLTX": Path("D:/DO/WEB/TOOLS/L0-CANON/VOLTX"),
    "WAZAA": Path("D:/DO/WEB/TOOLS/L4-TOOLS/WAZAA"),
}

DESIGN_SLUGS = {
    "safe-action-pattern": "safe_action_pattern",
    "safe-action-gate": "safe_action_gate",
    "ecosystem-meta-coherence": "ecosystem_meta_coherence",
    "ecosystem-meta-coherence-gate": "ecosystem_meta_coherence_gate",
    "meta-design-self-healing": "meta_design_self_healing",
    "design-ops-loop": "design_ops_loop",
    "session-boot-design": "session_boot_design",
    "artifact-layers-design": "artifact_layers_design",
    "talex-friction-analyzer": "talex_friction_analyzer",
}


def run_pytest(test_path: Path, cwd: Path) -> dict:
    """Run pytest on a specific test file."""
    if not test_path.exists():
        return {"status": "MISSING", "output": "Test file not found"}
    
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", str(test_path), "-v", "--tb=short", "--no-cov"],
            capture_output=True, text=True, timeout=60, cwd=str(cwd)
        )
        return {
            "status": "PASS" if result.returncode == 0 else "FAIL",
            "output": result.stdout + result.stderr,
        }
    except subprocess.TimeoutExpired:
        return {"status": "TIMEOUT", "output": "Test timed out"}
    except Exception as e:
        return {"status": "ERROR", "output": str(e)}


def check_consumer(consumer: str, design: str) -> dict:
    """Check a specific consumer/design pair."""
    consumer_path = CONSUMER_MAP.get(consumer)
    if not consumer_path:
        return {"consumer": consumer, "design": design, "status": "ERROR", "error": "Consumer not found"}
    
    slug = DESIGN_SLUGS.get(design, design.replace("-", "_"))
    
    # Determine integration directory
    pkg_dir = None
    if consumer == "KIVA-CLI":
        pkg_dir = "kiva_cli"
    elif consumer == "ECOS-CLI":
        pkg_dir = "ecos_cli"
    elif consumer == "KG-CAUSAL":
        pkg_dir = "src"
    elif consumer == "KG-L":
        pkg_dir = "kg_l"
    elif consumer == "KIX":
        pkg_dir = "kix"
    elif consumer == "VERSES":
        pkg_dir = "verses"
    elif consumer == "WAZAA":
        pkg_dir = "wazaa"
    
    # Find test file - try multiple naming conventions
    test_path = None
    tests_dir = consumer_path / "tests"
    
    # Try standard naming: test_<slug>_integration.py
    candidate = tests_dir / f"test_{slug}_integration.py"
    if candidate.exists():
        test_path = candidate
    else:
        # Try alternative: test_<slug_without_pattern>_integration.py
        # e.g., safe_action_pattern -> safe_action for KIVA-CLI POC naming
        slug_alt = slug.replace("_pattern", "").replace("_gate", "").replace("_design", "")
        candidate2 = tests_dir / f"test_{slug_alt}_integration.py"
        if candidate2.exists():
            test_path = candidate2
    
    if not test_path:
        return {
            "consumer": consumer,
            "design": design,
            "status": "MISSING",
            "test_path": str(tests_dir / f"test_{slug}_integration.py"),
        }
    
    result = run_pytest(test_path, consumer_path)
    
    return {
        "consumer": consumer,
        "design": design,
        "test_path": str(test_path),
        "status": result["status"],
        "output": result["output"][:500] if result.get("output") else "",
    }


def main():
    parser = argparse.ArgumentParser(description="Cross-Repo CI Pipeline")
    parser.add_argument("--all", action="store_true", help="Check all 126 pairs")
    parser.add_argument("--consumer", help="Check specific consumer")
    parser.add_argument("--design", help="Check specific design")
    parser.add_argument("--json-out", help="Output JSON report path")
    args = parser.parse_args()

    results = []
    
    if args.consumer and args.design:
        results.append(check_consumer(args.consumer, args.design))
    elif args.consumer:
        for design in DESIGN_SLUGS.keys():
            results.append(check_consumer(args.consumer, design))
    elif args.design:
        for consumer in CONSUMER_MAP.keys():
            results.append(check_consumer(consumer, args.design))
    elif args.all:
        for consumer in CONSUMER_MAP.keys():
            for design in DESIGN_SLUGS.keys():
                results.append(check_consumer(consumer, design))
    else:
        parser.print_help()
        sys.exit(1)

    # Summary
    passed = sum(1 for r in results if r["status"] == "PASS")
    failed = sum(1 for r in results if r["status"] == "FAIL")
    missing = sum(1 for r in results if r["status"] == "MISSING")
    errors = sum(1 for r in results if r["status"] == "ERROR")
    
    print(f"\n=== Cross-Repo CI Pipeline ===")
    print(f"Total checks: {len(results)}")
    print(f"PASS: {passed}")
    print(f"FAIL: {failed}")
    print(f"MISSING: {missing}")
    print(f"ERROR: {errors}")
    
    if failed > 0 or missing > 0 or errors > 0:
        print(f"\nFailures:")
        for r in results:
            if r["status"] in ("FAIL", "MISSING", "ERROR"):
                print(f"  {r['consumer']} / {r['design']}: {r['status']}")
    
    if args.json_out:
        report = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "total_checks": len(results),
            "passed": passed,
            "failed": failed,
            "missing": missing,
            "errors": errors,
            "results": results,
        }
        Path(args.json_out).write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(f"\nReport saved to: {args.json_out}")
    
    sys.exit(0 if failed == 0 and missing == 0 and errors == 0 else 1)


if __name__ == "__main__":
    main()
