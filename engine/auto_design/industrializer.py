"""Deploy auto-design runtimes into a target repo."""

from __future__ import annotations

import shutil
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


def deploy_repo(repo_root: Path, template_root: Path = TEMPLATE_ROOT) -> dict[str, Any]:
    return AutoDesignIndustrializer(repo_root, template_root).deploy()
