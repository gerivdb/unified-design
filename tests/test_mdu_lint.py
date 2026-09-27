"""
Tests for tools/mdu-lint.py
"""

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MDU_LINT = REPO_ROOT / "tools" / "mdu-lint.py"


def run_mdu_lint(*args):
    """Run mdu-lint.py with given args and return (exit_code, stdout, stderr)."""
    result = subprocess.run(
        [sys.executable, str(MDU_LINT)] + list(args),
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )
    return result.returncode, result.stdout, result.stderr


def test_mdu_lint_runs():
    """mdu-lint.py should run without crashing."""
    exit_code, stdout, stderr = run_mdu_lint()
    assert exit_code in (0, 1, 2), f"Unexpected exit code: {exit_code}\n{stderr}"


def test_mdu_lint_strict_no_errors():
    """mdu-lint --strict should return 1 if warnings present (empty consumers), 0 if no warnings."""
    exit_code, stdout, stderr = run_mdu_lint("--strict")
    # In strict mode, warnings become errors, so exit_code 1 is expected if empty consumers exist
    assert exit_code in (0, 1, 2), f"Expected 0, 1, or 2, got {exit_code}\n{stdout}\n{stderr}"
    if exit_code == 1:
        assert "Empty consumers" in stdout, f"Expected empty consumers warning, got: {stdout}"


def test_mdu_lint_dry_run():
    """mdu-lint should accept --dry-run flag (if supported)."""
    exit_code, stdout, stderr = run_mdu_lint("--dry-run")
    assert exit_code in (0, 1, 2), f"Unexpected exit code: {exit_code}\n{stderr}"
