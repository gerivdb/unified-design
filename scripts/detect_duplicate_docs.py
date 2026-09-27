#!/usr/bin/env python3
"""
detect_duplicate_docs.py — Détecte les documents dupliqués dans unified-design.

Compare les fichiers par nom et par contenu pour identifier les doublons.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"


def file_hash(path: Path) -> str:
    """Calcule le hash MD5 d'un fichier."""
    h = hashlib.md5()
    h.update(path.read_bytes())
    return h.hexdigest()


def find_duplicates_by_name(root: Path) -> dict[str, list[Path]]:
    """Trouve les fichiers avec le même nom dans des répertoires différents.
    Exclut .kilo, node_modules, __pycache__, .git, .pytest_cache.
    """
    exclude_dirs = {".kilo", "node_modules", "__pycache__", ".git", ".pytest_cache"}
    by_name: dict[str, list[Path]] = {}
    for path in root.rglob("*"):
        if path.is_file() and not path.name.startswith("."):
            if any(excluded in path.parts for excluded in exclude_dirs):
                continue
            by_name.setdefault(path.name, []).append(path)
    return {name: paths for name, paths in by_name.items() if len(paths) > 1}


def find_duplicates_by_content(root: Path) -> dict[str, list[Path]]:
    """Trouve les fichiers avec le même contenu.
    Exclut .kilo, node_modules, __pycache__, .git, .pytest_cache.
    """
    exclude_dirs = {".kilo", "node_modules", "__pycache__", ".git", ".pytest_cache"}
    by_hash: dict[str, list[Path]] = {}
    for path in root.rglob("*"):
        if path.is_file() and not path.name.startswith("."):
            if any(excluded in path.parts for excluded in exclude_dirs):
                continue
            try:
                h = file_hash(path)
                by_hash.setdefault(h, []).append(path)
            except Exception:
                continue
    return {h: paths for h, paths in by_hash.items() if len(paths) > 1}


def main() -> int:
    parser = argparse.ArgumentParser(description="Detect duplicate docs")
    parser.add_argument("--by-content", action="store_true", help="Detect duplicates by content")
    args = parser.parse_args()

    if args.by_content:
        duplicates = find_duplicates_by_content(REPO_ROOT)
        print(f"[INFO] Found {len(duplicates)} sets of duplicate files by content")
        for h, paths in duplicates.items():
            print(f"  Hash {h}:")
            for p in paths:
                print(f"    - {p.relative_to(REPO_ROOT)}")
    else:
        duplicates = find_duplicates_by_name(REPO_ROOT)
        print(f"[INFO] Found {len(duplicates)} sets of duplicate files by name")
        for name, paths in duplicates.items():
            print(f"  {name}:")
            for p in paths:
                print(f"    - {p.relative_to(REPO_ROOT)}")

    if duplicates:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
