#!/usr/bin/env python3
"""
ACT-020b: Validation globale simplifiée (SLM-friendly).
"""

from pathlib import Path
from datetime import datetime, timezone
import json

UNIFIED_DESIGN_ROOT = Path("D:/DO/WEB/TOOLS/L0-CANON/unified-design")
REPORT_PATH = UNIFIED_DESIGN_ROOT / "ACT-020b-global-validation-report.json"

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

# Chemins de déploiement connus (issus du rapport ACT-018)
KNOWN_DEPLOYMENTS = {
    ("safe-action-pattern", "KIVA-CLI"): Path("D:/DO/WEB/TOOLS/L1-INFRA/KIVA-CLI/PRD/safe_action_pattern.py"),
    ("safe-action-pattern", "ECOS-CLI"): Path("D:/DO/WEB/TOOLS/L1-INFRA/ECOS-CLI/PRD/safe_action_pattern.py"),
    ("safe-action-pattern", "ARGUS"): Path("D:/DO/WEB/TOOLS/L1-INFRA/ARGUS/PRD/safe_action_pattern.py"),
    ("safe-action-pattern", "CTULU"): Path("D:/DO/WEB/TOOLS/L4-TOOLS/CTULU/PRD/safe_action_pattern.py"),
    ("safe-action-pattern", "KG-CAUSAL"): Path("D:/DO/WEB/TOOLS/L4-TOOLS/KG-CAUSAL/PRD-MOC/safe_action_pattern.py"),
    ("safe-action-pattern", "VOLTX"): Path("D:/DO/WEB/TOOLS/L0-CANON/VOLTX/PRD-MOC/safe_action_pattern.py"),
    ("safe-action-pattern", "LOOPX"): Path("D:/DO/WEB/TOOLS/L3-CITIZENS/LOOPX/PRD/safe_action_pattern.py"),
    ("safe-action-pattern", "KIX"): Path("D:/DO/WEB/TOOLS/L2-PLATFORM/KIX/PRD-MOC/safe_action_pattern.py"),
    ("safe-action-pattern", "TALEX"): Path("D:/DO/WEB/TOOLS/L4-TOOLS/TALEX/PRD/safe_action_pattern.py"),
    ("safe-action-pattern", "NEXUS"): Path("D:/DO/WEB/TOOLS/L1-INFRA/NEXUS/PRD-MOC/safe_action_pattern.py"),
    ("safe-action-pattern", "KG-L"): Path("D:/DO/WEB/TOOLS/L4-TOOLS/KG-L/PRD/safe_action_pattern.py"),
    ("safe-action-pattern", "VERSES"): Path("D:/DO/WEB/TOOLS/L4-TOOLS/VERSES/PRD/safe_action_pattern.py"),
    ("safe-action-pattern", "TRIX"): Path("D:/DO/WEB/TOOLS/L4-TOOLS/TRIX/PRD/safe_action_pattern.py"),
    ("safe-action-pattern", "WAZAA"): Path("D:/DO/WEB/TOOLS/L4-TOOLS/WAZAA/PRD/safe_action_pattern.py"),
    ("safe-action-gate", "KIVA-CLI"): Path("D:/DO/WEB/TOOLS/L1-INFRA/KIVA-CLI/PRD/safe_action_gate.py"),
    ("safe-action-gate", "ECOS-CLI"): Path("D:/DO/WEB/TOOLS/L1-INFRA/ECOS-CLI/PRD/safe_action_gate.py"),
    ("safe-action-gate", "ARGUS"): Path("D:/DO/WEB/TOOLS/L1-INFRA/ARGUS/PRD/safe_action_gate.py"),
    ("safe-action-gate", "CTULU"): Path("D:/DO/WEB/TOOLS/L4-TOOLS/CTULU/PRD/safe_action_gate.py"),
    ("safe-action-gate", "KG-CAUSAL"): Path("D:/DO/WEB/TOOLS/L4-TOOLS/KG-CAUSAL/PRD-MOC/safe_action_gate.py"),
    ("safe-action-gate", "VOLTX"): Path("D:/DO/WEB/TOOLS/L0-CANON/VOLTX/PRD-MOC/safe_action_gate.py"),
    ("safe-action-gate", "LOOPX"): Path("D:/DO/WEB/TOOLS/L3-CITIZENS/LOOPX/PRD/safe_action_gate.py"),
    ("safe-action-gate", "KIX"): Path("D:/DO/WEB/TOOLS/L2-PLATFORM/KIX/PRD-MOC/safe_action_gate.py"),
    ("safe-action-gate", "TALEX"): Path("D:/DO/WEB/TOOLS/L4-TOOLS/TALEX/PRD/safe_action_gate.py"),
    ("safe-action-gate", "NEXUS"): Path("D:/DO/WEB/TOOLS/L1-INFRA/NEXUS/PRD-MOC/safe_action_gate.py"),
    ("safe-action-gate", "KG-L"): Path("D:/DO/WEB/TOOLS/L4-TOOLS/KG-L/PRD/safe_action_gate.py"),
    ("safe-action-gate", "VERSES"): Path("D:/DO/WEB/TOOLS/L4-TOOLS/VERSES/PRD/safe_action_gate.py"),
    ("safe-action-gate", "TRIX"): Path("D:/DO/WEB/TOOLS/L4-TOOLS/TRIX/PRD/safe_action_gate.py"),
    ("safe-action-gate", "WAZAA"): Path("D:/DO/WEB/TOOLS/L4-TOOLS/WAZAA/PRD/safe_action_gate.py"),
}


def validate_all() -> dict:
    details = []
    for design_name, impl_file in DESIGNS.items():
        for consumer in CONSUMER_PATHS.keys():
            key = (design_name, consumer)
            result = {
                "design": design_name,
                "consumer": consumer,
                "prd_moc_found": False,
                "implementation_found": False,
                "status": "MISSING",
            }

            # Vérifier l'implémentation
            impl_path = KNOWN_DEPLOYMENTS.get(key)
            if impl_path and impl_path.exists():
                result["implementation_found"] = True
                result["implementation_path"] = str(impl_path)

            # Chercher le PRD-MOC (simplifié)
            consumer_root = CONSUMER_PATHS[consumer]
            prd_mocs = list(consumer_root.glob(f"**/PRD*/*{design_name.upper()}*CONSUMER*.md"))
            if not prd_mocs:
                prd_mocs = list(consumer_root.glob(f"**/PRD*/*CONSUMER*{design_name.upper()}*.md"))
            if prd_mocs:
                result["prd_moc_found"] = True
                result["prd_moc_path"] = str(prd_mocs[0])

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

    print(f"[ACT-020b] Validation globale:")
    print(f"  Total checks: {total}")
    print(f"  Implemented: {implemented} ({report['coverage_pct']}%)")
    print(f"  PRD-MOC only: {prd_moc_only}")
    print(f"  Missing: {missing}")
    print(f"  Rapport: {REPORT_PATH}")
    return report


if __name__ == "__main__":
    validate_all()
