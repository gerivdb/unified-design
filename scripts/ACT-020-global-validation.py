#!/usr/bin/env python3
"""
ACT-020: Validation globale de tous les designs et consumers.
Tâche atomique SLM : un fichier, une action, résultat vérifiable.
"""

from pathlib import Path
from datetime import datetime, timezone
import json

UNIFIED_DESIGN_ROOT = Path("D:/DO/WEB/TOOLS/L0-CANON/unified-design")
REPORT_PATH = UNIFIED_DESIGN_ROOT / "ACT-020-global-validation-report.json"

# Tous les designs ACTIVE/STANDARD et leurs consumers
DESIGNS = {
    "safe-action-pattern": {
        "consumers": ["KIVA-CLI", "ECOS-CLI", "ARGUS", "CTULU", "KG-CAUSAL", "VOLTX", "LOOPX", "KIX", "TALEX", "NEXUS", "KG-L", "VERSES", "TRIX", "WAZAA"],
        "impl_file": "safe_action_pattern.py",
        "prd_pattern": "*SAFE-ACTION*CONSUMER*.md",
    },
    "safe-action-gate": {
        "consumers": ["KIVA-CLI", "ECOS-CLI", "ARGUS", "CTULU", "KG-CAUSAL", "VOLTX", "LOOPX", "KIX", "TALEX", "NEXUS", "KG-L", "VERSES", "TRIX", "WAZAA"],
        "impl_file": "safe_action_gate.py",
        "prd_pattern": "*SAFE-ACTION*CONSUMER*.md",
    },
    "ecosystem-meta-coherence": {
        "consumers": ["KIVA-CLI", "ECOS-CLI", "ARGUS", "CTULU", "KG-CAUSAL", "VOLTX", "LOOPX", "KIX", "TALEX", "NEXUS", "KG-L", "VERSES", "TRIX", "WAZAA"],
        "impl_file": "ecosystem_meta_coherence.py",
        "prd_pattern": "*ECOSYSTEM-META-COHERENCE*CONSUMER*.md",
    },
    "ecosystem-meta-coherence-gate": {
        "consumers": ["KIVA-CLI", "ECOS-CLI", "ARGUS", "CTULU", "KG-CAUSAL", "VOLTX", "LOOPX", "KIX", "TALEX", "NEXUS", "KG-L", "VERSES", "TRIX", "WAZAA"],
        "impl_file": "ecosystem_meta_coherence_gate.py",
        "prd_pattern": "*ECOSYSTEM-META-COHERENCE-GATE*CONSUMER*.md",
    },
    "design-ops-loop": {
        "consumers": ["KIVA-CLI", "ECOS-CLI", "ARGUS", "CTULU", "KG-CAUSAL", "VOLTX", "LOOPX", "KIX", "TALEX", "NEXUS", "KG-L", "VERSES", "TRIX", "WAZAA"],
        "impl_file": "design_ops_loop.py",
        "prd_pattern": "*DESIGN-OPS-LOOP*CONSUMER*.md",
    },
    "session-boot-design": {
        "consumers": ["KIVA-CLI", "ECOS-CLI", "ARGUS", "CTULU", "KG-CAUSAL", "VOLTX", "LOOPX", "KIX", "TALEX", "NEXUS", "KG-L", "VERSES", "TRIX", "WAZAA"],
        "impl_file": "session_boot_design.py",
        "prd_pattern": "*SESSION-BOOT*CONSUMER*.md",
    },
    "artifact-layers-design": {
        "consumers": ["KIVA-CLI", "ECOS-CLI", "ARGUS", "CTULU", "KG-CAUSAL", "VOLTX", "LOOPX", "KIX", "TALEX", "NEXUS", "KG-L", "VERSES", "TRIX", "WAZAA"],
        "impl_file": "artifact_layers_design.py",
        "prd_pattern": "*ARTIFACT-LAYERS*CONSUMER*.md",
    },
    "meta-design-self-healing": {
        "consumers": ["KIVA-CLI", "ECOS-CLI", "ARGUS", "CTULU", "KG-CAUSAL", "VOLTX", "LOOPX", "KIX", "TALEX", "NEXUS", "KG-L", "VERSES", "TRIX", "WAZAA"],
        "impl_file": "meta_design_self_healing.py",
        "prd_pattern": "*META-DESIGN-SELF-HEALING*CONSUMER*.md",
    },
    "talex-friction-analyzer": {
        "consumers": ["KIVA-CLI", "ECOS-CLI", "ARGUS", "CTULU", "KG-CAUSAL", "VOLTX", "LOOPX", "KIX", "TALEX", "NEXUS", "KG-L", "VERSES", "TRIX", "WAZAA"],
        "impl_file": "talex_friction_analyzer.py",
        "prd_pattern": "*TALEX-FRICTION-ANALYZER*CONSUMER*.md",
    },
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


def validate_design_consumer(design_name: str, consumer: str, design_config: dict) -> dict:
    """Valide un design pour un consumer."""
    result = {
        "design": design_name,
        "consumer": consumer,
        "prd_moc_found": False,
        "prd_moc_path": None,
        "implementation_found": False,
        "implementation_path": None,
        "status": "MISSING",
    }

    consumer_root = CONSUMER_PATHS.get(consumer)
    if not consumer_root or not consumer_root.exists():
        result["status"] = "REPO_NOT_FOUND"
        return result

    # Chercher le PRD-MOC
    prd_pattern = design_config["prd_pattern"]
    matches = list(consumer_root.glob(f"**/{prd_pattern}"))
    # Filtrer par consumer
    consumer_upper = consumer.upper()
    consumer_matches = [m for m in matches if consumer_upper in str(m).upper()]
    if not consumer_matches:
        consumer_matches = matches

    if consumer_matches:
        result["prd_moc_found"] = True
        result["prd_moc_path"] = str(consumer_matches[0])

    # Chercher l'implémentation
    impl_file = design_config["impl_file"]
    impl_matches = list(consumer_root.glob(f"**/{impl_file}"))
    if impl_matches:
        result["implementation_found"] = True
        result["implementation_path"] = str(impl_matches[0])

    if result["prd_moc_found"] and result["implementation_found"]:
        result["status"] = "IMPLEMENTED"
    elif result["prd_moc_found"]:
        result["status"] = "PRD_MOC_ONLY"
    else:
        result["status"] = "MISSING"

    return result


def validate_all() -> dict:
    """Valide tous les designs et consumers."""
    details = []
    for design_name, design_config in DESIGNS.items():
        for consumer in design_config["consumers"]:
            result = validate_design_consumer(design_name, consumer, design_config)
            details.append(result)

    total = len(details)
    implemented = sum(1 for r in details if r["status"] == "IMPLEMENTED")
    prd_moc_only = sum(1 for r in details if r["status"] == "PRD_MOC_ONLY")
    missing = sum(1 for r in details if r["status"] == "MISSING")
    repo_not_found = sum(1 for r in details if r["status"] == "REPO_NOT_FOUND")

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total_checks": total,
        "implemented": implemented,
        "prd_moc_only": prd_moc_only,
        "missing": missing,
        "repo_not_found": repo_not_found,
        "coverage_pct": round(implemented / total * 100, 2) if total > 0 else 0,
        "details": details,
    }

    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(f"[ACT-020] Validation globale :")
    print(f"  Total checks: {total}")
    print(f"  Implemented: {implemented} ({report['coverage_pct']}%)")
    print(f"  PRD-MOC only: {prd_moc_only}")
    print(f"  Missing: {missing}")
    print(f"  Repo not found: {repo_not_found}")
    print(f"  Rapport: {REPORT_PATH}")
    return report


if __name__ == "__main__":
    validate_all()
