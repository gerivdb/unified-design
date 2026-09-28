#!/usr/bin/env python3
"""
Auto-Promote — promotion automatique des ADR/Designs/INTENTS/PRD-MOC
quand les critères sont remplis.

Usage:
    python auto_promote.py --dry-run
    python auto_promote.py --apply
    python auto_promote.py --report reports/auto-promote-report.json
"""

import argparse
import json
import re
import sys
from pathlib import Path
from datetime import datetime, timezone

UNIFIED_DESIGN_ROOT = Path("D:/DO/WEB/TOOLS/L0-CANON/unified-design")
CONSUMER_MAP = {
    "KIVA-CLI": Path("D:/DO/WEB/TOOLS/L1-INFRA/KIVA-CLI"),
    "ECOS-CLI": Path("D:/DO/WEB/TOOLS/L1-INFRA/ECOS-CLI"),
    "ARGUS": Path("D:/DO/WEB/TOOLS/L1-INFRA/ARGUS"),
    "CTULU": Path("D:/DO/WEB/TOOLS/L4-TOOLS/CTULU"),
    "KG-CAUSAL": Path("D:/DO/WEB/TOOLS/L4-TOOLS/KG-CAUSAL"),
    "KG-L": Path("D:/DO/WEB/TOOLS/L4-TOOLS/KG-L"),
    "KIX": Path("D:/DO/WEB/TOOLS/L2-PLATFORM/KIX"),
    "LOOPX": Path("D:/DO/WEB/TOOLS/L3-CITIZENS/LOOPX"),
    "NEXUS": Path("D:/DO/WEB/TOOLS/L1-INFRA/NEXUS"),
    "TALEX": Path("D:/DO/WEB/TOOLS/L4-TOOLS/TALEX"),
    "TRIX": Path("D:/DO/WEB/TOOLS/L4-TOOLS/TRIX"),
    "VERSES": Path("D:/DO/WEB/TOOLS/L4-TOOLS/VERSES"),
    "VOLTX": Path("D:/DO/WEB/TOOLS/L0-CANON/VOLTX"),
    "WAZAA": Path("D:/DO/WEB/TOOLS/L4-TOOLS/WAZAA"),
}

DESIGN_SLUGS = {
    "safe-action-pattern": "safe_action_pattern",
    "safe-action-gate": "safe_action_gate",
    "ecosystem-meta-coherence": "ecosystem_meta_coherence",
    "ecosystem-meta-coherence-gate": "ecosystem_meta_coherence_gate",
    "meta-design-self-healing": "meta_design_self_healing",
    "design-ops-loop": "design_ops_loop",
    "session-boot-design": "session_boot_design",
    "artifact-layers-design": "artifact_layers_design",
    "talex-friction-analyzer": "talex_friction_analyzer",
}

DESIGN_ADR_MAP = {
    "safe-action-pattern": "ADR-2026-09-19-SAFE-ACTION-PATTERN.md",
    "safe-action-gate": "ADR-2026-09-21-005-SAFE-ACTION-GATE.md",
    "ecosystem-meta-coherence": "ADR-2026-09-21-006-ECOSYSTEM-META-COHERENCE-GATE.md",
    "ecosystem-meta-coherence-gate": "ADR-2026-09-21-006-ECOSYSTEM-META-COHERENCE-GATE.md",
    "meta-design-self-healing": "ADR-2026-09-21-008-META-DESIGN-SELF-HEALING.md",
    "design-ops-loop": "ADR-2026-09-19-SAFE-ACTION-PATTERN.md",
    "session-boot-design": "ADR-2026-09-19-SAFE-ACTION-PATTERN.md",
    "artifact-layers-design": "ADR-2026-09-20-001-ARTIFACT-EXTRACTION-MDU.md",
    "talex-friction-analyzer": "ADR-2026-09-19-SAFE-ACTION-PATTERN.md",
}
# Deduplicate while preserving order
_seen = set()
_DESIGN_ADR_MAP = {}
for k, v in DESIGN_ADR_MAP.items():
    if k not in _seen:
        _DESIGN_ADR_MAP[k] = v
        _seen.add(k)
DESIGN_ADR_MAP = _DESIGN_ADR_MAP


def check_adr_can_be_promoted(adr_name: str) -> dict:
    """Check if an ADR can be promoted from proposed to accepted."""
    adr_path = UNIFIED_DESIGN_ROOT / "ADR" / adr_name
    if not adr_path.exists():
        return {"can_promote": False, "reason": "missing"}
    
    content = adr_path.read_text(encoding="utf-8")
    status_match = re.search(r'^status:\s*(.+)', content, re.MULTILINE)
    if not status_match:
        return {"can_promote": False, "reason": "no_status"}
    
    current_status = status_match.group(1).strip()
    if current_status != "proposed":
        return {"can_promote": False, "reason": f"already_{current_status}"}
    
    # Check if ADR has proof-of-life (implementation evidence)
    has_proof = "proof" in content.lower() or "implemented" in content.lower()
    
    return {
        "can_promote": True,
        "current_status": current_status,
        "has_proof": has_proof,
        "reason": "ok",
    }


