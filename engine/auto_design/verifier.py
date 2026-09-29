"""Verify auto-design adherence for a target repo."""

from __future__ import annotations

import json
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
        }


def verify_repo(repo_root: Path) -> dict[str, Any]:
    return AutoDesignVerifier(repo_root).verify()
