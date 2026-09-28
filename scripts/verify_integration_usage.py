#!/usr/bin/env python3
"""
Verify Integration Usage — vérifie que les modules d'intégration
unified-design sont utilisés dans le code métier des consumers.

Usage:
    python verify_integration_usage.py --all
    python verify_integration_usage.py --consumer KIVA-CLI
    python verify_integration_usage.py --design safe-action-pattern
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


def verify_consumer_usage(consumer: str, design: str) -> dict:
    """Verify that integration module is used in consumer business code."""
    consumer_path = CONSUMER_MAP.get(consumer)
    if not consumer_path:
        return {"consumer": consumer, "design": design, "status": "ERROR", "error": "Consumer not found"}
    
    slug = DESIGN_SLUGS.get(design, design.replace("-", "_"))
    
    # Find integration module
    integration_files = list(consumer_path.rglob(f"{slug}_integration.py"))
    if not integration_files:
        return {
            "consumer": consumer,
            "design": design,
            "status": "MISSING_MODULE",
            "integration_path": "",
            "imports": [],
        }
    
    integration_path = str(integration_files[0])
    
    # Find imports in business code (exclude tests and integrations dirs)
    try:
        result = subprocess.run(
            ["grep", "-r", f"{slug}_integration", str(consumer_path), "--include=*.py"],
            capture_output=True, text=True, timeout=30
        )
        imports = []
        for line in result.stdout.split("\n"):
            line = line.strip()
            if line and "test" not in line.lower() and "integrations" not in line.lower():
                imports.append(line)
    except Exception as e:
        imports = [f"Error: {e}"]
    
    return {
        "consumer": consumer,
        "design": design,
        "status": "OK" if imports else "NOT_USED",
        "integration_path": integration_path,
        "imports": imports[:5],  # Limit to 5
    }


def main():
    parser = argparse.ArgumentParser(description="Verify Integration Usage")
    parser.add_argument("--all", action="store_true", help="Check all 126 pairs")
    parser.add_argument("--consumer", help="Check specific consumer")
    parser.add_argument("--design", help="Check specific design")
    parser.add_argument("--json-out", help="Output JSON report path")
    args = parser.parse_args()

    results = []
    
    if args.consumer and args.design:
        results.append(verify_consumer_usage(args.consumer, args.design))
    elif args.consumer:
        for design in DESIGN_SLUGS.keys():
            results.append(verify_consumer_usage(args.consumer, design))
    elif args.design:
        for consumer in CONSUMER_MAP.keys():
            results.append(verify_consumer_usage(consumer, args.design))
    elif args.all:
        for consumer in CONSUMER_MAP.keys():
            for design in DESIGN_SLUGS.keys():
                results.append(verify_consumer_usage(consumer, design))
    else:
        parser.print_help()
        sys.exit(1)

    # Summary
    ok = sum(1 for r in results if r["status"] == "OK")
    not_used = sum(1 for r in results if r["status"] == "NOT_USED")
    missing = sum(1 for r in results if r["status"] == "MISSING_MODULE")
    errors = sum(1 for r in results if r["status"] == "ERROR")
    
    print(f"\n=== Verify Integration Usage ===")
    print(f"Total checks: {len(results)}")
    print(f"OK (used): {ok}")
    print(f"NOT_USED: {not_used}")
    print(f"MISSING_MODULE: {missing}")
    print(f"ERROR: {errors}")
    
    if not_used > 0:
        print(f"\nNot used in business code:")
        for r in results:
            if r["status"] == "NOT_USED":
                print(f"  {r['consumer']} / {r['design']}: module exists but not imported")
    
    if missing > 0:
        print(f"\nMissing modules:")
        for r in results:
            if r["status"] == "MISSING_MODULE":
                print(f"  {r['consumer']} / {r['design']}")
    
    if args.json_out:
        report = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "total_checks": len(results),
            "ok": ok,
            "not_used": not_used,
            "missing": missing,
            "errors": errors,
            "results": results,
        }
        Path(args.json_out).write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(f"\nReport saved to: {args.json_out}")
    
    sys.exit(0 if not_used == 0 and missing == 0 and errors == 0 else 1)


if __name__ == "__main__":
    main()
