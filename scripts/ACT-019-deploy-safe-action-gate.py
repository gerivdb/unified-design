#!/usr/bin/env python3
"""
ACT-019: Déploiement de safe-action-gate.py vers tous les consumers.
"""

import shutil
from pathlib import Path
from datetime import datetime, timezone
import json

IMPL_DIR = Path("D:/DO/WEB/TOOLS/L0-CANON/unified-design/scripts/validators/implementations")
REPORT_PATH = Path("D:/DO/WEB/TOOLS/L0-CANON/unified-design/ACT-019-deployment-report.json")

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

CONSUMERS = list(CONSUMER_DEST_MAP.keys())
src_path = IMPL_DIR / "safe_action_gate.py"
deployments = []

for consumer in CONSUMERS:
    result = {"design": "safe-action-gate", "consumer": consumer, "status": "FAILED", "error": None}
    dest_base = CONSUMER_DEST_MAP.get(consumer)
    if not dest_base or not dest_base.exists():
        result["error"] = f"Consumer repo not found: {consumer}"
        deployments.append(result)
        continue

    dest_candidates = [
        dest_base / "PRD" / "safe_action_gate.py",
        dest_base / "PRD-MOC" / "safe_action_gate.py",
        dest_base / "scripts" / "safe_action_gate.py",
        dest_base / "safe_action_gate.py",
    ]

    dest_path = None
    for candidate in dest_candidates:
        if candidate.parent.exists():
            dest_path = candidate
            break

    if not dest_path:
        dest_path = dest_base / "PRD-MOC" / "safe_action_gate.py"
        dest_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        shutil.copy2(src_path, dest_path)
        result["status"] = "DEPLOYED"
        result["src"] = str(src_path)
        result["dest"] = str(dest_path)
    except Exception as e:
        result["error"] = str(e)

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

print(f"[ACT-019] Deploiement safe-action-gate : {report['successful']}/{report['total_deployments']} reussis")
