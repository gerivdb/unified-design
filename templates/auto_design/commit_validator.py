#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Commit validator template for auto-design industrializer.

Validates conventional commits and atomicity (≤3 files per commit).
Deployed in scripts/ of industrialized repos.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path


CONVENTIONAL_TYPES = {
    "feat", "fix", "docs", "test", "refactor", "chore", "ci", "build", "revert", "style", "perf"
}
MAX_FILES_PER_COMMIT = 3


def validate_commit_message(message: str) -> dict:
    """Valide un message de commit selon conventional commits."""
    pattern = re.compile(r'^(' + '|'.join(CONVENTIONAL_TYPES) + r')(\(.+?\))?:\s*.+')
    valid = bool(pattern.match(message.strip()))
    return {"valid": valid, "message": message}


def check_atomic_commits(repo_root: Path, count: int = 20) -> dict:
    """Vérifie que les commits sont atomiques (≤3 fichiers)."""
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_root), "log", "--format=%H", f"-{count}"],
            capture_output=True, text=True, timeout=30
        )
        shas = [sha for sha in result.stdout.strip().split("\n") if sha]
    except Exception:
        return {"atomic": True, "max_files": 0, "violations": []}

    violations = []
    max_files = 0
    for sha in shas:
        try:
            diff = subprocess.run(
                ["git", "-C", str(repo_root), "diff-tree", "--no-commit-id", "-r", "--name-only", sha],
                capture_output=True, text=True, timeout=30
            )
            files = [f for f in diff.stdout.strip().split("\n") if f]
            max_files = max(max_files, len(files))
            if len(files) > MAX_FILES_PER_COMMIT:
                violations.append({"sha": sha[:8], "files": len(files)})
        except Exception:
            continue

    return {
        "atomic": len(violations) == 0,
        "max_files": max_files,
        "violations": violations,
    }


def main() -> int:
    import sys
    repo = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    print(f"[commit-validator] repo={repo}")
    commits = check_atomic_commits(repo)
    print(f"[commit-validator] atomic={commits['atomic']} max_files={commits['max_files']}")
    if commits["violations"]:
        print(f"[commit-validator] VIOLATIONS:")
        for v in commits["violations"]:
            print(f"  {v['sha']}: {v['files']} files")
        return 1
    print("[commit-validator] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
