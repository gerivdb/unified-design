"""Global auto-design coverage report."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .verifier import verify_repo


class AutoDesignReporter:
    def __init__(self, known_repos: Path) -> None:
        self.known_repos = Path(known_repos)

    def report(self) -> dict[str, Any]:
        repos: list[dict[str, Any]] = []
        for repo_path in self.known_repos.parent.glob("*"):
            if not repo_path.is_dir():
                continue
            try:
                result = verify_repo(repo_path)
                repos.append(result)
            except Exception as exc:
                repos.append({"repo": str(repo_path), "error": str(exc)})

        mature = [r for r in repos if r.get("mature")]
        return {
            "total_repos": len(repos),
            "mature_repos": len(mature),
            "mature_pct": int((len(mature) / len(repos) * 100) if repos else 0),
            "repos": repos,
        }


def report_global(known_repos: Path) -> dict[str, Any]:
    return AutoDesignReporter(known_repos).report()
