#!/usr/bin/env python3
"""gap_combleur — Detects and optionally fixes implementation gaps in unified-design.

Usage:
    python gap_combleur.py --dry-run designs/
    python gap_combleur.py --apply designs/
    python gap_combleur.py --report gaps-report.json

Exit codes:
    0 = no gaps or gaps fixed
    1 = gaps found (in --dry-run mode)
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
UNIFIED_DESIGN_ROOT = SCRIPT_DIR.parent.parent


def _rel(path: Path) -> str:
    try:
        return str(path.relative_to(UNIFIED_DESIGN_ROOT))
    except ValueError:
        return str(path)


def load_design(path: Path) -> dict:
    path = path.resolve()
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    if text.startswith("---"):
        parts = text.split("---", 2)
        yaml_text = parts[1] if len(parts) >= 3 and parts[1].strip() else text
    else:
        yaml_text = text
    import yaml
    return yaml.safe_load(yaml_text) or {}


def detect_gaps(design_path: Path) -> list[dict]:
    design = load_design(design_path)
    gaps = []
    
    # Check for missing implementation_contract
    contract = design.get("implementation_contract")
    if not contract:
        gaps.append({
            "type": "missing_contract",
            "design": design_path.parent.name,
            "path": _rel(design_path),
            "severity": "high",
            "description": "Design missing implementation_contract",
            "fix": "Add implementation_contract with repo, repo_root, and artifacts",
        })
        return gaps
    
    # Check artifacts
    repo_root = Path(contract.get("repo_root", ""))
    if not repo_root.exists():
        gaps.append({
            "type": "missing_repo_root",
            "design": design_path.parent.name,
            "path": _rel(design_path),
            "severity": "critical",
            "description": f"repo_root does not exist: {repo_root}",
            "fix": f"Create repo at {repo_root} or update repo_root path",
        })
        return gaps
    
    for artifact in contract.get("artifacts", []):
        artifact_path = repo_root / artifact.get("path", "")
        if not artifact_path.exists():
            gaps.append({
                "type": "missing_artifact",
                "design": design_path.parent.name,
                "path": _rel(design_path),
                "severity": "high",
                "description": f"Artifact not found: {artifact.get('path')}",
                "fix": f"Create {artifact.get('path')} in {repo_root}",
                "artifact": artifact.get("path"),
            })
        else:
            # Check must_contain patterns
            content = artifact_path.read_text(encoding="utf-8", errors="ignore")
            for pattern in artifact.get("must_contain", []):
                if pattern not in content:
                    gaps.append({
                        "type": "missing_pattern",
                        "design": design_path.parent.name,
                        "path": _rel(design_path),
                        "severity": "medium",
                        "description": f"Pattern '{pattern}' not found in {artifact.get('path')}",
                        "fix": f"Add '{pattern}' to {artifact.get('path')}",
                        "artifact": artifact.get("path"),
                        "pattern": pattern,
                    })
    
    return gaps


def main() -> int:
    parser = argparse.ArgumentParser(description="Detect and fix implementation gaps")
    parser.add_argument("--check", default="designs/", help="Designs directory")
    parser.add_argument("--dry-run", action="store_true", help="Report gaps without fixing")
    parser.add_argument("--apply", action="store_true", help="Apply automatic fixes")
    parser.add_argument("--report", help="Write JSON report to file")
    args = parser.parse_args()
    
    designs_dir = Path(args.check)
    if not designs_dir.exists():
        print(f"[FAIL] Designs directory not found: {designs_dir}", file=sys.stderr)
        return 1
    
    design_files = sorted(set(designs_dir.rglob("design.yaml")))
    if not design_files:
        print("[SKIP] No designs found", file=sys.stderr)
        return 0
    
    all_gaps = []
    for design_path in design_files:
        gaps = detect_gaps(design_path)
        all_gaps.extend(gaps)
    
    # Summary
    by_type = {}
    for gap in all_gaps:
        by_type[gap["type"]] = by_type.get(gap["type"], 0) + 1
    
    print(f"[GAP-COMBILEUR] {len(all_gaps)} gaps detected across {len(design_files)} designs")
    for gtype, count in sorted(by_type.items()):
        print(f"  {gtype}: {count}")
    
    if args.report:
        report_path = Path(args.report)
        report_path.write_text(json.dumps({
            "total_gaps": len(all_gaps),
            "by_type": by_type,
            "gaps": all_gaps,
        }, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"[REPORT] Written to {report_path}")
    
    if args.apply:
        print("[APPLY] Automatic fixes not yet implemented")
        return 1
    
    if all_gaps and args.dry_run:
        print("\n[DRY-RUN] Use --apply to fix automatically (when implemented)")
        return 1
    
    return 0 if not all_gaps else 1


if __name__ == "__main__":
    sys.exit(main())
