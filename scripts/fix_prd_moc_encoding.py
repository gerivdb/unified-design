#!/usr/bin/env python3
"""
Fix encoding issues in PRD-MOC files for consumer repos.

Replaces non-ASCII characters with ASCII equivalents to satisfy
pre-commit encoding checks.

Usage:
    python fix_prd_moc_encoding.py --consumer KIVA-CLI
    python fix_prd_moc_encoding.py --all
"""

import argparse
import sys
from pathlib import Path

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

# Character replacements: non-ASCII -> ASCII
ENCODING_FIXES = {
    "\u0153": "oe",  # œ -> oe
    "\u2502": "|",  # │ -> |
    "\u2500": "-",  # ─ -> -
    "\u251c": "|-",  # ├ -> |-
    "\u2514": "`-",  # └ -> `-
    "\u2193": "v",  # ↓ -> v
    "\u2014": "--",  # — -> --
    "\u2022": "-",  # • -> -
    "\u2192": "->",  # → -> ->
    "\u21d2": "=>",  # ⇒ -> =>
    "\u2264": "<=",  # ≤ -> <=
    "\u2265": ">=",  # ≥ -> >=
    "\u2248": "~=",  # ≈ -> ~=
    "\u00e9": "e",  # é -> e
    "\u00e8": "e",  # è -> e
    "\u00ea": "e",  # ê -> e
    "\u00f9": "u",  # ù -> u
    "\u00f4": "o",  # ô -> o
}


def fix_encoding(content: str) -> tuple[str, int]:
    """Fix encoding issues in content. Returns (fixed_content, changes_count)."""
    changes = 0
    for old_char, new_char in ENCODING_FIXES.items():
        count = content.count(old_char)
        if count > 0:
            content = content.replace(old_char, new_char)
            changes += count
    return content, changes


def fix_prd_mocs_for_consumer(consumer: str, dry_run: bool = True) -> dict:
    """Fix encoding in all PRD-MOC files for a consumer."""
    consumer_path = CONSUMER_MAP.get(consumer)
    if not consumer_path:
        return {"consumer": consumer, "status": "error", "reason": "Consumer not found"}
    
    # Find all PRD-MOC files in both PRD/ and PRD-MOC/ directories
    prd_mocs = []
    for prd_dir in ["PRD", "PRD-MOC"]:
        prd_path = consumer_path / prd_dir
        if prd_path.exists():
            prd_mocs.extend(prd_path.glob("PRD-MOC-*.md"))
    
    if not prd_mocs:
        return {"consumer": consumer, "status": "skipped", "reason": "no_prd_mocs"}
    
    results = {
        "consumer": consumer,
        "files_checked": len(prd_mocs),
        "files_fixed": 0,
        "total_changes": 0,
        "details": [],
    }
    
    for prd_moc in prd_mocs:
        content = prd_moc.read_text(encoding="utf-8")
        fixed_content, changes = fix_encoding(content)
        
        if changes > 0:
            results["files_fixed"] += 1
            results["total_changes"] += changes
            results["details"].append({
                "file": prd_moc.name,
                "changes": changes,
            })
            
            if not dry_run:
                prd_moc.write_text(fixed_content, encoding="utf-8")
    
    return results


def main():
    parser = argparse.ArgumentParser(description="Fix encoding issues in PRD-MOC files")
    parser.add_argument("--dry-run", action="store_true", help="Simulate without applying changes")
    parser.add_argument("--apply", action="store_true", help="Apply fixes")
    parser.add_argument("--consumer", help="Fix specific consumer")
    parser.add_argument("--all", action="store_true", help="Fix all consumers")
    parser.add_argument("--json-out", help="Output JSON report path")
    args = parser.parse_args()

    if not args.dry_run and not args.apply:
        parser.print_help()
        sys.exit(1)
    
    if not args.consumer and not args.all:
        print("Error: Must specify --consumer <name> or --all")
        sys.exit(1)

    dry_run = not args.apply
    
    consumers = [args.consumer] if args.consumer else list(CONSUMER_MAP.keys())
    
    all_results = []
    for consumer in consumers:
        result = fix_prd_mocs_for_consumer(consumer, dry_run=dry_run)
        all_results.append(result)
    
    # Summary
    total_files = sum(r["files_checked"] for r in all_results)
    total_fixed = sum(r["files_fixed"] for r in all_results)
    total_changes = sum(r["total_changes"] for r in all_results)
    
    mode = "DRY-RUN" if dry_run else "APPLY"
    print(f"\n=== Fix PRD-MOC Encoding ({mode}) ===")
    print(f"Files checked: {total_files}")
    print(f"Files fixed: {total_fixed}")
    print(f"Total changes: {total_changes}")
    
    for result in all_results:
        if result["files_fixed"] > 0:
            print(f"\n{result['consumer']}: {result['files_fixed']} files, {result['total_changes']} changes")
            for detail in result["details"][:5]:
                print(f"  {detail['file']}: {detail['changes']} changes")
            if len(result["details"]) > 5:
                print(f"  ... and {len(result['details']) - 5} more files")
    
    if args.json_out:
        import json
        report_path = Path(args.json_out)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(all_results, indent=2), encoding="utf-8")
        print(f"\nReport saved to: {args.json_out}")
    
    sys.exit(0)


if __name__ == "__main__":
    main()
