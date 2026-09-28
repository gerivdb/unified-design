#!/usr/bin/env python3
"""
ACT-020c: Validation globale ultra-simplifiée (SLM-friendly).
Utilise uniquement les chemins du rapport ACT-018.
"""

from pathlib import Path
from datetime import datetime, timezone
import json

UNIFIED_DESIGN_ROOT = Path("D:/DO/WEB/TOOLS/L0-CANON/unified-design")
REPORT_PATH = UNIFIED_DESIGN_ROOT / "ACT-020c-global-validation-report.json"

# Charger le rapport ACT-018
ACT_018_REPORT = UNIFIED_DESIGN_ROOT / "ACT-018-deployment-report.json"
with open(ACT_018_REPORT, "r", encoding="utf-8") as f:
    act_018_data = json.load(f)

# Chemins PRD-MOC attendus (basés sur les fichiers créés précédemment)
PRD_MOC_PATHS = {
    ("safe-action-pattern", "KIVA-CLI"): Path("D:/DO/WEB/TOOLS/L1-INFRA/KIVA-CLI/PRD/PRD-MOC-KIVA-CLI-SAFE-ACTION-PATTERN-CONSUMER-20260928.md"),
    ("safe-action-pattern", "ECOS-CLI"): Path("D:/DO/WEB/TOOLS/L1-INFRA/ECOS-CLI/PRD/PRD-MOC-ECOS-SAFE-ACTION-PATTERN-CONSUMER-20260928.md"),
    ("safe-action-pattern", "ARGUS"): Path("D:/DO/WEB/TOOLS/L1-INFRA/ARGUS/PRD/PRD-MOC-ARGUS-SAFE-ACTION-PATTERN-CONSUMER-20260928.md"),
    ("safe-action-pattern", "CTULU"): Path("D:/DO/WEB/TOOLS/L4-TOOLS/CTULU/PRD/PRD-MOC-CTULU-SAFE-ACTION-PATTERN-CONSUMER-20260928.md"),
    ("safe-action-pattern", "KG-CAUSAL"): Path("D:/DO/WEB/TOOLS/L4-TOOLS/KG-CAUSAL/PRD-MOC/PRD-MOC-KG-CAUSAL-SAFE-ACTION-PATTERN-CONSUMER-20260928.md"),
    ("safe-action-pattern", "VOLTX"): Path("D:/DO/WEB/TOOLS/L0-CANON/VOLTX/PRD-MOC/PRD-MOC-VOLTX-SAFE-ACTION-PATTERN-CONSUMER-20260928.md"),
    ("safe-action-pattern", "LOOPX"): Path("D:/DO/WEB/TOOLS/L3-CITIZENS/LOOPX/PRD/PRD-MOC-LOOPX-SAFE-ACTION-PATTERN-CONSUMER-20260928.md"),
    ("safe-action-pattern", "KIX"): Path("D:/DO/WEB/TOOLS/L2-PLATFORM/KIX/PRD-MOC/PRD-MOC-KIX-SAFE-ACTION-PATTERN-CONSUMER-20260928.md"),
    ("safe-action-pattern", "TALEX"): Path("D:/DO/WEB/TOOLS/L4-TOOLS/TALEX/PRD-MOC/PRD-MOC-TALEX-SAFE-ACTION-PATTERN-CONSUMER-20260928.md"),
    ("safe-action-pattern", "NEXUS"): Path("D:/DO/WEB/TOOLS/L1-INFRA/NEXUS/PRD-MOC/PRD-MOC-NEXUS-SAFE-ACTION-PATTERN-CONSUMER-20260928.md"),
    ("safe-action-pattern", "KG-L"): Path("D:/DO/WEB/TOOLS/L4-TOOLS/KG-L/PRD/PRD-MOC-KG-L-SAFE-ACTION-GATE-CONSUMER-20260928.md"),
    ("safe-action-pattern", "VERSES"): Path("D:/DO/WEB/TOOLS/L4-TOOLS/VERSES/PRD/PRD-MOC-VERSES-SAFE-ACTION-GATE-CONSUMER-20260928.md"),
    ("safe-action-pattern", "TRIX"): Path("D:/DO/WEB/TOOLS/L4-TOOLS/TRIX/PRD/PRD-MOC-TRIX-SAFE-ACTION-PATTERN-CONSUMER-20260928.md"),
    ("safe-action-pattern", "WAZAA"): Path("D:/DO/WEB/TOOLS/L4-TOOLS/WAZAA/PRD/PRD-MOC-WAZAA-SAFE-ACTION-GATE-CONSUMER-20260928.md"),
}


def validate_all() -> dict:
    details = []
    for deployment in act_018_data["deployments"]:
        design = deployment["design"]
        consumer = deployment["consumer"]
        key = (design, consumer)

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

        # Vérifier le PRD-MOC
        prd_moc_path = PRD_MOC_PATHS.get(key)
        if prd_moc_path and prd_moc_path.exists():
            result["prd_moc_found"] = True
            result["prd_moc_path"] = str(prd_moc_path)

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

    print(f"[ACT-020c] Validation globale:")
    print(f"  Total checks: {total}")
    print(f"  Implemented: {implemented} ({report['coverage_pct']}%)")
    print(f"  PRD-MOC only: {prd_moc_only}")
    print(f"  Missing: {missing}")
    print(f"  Rapport: {REPORT_PATH}")
    return report


if __name__ == "__main__":
    validate_all()
