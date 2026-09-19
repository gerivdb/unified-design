#!/usr/bin/env python3
"""
branch-taxonomy-validator.py — Valide le nom de la branche courante
selon la taxonomie unifiée : type/jurisdiction-slug-id

Exit codes:
  0 = valid
  1 = invalid
  2 = not a feature branch (skip)
"""

from __future__ import annotations

import re
import sys

# Pattern: type/jurisdiction-slug-id
# type: feat|fix|docs|chore|refactor|perf|test|hotfix|emergency|release|experiment|deploy|rollback
# jurisdiction: lowercase, chiffres, tirets
# slug: lowercase, chiffres, tirets
# id: numerique ou date YYYYMMDD
BRANCH_PATTERN = re.compile(
    r"^(feat|fix|docs|chore|refactor|perf|test|hotfix|emergency|release|experiment|deploy|rollback)"
    r"/([a-z0-9-]+)"  # jurisdiction
    r"-([a-z0-9-]+)"  # slug
    r"-([a-z0-9]{1,8})$"  # id (max 8 chars)
)

# Branches exemptées de validation
EXEMPT_BRANCHES = {"main", "master", "develop", "dev"}


def get_current_branch() -> str:
    """Récupère le nom de la branche courante via git."""
    import subprocess
    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def validate_branch(branch: str) -> tuple[bool, str]:
    if branch in EXEMPT_BRANCHES:
        return True, f"Branch '{branch}' is exempt from taxonomy validation"

    match = BRANCH_PATTERN.match(branch)
    if not match:
        return False, (
            f"Branch '{branch}' does not match pattern 'type/jurisdiction-slug-id'. "
            "Example: feat/env2-lxc-network-001"
        )

    branch_type, jurisdiction, slug, branch_id = match.groups()
    return True, (
        f"Branch '{branch}' is valid: type={branch_type}, jurisdiction={jurisdiction}, slug={slug}, id={branch_id}"
    )


def main() -> int:
    try:
        branch = get_current_branch()
    except subprocess.CalledProcessError as exc:
        print(f"[FAIL] Could not determine current branch: {exc}")
        return 1

    ok, msg = validate_branch(branch)
    status = "OK" if ok else "FAIL"
    print(f"[{status}] {msg}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