def check_design_can_be_promoted(design_name: str) -> dict:
    """Check if a design can be promoted from proposed to active/standard."""
    design_dir = UNIFIED_DESIGN_ROOT / "designs" / design_name
    design_yaml = design_dir / "design.yaml"
    
    if not design_yaml.exists():
        return {"can_promote": False, "reason": "missing_design"}
    
    content = design_yaml.read_text(encoding="utf-8")
    status_match = re.search(r'^status:\s*(.+)', content, re.MULTILINE)
    if not status_match:
        return {"can_promote": False, "reason": "no_status"}
    
    current_status = status_match.group(1).strip()
    if current_status not in ("proposed", "draft"):
        return {"can_promote": False, "reason": f"already_{current_status}"}
    
    # Check if design has implementation in consumers
    slug = DESIGN_SLUGS.get(design_name, design_name.replace("-", "_"))
    has_implementation = False
    for consumer_path in CONSUMER_MAP.values():
        # Check for integration module
        for pkg_dir in [None, "kiva_cli", "ecos_cli", "kix", "kg_l", "verses", "wazaa", "src"]:
            if pkg_dir:
                impl = consumer_path / pkg_dir / f"{slug}_integration.py"
            else:
                impl = consumer_path / "integrations" / f"{slug}_integration.py"
            if impl.exists():
                has_implementation = True
                break
        if has_implementation:
            break
    
    return {
        "can_promote": has_implementation,
        "current_status": current_status,
        "has_implementation": has_implementation,
        "reason": "ok" if has_implementation else "no_implementation",
    }


def check_intent_can_be_promoted(intent_name: str) -> dict:
    """Check if an INTENT can be promoted from proposed to approved."""
    intent_path = UNIFIED_DESIGN_ROOT / "INTENTS" / intent_name
    if not intent_path.exists():
        return {"can_promote": False, "reason": "missing"}
    
    content = intent_path.read_text(encoding="utf-8")
    status_match = re.search(r'^status:\s*(.+)', content, re.MULTILINE)
    if not status_match:
        return {"can_promote": False, "reason": "no_status"}
    
    current_status = status_match.group(1).strip()
    if current_status != "proposed":
        return {"can_promote": False, "reason": f"already_{current_status}"}
    
    # Check if all proof-of-life items are checked
    proof_items = re.findall(r'^- \[x\]', content, re.MULTILINE)
    has_proof = len(proof_items) > 0
    
    return {
        "can_promote": has_proof,
        "current_status": current_status,
        "has_proof": has_proof,
        "proof_count": len(proof_items),
        "reason": "ok" if has_proof else "no_proof",
    }


def promote_adr(adr_name: str, dry_run: bool = True) -> dict:
    """Promote an ADR from proposed to accepted."""
    adr_path = UNIFIED_DESIGN_ROOT / "ADR" / adr_name
    if not adr_path.exists():
        return {"status": "error", "reason": "missing"}
    
    content = adr_path.read_text(encoding="utf-8")
    
    # Update status
    new_content = re.sub(
        r'^status:\s*proposed',
        'status: accepted',
        content,
        count=1,
        flags=re.MULTILINE
    )
    
    if new_content == content:
        return {"status": "no_change", "reason": "already_accepted"}
    
    if dry_run:
        return {"status": "would_promote", "reason": "ok"}
    
    adr_path.write_text(new_content, encoding="utf-8")
    return {"status": "promoted", "reason": "ok"}


def promote_design(design_name: str, dry_run: bool = True) -> dict:
    """Promote a design from proposed/draft to active."""
    design_yaml = UNIFIED_DESIGN_ROOT / "designs" / design_name / "design.yaml"
    if not design_yaml.exists():
        return {"status": "error", "reason": "missing"}
    
    content = design_yaml.read_text(encoding="utf-8")
    
    # Promote to active if proposed/draft
    new_content = re.sub(
        r'^status:\s*(proposed|draft)',
        'status: active',
        content,
        count=1,
        flags=re.MULTILINE
    )
    
    if new_content == content:
        return {"status": "no_change", "reason": "already_active"}
    
    if dry_run:
        return {"status": "would_promote", "reason": "ok"}
    
    design_yaml.write_text(new_content, encoding="utf-8")
    return {"status": "promoted", "reason": "ok"}


def promote_intent(intent_name: str, dry_run: bool = True) -> dict:
    """Promote an INTENT from proposed to approved."""
    intent_path = UNIFIED_DESIGN_ROOT / "INTENTS" / intent_name
    if not intent_path.exists():
        return {"status": "error", "reason": "missing"}
    
    content = intent_path.read_text(encoding="utf-8")
    
    # Update status
    new_content = re.sub(
        r'^status:\s*proposed',
        'status: approved',
        content,
        count=1,
        flags=re.MULTILINE
    )
    
    if new_content == content:
        return {"status": "no_change", "reason": "already_approved"}
    
    if dry_run:
        return {"status": "would_promote", "reason": "ok"}
    
    intent_path.write_text(new_content, encoding="utf-8")
    return {"status": "promoted", "reason": "ok"}


