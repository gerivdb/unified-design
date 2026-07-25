#!/usr/bin/env python3
"""
Validate YAML files, handling front matter blocks correctly.
Usage: python scripts/validate_yaml.py [--assert <key>] ... <pattern> [pattern ...]
"""
import sys
import yaml
import glob
from pathlib import Path


def load_yaml_frontmatter(path: str):
    content = Path(path).read_text(encoding="utf-8")
    parts = content.split("---", 2)
    if len(parts) >= 3:
        return yaml.safe_load(parts[1])
    return yaml.safe_load(content)


def validate_file(path: str, asserts: list[str]) -> bool:
    try:
        data = load_yaml_frontmatter(path)
    except Exception as e:
        print(f"FAIL {path}: {e}")
        return False

    for key in asserts:
        if isinstance(data, dict) and key not in data:
            print(f"FAIL {path}: Missing '{key}'")
            return False

    print(f"OK {path}")
    return True


def main() -> int:
    args = sys.argv[1:]
    asserts: list[str] = []
    patterns: list[str] = []

    i = 0
    while i < len(args):
        if args[i] == "--assert":
            if i + 1 >= len(args):
                print("Missing key after --assert")
                return 1
            asserts.append(args[i + 1])
            i += 2
        else:
            patterns.append(args[i])
            i += 1

    if not patterns:
        print("Usage: validate_yaml.py [--assert <key>] ... <pattern> [pattern ...]")
        return 1

    files = []
    for pattern in patterns:
        files.extend(glob.glob(pattern))

    failed = False
    for path in files:
        if not validate_file(path, asserts):
            failed = True

    if failed:
        return 1
    print(f"OK All {len(files)} YAML files valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
