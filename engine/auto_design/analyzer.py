"""Analyze auto-design readiness for a target repo."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from typing import Any

DEFAULT_KNOWN_REPOS = Path(__file__).resolve().parents[3] / "GOVERNANCE-HUB" / "known_repositories.yaml"
DIMENSIONS = (
    "design_coverage",
    "bridge_density",
    "test_coverage",
    "doc_coverage",
    "auto_debug_maturity",
)


class AutoDesignAnalyzer:
    def __init__(self, repo_root: Path, known_repos: Path = DEFAULT_KNOWN_REPOS) -> None:
        self.repo_root = Path(repo_root)
        self.known_repos = Path(known_repos)
        self.cache: dict[str, Any] = {}

    def analyze(self) -> dict[str, Any]:
        scores = {
            "design_coverage": self._score_design_coverage(),
            "bridge_density": self._score_bridge_density(),
            "test_coverage": self._score_test_coverage(),
            "doc_coverage": self._score_doc_coverage(),
            "auto_debug_maturity": self._score_auto_debug_maturity(),
            "conventional_commit_adherence": self._score_conventional_commit_adherence(),
            "tech_debt": self._score_tech_debt()["score"],
        }
        global_score = int(sum(scores.values()) / len(scores))
        return {
            "repo": str(self.repo_root),
            "scores": scores,
            "auto_design_readiness": global_score,
            "mature": global_score >= 80,
            "recommendations": self._recommendations(scores),
        }

    def _score_design_coverage(self) -> int:
        design_files = list(self.repo_root.glob("designs/*/design.yaml")) + list(
            self.repo_root.glob("design/*.yaml")
        )
        if not design_files:
            return 0
        with_contract = 0
        for design in design_files:
            try:
                content = design.read_text(encoding="utf-8")
                if "implementation_contract:" in content:
                    with_contract += 1
            except Exception:
                continue
        return int((with_contract / len(design_files)) * 100)

    def _score_bridge_density(self) -> int:
        bridges = list(self.repo_root.glob("bridges/*.yaml"))
        components = (
            list(self.repo_root.glob("designs/*/design.yaml"))
            + list(self.repo_root.glob("agents/*.py"))
            + list(self.repo_root.glob("src/*.py"))
        )
        if not components:
            return 0
        return min(100, int((len(bridges) / len(components)) * 100))

    def _score_test_coverage(self) -> int:
        tests = (
            list(self.repo_root.glob("tests/test_*.py"))
            + list(self.repo_root.glob("scripts/test_*.py"))
            + list(self.repo_root.glob("tests/**/test_*.py"))
        )
        return 100 if tests else 0

    def _score_doc_coverage(self) -> int:
        docs = list(self.repo_root.glob("docs/*.md")) + list(self.repo_root.glob("PRD/*.md")) + list(
            self.repo_root.glob("MOC/*.md")
        )
        return 100 if docs else 0

    def _score_auto_debug_maturity(self) -> int:
        if not (self.repo_root / "design.yaml").exists():
            return 0
        try:
            content = (self.repo_root / "design.yaml").read_text(encoding="utf-8")
        except Exception:
            return 0
        score = 0
        if "auto_debug_integrator" in content:
            score += 40
        if "auto_debug_pathways:" in content:
            score += 30
        if "scientific_reflection_protocols:" in content:
            score += 30
        return score

    def _score_conventional_commit_adherence(self) -> int:
        """Vérifie si le repo suit les conventional commits via CTULU ou git local."""
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location(
                "trix_git_workflow",
                r"D:\DO\WEB\TOOLS\L4-TOOLS\CTULU\tools\trix-box\trix-git-workflow.py"
            )
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                commits = module.get_recent_commits(str(self.repo_root), count=20)
            else:
                raise ImportError("Cannot load trix-git-workflow")
        except Exception:
            # Fallback local via git log
            try:
                result = subprocess.run(
                    ["git", "-C", str(self.repo_root), "log", "--oneline", "-20"],
                    capture_output=True, text=True, timeout=30
                )
                commits = [{"message": line.split(" ", 1)[-1]} for line in result.stdout.strip().split("\n") if line]
            except Exception:
                return 0
        pattern = re.compile(r'^(feat|fix|docs|test|refactor|chore|ci|build|revert|style|perf)')
        compliant = sum(1 for c in commits if pattern.match(c.get("message", "")))
        return int((compliant / len(commits)) * 100) if commits else 0

    def _score_tech_debt(self, registry_path: Path | None = None) -> dict[str, Any]:
        """Score la dette technique à partir du registry CRM."""
        registry = registry_path or Path(__file__).resolve().parents[3] / "crm" / "tech_debt_registry.yaml"
        if not registry.exists():
            return {"score": 0, "open_items": 0, "items": []}
        try:
            import yaml
            with registry.open("r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
        except Exception:
            return {"score": 0, "open_items": 0, "items": []}
        items = data.get("items", [])
        open_items = [item for item in items if item.get("status") == "open"]
        if not open_items:
            return {"score": 0, "open_items": 0, "items": []}
        avg_score = int(sum(item.get("score", 0) for item in open_items) / len(open_items))
        return {
            "score": avg_score,
            "open_items": len(open_items),
            "items": open_items,
        }

    def _recommendations(self, scores: dict[str, int]) -> list[str]:
        recommendations = []
        if scores["design_coverage"] < 80:
            recommendations.append("Add implementation_contract to active designs")
        if scores["bridge_density"] < 40:
            recommendations.append("Create bridges/*.yaml for cross-component mediation")
        if scores["test_coverage"] == 0:
            recommendations.append("Add tests/test_*.py integration tests")
        if scores["doc_coverage"] == 0:
            recommendations.append("Add docs/ + PRD/MOC documentation")
        if scores["auto_debug_maturity"] < 80:
            recommendations.append("Implement auto_debug_pathways in design.yaml")
        if scores.get("conventional_commit_adherence", 100) < 80:
            recommendations.append("Adopt conventional commits format: type(scope): description")
        if scores.get("tech_debt", 0) > 50:
            recommendations.append("Reduce tech debt via CRM workflow: crm/workflow.py")
        return recommendations


def analyze_repo(repo_root: Path, known_repos: Path = DEFAULT_KNOWN_REPOS) -> dict[str, Any]:
    return AutoDesignAnalyzer(repo_root, known_repos).analyze()
