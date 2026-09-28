#!/usr/bin/env python3
"""
ACT-021: Déploiement global de toutes les implémentations manquantes.
Script AUTO pour SLM : un fichier, une action, résultat vérifiable.
"""

import shutil
from pathlib import Path
from datetime import datetime, timezone
import json

UNIFIED_DESIGN_ROOT = Path("D:/DO/WEB/TOOLS/L0-CANON/unified-design")
IMPL_DIR = UNIFIED_DESIGN_ROOT / "scripts" / "validators" / "implementations"
REPORT_PATH = UNIFIED_DESIGN_ROOT / "ACT-021-deployment-report.json"

# Charger le rapport ACT-020d
ACT_020D_REPORT = UNIFIED_DESIGN_ROOT / "ACT-020d-global-validation-report.json"
with open(ACT_020D_REPORT, "r", encoding="utf-8") as f:
    act_020d_data = json.load(f)

# Mapping design -> fichier d'implémentation
DESIGN_IMPL_MAP = {
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

# Mapping consumer -> chemins de destination
CONSUMER_DEST_MAP = {
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


def deploy_implementation(design_name: str, consumer: str) -> dict:
    """Déploie une implémentation vers un consumer."""
    result = {
        "design": design_name,
        "consumer": consumer,
        "status": "FAILED",
        "error": None,
    }

    impl_file = DESIGN_IMPL_MAP.get(design_name)
    if not impl_file:
        result["error"] = f"No implementation file for design {design_name}"
        return result

    src_path = IMPL_DIR / impl_file
    if not src_path.exists():
        result["error"] = f"Source file not found: {src_path}"
        return result

    dest_base = CONSUMER_DEST_MAP.get(consumer)
    if not dest_base or not dest_base.exists():
        result["error"] = f"Consumer repo not found: {consumer}"
        return result

    # Déterminer le chemin de destination
    dest_candidates = [
        dest_base / "PRD" / impl_file,
        dest_base / "PRD-MOC" / impl_file,
        dest_base / "scripts" / impl_file,
        dest_base / impl_file,
    ]

    dest_path = None
    for candidate in dest_candidates:
        if candidate.parent.exists():
            dest_path = candidate
            break

    if not dest_path:
        # Créer le répertoire PRD-MOC si nécessaire
        dest_path = dest_base / "PRD-MOC" / impl_file
        dest_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        shutil.copy2(src_path, dest_path)
        result["status"] = "DEPLOYED"
        result["src"] = str(src_path)
        result["dest"] = str(dest_path)
    except Exception as e:
        result["error"] = str(e)

    return result


def deploy_all_missing() -> dict:
    """Déploie toutes les implémentations manquantes."""
    deployments = []

    for check in act_020d_data["details"]:
        if check["status"] in ("MISSING", "PRD_MOC_ONLY"):
            design = check["design"]
            consumer = check["consumer"]
            result = deploy_implementation(design, consumer)
            deployments.append(result)

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total_deployments": len(deployments),
        "successful": sum(1 for d in deployments if d["status"] == "DEPLOYED"),
        "failed": sum(1 for d in deployments if d["status"] == "FAILED"),
        "deployments": deployments,
    }

    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(f"[ACT-021] Déploiement manquant : {report['successful']}/{report['total_deployments']} réussis")
    print(f"[ACT-021] Rapport : {REPORT_PATH}")
    return report


if __name__ == "__main__":
    deploy_all_missing()
