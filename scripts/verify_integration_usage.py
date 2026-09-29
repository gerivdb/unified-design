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
    
    # Find integration module - try multiple naming conventions
    integration_files = []
    
    # Standard naming: <slug>_integration.py
    standard_pattern = f"{slug}_integration.py"
    integration_files = list(consumer_path.rglob(standard_pattern))
    
    # Legacy naming fallbacks
    if not integration_files:
        # Remove common suffixes/prefixes for legacy names
        legacy_slugs = [
            slug.replace("_pattern", "").replace("_gate", "").replace("_design", ""),
            slug.replace("safe_action_pattern", "safe_action"),
            slug.replace("meta_design_self_healing", "meta_design"),
        ]
        for legacy_slug in legacy_slugs:
            if legacy_slug != slug:
                legacy_pattern = f"{legacy_slug}_integration.py"
                integration_files = list(consumer_path.rglob(legacy_pattern))
                if integration_files:
                    break
    
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
    search_patterns = [
        f"{slug}_integration",
        integration_files[0].stem,
    ]
    imports = []
    for pattern in search_patterns:
        for py_file in consumer_path.rglob("*.py"):
            # Skip test files and integrations directory
            file_str = str(py_file)
            if "test" in file_str.lower() or "integrations" in file_str.lower():
                continue
            try:
                content = py_file.read_text(encoding="utf-8")
                for line in content.splitlines():
                    if pattern in line and line.strip().startswith(("from ", "import ")):
                        imports.append(f"{py_file.relative_to(consumer_path)}: {line.strip()}")
                        break
            except Exception:
                continue
    
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
