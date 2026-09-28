#!/usr/bin/env python3
"""
ACT-020d: Validation globale avec chemins réels.
"""

from pathlib import Path
from datetime import datetime, timezone
import json

UNIFIED_DESIGN_ROOT = Path("D:/DO/WEB/TOOLS/L0-CANON/unified-design")
REPORT_PATH = UNIFIED_DESIGN_ROOT / "ACT-020d-global-validation-report.json"

# Charger le rapport ACT-018
ACT_018_REPORT = UNIFIED_DESIGN_ROOT / "ACT-018-deployment-report.json"
with open(ACT_018_REPORT, "r", encoding="utf-8") as f:
    act_018_data = json.load(f)

# Mapping design -> patterns PRD-MOC
DESIGN_PRD_PATTERNS = {
    "safe-action-pattern": "*SAFE-ACTION*PATTERN*CONSUMER*.md",
    "safe-action-gate": "*SAFE-ACTION*GATE*CONSUMER*.md",
    "ecosystem-meta-coherence": "*ECOSYSTEM-META-COHERENCE*CONSUMER*.md",
    "ecosystem-meta-coherence-gate": "*ECOSYSTEM-META-COHERENCE-GATE*CONSUMER*.md",
    "design-ops-loop": "*DESIGN-OPS-LOOP*CONSUMER*.md",
    "session-boot-design": "*SESSION-BOOT*CONSUMER*.md",
    "artifact-layers-design": "*ARTIFACT-LAYERS*CONSUMER*.md",
    "meta-design-self-healing": "*META-DESIGN-SELF-HEALING*CONSUMER*.md",
    "talex-friction-analyzer": "*TALEX-FRICTION-ANALYZER*CONSUMER*.md",
}

CONSUMER_PATHS = {
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


def validate_all() -> dict:
    details = []
    for deployment in act_018_data["deployments"]:
        design = deployment["design"]
        consumer = deployment["consumer"]
        result = {
            "design": design,
            "consumer": consumer,
            "prd_moc_found": False,
            "prd_moc_path": None,
            "implementation_found": False,
            "implementation_path": None,
            "status": "MISSING",
        }

        # Vérifier l'implémentation
        if deployment["status"] == "DEPLOYED":
            impl_path = Path(deployment["dest"])
            if impl_path.exists():
                result["implementation_found"] = True
                result["implementation_path"] = str(impl_path)

        # Chercher le PRD-MOC avec le pattern correct
        consumer_root = CONSUMER_PATHS[consumer]
        pattern = DESIGN_PRD_PATTERNS.get(design, f"*{design.upper()}*CONSUMER*.md")
        matches = list(consumer_root.glob(f"**/{pattern}"))
        # Filtrer par consumer
        consumer_upper = consumer.upper()
        consumer_matches = [m for m in matches if consumer_upper in str(m).upper()]
        if not consumer_matches:
            consumer_matches = matches

        if consumer_matches:
            result["prd_moc_found"] = True
            result["prd_moc_path"] = str(consumer_matches[0])

        if result["prd_moc_found"] and result["implementation_found"]:
            result["status"] = "IMPLEMENTED"
        elif result["prd_moc_found"]:
            result["status"] = "PRD_MOC_ONLY"
        else:
            result["status"] = "MISSING"

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

    print(f"[ACT-020d] Validation globale:")
    print(f"  Total checks: {total}")
    print(f"  Implemented: {implemented} ({report['coverage_pct']}%)")
    print(f"  PRD-MOC only: {prd_moc_only}")
    print(f"  Missing: {missing}")
    print(f"  Rapport: {REPORT_PATH}")
    return report


if __name__ == "__main__":
    validate_all()
