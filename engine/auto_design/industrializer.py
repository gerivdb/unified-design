"""Deploy auto-design runtimes into a target repo."""

from __future__ import annotations

import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any

TEMPLATE_ROOT = Path(__file__).resolve().parents[2] / "templates" / "auto_design"


class AutoDesignIndustrializer:
    def __init__(self, repo_root: Path, template_root: Path = TEMPLATE_ROOT) -> None:
        self.repo_root = Path(repo_root)
        self.template_root = Path(template_root)

    def deploy(self) -> dict[str, Any]:
        deployed: list[str] = []
        for template in self.template_root.glob("*.py"):
            target = self.repo_root / "scripts" / template.name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(template, target)
            deployed.append(str(target))
        return {"repo": str(self.repo_root), "deployed": deployed, "status": "ok"}

    def deploy_with_auto_commit(self, message_template: str = "feat(auto_design): industrialize {repo}") -> dict[str, Any]:
        """Déploie et commit automatiquement les changements."""
        deploy_result = self.deploy()
        if deploy_result["status"] != "ok":
            return deploy_result

        try:
            status = subprocess.run(
                ["git", "-C", str(self.repo_root), "status", "--porcelain"],
                capture_output=True, text=True, timeout=30
            )
            changes = [l for l in status.stdout.strip().split("\n") if l]
            if not changes:
                deploy_result["committed"] = False
                deploy_result["reason"] = "no changes to commit"
                return deploy_result

            files = [c[3:] for c in changes if c[3:]]
            subprocess.run(["git", "-C", str(self.repo_root), "add"] + files, capture_output=True, timeout=30)

            message = message_template.format(repo=self.repo_root.name)
            commit = subprocess.run(
                ["git", "-C", str(self.repo_root), "commit", "-m", message],
                capture_output=True, text=True, timeout=30
            )
            deploy_result["committed"] = commit.returncode == 0
            deploy_result["commit_message"] = message
            if commit.returncode != 0:
                deploy_result["commit_error"] = commit.stderr[:200]
        except Exception as exc:
            deploy_result["committed"] = False
            deploy_result["error"] = str(exc)

        return deploy_result


def deploy_repo(repo_root: Path, template_root: Path = TEMPLATE_ROOT) -> dict[str, Any]:
    return AutoDesignIndustrializer(repo_root, template_root).deploy()
