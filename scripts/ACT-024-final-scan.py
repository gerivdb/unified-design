#!/usr/bin/env python3
"""
ACT-024: Validation finale avec scan direct du filesystem.
"""

from pathlib import Path
from datetime import datetime, timezone
import json

UNIFIED_DESIGN_ROOT = Path("D:/DO/WEB/TOOLS/L0-CANON/unified-design")
REPORT_PATH = UNIFIED_DESIGN_ROOT / "ACT-024-final-scan-report.json"

# Implémentations disponibles
IMPL_DIR = UNIFIED_DESIGN_ROOT / "scripts" / "validators" / "implementations"
IMPLS = {
    "safe-action-pattern": "safe_action_pattern.py",
    "safe-action-gate": "safe_action_gate.py",
    "ecosystem-meta-coherence": "ecosystem_meta_coherence.py",
    "ecosystem-meta-coherence-gate": "ecosystem_meta_coherence_gate.py",
    "design-ops-loop": "design_ops_loop.py",
    "session-boot-design": "session_boot_design.py",
    "artifact-layers-design": "artifact_layers_design.py",
    "meta-design-self-healing": "meta_design_self_healing.py",
    "talex-friction-analyzer": "talex_friction_analyzer.py",
}

CONSUMER_ROOTS = {
    "KIVA-CLI": Path("D:/DO/WEB/TOOLS/L1-INFRA/KIVA-CLI"),
    "ECOS-CLI": Path("D:/DO/WEB/TOOLS/L1-INFRA/ECOS-CLI"),
    "ARGUS": Path("D:/DO/WEB/TOOLS/L1-INFRA/ARGUS"),
    "CTULU": Path("D:/DO/WEB/TOOLS/L4-TOOLS/CTULU"),
    "KG-CAUSAL": Path("D:/DO/WEB/TOOLS/L4-TOOLS/KG-CAUSAL"),
    "VOLTX": Path("D:/DO/WEB/TOOLS/L0-CANON/VOLTX"),
    "LOOPX": Path("D:/DO/WEB/TOOLS/L3-CITIZENS/LOOPX"),
    "KIX": Path("D:/DO/WEB/TOOLS/L2-PLATFORM/KIX"),
    "TALEX": Path("D:/DO/WEB/TOOLS/L4-TOOLS/TALEX"),
    "NEXUS": Path("D:/DO/WEB/TOOLS/L1-INFRA/NEXUS"),
    "KG-L": Path("D:/DO/WEB/TOOLS/L4-TOOLS/KG-L"),
    "VERSES": Path("D:/DO/WEB/TOOLS/L4-TOOLS/VERSES"),
    "TRIX": Path("D:/DO/WEB/TOOLS/L4-TOOLS/TRIX"),
    "WAZAA": Path("D:/DO/WEB/TOOLS/L4-TOOLS/WAZAA"),
}

DESIGN_PRD_MATCHERS = {
    "safe-action-pattern": lambda p: "SAFE-ACTION" in p.name and "PATTERN" in p.name and "CONSUMER" in p.name,
    "safe-action-gate": lambda p: "SAFE-ACTION" in p.name and "GATE" in p.name and "CONSUMER" in p.name,
    "ecosystem-meta-coherence": lambda p: "ECOSYSTEM-META-COHERENCE" in p.name and "CONSUMER" in p.name,
    "ecosystem-meta-coherence-gate": lambda p: "ECOSYSTEM-META-COHERENCE-GATE" in p.name and "CONSUMER" in p.name,
    "design-ops-loop": lambda p: "DESIGN-OPS-LOOP" in p.name and "CONSUMER" in p.name,
    "session-boot-design": lambda p: "SESSION-BOOT" in p.name and "CONSUMER" in p.name,
    "artifact-layers-design": lambda p: "ARTIFACT-LAYERS" in p.name and "CONSUMER" in p.name,
    "meta-design-self-healing": lambda p: "META-DESIGN-SELF-HEALING" in p.name and "CONSUMER" in p.name,
    "talex-friction-analyzer": lambda p: "TALEX-FRICTION-ANALYZER" in p.name and "CONSUMER" in p.name,
}


def scan_consumer(consumer: str, design: str, matcher) -> dict:
    result = {
        "design": design,
        "consumer": consumer,
        "prd_moc_found": False,
        "prd_moc_path": None,
        "implementation_found": False,
        "implementation_path": None,
        "status": "MISSING",
    }

    root = CONSUMER_ROOTS.get(consumer)
    if not root or not root.exists():
        result["status"] = "REPO_NOT_FOUND"
        return result

    # Chercher PRD-MOC
    for candidate in root.glob("**/*CONSUMER*.md"):
        if matcher(candidate):
            result["prd_moc_found"] = True
            result["prd_moc_path"] = str(candidate)
            break

    # Chercher implémentation
    impl_file = IMPLS[design]
    matches = list(root.glob(f"**/{impl_file}"))
    if matches:
        result["implementation_found"] = True
        result["implementation_path"] = str(matches[0])

    if result["prd_moc_found"] and result["implementation_found"]:
        result["status"] = "IMPLEMENTED"
    elif result["prd_moc_found"]:
        result["status"] = "PRD_MOC_ONLY"
    else:
        result["status"] = "MISSING"

    return result


def scan_all() -> dict:
    details = []
    for design, matcher in DESIGN_PRD_MATCHERS.items():
        for consumer in CONSUMER_ROOTS.keys():
            result = scan_consumer(consumer, design, matcher)
            details.append(result)

    total = len(details)
    implemented = sum(1 for r in details if r["status"] == "IMPLEMENTED")
    prd_moc_only = sum(1 for r in details if r["status"] == "PRD_MOC_ONLY")
    missing = sum(1 for r in details if r["status"] == "MISSING")

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total_checks": total,
        "implemented": implemented,
        "prd_moc_only": prd_moc_only,
        "missing": missing,
        "coverage_pct": round(implemented / total * 100, 2) if total > 0 else 0,
        "details": details,
    }

    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print("[ACT-024] Validation finale:")
    print(f"  Total checks: {total}")
    print(f"  Implemented: {implemented} ({report['coverage_pct']}%)")
    print(f"  PRD-MOC only: {prd_moc_only}")
    print(f"  Missing: {missing}")
    print(f"  Rapport: {REPORT_PATH}")
    return report


if __name__ == "__main__":
    scan_all()
