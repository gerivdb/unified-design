"""
Tests unitaires pour tools/mdu-lint.py
Import direct pour couverture >= 80%.
"""

import sys
import tempfile
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

import importlib.util

_mdu_lint_path = REPO_ROOT / "tools" / "mdu-lint.py"
_spec = importlib.util.spec_from_file_location("mdu_lint", _mdu_lint_path)
mdu_lint = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mdu_lint)

check_consumers = mdu_lint.check_consumers
check_path_existence = mdu_lint.check_path_existence
check_status_harmonization = mdu_lint.check_status_harmonization
check_unique_ids = mdu_lint.check_unique_ids
lint_strict = mdu_lint.lint_strict
load_yaml = mdu_lint.load_yaml


def _write_yaml(path: Path, data):
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def test_load_yaml_roundtrip(tmp_path: Path):
    data = {"name": "test", "status": "active"}
    p = tmp_path / "sample.yaml"
    _write_yaml(p, data)
    loaded = load_yaml(p)
    assert loaded == data


def test_check_unique_ids_no_duplicates():
    meta = {
        "designs": [{"intent_hash": "0x1", "name": "a"}],
        "primitives": [{"intent_hash": "0x2", "name": "b"}],
    }
    catalogs = {"designs.index": [{"intent_hash": "0x3"}]}
    assert check_unique_ids(meta, catalogs) == []


def test_check_unique_ids_with_duplicates():
    meta = {
        "designs": [{"intent_hash": "0x1", "name": "a"}],
        "primitives": [{"intent_hash": "0x1", "name": "b"}],
    }
    catalogs = {}
    assert check_unique_ids(meta, catalogs) == ["0x1"]


def test_check_unique_ids_ignores_non_dict_entries():
    meta = {"designs": ["bad-entry"], "primitives": [{"intent_hash": "0x1"}]}
    catalogs = {}
    assert check_unique_ids(meta, catalogs) == []


def test_check_path_existence_all_exist(tmp_path: Path):
    p = tmp_path / "foo.yaml"
    p.write_text("x", encoding="utf-8")
    meta = {"designs": [{"path": str(p)}]}
    assert check_path_existence(meta) == []


def test_check_path_existence_missing():
    meta = {"designs": [{"path": "/nonexistent/path.yaml"}]}
    missing = check_path_existence(meta)
    assert len(missing) == 1
    assert str(Path("/nonexistent/path.yaml")) in missing[0]


def test_check_status_harmonization_valid():
    meta = {"designs": [{"name": "x", "status": "active"}]}
    assert check_status_harmonization(meta) == []


def test_check_status_harmonization_invalid():
    meta = {"designs": [{"name": "x", "status": "weird_status"}]}
    assert check_status_harmonization(meta) == ["x: status=weird_status"]


def test_check_consumers_empty():
    meta = {"designs": [{"name": "x", "consumers": []}]}
    assert check_consumers(meta) == ["x"]


def test_check_consumers_non_empty():
    meta = {"designs": [{"name": "x", "consumers": ["y"]}]}
    assert check_consumers(meta) == []


def test_lint_strict_returns_errors_and_warnings(monkeypatch, tmp_path: Path):
    meta = {
        "designs": [
            {"intent_hash": "0x1", "name": "a", "status": "active", "path": str(tmp_path / "nonexistent.yaml")},
            {"name": "b", "consumers": []},
        ]
    }
    monkeypatch.setattr(mdu_lint, "META_DESIGN", tmp_path / "meta.yaml")
    monkeypatch.setattr(mdu_lint, "CATALOG_DIR", tmp_path)
    monkeypatch.setattr(mdu_lint, "REPO_ROOT", tmp_path)
    _write_yaml(tmp_path / "meta.yaml", meta)
    _write_yaml(tmp_path / "designs.index.yaml", {"items": [{"intent_hash": "0x1"}]})

    errors, warnings = lint_strict()
    assert any("Duplicate IDs" in e for e in errors), f"Expected Duplicate IDs in {errors}"
    assert any("Missing paths" in e for e in errors), f"Expected Missing paths in {errors}"
    assert any("Empty consumers" in w for w in warnings), f"Expected Empty consumers in {warnings}"
