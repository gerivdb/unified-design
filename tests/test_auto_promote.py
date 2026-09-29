"""Tests unitaires pour engine/auto_design/auto_promote."""

from __future__ import annotations

from pathlib import Path

import pytest

from engine.auto_design.auto_promote import AutoPromoter


def test_auto_promoter_detects_proposed_with_proof_of_life(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    doc = repo / "INTENT-TEST.md"
    doc.write_text("status: proposed\nProof-of-Life\n- [x] 2026-09-29T00:00:00+00:00\n", encoding="utf-8")
    result = AutoPromoter(repo).promote(apply=False)
    assert result["candidates"] == 1
    assert result["actions"][0]["target_status"] == "approved"


def test_auto_promoter_ignores_non_proposed(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    doc = repo / "INTENT-TEST.md"
    doc.write_text("status: approved\n", encoding="utf-8")
    result = AutoPromoter(repo).promote(apply=False)
    assert result["candidates"] == 0


def test_auto_promoter_applies_promotion(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    doc = repo / "INTENT-TEST.md"
    doc.write_text("status: proposed\nProof-of-Life\n- [x] 2026-09-29T00:00:00+00:00\n", encoding="utf-8")
    result = AutoPromoter(repo).promote(apply=True)
    assert result["actions"][0]["applied"] is True
    assert "status: approved" in doc.read_text(encoding="utf-8")
