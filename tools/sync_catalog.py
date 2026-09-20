#!/usr/bin/env python3
"""Sync catalog/*.index.yaml with unified-design filesystem."""
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


def discover_atoms(atoms_root: Path) -> dict[str, dict]:
    found = {}
    for path in atoms_root.rglob('*.yaml'):
        rel = path.relative_to(atoms_root)
        parts = list(rel.parts)
        if len(parts) >= 2 and parts[0] == 'L2-PLATFORM' and len(parts) == 2:
            atom_id = path.stem
        else:
            atom_id = '__'.join(parts).replace('/', '__').replace('\\', '__')
            atom_id = atom_id.replace(' ', '_')
        found[atom_id] = {
            'source_path': f'atoms/{rel.as_posix()}',
            'sha256': sha256(path),
        }
    return found


def discover_primitives(primitives_root: Path) -> dict[str, dict]:
    found = {}
    for path in primitives_root.rglob('*.yaml'):
        rel = path.relative_to(primitives_root)
        parts = list(rel.parts)
        if len(parts) >= 2 and parts[0] == 'L2-PLATFORM' and len(parts) == 2:
            primitive_id = path.stem
        else:
            primitive_id = '__'.join(parts).replace('/', '__').replace('\\', '__')
            primitive_id = primitive_id.replace(' ', '_')
        found[primitive_id] = {
            'source_path': f'primitives/{rel.as_posix()}',
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
        if isinstance(item, dict) and item.get('id'):
            entries[item.get('id')] = item
    return entries


def save_catalog(catalog_path: Path, entries: list[dict]) -> None:
    catalog_path.parent.mkdir(parents=True, exist_ok=True)
    with catalog_path.open('w', encoding='utf-8') as f:
        yaml.dump({'entries': entries}, f, sort_keys=False, allow_unicode=True)


def sync_catalog(dry_run: bool = False) -> int:
    repo_root = Path(__file__).resolve().parent.parent
    results = []

    # Sync designs
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
                'updated': '2026-09-21',
            }
            new_entries.append(entry)
            print(f'ADD design {design_id} -> {info["source_path"]}')
        else:
            new_entries.append(current[design_id])
    if not dry_run:
        save_catalog(catalog_path, new_entries)
    results.append(('designs', len(new_entries), len(found)))

    # Sync atoms
    atoms_root = repo_root / 'atoms'
    catalog_path = repo_root / 'catalog' / 'atoms.index.yaml'
    found = discover_atoms(atoms_root)
    current = load_catalog(catalog_path)
    new_entries = []
    for atom_id, info in found.items():
        if atom_id not in current:
            entry = {
                'id': atom_id,
                'source_path': info['source_path'],
                'source_repo': 'unified-design',
                'status': 'active',
                'type': 'atom',
                'updated': '2026-09-21',
            }
            new_entries.append(entry)
            print(f'ADD atom {atom_id} -> {info["source_path"]}')
        else:
            new_entries.append(current[atom_id])
    if not dry_run:
        save_catalog(catalog_path, new_entries)
    results.append(('atoms', len(new_entries), len(found)))

    # Sync primitives
    primitives_root = repo_root / 'primitives'
    catalog_path = repo_root / 'catalog' / 'primitives.index.yaml'
    found = discover_primitives(primitives_root)
    current = load_catalog(catalog_path)
    new_entries = []
    for primitive_id, info in found.items():
        if primitive_id not in current:
            entry = {
                'id': primitive_id,
                'source_path': info['source_path'],
                'source_repo': 'unified-design',
                'status': 'active',
                'type': 'primitive',
                'updated': '2026-09-21',
            }
            new_entries.append(entry)
            print(f'ADD primitive {primitive_id} -> {info["source_path"]}')
        else:
            new_entries.append(current[primitive_id])
    if not dry_run:
        save_catalog(catalog_path, new_entries)
    results.append(('primitives', len(new_entries), len(found)))

    if dry_run:
        for kind, total, disk in results:
            print(f'[DRY-RUN] {kind}: {total} entries, {disk} on disk')
    else:
        for kind, total, disk in results:
            print(f'[OK] {kind} catalog synced: {total} entries')
    return 0


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description='Sync catalog/*.index.yaml')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    return sync_catalog(dry_run=args.dry_run)


if __name__ == '__main__':
    raise SystemExit(main())
