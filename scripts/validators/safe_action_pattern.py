#!/usr/bin/env python3
"""
ACT-002: Script de validation central safe-action-pattern.
Tâche atomique SLM : un fichier, une action, résultat vérifiable.
"""

from pathlib import Path

UNIFIED_DESIGN_ROOT = Path("D:/DO/WEB/TOOLS/L0-CANON/unified-design")
VALIDATOR_PATH = UNIFIED_DESIGN_ROOT / "scripts" / "validators" / "safe_action_pattern.py"

# Consumers cibles pour safe-action-pattern
CONSUMERS = [
    "KIVA-CLI", "ECOS-CLI", "ARGUS", "CTULU", "KG-CAUSAL", "VOLTX",
    "LOOPX", "KIX", "TALEX", "NEXUS", "KG-L", "VERSES", "TRIX", "WAZAA"
]


def validate_consumer_prd_moc(consumer_repo: str) -> dict:
    """Valide qu'un consumer a un PRD-MOC safe-action-pattern."""
    result = {
        "consumer": consumer_repo,
        "prd_moc_found": False,
        "prd_moc_path": None,
        "implementation_found": False,
        "implementation_path": None,
        "status": "MISSING",
    }

    # Chercher le PRD-MOC dans le repo du consumer
    consumer_paths = {
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

    consumer_root = consumer_paths.get(consumer_repo)
    if not consumer_root or not consumer_root.exists():
        result["status"] = "REPO_NOT_FOUND"
        return result

    # Chercher le PRD-MOC
    prd_moc_patterns = [
        f"**/PRD-MOC-{consumer_repo.upper()}-SAFE-ACTION-PATTERN-CONSUMER-*.md",
        f"**/PRD-MOC-{consumer_repo.upper()}-SAFE-ACTION-GATE-CONSUMER-*.md",
        f"**/PRD-MOC-*-SAFE-ACTION-PATTERN-CONSUMER-*.md",
        f"**/PRD-MOC-*-SAFE-ACTION-GATE-CONSUMER-*.md",
    ]

    for pattern in prd_moc_patterns:
        matches = list(consumer_root.glob(pattern))
        if matches:
            result["prd_moc_found"] = True
            result["prd_moc_path"] = str(matches[0])
            break

    # Chercher l'implémentation
    impl_patterns = [
        f"**/safe_action_*.py",
        f"**/safe-action-*.py",
    ]

    for pattern in impl_patterns:
        matches = list(consumer_root.glob(pattern))
        if matches:
            result["implementation_found"] = True
            result["implementation_path"] = str(matches[0])
            break

    # Déterminer le statut
    if result["prd_moc_found"] and result["implementation_found"]:
        result["status"] = "IMPLEMENTED"
    elif result["prd_moc_found"]:
        result["status"] = "PRD_MOC_ONLY"
    else:
        result["status"] = "MISSING"

    return result


def validate_all_consumers() -> dict:
    """Valide tous les consumers."""
    results = []
    for consumer in CONSUMERS:
        result = validate_consumer_prd_moc(consumer)
        results.append(result)

    report = {
        "design": "safe-action-pattern",
        "timestamp": __import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat(),
        "total_consumers": len(CONSUMERS),
        "implemented": sum(1 for r in results if r["status"] == "IMPLEMENTED"),
        "prd_moc_only": sum(1 for r in results if r["status"] == "PRD_MOC_ONLY"),
        "missing": sum(1 for r in results if r["status"] == "MISSING"),
        "repo_not_found": sum(1 for r in results if r["status"] == "REPO_NOT_FOUND"),
        "details": results,
    }

    return report


if __name__ == "__main__":
    report = validate_all_consumers()
    print(f"[ACT-002] safe-action-pattern validation:")
    print(f"  Total consumers: {report['total_consumers']}")
    print(f"  Implemented: {report['implemented']}")
    print(f"  PRD-MOC only: {report['prd_moc_only']}")
    print(f"  Missing: {report['missing']}")
    print(f"  Repo not found: {report['repo_not_found']}")
