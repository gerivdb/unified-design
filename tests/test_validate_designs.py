"""
Tests for scripts/validate_designs.py
"""

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
VALIDATE_SCRIPT = REPO_ROOT / "scripts" / "validate_designs.py"


def run_validate(*args):
    """Run validate_designs.py with given args and return (exit_code, stdout, stderr)."""
    result = subprocess.run(
        [sys.executable, str(VALIDATE_SCRIPT)] + list(args),
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )
    return result.returncode, result.stdout, result.stderr


def test_validate_designs_runs():
    """validate_designs.py should run without crashing."""
    exit_code, stdout, stderr = run_validate()
    assert exit_code in (0, 1), f"Unexpected exit code: {exit_code}\n{stderr}"


def test_validate_designs_strict():
    """validate_designs.py --strict should run without crashing."""
    exit_code, stdout, stderr = run_validate("--strict")
    assert exit_code in (0, 1), f"Unexpected exit code: {exit_code}\n{stderr}"


def test_validate_designs_path():
    """validate_designs.py should accept a path argument."""
    exit_code, stdout, stderr = run_validate(str(REPO_ROOT / "designs"))
    assert exit_code in (0, 1), f"Unexpected exit code: {exit_code}\n{stderr}"
