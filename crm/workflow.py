"""Workflow end-to-end pour la gestion de la dette technique CRM."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from engine.auto_design.analyzer import AutoDesignAnalyzer
from engine.auto_design.generator import AutoDesignGenerator

from crm.notifier import TechDebtNotifier


class TechDebtWorkflow:
    def __init__(self, repo_root: Path, registry_path: Path | None = None) -> None:
        self.repo_root = Path(repo_root)
        self.registry_path = registry_path or Path(__file__).resolve().parents[1] / "crm" / "tech_debt_registry.yaml"
        self.analyzer = AutoDesignAnalyzer(self.repo_root)
        self.generator = AutoDesignGenerator(self.repo_root)
        self.notifier = TechDebtNotifier(self.registry_path)

    def run(self) -> dict[str, Any]:
        score = self.analyzer._score_tech_debt(self.registry_path)
        tickets = self.generator.generate_crm_tasks(self.registry_path)
        notifications = self.notifier.notify_all()
        return {
            "repo": str(self.repo_root),
            "tech_debt_score": score.get("score", 0),
            "open_items": score.get("open_items", 0),
            "tickets": tickets,
            "notifications": notifications,
        }


def run_tech_debt_workflow(repo_root: Path, registry_path: Path | None = None) -> dict[str, Any]:
    return TechDebtWorkflow(repo_root, registry_path).run()
