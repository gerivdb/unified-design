#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MDU Preflight — Vérification prérequis avant orchestration MDU.

Usage:
    python mdu_preflight.py --check-all
    python mdu_preflight.py --check repos
    python mdu_preflight.py --check credentials
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Literal

UNIFIED_DESIGN_ROOT = Path(r"D:\DO\WEB\TOOLS\L0-CANON\unified-design")
ECOS_CLI_ROOT = Path(r"D:\DO\WEB\TOOLS\L1-INFRA\ECOS-CLI")
ARGUS_ROOT = Path(r"D:\DO\WEB\TOOLS\L1-INFRA\ARGUS")


class MDUPreflight:
    """Vérifications prérequis pour l'orchestration MDU."""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.checks_passed = 0
        self.checks_total = 0
    
    def _check(self, name: str, condition: bool, error_msg: str = "", warn_msg: str = "") -> bool:
        self.checks_total += 1
        if condition:
            self.checks_passed += 1
            print(f"  [OK] {name}")
            return True
        else:
            if error_msg:
                self.errors.append(f"{name}: {error_msg}")
                print(f"  [ERROR] {name}: {error_msg}")
            elif warn_msg:
                self.warnings.append(f"{name}: {warn_msg}")
                print(f"  [WARN] {name}: {warn_msg}")
            else:
                self.errors.append(f"{name}: Check failed")
                print(f"  [ERROR] {name}: Check failed")
            return False
    
    def check_repos_exist(self) -> bool:
        """Vérifie que les repos principaux existent localement."""
        repos = [
            ("unified-design", UNIFIED_DESIGN_ROOT),
            ("ECOS-CLI", ECOS_CLI_ROOT),
            ("ARGUS", ARGUS_ROOT),
            ("RADX", Path(r"D:\DO\WEB\TOOLS\L3-CITIZENS\RADX")),
            ("ONTOLOGY", Path(r"D:\DO\WEB\ONTOLOGY")),
        ]
        
        all_ok = True
        for name, path in repos:
            ok = self._check(
                f"Repo {name}",
                path.exists() and (path / ".git").exists(),
                f"Repo {name} non trouvé ou pas un repo git: {path}"
            )
            all_ok = all_ok and ok
        return all_ok
    
    def check_git_clean(self) -> bool:
        """Vérifie que les repos principaux ont un working tree clean (sauf untracked)."""
        all_ok = True
        for name, path in [
            ("unified-design", UNIFIED_DESIGN_ROOT),
            ("ECOS-CLI", ECOS_CLI_ROOT),
            ("ARGUS", ARGUS_ROOT),
        ]:
            try:
                result = subprocess.run(
                    ["git", "status", "--porcelain"],
                    cwd=path, capture_output=True, text=True, timeout=10
                )
                if result.returncode == 0:
                    changes = [l for l in result.stdout.strip().split('\n') if l and not l.startswith('?')]
                    ok = self._check(
                        f"Git clean {name}",
                        len(changes) == 0,
                        f"Repo {name} a des changements non committés: {len(changes)} fichier(s)"
                    )
                    all_ok = all_ok and ok
                else:
                    self._check(f"Git status {name}", False, f"git status failed: {result.stderr}")
                    all_ok = False
            except Exception as e:
                self._check(f"Git status {name}", False, f"Exception: {e}")
                all_ok = False
        return all_ok
    
    def check_python_deps(self) -> bool:
        """Vérifie les dépendances Python requises."""
        required = [
            "yaml", "requests", "prometheus_client"
        ]
        all_ok = True
        for dep in required:
            try:
                __import__(dep.replace("-", "_"))
                self._check(f"Python dep {dep}", True)
            except ImportError:
                ok = self._check(f"Python dep {dep}", False, f"Module {dep} non installé")
                all_ok = all_ok and ok
        return all_ok
    
    def check_cli_tools(self) -> bool:
        """Vérifie les outils CLI requis."""
        tools = [
            ("python", "python --version"),
            ("git", "git --version"),
            ("gh", "gh --version"),
        ]
        all_ok = True
        for name, cmd in tools:
            try:
                result = subprocess.run(cmd.split(), capture_output=True, timeout=5)
                ok = self._check(f"CLI {name}", result.returncode == 0, f"{name} non disponible")
                all_ok = all_ok and ok
            except Exception as e:
                self._check(f"CLI {name}", False, f"Exception: {e}")
                all_ok = False
        return all_ok
    
    def check_credentials(self) -> bool:
        """Vérifie les credentials (GitHub token, etc.)."""
        all_ok = True
        
        # GitHub token
        gh_token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
        ok = self._check(
            "GitHub Token",
            bool(gh_token),
            "GITHUB_TOKEN ou GH_TOKEN non défini dans l'environnement",
            "GITHUB_TOKEN non défini (requis pour gh API)"
        )
        all_ok = all_ok and ok
        
        # gh auth status
        try:
            result = subprocess.run(["gh", "auth", "status"], capture_output=True, text=True, timeout=10)
            ok = self._check(
                "gh auth",
                result.returncode == 0,
                f"gh auth failed: {result.stderr}",
                "gh auth status non vérifié"
            )
            all_ok = all_ok and ok
        except Exception as e:
            self._check("gh auth", False, f"Exception: {e}")
            all_ok = False
        
        return all_ok
    
    def check_network(self) -> bool:
        """Vérifie la connectivité réseau basique."""
        all_ok = True
        endpoints = [
            ("GitHub API", "https://api.github.com"),
            ("GitHub", "https://github.com"),
        ]
        for name, url in endpoints:
            try:
                import urllib.request
                req = urllib.request.Request(url, method="HEAD")
                response = urllib.request.urlopen(req, timeout=5)
                ok = self._check(f"Network {name}", response.status == 200, f"{name} inaccessible")
                all_ok = all_ok and ok
            except Exception as e:
                self._check(f"Network {name}", False, f"Exception: {e}")
                all_ok = False
        return all_ok
    
    def check_mdu_configs(self) -> bool:
        """Vérifie les configs MDU essentielles."""
        configs = [
            ("mdu-validation.yaml", UNIFIED_DESIGN_ROOT / "pipelines" / "mdu-validation.yaml"),
            ("compliance_scanner.py", UNIFIED_DESIGN_ROOT / "scripts" / "compliance_scanner.py"),
            ("design_coverage_scanner.py", UNIFIED_DESIGN_ROOT / "scripts" / "design_coverage_scanner.py"),
            ("mdu-compliance-scanner config", ECOS_CLI_ROOT / "citizens" / "mdu-compliance-scanner" / "config.yaml"),
        ]
        all_ok = True
        for name, path in configs:
            ok = self._check(
                f"Config {name}",
                path.exists(),
                f"Config manquante: {path}"
            )
            all_ok = all_ok and ok
        return all_ok
    
    def run_all(self) -> dict:
        """Exécute tous les checks."""
        print("[PREFLIGHT] Starting MDU Orchestration Preflight Checks")
        print("=" * 60)
        
        checks = [
            ("CLI Tools", self.check_cli_tools),
            ("Python Dependencies", self.check_python_deps),
            ("Network Connectivity", self.check_network),
            ("Credentials", self.check_credentials),
            ("Repositories Exist", self.check_repos_exist),
            ("Git Clean", self.check_git_clean),
            ("MDU Configs", self.check_mdu_configs),
        ]
        
        for name, check_fn in checks:
            print(f"\n[PREFLIGHT] {name}:")
            check_fn()
        
        print("\n" + "=" * 60)
        print(f"[PREFLIGHT] Results: {self.checks_passed}/{self.checks_total} checks passed")
        
        if self.warnings:
            print(f"[PREFLIGHT] Warnings ({len(self.warnings)}):")
            for w in self.warnings:
                print(f"  - {w}")
        
        if self.errors:
            print(f"[PREFLIGHT] Errors ({len(self.errors)}):")
            for e in self.errors:
                print(f"  - {e}")
        
        success = len(self.errors) == 0
        print(f"[PREFLIGHT] Overall: {'PASS' if success else 'FAIL'}")
        
        return {
            "success": success,
            "checks_passed": self.checks_passed,
            "checks_total": self.checks_total,
            "warnings": self.warnings,
            "errors": self.errors,
        }


