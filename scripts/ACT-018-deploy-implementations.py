#!/usr/bin/env python3
"""
ACT-018: Déploiement des implémentations centrales vers les repos consumers.
Tâche atomique SLM : un fichier, une action, résultat vérifiable.
"""

import shutil
from pathlib import Path
from datetime import datetime, timezone
import json

UNIFIED_DESIGN_ROOT = Path("D:/DO/WEB/TOOLS/L0-CANON/unified-design")
IMPL_DIR = UNIFIED_DESIGN_ROOT / "scripts" / "validators" / "implementations"
REPORT_PATH = UNIFIED_DESIGN_ROOT / "ACT-018-deployment-report.json"

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

# Mapping design -> consumers
DESIGN_CONSUMERS_MAP = {
    "safe-action-pattern": ["KIVA-CLI", "ECOS-CLI", "ARGUS", "CTULU", "KG-CAUSAL", "VOLTX", "LOOPX", "KIX", "TALEX", "NEXUS", "KG-L", "VERSES", "TRIX", "WAZAA"],
    "safe-action-gate": ["KIVA-CLI", "ECOS-CLI", "ARGUS", "CTULU", "KG-CAUSAL", "VOLTX", "LOOPX", "KIX", "TALEX", "NEXUS", "KG-L", "VERSES", "TRIX", "WAZAA"],
    "ecosystem-meta-coherence": ["KIVA-CLI", "ECOS-CLI", "ARGUS", "CTULU", "KG-CAUSAL", "VOLTX", "LOOPX", "KIX", "TALEX", "NEXUS", "KG-L", "VERSES", "TRIX", "WAZAA"],
    "ecosystem-meta-coherence-gate": ["KIVA-CLI", "ECOS-CLI", "ARGUS", "CTULU", "KG-CAUSAL", "VOLTX", "LOOPX", "KIX", "TALEX", "NEXUS", "KG-L", "VERSES", "TRIX", "WAZAA"],
    "design-ops-loop": ["KIVA-CLI", "ECOS-CLI", "ARGUS", "CTULU", "KG-CAUSAL", "VOLTX", "LOOPX", "KIX", "TALEX", "NEXUS", "KG-L", "VERSES", "TRIX", "WAZAA"],
    "session-boot-design": ["KIVA-CLI", "ECOS-CLI", "ARGUS", "CTULU", "KG-CAUSAL", "VOLTX", "LOOPX", "KIX", "TALEX", "NEXUS", "KG-L", "VERSES", "TRIX", "WAZAA"],
    "artifact-layers-design": ["KIVA-CLI", "ECOS-CLI", "ARGUS", "CTULU", "KG-CAUSAL", "VOLTX", "LOOPX", "KIX", "TALEX", "NEXUS", "KG-L", "VERSES", "TRIX", "WAZAA"],
    "meta-design-self-healing": ["KIVA-CLI", "ECOS-CLI", "ARGUS", "CTULU", "KG-CAUSAL", "VOLTX", "LOOPX", "KIX", "TALEX", "NEXUS", "KG-L", "VERSES", "TRIX", "WAZAA"],
    "talex-friction-analyzer": ["KIVA-CLI", "ECOS-CLI", "ARGUS", "CTULU", "KG-CAUSAL", "VOLTX", "LOOPX", "KIX", "TALEX", "NEXUS", "KG-L", "VERSES", "TRIX", "WAZAA"],
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
    # Pour les repos avec PRD/PRD-MOC/ ou PRD-MOC/
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


def deploy_all() -> dict:
    """Déploie toutes les implémentations vers tous les consumers."""
    deployments = []

    for design_name, consumers in DESIGN_CONSUMERS_MAP.items():
        for consumer in consumers:
            result = deploy_implementation(design_name, consumer)
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

    print(f"[ACT-018] Déploiement terminé : {report['successful']}/{report['total_deployments']} réussis")
    print(f"[ACT-018] Rapport : {REPORT_PATH}")
    return report


if __name__ == "__main__":
    deploy_all()
