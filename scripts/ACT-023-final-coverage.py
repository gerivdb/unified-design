#!/usr/bin/env python3
"""
ACT-023: Validation finale avec chemins réels et déploiés.
"""

from pathlib import Path
from datetime import datetime, timezone
import json

UNIFIED_DESIGN_ROOT = Path("D:/DO/WEB/TOOLS/L0-CANON/unified-design")
REPORT_PATH = UNIFIED_DESIGN_ROOT / "ACT-023-final-coverage-report.json"

# Charger ACT-021 pour les implémentations déployées
ACT_021_REPORT = UNIFIED_DESIGN_ROOT / "ACT-021-deployment-report.json"
with open(ACT_021_REPORT, "r", encoding="utf-8") as f:
    act_021_data = json.load(f)

# Créer un mapping (design, consumer) -> chemin implémenté
deployed_impls = {}
for d in act_021_data["deployments"]:
    if d["status"] == "DEPLOYED":
        key = (d["design"], d["consumer"])
        deployed_impls[key] = Path(d["dest"])

# Chemins PRD-MOC attendus (basés sur les fichiers créés précédemment)
PRD_MOC_PATHS = {
    ("safe-action-pattern", "KIVA-CLI"): Path("D:/DO/WEB/TOOLS/L1-INFRA/KIVA-CLI/PRD/PRD-MOC-KIVA-SAFE-ACTION-PATTERN-CONSUMER-20260928.md"),
    ("safe-action-pattern", "ECOS-CLI"): Path("D:/DO/WEB/TOOLS/L1-INFRA/ECOS-CLI/PRD/PRD-MOC-ECOS-SAFE-ACTION-PATTERN-CONSUMER-20260928.md"),
    ("safe-action-pattern", "ARGUS"): Path("D:/DO/WEB/TOOLS/L1-INFRA/ARGUS/PRD/PRD-MOC-ARGUS-SAFE-ACTION-PATTERN-CONSUMER-20260928.md"),
    ("safe-action-pattern", "CTULU"): Path("D:/DO/WEB/TOOLS/L4-TOOLS/CTULU/PRD/PRD-MOC-CTULU-SAFE-ACTION-PATTERN-CONSUMER-20260928.md"),
    ("safe-action-pattern", "KG-CAUSAL"): Path("D:/DO/WEB/TOOLS/L4-TOOLS/KG-CAUSAL/PRD-MOC/PRD-MOC-KG-CAUSAL-SAFE-ACTION-PATTERN-CONSUMER-20260928.md"),
    ("safe-action-pattern", "VOLTX"): Path("D:/DO/WEB/TOOLS/L0-CANON/VOLTX/PRD-MOC/PRD-MOC-VOLTX-SAFE-ACTION-PATTERN-CONSUMER-20260928.md"),
    ("safe-action-pattern", "LOOPX"): Path("D:/DO/WEB/TOOLS/L3-CITIZENS/LOOPX/PRD/PRD-MOC-LOOPX-SAFE-ACTION-PATTERN-CONSUMER-20260928.md"),
    ("safe-action-pattern", "KIX"): Path("D:/DO/WEB/TOOLS/L2-PLATFORM/KIX/PRD-MOC/PRD-MOC-KIX-SAFE-ACTION-PATTERN-CONSUMER-20260928.md"),
    ("safe-action-pattern", "TALEX"): Path("D:/DO/WEB/TOOLS/L4-TOOLS/TALEX/PRD-MOC/PRD-MOC-TALEX-SAFE-ACTION-PATTERN-CONSUMER-20260928.md"),
    ("safe-action-pattern", "NEXUS"): Path("D:/DO/WEB/TOOLS/L1-INFRA/NEXUS/PRD-MOC/PRD-MOC-NEXUS-SAFE-ACTION-PATTERN-CONSUMER-20260928.md"),
    ("safe-action-pattern", "KG-L"): Path("D:/DO/WEB/TOOLS/L4-TOOLS/KG-L/PRD/PRD-MOC-KG-L-SAFE-ACTION-GATE-CONSUMER-20260928.md"),
    ("safe-action-pattern", "VERSES"): Path("D:/DO/WEB/TOOLS/L4-TOOLS/VERSES/PRD/PRD-MOC-VERSES-SAFE-ACTION-GATE-CONSUMER-20260928.md"),
    ("safe-action-pattern", "TRIX"): Path("D:/DO/WEB/TOOLS/L4-TOOLS/TRIX/PRD/PRD-MOC-TRIX-SAFE-ACTION-PATTERN-CONSUMER-20260928.md"),
    ("safe-action-pattern", "WAZAA"): Path("D:/DO/WEB/TOOLS/L4-TOOLS/WAZAA/PRD/PRD-MOC-WAZAA-SAFE-ACTION-GATE-CONSUMER-20260928.md"),
    ("safe-action-gate", "KIVA-CLI"): Path("D:/DO/WEB/TOOLS/L1-INFRA/KIVA-CLI/PRD/PRD-MOC-KIVA-SAFE-ACTION-GATE-CONSUMER-20260928.md"),
    ("safe-action-gate", "ECOS-CLI"): Path("D:/DO/WEB/TOOLS/L1-INFRA/ECOS-CLI/PRD/PRD-MOC-ECOS-SAFE-ACTION-GATE-CONSUMER-20260928.md"),
    ("safe-action-gate", "ARGUS"): Path("D:/DO/WEB/TOOLS/L1-INFRA/ARGUS/PRD/PRD-MOC-ARGUS-SAFE-ACTION-GATE-CONSUMER-20260928.md"),
    ("safe-action-gate", "CTULU"): Path("D:/DO/WEB/TOOLS/L4-TOOLS/CTULU/PRD/PRD-MOC-CTULU-SAFE-ACTION-GATE-CONSUMER-20260928.md"),
    ("safe-action-gate", "KG-CAUSAL"): Path("D:/DO/WEB/TOOLS/L4-TOOLS/KG-CAUSAL/PRD-MOC/PRD-MOC-KG-CAUSAL-SAFE-ACTION-GATE-CONSUMER-20260928.md"),
    ("safe-action-gate", "VOLTX"): Path("D:/DO/WEB/TOOLS/L0-CANON/VOLTX/PRD-MOC/PRD-MOC-VOLTX-SAFE-ACTION-GATE-CONSUMER-20260928.md"),
    ("safe-action-gate", "LOOPX"): Path("D:/DO/WEB/TOOLS/L3-CITIZENS/LOOPX/PRD/PRD-MOC-LOOPX-SAFE-ACTION-GATE-CONSUMER-20260928.md"),
    ("safe-action-gate", "KIX"): Path("D:/DO/WEB/TOOLS/L2-PLATFORM/KIX/PRD-MOC/PRD-MOC-KIX-SAFE-ACTION-GATE-CONSUMER-20260928.md"),
    ("safe-action-gate", "TALEX"): Path("D:/DO/WEB/TOOLS/L4-TOOLS/TALEX/PRD-MOC/PRD-MOC-TALEX-SAFE-ACTION-GATE-CONSUMER-20260928.md"),
    ("safe-action-gate", "NEXUS"): Path("D:/DO/WEB/TOOLS/L1-INFRA/NEXUS/PRD-MOC/PRD-MOC-NEXUS-SAFE-ACTION-GATE-CONSUMER-20260928.md"),
    ("safe-action-gate", "KG-L"): Path("D:/DO/WEB/TOOLS/L4-TOOLS/KG-L/PRD/PRD-MOC-KG-L-SAFE-ACTION-GATE-CONSUMER-20260928.md"),
    ("safe-action-gate", "VERSES"): Path("D:/DO/WEB/TOOLS/L4-TOOLS/VERSES/PRD/PRD-MOC-VERSES-SAFE-ACTION-GATE-CONSUMER-20260928.md"),
    ("safe-action-gate", "TRIX"): Path("D:/DO/WEB/TOOLS/L4-TOOLS/TRIX/PRD/PRD-MOC-TRIX-SAFE-ACTION-GATE-CONSUMER-20260928.md"),
    ("safe-action-gate", "WAZAA"): Path("D:/DO/WEB/TOOLS/L4-TOOLS/WAZAA/PRD/PRD-MOC-WAZAA-SAFE-ACTION-GATE-CONSUMER-20260928.md"),
}

