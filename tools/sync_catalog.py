#!/usr/bin/env python3
"""Sync catalog/designs.index.yaml with unified-design filesystem."""
from __future__ import annotations

import hashlib
from pathlib import Path

try:
    import yaml
except ImportError:
    print('PyYAML is required for catalog sync', __import__('sys').stderr)
    __import__('sys').exit(2)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()


def discover_designs(designs_root: Path) -> dict[str, dict]:
    found = {}
    for path in designs_root.rglob('*.yaml'):
        rel = path.relative_to(designs_root)
        parts = list(rel.parts)
        if len(parts) >= 2 and parts[0] == 'L2-PLATFORM' and len(parts) == 2:
            design_id = path.stem
        else:
            design_id = '__'.join(parts).replace('/', '__').replace('\\', '__')
            design_id = design_id.replace(' ', '_')
        found[design_id] = {
            'source_path': f'designs/{rel.as_posix()}',
            'sha256': sha256(path),
        }
    return found


def load_catalog(catalog_path: Path) -> dict[str, dict]:
    if not catalog_path.exists():
        return {}
    with catalog_path.open('r', encoding='utf-8') as f:
        data = yaml.safe_load(f) or {}
    entries = {}
    for item in data.get('entries', []):
        if isinstance(item, dict) and item.get('type') == 'design':
            entries[item.get('id')] = item
    return entries


def save_catalog(catalog_path: Path, entries: list[dict]) -> None:
    catalog_path.parent.mkdir(parents=True, exist_ok=True)
    with catalog_path.open('w', encoding='utf-8') as f:
        yaml.dump({'entries': entries}, f, sort_keys=False, allow_unicode=True)


def sync_catalog(dry_run: bool = False) -> int:
    repo_root = Path(__file__).resolve().parent.parent
    designs_root = repo_root / 'designs'
    catalog_path = repo_root / 'catalog' / 'designs.index.yaml'

    found = discover_designs(designs_root)
    current = load_catalog(catalog_path)

    new_entries = []
    for design_id, info in found.items():
        if design_id not in current:
            entry = {
                'id': design_id,
                'source_path': info['source_path'],
                'source_repo': 'unified-design',
                'status': 'active',
                'type': 'design',
                'updated': '2026-09-20',
            }
            new_entries.append(entry)
            print(f'ADD {design_id} -> {info["source_path"]}')
        else:
            new_entries.append(current[design_id])

    if dry_run:
        print(f'[DRY-RUN] {len(new_entries)} entries, {len(found)} designs on disk')
        return 0

    save_catalog(catalog_path, new_entries)
    print(f'[OK] Catalog synced: {len(new_entries)} entries')
    return 0


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description='Sync catalog/designs.index.yaml')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    return sync_catalog(dry_run=args.dry_run)


if __name__ == '__main__':
    raise SystemExit(main())
