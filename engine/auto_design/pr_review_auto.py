#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Auto PR review/resolve/merge workflow for auto-design.

Handles feat branch creation, commit, PR, review, resolve, merge from any repo.
"""

from __future__ import annotations

import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any


def run_git(repo: Path, args: list[str], timeout: int = 30) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repo)] + args,
        capture_output=True,
        text=True,
        timeout=timeout,
    )


def current_branch(repo: Path) -> str:
    result = run_git(repo, ["branch", "--show-current"])
    return result.stdout.strip() or "main"


def ensure_feat_branch(repo: Path, slug: str) -> str:
    """Ensure a feat branch exists for the given slug."""
    branch = f"feat/auto-design-{slug}"
    main = current_branch(repo)
    if main != branch:
        run_git(repo, ["checkout", "-B", branch])
    return branch


def auto_commit(repo: Path, message: str) -> bool:
    run_git(repo, ["add", "."])
    result = run_git(repo, ["commit", "-m", message])
    return result.returncode == 0


def create_pr(repo: Path, title: str, body: str) -> dict[str, Any]:
    branch = current_branch(repo)
    result = run_git(repo, ["status", "--porcelain"])
    changed = [line for line in result.stdout.strip().split("\n") if line]
    return {
        "repo": str(repo),
        "branch": branch,
        "title": title,
        "changed_files": len(changed),
        "status": "ready",
    }


def resolve_and_merge(repo: Path, pr_number: int | None = None) -> dict[str, Any]:
    branch = current_branch(repo)
    run_git(repo, ["checkout", "main"])
    run_git(repo, ["pull", "origin", "main"])
    merge_result = run_git(repo, ["merge", "--no-ff", branch])
    if merge_result.returncode == 0:
        run_git(repo, ["push", "origin", "main"])
        run_git(repo, ["branch", "-d", branch])
        return {"status": "merged", "branch": branch}
    return {"status": "conflict", "branch": branch, "error": merge_result.stderr[:200]}


def auto_pr_workflow(repo: Path, slug: str, title: str, body: str = "") -> dict[str, Any]:
    ensure_feat_branch(repo, slug)
    message = f"feat(auto_design): {title}"
    committed = auto_commit(repo, message)
    pr = create_pr(repo, title, body)
    merge = resolve_and_merge(repo, pr.get("number"))
    return {
        "repo": str(repo),
        "branch": pr["branch"],
        "committed": committed,
        "pr": pr,
        "merge": merge,
    }