# Ajouter les chemins pour les autres designs
OTHER_DESIGNS = {
    "ecosystem-meta-coherence": "ECOSYSTEM-META-COHERENCE",
    "ecosystem-meta-coherence-gate": "ECOSYSTEM-META-COHERENCE-GATE",
    "design-ops-loop": "DESIGN-OPS-LOOP",
    "session-boot-design": "SESSION-BOOT",
    "artifact-layers-design": "ARTIFACT-LAYERS",
    "meta-design-self-healing": "META-DESIGN-SELF-HEALING",
    "talex-friction-analyzer": "TALEX-FRICTION-ANALYZER",
}

CONSUMERS = ["KIVA-CLI", "ECOS-CLI", "ARGUS", "CTULU", "KG-CAUSAL", "VOLTX", "LOOPX", "KIX", "TALEX", "NEXUS", "KG-L", "VERSES", "TRIX", "WAZAA"]

for design, suffix in OTHER_DESIGNS.items():
    for consumer in CONSUMERS:
        # PRD-MOC path
        prd_path = Path(f"D:/DO/WEB/TOOLS/L4-TOOLS/{consumer}/PRD/PRD-MOC-{consumer}-{suffix}-CONSUMER-20260928.md")
        if not prd_path.exists():
            prd_path = Path(f"D:/DO/WEB/TOOLS/L4-TOOLS/{consumer}/PRD-MOC/PRD-MOC-{consumer}-{suffix}-CONSUMER-20260928.md")
        PRD_MOC_PATHS[(design, consumer)] = prd_path


