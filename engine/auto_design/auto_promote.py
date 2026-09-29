"""Auto-promote governance documents when objective criteria are met."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class AutoPromoter:
    def __init__(self, repo_root: Path) -> None:
        self.repo_root = Path(repo_root)

    def promote(self, apply: bool = False) -> dict[str, Any]:
        candidates = self._scan()
        actions: list[dict[str, object]] = []
        for doc in candidates:
            action = {
                "path": str(doc["path"]),
                "current_status": doc.get("status", "unknown"),
                "target_status": doc.get("target_status", "unknown"),
                "reason": doc.get("reason", ""),
                "applied": False,
            }
            if apply:
                action["applied"] = self._apply_promotion(doc)
            actions.append(action)
        return {"repo": str(self.repo_root), "candidates": len(candidates), "actions": actions}

    def _scan(self) -> list[dict[str, object]]:
        candidates: list[dict[str, object]] = []
        for path in self.repo_root.glob("**/*.md"):
            if any(part.startswith(".") for part in path.parts):
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            if "status: proposed" not in text:
                continue
            if "Proof-of-Life" in text and "[x]" in text:
                candidates.append(
                    {
                        "path": path,
                        "status": "proposed",
                        "target_status": "approved",
                        "reason": "Proof-of-Life present",
                    }
                )
        return candidates

    def _apply_promotion(self, doc: dict[str, object]) -> bool:
        try:
            path = Path(doc["path"])
            content = path.read_text(encoding="utf-8")
            content = content.replace("status: proposed", "status: approved")
            path.write_text(content, encoding="utf-8")
            return True
        except Exception:
            return False


def promote_repo(repo_root: Path, apply: bool = False) -> dict[str, Any]:
    return AutoPromoter(repo_root).promote(apply=apply)
