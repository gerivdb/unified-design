#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MDU Consolidated Report — Génère rapport Markdown consolidé de l'orchestration.

Usage:
    python mdu_consolidated_report.py --output /tmp/report.md
    python mdu_consolidated_report.py --output /tmp/report.md --include-details
"""

from __future__ import annotations

import argparse
import json
import sys
import glob
from datetime import datetime
from pathlib import Path
from typing: Optional

# Add project paths
UNIFIED_DESIGN_ROOT = Path(r"D:\DO\WEB\TOOLS\L0-CANON\unified-design")
REPORTS_DIR = UNIFIED_DESIGN_ROOT / "reports"
sys.path.insert(0, str(UNIFIED_DESIGN_ROOT / "scripts"))

try:
    from compliance_scanner import check_repo_compliance  # type: ignore
    from mdu_compliance_scanner import load_catalog_designs, discover_repos_from_catalog
except ImportError:
    check_repo_compliance = None
    load_catalog_designs = None
    discover_repos_from_catalog = None


class MDU_ConsolidatedReport:
    """Générateur de rapport consolidé MDU."""
    
    def __init__(self, include_details: bool = False):
        self.include_details = include_details
        self.timestamp = datetime.utcnow().isoformat() + "Z"
    
    def find_latest_reports(self) -> dict[str, Path]:
        """Trouve les derniers fichiers de rapport dans le répertoire reports."""
        reports = {}
        
        patterns = {
            "design_coverage": "mdu-compliance-*.json",
            "compliance_full": "mdu-compliance-full-*.json",
            "argus_drift": "argus-mdu-drift-*.json",
            "argus_full": "argus-full-*.json",
            "remediation_plan": "mdu-remediation-plan-*.json",
            "remediation_applied": "mdu-remediation-applied-*.json",
        }
        
        for key, pattern in patterns.items():
            files = list(REPORTS_DIR.glob(pattern))
            if files:
                # Prendre le plus récent
                latest = max(files, key=lambda f: f.stat().st_mtime)
                reports[key] = latest
        
        return reports
    
    def load_report(self, path: Path) -> dict | None:
        """Charge un rapport JSON."""
        try:
            with path.open("r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[REPORT] Error loading {path}: {e}")
            return None
    
    def generate_current_compliance(self) -> dict:
        """Génère un snapshot de conformité actuel."""
        if not (check_repo_compliance and load_catalog_designs and discover_repos_from_catalog):
            return {"error": "Scanner modules not available"}
        
        catalog_path = UNIFIED_DESIGN_ROOT / "catalog" / "designs.index.yaml"
        catalog_designs = load_catalog_designs(catalog_path)
        repos = discover_repos_from_catalog(catalog_designs)
        
        results = {}
        total = len(repos)
        compliant = 0
        gaps_by_type = {}
        
        for repo in repos:
            result = check_repo_compliance(repo)
            results[repo] = result
            if result.get("compliant", False):
                compliant += 1
            for gap in result.get("gaps", []):
                gaps_by_type[gap] = gaps_by_type.get(gap, 0) + 1
        
        return {
            "timestamp": self.timestamp,
            "total_repos": total,
            "compliant_repos": compliant,
            "non_compliant_repos": total - compliant,
            "compliance_rate": f"{(compliant/total*100):.1f}%" if total > 0 else "0%",
            "gaps_by_type": gaps_by_type,
            "results": results if self.include_details else {},
        }
    
    def generate_report(self) -> str:
        """Génère le rapport Markdown complet."""
        reports = self.find_latest_reports()
        current = self.generate_current_compliance()
        
        md = []
        md.append(f"# MDU Orchestration Consolidated Report")
        md.append(f"**Généré le**: {self.timestamp}")
        md.append(f"**Source**: unified-design/scripts/mdu_consolidated_report.py")
        md.append("")
        
        # Résumé exécutif
        md.append("## 📊 Résumé Exécutif")
        md.append("")
        
        if "error" not in current:
            md.append(f"- **Total Repos**: {current['total_repos']}")
            md.append(f"- **Conformes**: {current['compliant_repos']} ({current['compliance_rate']})")
            md.append(f"- **Non-conformes**: {current['non_compliant_repos']}")
            
            if current.get("gaps_by_type"):
                md.append("- **Gaps par type**:")
                for gap, count in sorted(current["gaps_by_type"].items()):
                    md.append(f"  - `{gap}`: {count}")
        else:
            md.append(f"- **Erreur**: {current['error']}")
        
        md.append("")
        
        # État des rapports trouvés
        md.append("## 📁 Rapports Disponibles")
        md.append("")
        md.append("| Rapport | Fichier | Taille | Modifié |")
        md.append("|---------|---------|--------|---------|")
        
        for key, path in reports.items():
            size = path.stat().st_size
            mtime = datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
            md.append(f"| {key} | `{path.name}` | {size} B | {mtime} |")
        
        md.append("")
        
        # Détail conformité actuelle
        if "error" not in current and self.include_details:
            md.append("## 🔍 Détail Conformité Actuelle")
            md.append("")
            md.append("| Repo | Conforme | Gaps |")
            md.append("|------|----------|------|")
            
            for repo, result in sorted(current.get("results", {}).items()):
                status = "✅" if result.get("compliant", False) else "❌"
                gaps = ", ".join(result.get("gaps", [])) or "—"
                md.append(f"| {repo} | {status} | {gaps} |")
            
            md.append("")
        
        # Rapports de compliance
        if "compliance_full" in reports:
            report = self.load_report(reports["compliance_full"])
            if report:
                md.append("## 📋 Compliance Scan (Full)")
                md.append("")
                self._append_compliance_details(md, report)
        
        # Rapports ARGUS
        if "argus_drift" in reports:
            report = self.load_report(reports["argus_drift"])
            if report:
                md.append("## 🛡️ ARGUS MDU Drift")
                md.append("")
                self._append_argus_details(md, report)
        
        if "argus_full" in reports:
            report = self.load_report(reports["argus_full"])
            if report:
                md.append("## 🛡️ ARGUS Full Scan")
                md.append("")
                self._append_argus_details(md, report)
        
        # Rapports Remédiation
        if "remediation_plan" in reports:
            report = self.load_report(reports["remediation_plan"])
            if report:
                md.append("## 🔧 Plan de Remédiation")
                md.append("")
                self._append_remediation_details(md, report)
        
        if "remediation_applied" in reports:
            report = self.load_report(reports["remediation_applied"])
            if report:
                md.append("## 🔧 Remédiation Appliquée")
                md.append("")
                self._append_remediation_details(md, report)
        
        # Footer
        md.append("")
        md.append("---")
        md.append(f"*Rapport généré automatiquement par MDU Orchestration le {self.timestamp}*")
        
        return "\n".join(md)
    
    def _append_compliance_details(self, md: list, report: dict):
        """Ajoute les détails du rapport compliance."""
        results = report.get("results", {})
        if not results:
            md.append("_Aucun détail disponible_")
            md.append("")
            return
        
        md.append("| Repo | Conforme | Gaps |")
        md.append("|------|----------|------|")
        
        for repo, result in sorted(results.items()):
            status = "✅" if result.get("compliant", False) else "❌"
            gaps = ", ".join(result.get("gaps", [])) or "—"
            md.append(f"| {repo} | {status} | {gaps} |")
        
        md.append("")
    
    def _append_argus_details(self, md: list, report: dict):
        """Ajoute les détails ARGUS."""
        # Format ARGUS variable, on affiche ce qu'on a
        if isinstance(report, dict):
            for key, value in report.items():
                if key not in ["timestamp", "session_id"]:
                    md.append(f"- **{key}**: {value}")
        md.append("")
    
    def _append_remediation_details(self, md: list, report: dict):
        """Ajoute les détails remédiation."""
        if isinstance(report, dict) and "results" in report:
            for repo, result in report.get("results", {}).items():
                md.append(f"### {repo}")
                md.append(f"- Status: {result.get('status', 'unknown')}")
                for action in result.get("actions", []):
                    md.append(f"  - {action}")
                for failed in result.get("failed", []):
                    md.append(f"  - ❌ ÉCHEC: {failed['action']} - {failed['error']}")
        md.append("")


def main():
    parser = argparse.ArgumentParser(description="MDU Consolidated Report Generator")
    parser.add_argument("--output", type=Path, required=True, help="Output Markdown file path")
    parser.add_argument("--include-details", action="store_true", help="Include per-repo details")
    args = parser.parse_args()
    
    generator = MDU_ConsolidatedReport(include_details=args.include_details)
    report = generator.generate_report()
    
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report, encoding="utf-8")
    
    print(f"[REPORT] Generated: {args.output}")
    print(f"[REPORT] Size: {len(report)} chars")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())