def validate_all() -> dict:
    details = []
    for design, consumers in {
        "safe-action-pattern": CONSUMERS,
        "safe-action-gate": CONSUMERS,
        "ecosystem-meta-coherence": CONSUMERS,
        "ecosystem-meta-coherence-gate": CONSUMERS,
        "design-ops-loop": CONSUMERS,
        "session-boot-design": CONSUMERS,
        "artifact-layers-design": CONSUMERS,
        "meta-design-self-healing": CONSUMERS,
        "talex-friction-analyzer": CONSUMERS,
    }.items():
        for consumer in consumers:
            key = (design, consumer)
            result = {
                "design": design,
                "consumer": consumer,
                "prd_moc_found": False,
                "prd_moc_path": None,
                "implementation_found": False,
                "implementation_path": None,
                "status": "MISSING",
            }

            # Vérifier l'implémentation déployée
            impl_path = deployed_impls.get(key)
            if impl_path and impl_path.exists():
                result["implementation_found"] = True
                result["implementation_path"] = str(impl_path)

            # Vérifier le PRD-MOC
            prd_moc_path = PRD_MOC_PATHS.get(key)
            if prd_moc_path and prd_moc_path.exists():
                result["prd_moc_found"] = True
                result["prd_moc_path"] = str(prd_moc_path)

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

    print("[ACT-023] Validation finale:")
    print(f"  Total checks: {total}")
    print(f"  Implemented: {implemented} ({report['coverage_pct']}%)")
    print(f"  PRD-MOC only: {prd_moc_only}")
    print(f"  Missing: {missing}")
    print(f"  Rapport: {REPORT_PATH}")
    return report


if __name__ == "__main__":
    validate_all()
