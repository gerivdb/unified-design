"""Tests for auto_design ARGUS/CTULU integration."""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path
from unittest import mock

import pytest

from engine.auto_design.analyzer import AutoDesignAnalyzer
from engine.auto_design.generator import AutoDesignGenerator
from engine.auto_design.verifier import AutoDesignVerifier


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_conventional_commit_scoring():
    analyzer = AutoDesignAnalyzer(REPO_ROOT)
    score = analyzer._score_conventional_commit_adherence()
    assert 0 <= score <= 100


def test_commit_message_generation():
    msg = AutoDesignGenerator.generate_commit_message("feat", "engine", "add analyzer")
    assert msg == "feat(engine): add analyzer"
    msg_no_scope = AutoDesignGenerator.generate_commit_message("fix", "", "bug fix")
    assert msg_no_scope == "fix: bug fix"
    with pytest.raises(ValueError):
        AutoDesignGenerator.generate_commit_message("invalid", "scope", "desc")


def test_atomic_commit_checking():
    verifier = AutoDesignVerifier(REPO_ROOT)
    result = verifier._check_atomic_commits()
    assert "atomic" in result
    assert "max_files" in result
    assert "violations" in result
    assert isinstance(result["atomic"], bool)
    assert isinstance(result["violations"], list)


def test_argus_bridge_validation():
    verifier = AutoDesignVerifier(REPO_ROOT)
    mock_result = {"status": "ok", "findings": {"GAP": [], "VOID": [], "DRIFT": [], "UNPROVEN": []}}
    with mock.patch("subprocess.run") as mock_run:
        mock_run.return_value.stdout = '{"status": "ok", "findings": {}}'
        mock_run.return_value.returncode = 0
        result = verifier._validate_bridges_argus()
    assert "status" in result


def test_argus_crossref_validation():
    verifier = AutoDesignVerifier(REPO_ROOT)
    with mock.patch("subprocess.run") as mock_run:
        mock_run.return_value.stdout = '{"status": "ok", "findings": {}}'
        mock_run.return_value.returncode = 0
        result = verifier._validate_crossrefs_argus()
    assert "status" in result


def test_fallback_without_argus():
    analyzer = AutoDesignAnalyzer(REPO_ROOT)
    score = analyzer._score_conventional_commit_adherence()
    assert isinstance(score, int)


def test_analyzer_includes_conventional_commits():
    analyzer = AutoDesignAnalyzer(REPO_ROOT)
    result = analyzer.analyze()
    assert "conventional_commit_adherence" in result["scores"]


def test_verifier_includes_atomic_commits():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        (tmp_path / "design.yaml").write_text("status: active\n", encoding="utf-8")
        verifier = AutoDesignVerifier(tmp_path)
        result = verifier.verify()
        assert "atomic_commits" in result


def test_verifier_includes_meta_coherence():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        (tmp_path / "design.yaml").write_text("status: active\n", encoding="utf-8")
        verifier = AutoDesignVerifier(tmp_path)
        result = verifier.verify()
        assert "meta_coherence" in result


def test_verifier_includes_traceability():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        (tmp_path / "design.yaml").write_text("status: active\n", encoding="utf-8")
        verifier = AutoDesignVerifier(tmp_path)
        result = verifier.verify()
        assert "traceability" in result


def test_commit_validator_template():
    template_path = REPO_ROOT / "templates" / "auto_design" / "commit_validator.py"
    assert template_path.exists()
    msg = AutoDesignGenerator.generate_commit_message("feat", "engine", "add analyzer")
    assert msg == "feat(engine): add analyzer"


def test_commit_monitor_template():
    template_path = REPO_ROOT / "templates" / "auto_design" / "commit_monitor.py"
    assert template_path.exists()


def test_pr_factory_template():
    template_path = REPO_ROOT / "templates" / "auto_design" / "pr_factory.py"
    assert template_path.exists()


def test_industrializer_deploy():
    from engine.auto_design.industrializer import AutoDesignIndustrializer
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        (tmp_path / "scripts").mkdir(parents=True, exist_ok=True)
        industrializer = AutoDesignIndustrializer(tmp_path)
        result = industrializer.deploy()
        assert result["status"] == "ok"
        assert len(result["deployed"]) >= 2


def test_industrializer_auto_commit():
    from engine.auto_design.industrializer import AutoDesignIndustrializer
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        (tmp_path / "scripts").mkdir(parents=True, exist_ok=True)
        (tmp_path / ".git").mkdir(parents=True, exist_ok=True)
        industrializer = AutoDesignIndustrializer(tmp_path)
        result = industrializer.deploy_with_auto_commit()
        assert result["status"] == "ok"


def test_generator_classify_components_noded():
    from engine.auto_design.generator import AutoDesignGenerator
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        (tmp_path / "src").mkdir(parents=True, exist_ok=True)
        (tmp_path / "src" / "sample.py").write_text("x = 1\n", encoding="utf-8")
        generator = AutoDesignGenerator(tmp_path)
        result = generator._classify_components_noded()
        assert isinstance(result, dict)


def test_jevi_projection_templates():
    jevi_dir = REPO_ROOT / "templates" / "auto_design" / "jevi_projection"
    assert jevi_dir.exists()
    assert (jevi_dir / "__init__.py").exists()


def test_auto_promote_governance_synthesizer():
    from engine.auto_design.auto_promote import AutoPromoter
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        promoter = AutoPromoter(tmp_path)
        result = promoter.governance_synthesizer()
        assert "status" in result


def test_pr_review_auto_workflow():
    from engine.auto_design.pr_review_auto import ensure_feat_branch, auto_commit, create_pr, resolve_and_merge
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        subprocess.run(["git", "-C", str(tmp_path), "init"], capture_output=True, timeout=30)
        subprocess.run(["git", "-C", str(tmp_path), "config", "user.email", "test@example.com"], capture_output=True, timeout=30)
        subprocess.run(["git", "-C", str(tmp_path), "config", "user.name", "Test User"], capture_output=True, timeout=30)
        (tmp_path / "README.md").write_text("x", encoding="utf-8")
        subprocess.run(["git", "-C", str(tmp_path), "add", "README.md"], capture_output=True, timeout=30)
        subprocess.run(["git", "-C", str(tmp_path), "commit", "-m", "init"], capture_output=True, timeout=30)
        branch = ensure_feat_branch(tmp_path, "test-skill")
        assert branch == "feat/auto-design-test-skill"
        (tmp_path / "README.md").write_text("xy", encoding="utf-8")
        assert auto_commit(tmp_path, "feat(auto_design): test-skill") is True
        pr = create_pr(tmp_path, "test-skill", "body")
        assert pr["status"] == "ready"
        merge = resolve_and_merge(tmp_path, pr.get("number"))
        assert merge["status"] in ("merged", "conflict")


def test_auto_operator_full_cycle():
    from engine.auto_design.auto_operator import AutoOperator
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        (tmp_path / "design.yaml").write_text("status: active\n", encoding="utf-8")
        (tmp_path / ".git").mkdir(parents=True, exist_ok=True)
        operator = AutoOperator(tmp_path)
        result = operator.run_full_cycle(apply=False)
        assert result["repo"] == str(tmp_path)
        assert "analysis" in result
        assert "generated" in result
        assert "verification" in result
        assert "deployed" in result
