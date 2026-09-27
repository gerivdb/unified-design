"""
Tests for scripts/sync-mdu-catalog.py
"""

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SYNC_SCRIPT = REPO_ROOT / "scripts" / "sync-mdu-catalog.py"


def run_sync(*args):
    """Run sync-mdu-catalog.py with given args and return (exit_code, stdout, stderr)."""
    result = subprocess.run(
        [sys.executable, str(SYNC_SCRIPT)] + list(args),
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )
    return result.returncode, result.stdout, result.stderr


def test_sync_dry_run_designs():
    """sync-mdu-catalog.py --designs --dry-run should run without error."""
    exit_code, stdout, stderr = run_sync("--designs", "--dry-run")
    assert exit_code == 0, f"Sync failed: {stderr}"


def test_sync_dry_run_atoms():
    """sync-mdu-catalog.py --atoms --dry-run should run without error."""
    exit_code, stdout, stderr = run_sync("--atoms", "--dry-run")
    assert exit_code == 0, f"Sync failed: {stderr}"


def test_sync_dry_run_all():
    """sync-mdu-catalog.py --all --dry-run should run without error."""
    exit_code, stdout, stderr = run_sync("--all", "--dry-run")
    assert exit_code == 0, f"Sync failed: {stderr}"


def test_sync_creates_catalog_files():
    """sync-mdu-catalog.py --all should update catalog files."""
    exit_code, stdout, stderr = run_sync("--all")
    assert exit_code == 0, f"Sync failed: {stderr}"
    designs_index = REPO_ROOT / "catalog" / "designs.index.yaml"
    atoms_index = REPO_ROOT / "catalog" / "atoms.index.yaml"
    assert designs_index.exists(), "designs.index.yaml should exist"
    assert atoms_index.exists(), "atoms.index.yaml should exist"
