"""Tests for CRM tech debt management."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from engine.auto_design.analyzer import AutoDesignAnalyzer
from engine.auto_design.generator import AutoDesignGenerator

from crm.notifier import TechDebtNotifier
from crm.workflow import TechDebtWorkflow


REPO_ROOT = Path(__file__).resolve().parents[2]
REGISTRY = REPO_ROOT / "crm" / "tech_debt_registry.yaml"


def test_analyzer_scores_tech_debt_when_registry_exists():
    if not REGISTRY.exists():
        pytest.skip("Registry missing")
    analyzer = AutoDesignAnalyzer(REPO_ROOT)
    result = analyzer._score_tech_debt(REGISTRY)
    assert "score" in result
    assert "open_items" in result
    assert result["score"] >= 0


def test_analyzer_returns_zero_when_registry_missing(tmp_path):
    analyzer = AutoDesignAnalyzer(tmp_path)
    result = analyzer._score_tech_debt(tmp_path / "missing.yaml")
    assert result == {"score": 0, "open_items": 0, "items": []}


def test_analyzer_tech_debt_integrated_in_analyze():
    if not REGISTRY.exists():
        pytest.skip("Registry missing")
    analyzer = AutoDesignAnalyzer(REPO_ROOT)
    result = analyzer.analyze()
    assert "tech_debt" in result["scores"]
    assert result["scores"]["tech_debt"] >= 0


def test_generator_generates_crm_tasks_when_registry_exists():
    if not REGISTRY.exists():
        pytest.skip("Registry missing")
    generator = AutoDesignGenerator(REPO_ROOT)
    tickets = generator.generate_crm_tasks(REGISTRY)
    assert isinstance(tickets, list)
    for ticket in tickets:
        assert "id" in ticket
        assert ticket.get("type") == "tech_debt"


def test_generator_returns_empty_when_registry_missing(tmp_path):
    generator = AutoDesignGenerator(tmp_path)
    tickets = generator.generate_crm_tasks(tmp_path / "missing.yaml")
    assert tickets == []


def test_notifier_loads_open_items():
    if not REGISTRY.exists():
        pytest.skip("Registry missing")
    notifier = TechDebtNotifier(REGISTRY)
    items = notifier.load_items()
    assert isinstance(items, list)
    for item in items:
        assert item.get("status") == "open"


def test_notifier_builds_notification():
    notifier = TechDebtNotifier(REGISTRY)
    payload = notifier.build_notification({
        "id": "DEBT-001",
        "repo": "gerivdb/unified-design",
        "component": "engine/auto_design/analyzer.py",
        "description": "missing scoring",
        "severity": "high",
        "score": 85,
        "assignee": "L0-CANON",
        "labels": ["crm"],
    })
    assert payload["type"] == "tech_debt"
    assert payload["action"] == "create_or_update_ticket"


def test_notifier_notify_all_queues_repos():
    if not REGISTRY.exists():
        pytest.skip("Registry missing")
    notifier = TechDebtNotifier(REGISTRY)
    notifications = notifier.notify_all()
    assert isinstance(notifications, list)
    for notification in notifications:
        assert notification["status"] == "queued"
        assert notification["fallback"] is True


def test_workflow_returns_tech_debt_score():
    if not REGISTRY.exists():
        pytest.skip("Registry missing")
    workflow = TechDebtWorkflow(REPO_ROOT, REGISTRY)
    result = workflow.run()
    assert "tech_debt_score" in result
    assert "open_items" in result
    assert "tickets" in result
    assert "notifications" in result
    assert result["tech_debt_score"] >= 0


def test_workflow_tickets_are_crm_type():
    if not REGISTRY.exists():
        pytest.skip("Registry missing")
    workflow = TechDebtWorkflow(REPO_ROOT, REGISTRY)
    result = workflow.run()
    for ticket in result["tickets"]:
        assert ticket["type"] == "tech_debt"


def test_registry_has_required_fields():
    if not REGISTRY.exists():
        pytest.skip("Registry missing")
    import yaml
    with REGISTRY.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    items = data.get("items", [])
    assert items, "Registry must contain items"
    for item in items:
        assert "id" in item
        assert "repo" in item
        assert "component" in item
        assert "description" in item
        assert "score" in item
        assert "status" in item
