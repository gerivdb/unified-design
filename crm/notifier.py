"""Notify CRM tech debt items to target repos."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class TechDebtNotifier:
    def __init__(self, registry_path: Path | None = None) -> None:
        self.registry_path = registry_path or Path(__file__).resolve().parents[1] / "crm" / "tech_debt_registry.yaml"

    def load_items(self) -> list[dict[str, Any]]:
        if not self.registry_path.exists():
            return []
        try:
            import yaml
            with self.registry_path.open("r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
        except Exception:
            return []
        return [item for item in data.get("items", []) if item.get("status") == "open"]

    def build_notification(self, item: dict[str, Any]) -> dict[str, Any]:
        return {
            "type": "tech_debt",
            "repo": item.get("repo"),
            "component": item.get("component"),
            "id": item.get("id"),
            "description": item.get("description"),
            "severity": item.get("severity"),
            "score": item.get("score"),
            "assignee": item.get("assignee"),
            "labels": item.get("labels", []),
            "action": "create_or_update_ticket",
        }

    def notify_repo(self, repo: str, payload: dict[str, Any]) -> dict[str, Any]:
        # Fallback local si ARGUS/CTULU indisponibles
        return {
            "repo": repo,
            "status": "queued",
            "payload": payload,
            "fallback": True,
        }

    def notify_all(self) -> list[dict[str, Any]]:
        items = self.load_items()
        notifications: list[dict[str, Any]] = []
        seen: set[str] = set()
        for item in items:
            repo = item.get("repo")
            if not repo or repo in seen:
                continue
            seen.add(repo)
            payload = self.build_notification(item)
            notifications.append(self.notify_repo(repo, payload))
        return notifications


def notify_tech_debt(registry_path: Path | None = None) -> list[dict[str, Any]]:
    return TechDebtNotifier(registry_path).notify_all()
