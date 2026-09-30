#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PR factory template for auto-design industrializer.

Validates branch/commit coupling before PR creation.
Deployed in scripts/ of industrialized repos.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path


CONVENTIONAL_TYPES = {
    "feat", "fix", "docs", "test", "refactor", "chore", "ci", "build", "revert", "style", "perf"
}


def get_current_branch(repo_root: Path) -> str:
    """Get current git branch."""
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_root), "branch", "--show-current"],
            capture_output=True, text=True, timeout=10
        )
        return result.stdout.strip()
    except Exception:
        return "unknown"


def get_last_commit_message(repo_root: Path) -> str:
    """Get last commit message."""
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_root), "log", "-1", "--format=%B"],
            capture_output=True, text=True, timeout=10
        )
        return result.stdout.strip()
    except Exception:
        return ""


def get_last_commit_files(repo_root: Path) -> int:
    """Get number of files in last commit."""
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_root), "diff-tree", "--no-commit-id", "-r", "--name-only", "HEAD"],
            capture_output=True, text=True, timeout=10
        )
        files = [f for f in result.stdout.strip().split("\n") if f]
        return len(files)
    except Exception:
        return 0


def validate_branch_commit_coupling(repo_root: Path, expected_branch: str) -> dict:
    """Vérifie la cohérence branch → commit → PR."""
    current = get_current_branch(repo_root)
    message = get_last_commit_message(repo_root)
    files = get_last_commit_files(repo_root)

    conventional_match = re.match(r'^(' + '|'.join(CONVENTIONAL_TYPES) + r')(\(.+?\))?:\s*.+', message.strip())
    atomic = files <= 3

    return {
        "branch_ok": current == expected_branch,
        "current_branch": current,
        "expected_branch": expected_branch,
        "conventional_commit": bool(conventional_match),
        "atomic_commit": atomic,
        "files_in_last_commit": files,
        "valid": current == expected_branch and bool(conventional_match) and atomic,
    }


def main() -> int:
    import sys
    repo = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    branch = sys.argv[2] if len(sys.argv) > 2 else get_current_branch(repo)
    result = validate_branch_commit_coupling(repo, branch)
    print(f"[pr-factory] branch_ok={result['branch_ok']} conventional={result['conventional_commit']} atomic={result['atomic_commit']}")
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
