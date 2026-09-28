#!/usr/bin/env python3
"""
ACT-028: Auditer les PRD-MOC existants dans les 14 consumers.
Évalue la pertinence et identifie les gaps réels.
"""

from pathlib import Path
from datetime import datetime, timezone
import json

UNIFIED_DESIGN_ROOT = Path("D:/DO/WEB/TOOLS/L0-CANON/unified-design")
REPORT_PATH = UNIFIED_DESIGN_ROOT / "ACT-028-prd-moc-audit-report.json"

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

# Designs attendus
DESIGNS = [
    "safe-action-pattern",
    "safe-action-gate",
    "ecosystem-meta-coherence",
    "ecosystem-meta-coherence-gate",
    "design-ops-loop",
    "session-boot-design",
    "artifact-layers-design",
    "meta-design-self-healing",
    "talex-friction-analyzer",
]

# Mapping design -> impl file
IMPL_FILES = {d: d.replace("-", "_") + ".py" for d in DESIGNS}

# Scan directories
SCAN_DIRS = {
    "KIVA-CLI": [Path("D:/DO/WEB/TOOLS/L1-INFRA/KIVA-CLI/PRD"), Path("D:/DO/WEB/TOOLS/L1-INFRA/KIVA-CLI/PRD-MOC")],
    "ECOS-CLI": [Path("D:/DO/WEB/TOOLS/L1-INFRA/ECOS-CLI/PRD"), Path("D:/DO/WEB/TOOLS/L1-INFRA/ECOS-CLI/PRD-MOC")],
    "ARGUS": [Path("D:/DO/WEB/TOOLS/L1-INFRA/ARGUS/PRD"), Path("D:/DO/WEB/TOOLS/L1-INFRA/ARGUS/PRD-MOC")],
    "CTULU": [Path("D:/DO/WEB/TOOLS/L4-TOOLS/CTULU/PRD"), Path("D:/DO/WEB/TOOLS/L4-TOOLS/CTULU/PRD-MOC")],
    "KG-CAUSAL": [Path("D:/DO/WEB/TOOLS/L4-TOOLS/KG-CAUSAL/PRD"), Path("D:/DO/WEB/TOOLS/L4-TOOLS/KG-CAUSAL/PRD-MOC")],
    "VOLTX": [Path("D:/DO/WEB/TOOLS/L0-CANON/VOLTX/PRD"), Path("D:/DO/WEB/TOOLS/L0-CANON/VOLTX/PRD-MOC")],
    "LOOPX": [Path("D:/DO/WEB/TOOLS/L3-CITIZENS/LOOPX/PRD"), Path("D:/DO/WEB/TOOLS/L3-CITIZENS/LOOPX/PRD-MOC")],
    "KIX": [Path("D:/DO/WEB/TOOLS/L2-PLATFORM/KIX/PRD"), Path("D:/DO/WEB/TOOLS/L2-PLATFORM/KIX/PRD-MOC")],
    "TALEX": [Path("D:/DO/WEB/TOOLS/L4-TOOLS/TALEX/PRD"), Path("D:/DO/WEB/TOOLS/L4-TOOLS/TALEX/PRD-MOC")],
    "NEXUS": [Path("D:/DO/WEB/TOOLS/L1-INFRA/NEXUS/PRD"), Path("D:/DO/WEB/TOOLS/L1-INFRA/NEXUS/PRD-MOC")],
    "KG-L": [Path("D:/DO/WEB/TOOLS/L4-TOOLS/KG-L/PRD"), Path("D:/DO/WEB/TOOLS/L4-TOOLS/KG-L/PRD-MOC")],
    "VERSES": [Path("D:/DO/WEB/TOOLS/L4-TOOLS/VERSES/PRD"), Path("D:/DO/WEB/TOOLS/L4-TOOLS/VERSES/PRD-MOC")],
    "TRIX": [Path("D:/DO/WEB/TOOLS/L4-TOOLS/TRIX/PRD"), Path("D:/DO/WEB/TOOLS/L4-TOOLS/TRIX/PRD-MOC")],
    "WAZAA": [Path("D:/DO/WEB/TOOLS/L4-TOOLS/WAZAA/PRD"), Path("D:/DO/WEB/TOOLS/L4-TOOLS/WAZAA/PRD-MOC")],
}

DESIGN_PRD_MATCHERS = {
    "safe-action-pattern": lambda n: "SAFE-ACTION" in n and "PATTERN" in n and "CONSUMER" in n,
    "safe-action-gate": lambda n: "SAFE-ACTION" in n and "GATE" in n and "CONSUMER" in n,
    "ecosystem-meta-coherence": lambda n: "ECOSYSTEM-META-COHERENCE" in n and "CONSUMER" in n,
    "ecosystem-meta-coherence-gate": lambda n: "ECOSYSTEM-META-COHERENCE-GATE" in n and "CONSUMER" in n,
    "design-ops-loop": lambda n: "DESIGN-OPS-LOOP" in n and "CONSUMER" in n,
    "session-boot-design": lambda n: "SESSION-BOOT" in n and "CONSUMER" in n,
    "artifact-layers-design": lambda n: "ARTIFACT-LAYERS" in n and "CONSUMER" in n,
    "meta-design-self-healing": lambda n: "META-DESIGN-SELF-HEALING" in n and "CONSUMER" in n,
    "talex-friction-analyzer": lambda n: "TALEX-FRICTION-ANALYZER" in n and "CONSUMER" in n,
}


