#!/usr/bin/env python3
"""
talex_friction_analyzer.py — Analyse des frictions TALEX pour unified-design.

Scanne REPORTS/REPORT-TALEX-FRICTION-*.md, extrait les frictions,
classifie par impact, et génère un rapport d'analyse avec actions correctives.

Usage:
  python tools/talex_friction_analyzer.py --strict
  python tools/talex_friction_analyzer.py --output reports/talex-friction-analysis.md
"""

import argparse
import json
import re
import sys
from pathlib import Path
from datetime import datetime
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
REPORTS_DIR = REPO_ROOT / "REPORTS"
OUTPUT_DEFAULT = REPO_ROOT / "REPORTS" / "REPORT-TALEX-FRICTION-ANALYSIS.md"


def find_friction_reports() -> list[Path]:
    """Trouve tous les rapports de friction TALEX."""
    if not REPORTS_DIR.exists():
        return []
    return sorted(REPORTS_DIR.glob("REPORT-TALEX-FRICTION-*.md"))


def parse_friction_report(path: Path) -> list[dict[str, Any]]:
    """Parse un rapport de friction TALEX et extrait les frictions."""
    content = path.read_text(encoding="utf-8")
    frictions = []
    current_section = None

    for line in content.split("\n"):
        line = line.strip()
        if line.startswith("##"):
            current_section = line
        elif line.startswith("|") and "Erreur" not in line and "---" not in line:
            parts = [p.strip() for p in line.split("|") if p.strip()]
            if len(parts) >= 5:
                frictions.append({
                    "section": current_section,
                    "source": str(path.name),
                    "erreur": parts[0],
                    "frequence": parts[1],
                    "impact": parts[2],
                    "degradabilite": parts[3],
                    "cause_racine": parts[4],
                })
    return frictions


def classify_friction(friction: dict[str, Any]) -> str:
    """Classifie une friction par niveau d'impact."""
    impact = friction.get("impact", "").lower()
    if "élevé" in impact or "eleve" in impact:
        return "P0"
    elif "moyen" in impact:
        return "P1"
    else:
        return "P2"


def analyze_frictions(frictions: list[dict[str, Any]]) -> dict[str, Any]:
    """Analyse les frictions et génère un rapport structuré."""
    classified: dict[str, list[dict[str, Any]]] = {"P0": [], "P1": [], "P2": []}
    for friction in frictions:
        level = classify_friction(friction)
        classified[level].append(friction)

    return {
        "total": len(frictions),
        "by_level": {k: len(v) for k, v in classified.items()},
        "p0": classified["P0"],
        "p1": classified["P1"],
        "p2": classified["P2"],
        "generated_at": datetime.utcnow().isoformat() + "Z",
    }


def generate_report(analysis: dict[str, Any], output_path: Path) -> None:
    """Génère le rapport Markdown."""
    lines = [
        "# TALEX Friction Analysis",
        "",
        f"**Generated** : {analysis['generated_at']}",
        f"**Total frictions** : {analysis['total']}",
        "",
        "## Summary",
        "",
        f"| Level | Count |",
        f"|-------|-------|",
        f"| P0 | {analysis['by_level']['P0']} |",
        f"| P1 | {analysis['by_level']['P1']} |",
        f"| P2 | {analysis['by_level']['P2']} |",
        "",
    ]

    for level in ["P0", "P1", "P2"]:
        frictions = analysis[level.lower()]
        if not frictions:
            continue
        lines.append(f"## {level} Frictions")
        lines.append("")
        lines.append("| # | Erreur | Impact | Cause racine | Source |")
        lines.append("|---|--------|--------|--------------|--------|")
        for i, f in enumerate(frictions, 1):
            lines.append(f"| {i} | {f['erreur']} | {f['impact']} | {f['cause_racine']} | {f['source']} |")
        lines.append("")

    output_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="TALEX Friction Analyzer")
    parser.add_argument("--strict", action="store_true", help="Exit 1 if P0 frictions found")
    parser.add_argument("--output", type=Path, default=OUTPUT_DEFAULT, help="Output path")
    args = parser.parse_args()

    reports = find_friction_reports()
    if not reports:
        print("[TALEX] No friction reports found.")
        return 0

    all_frictions = []
    for report in reports:
        all_frictions.extend(parse_friction_report(report))

    analysis = analyze_frictions(all_frictions)
    generate_report(analysis, args.output)

    print(f"[TALEX] Analyzed {analysis['total']} frictions:")
    print(f"  P0: {analysis['by_level']['P0']}")
    print(f"  P1: {analysis['by_level']['P1']}")
    print(f"  P2: {analysis['by_level']['P2']}")
    print(f"[TALEX] Report: {args.output}")

    if args.strict and analysis["by_level"]["P0"] > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
