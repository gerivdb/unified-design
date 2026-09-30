#!/usr/bin/env python3
"""
ACT-022: Validation finale avec chemins réels.
"""

from pathlib import Path
from datetime import datetime, timezone
import json

UNIFIED_DESIGN_ROOT = Path("D:/DO/WEB/TOOLS/L0-CANON/unified-design")
REPORT_PATH = UNIFIED_DESIGN_ROOT / "ACT-022-final-validation-report.json"

DESIGNS = {
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
    for design_name, impl_file in DESIGNS.items():
        for consumer, consumer_root in CONSUMER_PATHS.items():
            result = {
                "design": design_name,
                "consumer": consumer,
                "prd_moc_found": False,
                "prd_moc_path": None,
                "implementation_found": False,
                "implementation_path": None,
                "status": "MISSING",
            }

            # Chercher l'implémentation (limité à 10 résultats)
            impl_matches = list(consumer_root.glob(f"**/{impl_file}"))[:10]
            if impl_matches:
                result["implementation_found"] = True
                result["implementation_path"] = str(impl_matches[0])

            # Chercher le PRD-MOC (limité à 10 résultats)
            pattern = DESIGN_PRD_PATTERNS.get(design_name, f"*{design_name.upper()}*CONSUMER*.md")
            prd_mocs = list(consumer_root.glob(f"**/{pattern}"))[:10]
            consumer_upper = consumer.upper()
            consumer_matches = [m for m in prd_mocs if consumer_upper in str(m).upper()]
            if not consumer_matches:
                consumer_matches = prd_mocs

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

    print(f"[ACT-022] Validation finale:")
    print(f"  Total checks: {total}")
    print(f"  Implemented: {implemented} ({report['coverage_pct']}%)")
    print(f"  PRD-MOC only: {prd_moc_only}")
    print(f"  Missing: {missing}")
    print(f"  Rapport: {REPORT_PATH}")
    return report


if __name__ == "__main__":
    validate_all()
