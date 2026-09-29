"""Template: pr_factory.py — create PR artifacts for auto-design."""

from __future__ import annotations

from pathlib import Path


def create_pr(repo_root: Path, title: str, body: str) -> dict[str, object]:
    pr_dir = repo_root / "pr_artifacts"
    pr_dir.mkdir(exist_ok=True)
    (pr_dir / "title.txt").write_text(title, encoding="utf-8")
    (pr_dir / "body.md").write_text(body, encoding="utf-8")
    return {"repo": str(repo_root), "title": title, "status": "created"}


if __name__ == "__main__":
    import json
    print(json.dumps(create_pr(Path(".").resolve(), "auto-design", "auto-design industrialization"), ensure_ascii=False, indent=2))
