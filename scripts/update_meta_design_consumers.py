#!/usr/bin/env python3
"""
ACT-001: Mettre à jour meta-design.yaml avec les consumers pour chaque design.
Tâche atomique SLM : un fichier, une action, résultat vérifiable.
"""

import yaml
import json
from pathlib import Path
from datetime import datetime, timezone

META_DESIGN_PATH = Path("D:/DO/WEB/TOOLS/L0-CANON/unified-design/meta-design.yaml")
REPORT_PATH = Path("D:/DO/WEB/TOOLS/L0-CANON/unified-design/ACT-001-consumers-added.json")

# Mapping design -> consumers inférés depuis les cross_references et la structure
CONSUMERS_MAP = {
    "safe-action-pattern": ["KIVA-CLI", "ECOS-CLI", "ARGUS", "CTULU", "KG-CAUSAL", "VOLTX", "LOOPX", "KIX", "TALEX", "NEXUS", "KG-L", "VERSES", "TRIX", "WAZAA"],
    "safe-action-gate": ["KIVA-CLI", "ECOS-CLI", "ARGUS", "CTULU", "KG-CAUSAL", "VOLTX", "LOOPX", "KIX", "TALEX", "NEXUS", "KG-L", "VERSES", "TRIX", "WAZAA"],
    "ecosystem-meta-coherence": ["KIVA-CLI", "ECOS-CLI", "ARGUS", "CTULU", "KG-CAUSAL", "VOLTX", "LOOPX", "KIX", "TALEX", "NEXUS", "KG-L", "VERSES", "TRIX", "WAZAA"],
    "ecosystem-meta-coherence-gate": ["KIVA-CLI", "ECOS-CLI", "ARGUS", "CTULU", "KG-CAUSAL", "VOLTX", "LOOPX", "KIX", "TALEX", "NEXUS", "KG-L", "VERSES", "TRIX", "WAZAA"],
    "design-ops-loop": ["KIVA-CLI", "ECOS-CLI", "ARGUS", "CTULU", "KG-CAUSAL", "VOLTX", "LOOPX", "KIX", "TALEX", "NEXUS", "KG-L", "VERSES", "TRIX", "WAZAA"],
    "session-boot-design": ["KIVA-CLI", "ECOS-CLI", "ARGUS", "CTULU", "KG-CAUSAL", "VOLTX", "LOOPX", "KIX", "TALEX", "NEXUS", "KG-L", "VERSES", "TRIX", "WAZAA"],
    "artifact-layers-design": ["KIVA-CLI", "ECOS-CLI", "ARGUS", "CTULU", "KG-CAUSAL", "VOLTX", "LOOPX", "KIX", "TALEX", "NEXUS", "KG-L", "VERSES", "TRIX", "WAZAA"],
    "meta-design-self-healing": ["KIVA-CLI", "ECOS-CLI", "ARGUS", "CTULU", "KG-CAUSAL", "VOLTX", "LOOPX", "KIX", "TALEX", "NEXUS", "KG-L", "VERSES", "TRIX", "WAZAA"],
    "talex-friction-analyzer": ["KIVA-CLI", "ECOS-CLI", "ARGUS", "CTULU", "KG-CAUSAL", "VOLTX", "LOOPX", "KIX", "TALEX", "NEXUS", "KG-L", "VERSES", "TRIX", "WAZAA"],
    "kg-causal-integration-pattern": ["KG-CAUSAL", "KG-L", "VERSES", "CTULU", "TRIX", "WAZAA", "KIX"],
    "pipeline-mdu-validation": ["KIVA-CLI", "ECOS-CLI", "CTULU", "LOOPX"],
    "pipeline-dryrun-causal-audit": ["KIVA-CLI", "ECOS-CLI", "CTULU", "LOOPX", "KG-CAUSAL"],
    "pipeline-friction-analysis-to-fix": ["KIVA-CLI", "ECOS-CLI", "CTULU", "LOOPX", "TALEX"],
    "pipeline-session-boot-closeout": ["KIVA-CLI", "ECOS-CLI", "CTULU", "LOOPX", "ARGUS"],
    "pipeline-sot-completeness": ["KIVA-CLI", "ECOS-CLI", "CTULU", "LOOPX", "GOVERNANCE-HUB"],
    "pipeline-yaml-structure-validation": ["KIVA-CLI", "ECOS-CLI", "CTULU", "LOOPX", "GOVERNANCE-HUB"],
    "workflow-sot-completeness": ["KIVA-CLI", "ECOS-CLI", "CTULU", "LOOPX", "GOVERNANCE-HUB"],
    "workflow-yaml-structure-validator": ["KIVA-CLI", "ECOS-CLI", "CTULU", "LOOPX", "GOVERNANCE-HUB"],
    "artifact-layers-primitive": ["KIVA-CLI", "ECOS-CLI", "CTULU", "KG-CAUSAL", "VOLTX"],
    "design-ops-loop-primitive": ["KIVA-CLI", "ECOS-CLI", "CTULU", "LOOPX", "ARGUS"],
    "ecosystem-meta-coherence-primitive": ["KIVA-CLI", "ECOS-CLI", "CTULU", "LOOPX", "ARGUS"],
    "ecosystem-meta-coherence-gate-primitive": ["KIVA-CLI", "ECOS-CLI", "CTULU", "LOOPX", "ARGUS"],
    "safe-action-gate-primitive": ["KIVA-CLI", "ECOS-CLI", "CTULU", "LOOPX", "ARGUS"],
    "session-boot-primitive": ["KIVA-CLI", "ECOS-CLI", "CTULU", "LOOPX", "ARGUS"],
    "talex-friction-analyzer-primitive": ["KIVA-CLI", "ECOS-CLI", "CTULU", "LOOPX", "ARGUS"],
    "boot-sequence-validator": ["KIVA-CLI", "ECOS-CLI", "CTULU", "LOOPX", "ARGUS"],
    "symbiose-coordinated-reload": ["KIVA-CLI", "ECOS-CLI", "CTULU", "LOOPX", "ARGUS"],
}


