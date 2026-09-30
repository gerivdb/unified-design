#!/usr/bin/env python3
"""Tests pour codedb_design_reader.py."""
from __future__ import annotations

from pathlib import Path

import pytest

from tools.codedb_design_reader import read_design


def test_read_design_returns_facts():
    design_path = Path(__file__).resolve().parent.parent / "designs" / "codedb-e5620" / "design.yaml"
    facts = read_design(design_path)
    assert "cpu" in facts
    assert "constraints" in facts
    assert facts["cpu"]["model"] == "Xeon E5620"


def test_read_design_source_is_design_yaml():
    design_path = Path(__file__).resolve().parent.parent / "designs" / "codedb-e5620" / "design.yaml"
    facts = read_design(design_path)
    assert facts["source"] == str(design_path)
