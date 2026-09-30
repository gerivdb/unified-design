"""Tests unitaires pour engine/auto_design."""

from __future__ import annotations

from pathlib import Path

import pytest

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.engines.auto_design.analyzer import AutoDesignAnalyzer
from src.engines.auto_design.generator import AutoDesignGenerator
from src.engines.auto_design.industrializer import AutoDesignIndustrializer
from src.engines.auto_design.verifier import AutoDesignVerifier
from src.engines.auto_design.reporter import AutoDesignReporter


def test_analyzer_returns_scores(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "design.yaml").write_text("name: test\n", encoding="utf-8")
    (repo / "bridges").mkdir()
    (repo / "bridges" / "b1.yaml").write_text("from: a\nto: b\n", encoding="utf-8")
    (repo / "tests").mkdir()
    (repo / "tests" / "test_x.py").write_text("def test_x(): pass\n", encoding="utf-8")
    (repo / "docs").mkdir()
    (repo / "docs" / "README.md").write_text("# docs\n", encoding="utf-8")
    result = AutoDesignAnalyzer(repo).analyze()
    assert "auto_design_readiness" in result
    assert 0 <= result["auto_design_readiness"] <= 100


def test_generator_produces_design_yaml(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "agents").mkdir()
    (repo / "agents" / "a.py").write_text("x=1\n", encoding="utf-8")
    result = AutoDesignGenerator(repo).generate(apply=False)
    assert "design_yaml" in result
    assert "name:" in result["design_yaml"]


def test_industrializer_copies_templates(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "scripts").mkdir()
    template = tmp_path / "cycle_runner.py"
    template.write_text("print('tpl')\n", encoding="utf-8")
    result = AutoDesignIndustrializer(repo, template_root=tmp_path).deploy()
    assert len(result["deployed"]) == 1


def test_verifier_detects_design_yaml(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "design.yaml").write_text("name: test\nimplementation_contract:\n", encoding="utf-8")
    (repo / "bridges").mkdir(exist_ok=True)
    result = AutoDesignVerifier(repo).verify()
    assert "auto_design_score" in result


def test_reporter_returns_aggregate(tmp_path: Path) -> None:
    known = tmp_path / "known_repositories.yaml"
    known.write_text("repos:\n", encoding="utf-8")
    result = AutoDesignReporter(known).report()
    assert "total_repos" in result
    assert "mature_pct" in result
