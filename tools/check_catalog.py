#!/usr/bin/env python3
"""Validate catalog/designs.index.yaml against filesystem."""
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print('PyYAML is required for catalog validation', file=sys.stderr)
    sys.exit(2)


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    catalog_path = repo_root / 'catalog' / 'designs.index.yaml'
    if not catalog_path.exists():
        print(f'Missing catalog: {catalog_path}')
        return 1

    with catalog_path.open('r', encoding='utf-8') as f:
        catalog = yaml.safe_load(f) or {}

    entries = []
    raw = catalog.get('entries') or catalog
    if isinstance(raw, list):
        for item in raw:
            if isinstance(item, dict) and item.get('type') == 'design':
                entries.append(item)

    missing = []
    for entry in entries:
        source = entry.get('source_path')
        if not source:
            continue
        target = repo_root / source
        if not target.exists():
            missing.append((entry.get('id'), source))

    if missing:
        print('Catalog validation failed:')
        for entry_id, source in missing:
            print(f'  - missing file: {entry_id} -> {source}')
        return 1

    print(f'Catalog validation passed: {len(entries)} entries checked')
    return 0


if __name__ == '__main__':
    sys.exit(main())
