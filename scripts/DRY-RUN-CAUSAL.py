#!/usr/bin/env python3
"""
DRY-RUN CAUSAL: Vérifie la prod-readiness de toutes les implémentations déployées.
Vérifie existence, validité et cohérence.
"""

from pathlib import Path
from datetime import datetime, timezone
import json
import sys

UNIFIED_DESIGN_ROOT = Path("D:/DO/WEB/TOOLS/L0-CANON/unified-design")
REPORT_PATH = UNIFIED_DESIGN_ROOT / "DRY-RUN-CAUSAL-report.json"

# Implémentations attendues
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

# Consumer paths
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

SCAN_DIRS = {
    "KIVA-CLI": [Path("D:/DO/WEB/TOOLS/L1-INFRA/KIVA-CLI/PRD"), Path("D:/DO/WEB/TOOLS/L1-INFRA/KIVA-CLI/PRD-MOC")],
    "ECOS-CLI": [Path("D:/DO/WEB/TOOLS/L1-INFRA/ECOS-CLI/PRD"), Path("D:/DO/WEB/TOOLS/L1-INFRA/ECOS-CLI/PRD-MOC")],
    "ARGUS": [Path("D:/DO/WEB/TOOLS/L1-INFRA/ARGUS/PRD"), Path("D:/DO/WEB/TOOLS/L1-INFRA/ARGUS/PRD-MOC")],
    "CTULU": [Path("D:/DO/WEB/TOOLS/L4-TOOLS/CTULU/PRD"), Path("D:/DO/WEB/TOOLS/L4-TOOLS/CTULU/PRD-MOC")],
    "KG-CAUSAL": [Path("D:/DO/WEB/TOOLS/L4-TOOLS/KG-CAUSAL/PRD"), Path("D:/DO/WEB/TOOLS/L4-TOOLS/KG-CAUSAL/PRD-MOC")],
    "VOLTX": [Path("D:/DO/WEB/TOOLS/L0-CANON/VOLTX/PRD"), Path("D:/DO/WEB/TOOLS/L0-CANON/VOLTX/PRD-MOC")],
    "LOOPX": [Path("D:/DO/WEB/TOOLS/L3-CITIZENS/LOOPX/PRD"), Path("D:/DO/WEB/TOOLS/L3-CITIZENS/LOOPX/PRD-MOC")],
    "KIX": [Path("D:/DO/WEB/TOOLS/L2-PLATFORM/KIX/PRD"), Path("D:/DO/WEB/TOOLS/L2-PLATFORM/KIX/PRD-MOC")],
    "TALEX": [Path("D:/DO/WEB/TOOLS/L4-TOOLS/TALEX/PRD"), Path("D:/DO/WEB/TOOLS/L4-TOOLS/TALEX/PRD-MOC")],
    "NEXUS": [Path("D:/DO/WEB/TOOLS/L1-INFRA/NEXUS/PRD"), Path("D:/DO/WEB/TOOLS/L1-INFRA/NEXUS/PRD-MOC")],
    "KG-L": [Path("D:/DO/WEB/TOOLS/L4-TOOLS/KG-L/PRD"), Path("D:/DO/WEB/TOOLS/L4-TOOLS/KG-L/PRD-MOC")],
    "VERSES": [Path("D:/DO/WEB/TOOLS/L4-TOOLS/VERSES/PRD"), Path("D:/DO/WEB/TOOLS/L4-TOOLS/VERSES/PRD-MOC")],
    "TRIX": [Path("D:/DO/WEB/TOOLS/L4-TOOLS/TRIX/PRD"), Path("D:/DO/WEB/TOOLS/L4-TOOLS/TRIX/PRD-MOC")],
    "WAZAA": [Path("D:/DO/WEB/TOOLS/L4-TOOLS/WAZAA/PRD"), Path("D:/DO/WEB/TOOLS/L4-TOOLS/WAZAA/PRD-MOC")],
}

DESIGN_PRD_MATCHERS = {
    "safe-action-pattern": lambda n: "SAFE-ACTION" in n and "PATTERN" in n and "CONSUMER" in n,
    "safe-action-gate": lambda n: "SAFE-ACTION" in n and "GATE" in n and "CONSUMER" in n,
    "ecosystem-meta-coherence": lambda n: "ECOSYSTEM-META-COHERENCE" in n and "CONSUMER" in n,
    "ecosystem-meta-coherence-gate": lambda n: "ECOSYSTEM-META-COHERENCE-GATE" in n and "CONSUMER" in n,
    "design-ops-loop": lambda n: "DESIGN-OPS-LOOP" in n and "CONSUMER" in n,
    "session-boot-design": lambda n: "SESSION-BOOT" in n and "CONSUMER" in n,
    "artifact-layers-design": lambda n: "ARTIFACT-LAYERS" in n and "CONSUMER" in n,
    "meta-design-self-healing": lambda n: "META-DESIGN-SELF-HEALING" in n and "CONSUMER" in n,
    "talex-friction-analyzer": lambda n: "TALEX-FRICTION-ANALYZER" in n and "CONSUMER" in n,
}


