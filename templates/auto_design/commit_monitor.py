#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Commit monitor template for auto-design industrializer.

Auto-commit and push changes in industrialized repos.
Deployed in scripts/ of industrialized repos.
"""

from __future__ import annotations

import subprocess
import sys
from datetime import datetime
from pathlib import Path


def git_status(repo_path: Path) -> list[str]:
    """Get git status for a repo."""
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_path), "status", "--porcelain"],
            capture_output=True, text=True, timeout=10
        )
        lines = [l for l in result.stdout.strip().split('\n') if l]
        return lines
    except Exception:
        return []


def git_add(repo_path: Path, files: list[str]) -> bool:
    """Stage files for commit."""
    try:
        subprocess.run(["git", "-C", str(repo_path), "add"] + files, capture_output=True, timeout=10)
        return True
    except Exception:
        return False


def git_commit(repo_path: Path, message: str) -> bool:
    """Commit staged changes."""
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_path), "commit", "-m", message],
            capture_output=True, text=True, timeout=10
        )
        return result.returncode == 0
    except Exception:
        return False


def git_push(repo_path: Path) -> bool:
    """Push commits to remote."""
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_path), "push", "origin"],
            capture_output=True, text=True, timeout=30
        )
        return result.returncode == 0
    except Exception:
        return False


def auto_commit(repo_path: Path, message_template: str = "chore(auto_design): auto-commit {timestamp}") -> dict:
    """Auto-commit all changes in repo."""
    changes = git_status(repo_path)
    if not changes:
        return {"status": "clean", "committed": False}

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    message = message_template.format(timestamp=timestamp)

    files = [line[3:] for line in changes if line[3:]]
    if not files:
        return {"status": "no_files", "committed": False}

    staged = git_add(repo_path, files)
    if not staged:
        return {"status": "add_failed", "committed": False}

    committed = git_commit(repo_path, message)
    if not committed:
        return {"status": "commit_failed", "committed": False}

    pushed = git_push(repo_path)
    return {
        "status": "ok",
        "committed": True,
        "pushed": pushed,
        "message": message,
        "files": len(files),
    }


def main() -> int:
    import sys
    repo = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    print(f"[commit-monitor] repo={repo}")
    result = auto_commit(repo)
    print(f"[commit-monitor] status={result['status']}")
    if result.get("committed"):
        print(f"[commit-monitor] committed: {result.get('message')}")
        print(f"[commit-monitor] pushed={result.get('pushed', False)}")
    return 0 if result["status"] == "clean" or result.get("committed") else 1


if __name__ == "__main__":
    raise SystemExit(main())
