#!/usr/bin/env python3
"""
ADR-Design-Integration Traceability Checker.

Vérifie que chaque design intégré dans un consumer repo est backed par un ADR accepté,
avec traçabilité complète Design → ADR → Consumer → Integration.

Usage:
    python adr_design_traceability.py --check-all
    python adr_design_traceability.py --consumer KIVA-CLI
    python adr_design_traceability.py --design safe-action-pattern
"""

import argparse
import json
import re
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

DESIGN_ADR_MAP = {
    "safe-action-pattern": "ADR-2026-09-19-SAFE-ACTION-PATTERN.md",
    "safe-action-gate": "ADR-2026-09-21-005-SAFE-ACTION-GATE.md",
    "ecosystem-meta-coherence": "ADR-2026-09-21-006-ECOSYSTEM-META-COHERENCE-GATE.md",
    "ecosystem-meta-coherence-gate": "ADR-2026-09-21-006-ECOSYSTEM-META-COHERENCE-GATE.md",
    "meta-design-self-healing": "ADR-2026-09-21-008-META-DESIGN-SELF-HEALING.md",
    "design-ops-loop": "ADR-2026-09-19-SAFE-ACTION-PATTERN.md",
    "session-boot-design": "ADR-2026-09-19-SAFE-ACTION-PATTERN.md",
    "artifact-layers-design": "ADR-2026-09-20-001-ARTIFACT-EXTRACTION-MDU.md",
    "talex-friction-analyzer": "ADR-2026-09-19-SAFE-ACTION-PATTERN.md",
}

# Additional ADR mappings for designs without specific ADR
DESIGN_ADR_ADDITIONAL = {
    "design-ops-loop": "ADR-2026-09-19-SAFE-ACTION-PATTERN.md",
    "session-boot-design": "ADR-2026-09-19-SAFE-ACTION-PATTERN.md",
    "talex-friction-analyzer": "ADR-2026-09-19-SAFE-ACTION-PATTERN.md",
    "meta-design-self-healing": "ADR-2026-09-21-008-META-DESIGN-SELF-HEALING.md",
}


def get_adr_status(adr_name: str) -> str:
    """Get the status of an ADR file."""
    adr_path = UNIFIED_DESIGN_ROOT / "ADR" / adr_name
    if not adr_path.exists():
        return "missing"
    content = adr_path.read_text(encoding="utf-8")
    match = re.search(r'^status:\s*(.+)', content, re.MULTILINE)
    return match.group(1).strip() if match else "unknown"


def find_prd_mocs_for_consumer(consumer: str, design: str) -> list:
    """Find all PRD-MOC files for a consumer/design pair."""
    consumer_path = CONSUMER_MAP.get(consumer)
    if not consumer_path:
        return []
    
    # Normalize design name for matching
    design_variants = {
        design.lower(),
        design.replace("-", "_").lower(),
        design.replace("-", "").lower(),
        design.replace("_", "-").lower(),
        design.replace("-", " ").lower(),
    }
    # Add title-case variants
    design_variants.update([v.title() for v in design_variants])
    design_variants.update([v.upper() for v in design_variants])
    
    prd_mocs = []
    
    # Search in PRD and PRD-MOC directories
    for prd_dir in ["PRD", "PRD-MOC"]:
        prd_path = consumer_path / prd_dir
        if prd_path.exists():
            # Look for files matching the design slug
            for f in prd_path.glob("*.md"):
                fname_lower = f.name.lower()
                if any(variant in fname_lower for variant in design_variants):
                    prd_mocs.append(f)
    
    return prd_mocs


def check_traceability(consumer: str, design: str) -> dict:
    """Check traceability for a specific consumer/design pair."""
    adr_name = DESIGN_ADR_MAP.get(design, "unknown")
    adr_status = get_adr_status(adr_name)
    
    prd_mocs = find_prd_mocs_for_consumer(consumer, design)
    design_slug = design.replace("-", "_")
    
    prd_moc_found = len(prd_mocs) > 0
    prd_moc_has_adr = False
    
    for prd_moc in prd_mocs:
        content = prd_moc.read_text(encoding="utf-8")
        adr_base = adr_name.replace(".md", "")
        if adr_base in content:
            prd_moc_has_adr = True
            break
    
    status = "OK"
    if adr_status != "accepted":
        status = "WARN"
    if not prd_moc_found:
        status = "WARN"
    if not prd_moc_has_adr:
        status = "WARN"
    
    return {
        "consumer": consumer,
        "design": design,
        "adr": adr_name,
        "adr_status": adr_status,
        "prd_moc_found": prd_moc_found,
        "prd_moc_has_adr": prd_moc_has_adr,
        "status": status,
    }


def main():
    parser = argparse.ArgumentParser(description="ADR-Design-Integration Traceability Checker")
    parser.add_argument("--check-all", action="store_true", help="Check all 126 pairs")
    parser.add_argument("--consumer", help="Check specific consumer")
    parser.add_argument("--design", help="Check specific design")
    parser.add_argument("--json-out", help="Output JSON report path")
    args = parser.parse_args()

    results = []
    
    if args.consumer and args.design:
        results.append(check_traceability(args.consumer, args.design))
    elif args.consumer:
        for design in DESIGN_ADR_MAP.keys():
            results.append(check_traceability(args.consumer, design))
    elif args.design:
        for consumer in CONSUMER_MAP.keys():
            results.append(check_traceability(consumer, args.design))
    elif args.check_all:
        for consumer in CONSUMER_MAP.keys():
            for design in DESIGN_ADR_MAP.keys():
                results.append(check_traceability(consumer, design))
    else:
        parser.print_help()
        sys.exit(1)

    # Summary
    ok = sum(1 for r in results if r["status"] == "OK")
    warn = sum(1 for r in results if r["status"] == "WARN")
    missing_adr = sum(1 for r in results if r["adr_status"] == "missing")
    
    print(f"\n=== ADR-Design-Integration Traceability ===")
    print(f"Total checks: {len(results)}")
    print(f"OK: {ok}")
    print(f"WARN: {warn}")
    print(f"Missing ADR: {missing_adr}")
    
    if warn > 0:
        print(f"\nWarnings:")
        for r in results:
            if r["status"] == "WARN":
                print(f"  {r['consumer']} / {r['design']}: ADR={r['adr_status']}, PRD-MOC={r['prd_moc_found']}, ADR-ref={r['prd_moc_has_adr']}")
    
    if args.json_out:
        report = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "total_checks": len(results),
            "ok": ok,
            "warn": warn,
            "missing_adr": missing_adr,
            "results": results,
        }
        Path(args.json_out).write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(f"\nReport saved to: {args.json_out}")
    
    sys.exit(0 if warn == 0 else 1)


if __name__ == "__main__":
    main()
