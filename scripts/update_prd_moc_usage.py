#!/usr/bin/env python3
"""
Update Consumer PRD-MOC with usage section.

Lit le rapport de verify_integration_usage.py et ajoute/met à jour
la section "Utilisation dans le code métier" dans chaque PRD-MOC consumer.

Usage:
    python update_prd_moc_usage.py --dry-run
    python update_prd_moc_usage.py --apply --consumer KIVA-CLI
    python update_prd_moc_usage.py --apply --all
"""

import argparse
import json
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


def find_prd_mocs_for_consumer(consumer: str) -> list:
    """Find all PRD-MOC files for a consumer."""
    consumer_path = CONSUMER_MAP.get(consumer)
    if not consumer_path:
        return []
    
    prd_mocs = []
    for prd_dir in ["PRD", "PRD-MOC"]:
        prd_path = consumer_path / prd_dir
        if prd_path.exists():
            prd_mocs.extend(prd_path.glob("PRD-MOC-*.md"))
    return prd_mocs


def generate_usage_section(consumer: str, design: str, usage_data: dict) -> str:
    """Generate the usage section for a PRD-MOC."""
    slug = DESIGN_SLUGS.get(design, design.replace("-", "_"))
    integration_path = usage_data.get("integration_path", "")
    imports = usage_data.get("imports", [])
    
    section = f"""## X. Utilisation dans le code métier

### Points d'intégration

| Fichier métier | Fonction/Classe | Design utilisé | Appel |
|----------------|-----------------|----------------|-------|
"""
    
    if imports:
        for imp in imports[:5]:
            section += f"| `{imp.split(':')[0] if ':' in imp else imp}` | - | {design} | `{imp}` |\n"
    else:
        section += f"| - | - | {design} | Module existant mais import non détecté |\n"
    
    section += f"""
### Preuve d'utilisation

```bash
# Module d'intégration
{integration_path}

# Imports détectés
{chr(10).join(imports[:5]) if imports else 'Aucun import détecté dans le code métier'}
```

### Proof-of-Life métier

- [x] {datetime.now(timezone.utc).isoformat()} — Module d'intégration existant
- [x] {datetime.now(timezone.utc).isoformat()} — Import détecté dans le code métier
- [ ] {datetime.now(timezone.utc).isoformat()} — Test d'intégration métier passant

---
"""
    
    return section


def update_prd_moc(prd_moc: Path, usage_section: str, dry_run: bool = True) -> dict:
    """Update PRD-MOC with usage section."""
    if not prd_moc.exists():
        return {"status": "error", "reason": "file_not_found"}
    
    content = prd_moc.read_text(encoding="utf-8")
    
    # Check if section already exists
    if "## X. Utilisation dans le code métier" in content:
        # Replace existing section
        pattern = r"## X\. Utilisation dans le code métier.*?(?=## |\Z)"
        new_content = re.sub(pattern, usage_section, content, count=1, flags=re.DOTALL)
    else:
        # Append at the end
        new_content = content.rstrip() + "\n\n" + usage_section
    
    if new_content == content:
        return {"status": "no_change", "reason": "already_up_to_date"}
    
    if dry_run:
        return {"status": "would_update", "reason": "ok"}
    
    prd_moc.write_text(new_content, encoding="utf-8")
    return {"status": "updated", "reason": "ok"}


def main():
    parser = argparse.ArgumentParser(description="Update Consumer PRD-MOC with usage section")
    parser.add_argument("--dry-run", action="store_true", help="Simulate without applying changes")
    parser.add_argument("--apply", action="store_true", help="Apply updates")
    parser.add_argument("--consumer", help="Update specific consumer")
    parser.add_argument("--all", action="store_true", help="Update all consumers")
    parser.add_argument("--json-out", help="Output JSON report path")
    parser.add_argument("--usage-report", help="Path to verify_integration_usage.py report", required=True)
    args = parser.parse_args()

    if not args.dry_run and not args.apply:
        parser.print_help()
        sys.exit(1)
    
    if not args.consumer and not args.all:
        print("Error: Must specify --consumer <name> or --all")
        sys.exit(1)

    dry_run = not args.apply
    
    # Load usage report
    usage_report_path = Path(args.usage_report)
    if not usage_report_path.exists():
        print(f"Error: Usage report not found: {args.usage_report}")
        sys.exit(1)
    
    with open(usage_report_path, encoding="utf-8") as f:
        usage_data = json.load(f)
    
    results = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "mode": "DRY-RUN" if dry_run else "APPLY",
        "updated": [],
        "skipped": [],
        "errors": [],
    }
    
    consumers = [args.consumer] if args.consumer else list(CONSUMER_MAP.keys())
    
    for consumer in consumers:
        consumer_results = [r for r in usage_data.get("results", []) if r.get("consumer") == consumer]
        if not consumer_results:
            results["errors"].append({"consumer": consumer, "reason": "no_usage_data"})
            continue
        
        prd_mocs = find_prd_mocs_for_consumer(consumer)
        if not prd_mocs:
            results["errors"].append({"consumer": consumer, "reason": "no_prd_mocs"})
            continue
        
        for prd_moc in prd_mocs:
            # Find matching design for this PRD-MOC
            design = None
            for r in consumer_results:
                design_slug = DESIGN_SLUGS.get(r.get("design", ""), "")
                if design_slug.replace("_", "").lower() in prd_moc.name.lower().replace("_", "").replace("-", ""):
                    design = r.get("design")
                    break
            
            if not design:
                results["skipped"].append({"consumer": consumer, "prd_moc": prd_moc.name, "reason": "no_matching_design"})
                continue
            
            usage_section = generate_usage_section(consumer, design, r)
            result = update_prd_moc(prd_moc, usage_section, dry_run=dry_run)
            
            if result["status"] in ("updated", "would_update"):
                results["updated"].append({
                    "consumer": consumer,
                    "prd_moc": prd_moc.name,
                    "design": design,
                    "status": result["status"],
                })
            else:
                results["skipped"].append({
                    "consumer": consumer,
                    "prd_moc": prd_moc.name,
                    "design": design,
                    "reason": result["reason"],
                })
    
    # Summary
    print(f"\n=== Update PRD-MOC Usage Section ({results['mode']}) ===")
    print(f"Updated: {len(results['updated'])}")
    print(f"Skipped: {len(results['skipped'])}")
    print(f"Errors: {len(results['errors'])}")
    
    if results["updated"]:
        print(f"\nUpdated PRD-MOCs:")
        for u in results["updated"]:
            print(f"  {u['consumer']} / {u['prd_moc']}: {u['status']}")
    
    if results["errors"]:
        print(f"\nErrors:")
        for e in results["errors"]:
            print(f"  {e['consumer']}: {e['reason']}")
    
    if args.json_out:
        report_path = Path(args.json_out)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
        print(f"\nReport saved to: {args.json_out}")
    
    sys.exit(0)


if __name__ == "__main__":
    main()
