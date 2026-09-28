#!/usr/bin/env python3
"""
ACT-027: Déployer le hook pre-commit validate_consumer_designs.py
dans tous les repos consumers.
"""

from pathlib import Path
from datetime import datetime, timezone
import json
import shutil

UNIFIED_DESIGN_ROOT = Path("D:/DO/WEB/TOOLS/L0-CANON/unified-design")
REPORT_PATH = UNIFIED_DESIGN_ROOT / "ACT-027-hook-deployment-report.json"

# Consumers et leurs chemins
CONSUMERS = {
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

# Script source
HOOK_SOURCE = UNIFIED_DESIGN_ROOT / "scripts" / "validate_consumer_designs.py"


def deploy_hook(consumer: str, root: Path) -> dict:
    result = {
        "consumer": consumer,
        "status": "FAILED",
        "hook_path": None,
        "error": None,
    }

    if not root.exists():
        result["error"] = f"Repo not found: {root}"
        return result

    # Créer le répertoire .git/hooks si nécessaire
    git_hooks_dir = root / ".git" / "hooks"
    if not git_hooks_dir.exists():
        git_hooks_dir.mkdir(parents=True, exist_ok=True)

    hook_path = git_hooks_dir / "validate_consumer_designs.py"
    try:
        if HOOK_SOURCE.exists():
            shutil.copy2(HOOK_SOURCE, hook_path)
            result["status"] = "DEPLOYED"
            result["hook_path"] = str(hook_path)
        else:
            # Créer un stub si le script source n'existe pas encore
            hook_path.write_text("#!/usr/bin/env python3\n# TODO: implement validate_consumer_designs.py\n", encoding="utf-8")
            result["status"] = "STUB_CREATED"
            result["hook_path"] = str(hook_path)
            result["error"] = "Source hook not found, stub created"
    except Exception as e:
        result["error"] = str(e)

    return result


def deploy_all() -> dict:
    results = []
    for consumer, root in CONSUMERS.items():
        result = deploy_hook(consumer, root)
        results.append(result)

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total_consumers": len(results),
        "deployed": sum(1 for r in results if r["status"] == "DEPLOYED"),
        "stub_created": sum(1 for r in results if r["status"] == "STUB_CREATED"),
        "failed": sum(1 for r in results if r["status"] == "FAILED"),
        "results": results,
    }

    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(f"[ACT-027] Déploiement hooks: {report['deployed']}/{report['total_consumers']} déployés, {report['stub_created']} stubs, {report['failed']} échecs")
    print(f"[ACT-027] Rapport: {REPORT_PATH}")
    return report


if __name__ == "__main__":
    deploy_all()