def main():
    parser = argparse.ArgumentParser(description="MDU Orchestration Preflight")
    parser.add_argument("--check", choices=["all", "repos", "credentials", "network", "configs"], 
                        default="all", help="Specific check to run")
    parser.add_argument("--report-json", type=Path, help="Output JSON report")
    args = parser.parse_args()
    
    preflight = MDUPreflight()
    
    if args.check == "all":
        result = preflight.run_all()
    elif args.check == "repos":
        preflight.check_repos_exist()
        result = {"success": len(preflight.errors) == 0, "errors": preflight.errors}
    elif args.check == "credentials":
        preflight.check_credentials()
        result = {"success": len(preflight.errors) == 0, "errors": preflight.errors}
    elif args.check == "network":
        preflight.check_network()
        result = {"success": len(preflight.errors) == 0, "errors": preflight.errors}
    elif args.check == "configs":
        preflight.check_mdu_configs()
        result = {"success": len(preflight.errors) == 0, "errors": preflight.errors}
    else:
        result = preflight.run_all()
    
    if args.report_json:
        args.report_json.parent.mkdir(parents=True, exist_ok=True)
        args.report_json.write_text(json.dumps(result, indent=2, ensure_ascii=False))
        print(f"[INFO] Report written to {args.report_json}")
    
    return 0 if result["success"] else 1


if __name__ == "__main__":
    sys.exit(main())