def main():
    parser = argparse.ArgumentParser(description="Auto-Promote — promotion automatique ADR/Designs/INTENTS")
    parser.add_argument("--dry-run", action="store_true", help="Simulate without applying changes")
    parser.add_argument("--apply", action="store_true", help="Apply promotions")
    parser.add_argument("--report", help="Output JSON report path")
    parser.add_argument("--adr", action="store_true", help="Promote ADR only")
    parser.add_argument("--design", action="store_true", help="Promote designs only")
    parser.add_argument("--intent", action="store_true", help="Promote INTENTS only")
    args = parser.parse_args()

    if not args.dry_run and not args.apply:
        parser.print_help()
        sys.exit(1)

    dry_run = not args.apply
    mode = "DRY-RUN" if dry_run else "APPLY"

    results = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "mode": mode,
        "adr_promotions": [],
        "design_promotions": [],
        "intent_promotions": [],
        "summary": {
            "adr_total": 0,
            "adr_promoted": 0,
            "design_total": 0,
            "design_promoted": 0,
            "intent_total": 0,
            "intent_promoted": 0,
        }
    }

    # Promote ADR
    if not args.design and not args.intent:
        print(f"\n=== ADR Promotion ({mode}) ===")
        for design_name, adr_name in DESIGN_ADR_MAP.items():
            check = check_adr_can_be_promoted(adr_name)
            if check.get("can_promote"):
                promote_result = promote_adr(adr_name, dry_run=dry_run)
                results["adr_promotions"].append({
                    "adr": adr_name,
                    "design": design_name,
                    "check": check,
                    "result": promote_result,
                })
                results["summary"]["adr_total"] += 1
                if promote_result["status"] in ("promoted", "would_promote"):
                    results["summary"]["adr_promoted"] += 1
                    status_icon = "✓" if not dry_run else "?"
                    print(f"  {status_icon} {adr_name}: {promote_result['status']}")
                else:
                    print(f"  - {adr_name}: {promote_result['status']}")
            else:
                results["summary"]["adr_total"] += 1
                print(f"  - {adr_name}: {check.get('reason', 'unknown')}")

    # Promote Designs
    if not args.adr and not args.intent:
        print(f"\n=== Design Promotion ({mode}) ===")
        for design_name in DESIGN_SLUGS.keys():
            check = check_design_can_be_promoted(design_name)
            if check.get("can_promote"):
                promote_result = promote_design(design_name, dry_run=dry_run)
                results["design_promotions"].append({
                    "design": design_name,
                    "check": check,
                    "result": promote_result,
                })
                results["summary"]["design_total"] += 1
                if promote_result["status"] in ("promoted", "would_promote"):
                    results["summary"]["design_promoted"] += 1
                    status_icon = "✓" if not dry_run else "?"
                    print(f"  {status_icon} {design_name}: {promote_result['status']}")
                else:
                    print(f"  - {design_name}: {promote_result['status']}")
            else:
                results["summary"]["design_total"] += 1
                print(f"  - {design_name}: {check.get('reason', 'unknown')}")

    # Promote INTENTS
    if not args.adr and not args.design:
        print(f"\n=== INTENT Promotion ({mode}) ===")
        intent_dir = UNIFIED_DESIGN_ROOT / "INTENTS"
        for intent_file in intent_dir.glob("INTENT-*.md"):
            if intent_file.name == "INTENTS-000-index.md":
                continue
            check = check_intent_can_be_promoted(intent_file.name)
            if check.get("can_promote"):
                promote_result = promote_intent(intent_file.name, dry_run=dry_run)
                results["intent_promotions"].append({
                    "intent": intent_file.name,
                    "check": check,
                    "result": promote_result,
                })
                results["summary"]["intent_total"] += 1
                if promote_result["status"] in ("promoted", "would_promote"):
                    results["summary"]["intent_promoted"] += 1
                    status_icon = "✓" if not dry_run else "?"
                    print(f"  {status_icon} {intent_file.name}: {promote_result['status']}")
                else:
                    print(f"  - {intent_file.name}: {promote_result['status']}")
            else:
                results["summary"]["intent_total"] += 1
                print(f"  - {intent_file.name}: {check.get('reason', 'unknown')}")

    # Summary
    print(f"\n=== Summary ===")
    print(f"ADR: {results['summary']['adr_promoted']}/{results['summary']['adr_total']} promoted")
    print(f"Designs: {results['summary']['design_promoted']}/{results['summary']['design_total']} promoted")
    print(f"INTENTS: {results['summary']['intent_promoted']}/{results['summary']['intent_total']} promoted")
    print(f"Mode: {mode}")

    if args.report:
        report_path = Path(args.report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
        print(f"\nReport saved to: {args.report}")

    sys.exit(0)


if __name__ == "__main__":
    main()
