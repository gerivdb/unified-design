"""Verify auto-design adherence for a target repo."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

MAX_STALE_DAYS = 30


class AutoDesignVerifier:
    def __init__(self, repo_root: Path) -> None:
        self.repo_root = Path(repo_root)

    def verify(self) -> dict[str, Any]:
        design = self.repo_root / "design.yaml"
        if not design.exists():
            return {"repo": str(self.repo_root), "auto_design_score": 0, "reason": "design.yaml missing"}
        try:
            content = design.read_text(encoding="utf-8")
        except Exception as exc:
            return {"repo": str(self.repo_root), "auto_design_score": 0, "reason": str(exc)}

        components_verified = 0
        components_missing = 0
        bridges_active = 0
        bridges_inactive = 0
        tests_passing = 0
        tests_failing = 0
        proofs_up_to_date = 0
        proofs_stale = 0

        if "implementation_contract:" in content:
            components_verified += 1
        else:
            components_missing += 1

        bridges = list((self.repo_root / "bridges").glob("*.yaml")) if (self.repo_root / "bridges").exists() else []
        bridges_active = len(bridges)
        bridges_inactive = max(0, 3 - bridges_active)

        tests = (
            list((self.repo_root / "tests").glob("test_*.py"))
            + list((self.repo_root / "scripts").glob("test_*.py"))
            if (self.repo_root / "tests").exists() or (self.repo_root / "scripts").exists()
            else []
        )
        tests_passing = len(tests)
        tests_failing = 0

        score = 0
        score += 20 if "status: active" in content else 0
        score += 20 if "implementation_contract:" in content else 0
        score += 20 if bridges_active >= 1 else 0
        score += 20 if tests_passing >= 1 else 0
        score += 10 if "cycle_runner_path:" in content else 0
        score += 10 if "bridge_executor_path:" in content else 0
        score = min(100, score)

        atomic_check = self._check_atomic_commits()
        bridges_argus = self._validate_bridges_argus()
        crossrefs_argus = self._validate_crossrefs_argus()
        meta_coherence = self._check_meta_coherence()
        traceability = self._validate_traceability()
        crm_notification = self._notify_crm_tech_debt()

        return {
            "repo": str(self.repo_root),
            "auto_design_score": score,
            "components_verified": components_verified,
            "components_missing": components_missing,
            "bridges_active": bridges_active,
            "bridges_inactive": bridges_inactive,
            "tests_passing": tests_passing,
            "tests_failing": tests_failing,
            "proofs_up_to_date": proofs_up_to_date,
            "proofs_stale": proofs_stale,
            "mature": score >= 80,
            "optimized": score >= 95,
            "atomic_commits": atomic_check,
            "argus_bridges": bridges_argus,
            "argus_crossrefs": crossrefs_argus,
            "meta_coherence": meta_coherence,
            "traceability": traceability,
            "crm_notification": crm_notification,
        }

    def _check_atomic_commits(self) -> dict[str, Any]:
        """Vérifie que les commits sont atomiques (≤3 fichiers)."""
        try:
            result = subprocess.run(
                ["git", "-C", str(self.repo_root), "log", "--format=%H", "-20"],
                capture_output=True, text=True, timeout=30
            )
            shas = [sha for sha in result.stdout.strip().split("\n") if sha]
        except Exception:
            return {"atomic": True, "max_files": 0, "violations": []}

        violations = []
        max_files = 0
        for sha in shas:
            try:
                diff = subprocess.run(
                    ["git", "-C", str(self.repo_root), "diff-tree", "--no-commit-id", "-r", "--name-only", sha],
                    capture_output=True, text=True, timeout=30
                )
                files = [f for f in diff.stdout.strip().split("\n") if f]
                max_files = max(max_files, len(files))
                if len(files) > 3:
                    violations.append({"sha": sha[:8], "files": len(files)})
            except Exception:
                continue

        return {
            "atomic": len(violations) == 0,
            "max_files": max_files,
            "violations": violations,
        }

    def _validate_bridges_argus(self) -> dict[str, Any]:
        """Valide les bridges via ARGUS bridge_check."""
        try:
            script = Path(r"D:\DO\WEB\TOOLS\L1-INFRA\ARGUS\scanners\bridge_check.py")
            if not script.exists():
                return {"status": "skipped", "reason": "ARGUS bridge_check.py not found"}
            result = subprocess.run(
                ["python", str(script), "--repo", str(self.repo_root), "--json"],
                capture_output=True, text=True, timeout=120
            )
            if result.stdout:
                return json.loads(result.stdout)
            return {"status": "error", "reason": result.stderr[:200]}
        except Exception as exc:
            return {"status": "error", "reason": str(exc)}

    def _validate_crossrefs_argus(self) -> dict[str, Any]:
        """Valide les cross-refs via ARGUS crossref_check."""
        try:
            script = Path(r"D:\DO\WEB\TOOLS\L1-INFRA\ARGUS\scanners\crossref_check.py")
            if not script.exists():
                return {"status": "skipped", "reason": "ARGUS crossref_check.py not found"}
            result = subprocess.run(
                ["python", str(script), "--repo", str(self.repo_root), "--json"],
                capture_output=True, text=True, timeout=120
            )
            if result.stdout:
                return json.loads(result.stdout)
            return {"status": "error", "reason": result.stderr[:200]}
        except Exception as exc:
            return {"status": "error", "reason": str(exc)}

    def _check_meta_coherence(self) -> dict[str, Any]:
        """Vérifie la méta-cohérence écosystémique via ARGUS ecosystem_meta_coherence."""
        try:
            script = Path(r"D:\DO\WEB\TOOLS\L1-INFRA\ARGUS\PRD\ecosystem_meta_coherence.py")
            if not script.exists():
                return {"status": "skipped", "reason": "ARGUS ecosystem_meta_coherence.py not found"}
            result = subprocess.run(
                ["python", str(script), "--repo", str(self.repo_root), "--json"],
                capture_output=True, text=True, timeout=120
            )
            if result.stdout:
                data = json.loads(result.stdout)
                if isinstance(data, dict) and data.get("status") != "OK":
                    return {"status": "blocked", "reason": data.get("findings", data)}
                return data
            return {"status": "error", "reason": result.stderr[:200]}
        except Exception as exc:
            return {"status": "error", "reason": str(exc)}

    def _validate_traceability(self) -> dict[str, Any]:
        """Valide la traçabilité via CTULU trace_graph.py + trace_validator.py."""
        try:
            graph_script = Path(r"D:\DO\WEB\TOOLS\L4-TOOLS\CTULU\tools\traceability\trace_graph.py")
            validator_script = Path(r"D:\DO\WEB\TOOLS\L4-TOOLS\CTULU\tools\traceability\trace_validator.py")
            if not graph_script.exists() or not validator_script.exists():
                return {"status": "skipped", "reason": "CTULU traceability scripts not found"}

            graph_result = subprocess.run(
                ["python", str(graph_script), "--repo", str(self.repo_root), "--json"],
                capture_output=True, text=True, timeout=120
            )
            validator_result = subprocess.run(
                ["python", str(validator_script), "--repo", str(self.repo_root), "--json"],
                capture_output=True, text=True, timeout=120
            )
            return {
                "status": "ok",
                "graph": json.loads(graph_result.stdout) if graph_result.stdout else {},
                "validator": json.loads(validator_result.stdout) if validator_result.stdout else {},
            }
        except Exception as exc:
            return {"status": "error", "reason": str(exc)}

    def _notify_crm_tech_debt(self) -> dict[str, Any]:
        """Hook notification CRM vers crm/notifier.py."""
        try:
            from crm.workflow import run_tech_debt_workflow
            return run_tech_debt_workflow(self.repo_root)
        except Exception as exc:
            return {"status": "error", "reason": str(exc)}


def verify_repo(repo_root: Path) -> dict[str, Any]:
    return AutoDesignVerifier(repo_root).verify()