def update_meta_design():
    """Met à jour meta-design.yaml avec les consumers."""
    with open(META_DESIGN_PATH, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    # meta-design.yaml est une liste de capacités
    capabilities = data if isinstance(data, list) else data.get("capabilities", [])
    consumers_added = []

    # Mapping port_id -> consumers (inférés depuis les designs)
    PORT_CONSUMERS_MAP = {
        "latency-bound": ["KIX", "TRIX", "CTULU"],
        "power-capped": ["KIX", "TRIX", "CTULU"],
        "attention-mechanism": ["TALEX", "NEXUS", "KIX"],
        "symbol-retrieval": ["KIVA-CLI", "ECOS-CLI", "ARGUS", "NEXUS"],
        "worktree-isolation": ["KIVA-CLI", "ECOS-CLI", "LOOPX", "NEXUS"],
        "beads-sql-memory": ["KIVA-CLI", "ECOS-CLI", "LOOPX", "NEXUS"],
        "exit-interceptor": ["KIVA-CLI", "ECOS-CLI", "LOOPX", "NEXUS"],
        "tdd-airain-law": ["KIVA-CLI", "ECOS-CLI", "ARGUS", "CTULU", "LOOPX", "NEXUS"],
        "trace-replay-proof": ["KIVA-CLI", "ECOS-CLI", "VOLTX", "NEXUS"],
    }

    for capability in capabilities:
        if not isinstance(capability, dict):
            continue
        port_id = capability.get("port_id", "")
        current_consumers = capability.get("consumers", [])
        if not current_consumers and port_id in PORT_CONSUMERS_MAP:
            inferred = PORT_CONSUMERS_MAP[port_id]
            capability["consumers"] = inferred
            consumers_added.append({
                "port_id": port_id,
                "consumers_added": inferred,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })

    with open(META_DESIGN_PATH, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False, default_flow_style=False)

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total_capabilities": len(capabilities),
        "consumers_added_count": len(consumers_added),
        "consumers_added": consumers_added,
    }

    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(f"[ACT-001] Meta-design mis à jour : {len(consumers_added)} capacités enrichies")
    print(f"[ACT-001] Rapport : {REPORT_PATH}")
    return report


if __name__ == "__main__":
    update_meta_design()