def check_implementation_validity(path: Path) -> dict:
    result = {"valid": False, "size": 0, "has_code": False, "is_stub": True, "error": None}
    try:
        content = path.read_text(encoding="utf-8", errors="ignore")
        result["size"] = len(content)
        result["has_code"] = bool(content.strip())
        # Un stub a typiquement < 200 caractères et contient "TODO" ou "stub"
        if result["has_code"] and result["size"] > 200:
            result["is_stub"] = False
            result["valid"] = True
        elif result["has_code"] and ("TODO" in content or "stub" in content.lower()):
            result["is_stub"] = True
            result["valid"] = False
        else:
            result["valid"] = result["has_code"]
    except Exception as e:
        result["error"] = str(e)
    return result


def audit_consumer(consumer: str) -> dict:
    result = {
        "consumer": consumer,
        "total_designs": len(DESIGNS),
        "prd_moc_count": 0,
        "impl_count": 0,
        "valid_impl_count": 0,
        "stub_count": 0,
        "missing_count": 0,
        "designs": [],
    }

    root = CONSUMERS.get(consumer)
    if not root or not root.exists():
        result["missing_count"] = len(DESIGNS)
        return result

    for design in DESIGNS:
        impl_file = IMPL_FILES[design]
        matcher = DESIGN_PRD_MATCHERS.get(design, lambda n: False)

        # Chercher implémentation
        impl_matches = list(root.glob(f"**/{impl_file}"))
        impl_found = bool(impl_matches)
        impl_valid = False
        impl_is_stub = True
        impl_path = str(impl_matches[0]) if impl_matches else None

        if impl_found:
            validity = check_implementation_validity(impl_matches[0])
            impl_valid = validity["valid"]
            impl_is_stub = validity["is_stub"]

        # Chercher PRD-MOC
        prd_moc_found = False
        prd_moc_path = None
        for scan_dir in SCAN_DIRS.get(consumer, []):
            if not scan_dir.exists():
                continue
            for candidate in scan_dir.glob("*.md"):
                if matcher(candidate.name):
                    prd_moc_found = True
                    prd_moc_path = str(candidate)
                    break
            if prd_moc_found:
                break

        design_status = {
            "design": design,
            "prd_moc_found": prd_moc_found,
            "prd_moc_path": prd_moc_path,
            "impl_found": impl_found,
            "impl_path": impl_path,
            "impl_valid": impl_valid,
            "impl_is_stub": impl_is_stub,
            "status": "MISSING",
        }

        if prd_moc_found and impl_found and impl_valid and not impl_is_stub:
            design_status["status"] = "FULLY_IMPLEMENTED"
        elif prd_moc_found and impl_found:
            if impl_is_stub:
                design_status["status"] = "STUB_IMPL"
            else:
                design_status["status"] = "PARTIAL_IMPL"
        elif prd_moc_found:
            design_status["status"] = "PRD_MOC_ONLY"
        else:
            design_status["status"] = "MISSING"

        result["designs"].append(design_status)
        if prd_moc_found:
            result["prd_moc_count"] += 1
        if impl_found:
            result["impl_count"] += 1
        if impl_valid and not impl_is_stub:
            result["valid_impl_count"] += 1
        if impl_is_stub:
            result["stub_count"] += 1
        if design_status["status"] == "MISSING":
            result["missing_count"] += 1

    return result


def audit_all() -> dict:
    results = []
    for consumer in CONSUMERS.keys():
        result = audit_consumer(consumer)
        results.append(result)

    total_designs = sum(r["total_designs"] for r in results)
    total_prd_mocs = sum(r["prd_moc_count"] for r in results)
    total_impls = sum(r["impl_count"] for r in results)
    total_valid = sum(r["valid_impl_count"] for r in results)
    total_stubs = sum(r["stub_count"] for r in results)
    total_missing = sum(r["missing_count"] for r in results)

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total_consumers": len(results),
        "total_designs": total_designs,
        "total_prd_mocs": total_prd_mocs,
        "total_impls": total_impls,
        "total_valid_impls": total_valid,
        "total_stubs": total_stubs,
        "total_missing": total_missing,
        "coverage_pct": round(total_prd_mocs / total_designs * 100, 2) if total_designs > 0 else 0,
        "valid_impl_pct": round(total_valid / total_designs * 100, 2) if total_designs > 0 else 0,
        "stub_pct": round(total_stubs / total_designs * 100, 2) if total_designs > 0 else 0,
        "target": "100%",
        "consumers": results,
    }

    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print("[ACT-028] Audit PRD-MOC:")
    print(f"  Consumers: {len(results)}")
    print(f"  Total designs: {total_designs}")
    print(f"  PRD-MOC présents: {total_prd_mocs} ({report['coverage_pct']}%)")
    print(f"  Implémentations: {total_impls}")
    print(f"  Implémentations valides: {total_valid} ({report['valid_impl_pct']}%)")
    print(f"  Stubs: {total_stubs} ({report['stub_pct']}%)")
    print(f"  Missing: {total_missing}")
    print(f"  Target: 100%")
    print(f"  Rapport: {REPORT_PATH}")

    return report


if __name__ == "__main__":
    audit_all()