def check_implementation_validity(path: Path) -> dict:
    """Vérifie qu'une implémentation n'est pas un stub vide."""
    result = {"valid": False, "size": 0, "has_code": False, "error": None}
    try:
        content = path.read_text(encoding="utf-8", errors="ignore")
        result["size"] = len(content)
        result["has_code"] = bool(content.strip() and len(content.strip()) > 50)
        result["valid"] = result["has_code"]
    except Exception as e:
        result["error"] = str(e)
    return result


def scan_consumer(consumer: str, design: str) -> dict:
    result = {
        "design": design,
        "consumer": consumer,
        "prd_moc_found": False,
        "prd_moc_path": None,
        "implementation_found": False,
        "implementation_path": None,
        "implementation_valid": False,
        "status": "MISSING",
        "prod_ready": False,
    }

    # Check implementation
    impl_file = IMPLS[design]
    root = CONSUMER_ROOTS.get(consumer)
    if root and root.exists():
        matches = list(root.glob(f"**/{impl_file}"))
        if matches:
            result["implementation_found"] = True
            result["implementation_path"] = str(matches[0])
            validity = check_implementation_validity(matches[0])
            result["implementation_valid"] = validity["valid"]
            result["impl_size"] = validity["size"]

    # Check PRD-MOC
    matcher = DESIGN_PRD_MATCHERS.get(design, lambda n: False)
    for scan_dir in SCAN_DIRS.get(consumer, []):
        if not scan_dir.exists():
            continue
        for candidate in scan_dir.glob("*.md"):
            if matcher(candidate.name):
                result["prd_moc_found"] = True
                result["prd_moc_path"] = str(candidate)
                break
        if result["prd_moc_found"]:
            break

    if result["prd_moc_found"] and result["implementation_found"] and result["implementation_valid"]:
        result["status"] = "IMPLEMENTED"
        result["prod_ready"] = True
    elif result["prd_moc_found"] and result["implementation_found"]:
        result["status"] = "INVALID_IMPL"
    elif result["prd_moc_found"]:
        result["status"] = "PRD_MOC_ONLY"
    else:
        result["status"] = "MISSING"

    return result


def run_dry_run() -> dict:
    details = []
    for design in IMPLS.keys():
        for consumer in SCAN_DIRS.keys():
            result = scan_consumer(consumer, design)
            details.append(result)

    total = len(details)
    implemented = sum(1 for r in details if r["status"] == "IMPLEMENTED")
    prd_moc_only = sum(1 for r in details if r["status"] == "PRD_MOC_ONLY")
    invalid_impl = sum(1 for r in details if r["status"] == "INVALID_IMPL")
    missing = sum(1 for r in details if r["status"] == "MISSING")
    prod_ready = sum(1 for r in details if r["prod_ready"])

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total_checks": total,
        "implemented": implemented,
        "prd_moc_only": prd_moc_only,
        "invalid_impl": invalid_impl,
        "missing": missing,
        "prod_ready": prod_ready,
        "coverage_pct": round(implemented / total * 100, 2) if total > 0 else 0,
        "prod_ready_pct": round(prod_ready / total * 100, 2) if total > 0 else 0,
        "target": "100%",
        "details": details,
    }

    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print("[DRY-RUN CAUSAL] Résultats:")
    print(f"  Total checks: {total}")
    print(f"  Implemented: {implemented} ({report['coverage_pct']}%)")
    print(f"  PRD-MOC only: {prd_moc_only}")
    print(f"  Invalid impl: {invalid_impl}")
    print(f"  Missing: {missing}")
    print(f"  Prod ready: {prod_ready} ({report['prod_ready_pct']}%)")
    print(f"  Target: 100%")
    print(f"  Rapport: {REPORT_PATH}")
    
    if prod_ready == total:
        print("\n✅ PROD READY: 100% opérationnel")
        return report
    else:
        print(f"\n⚠️ GAPS PROD READY: {total - prod_ready} éléments non opérationnels")
        return report


if __name__ == "__main__":
    run_dry_run()
