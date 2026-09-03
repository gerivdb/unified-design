#!/usr/bin/env python3
"""Analyze and fix governance gaps in unified-design repo."""
import io, os, re, hashlib, yaml, glob, json
from collections import Counter

REPO_ROOT = os.getcwd()

# ============================================================
# 1. Validate JSON schemas
# ============================================================
print("=== 1. JSON Schema Validation ===")
schemas = [
    'schemas/design.schema.json',
    'schemas/meta-design.schema.json',
    'schemas/registry.schema.json',
]
for s in schemas:
    path = os.path.join(REPO_ROOT, s)
    try:
        with io.open(path, encoding='utf-8') as f:
            json.load(f)
        print(f"  {s}: VALID")
    except Exception as e:
        print(f"  {s}: INVALID - {e}")

# ============================================================
# 2. Analyze atoms_registry.yaml
# ============================================================
print("\n=== 2. atoms_registry.yaml Analysis ===")
reg_path = os.path.join(REPO_ROOT, 'atoms_registry.yaml')
with io.open(reg_path, encoding='utf-8') as f:
    data = yaml.safe_load(f)
atoms = data['atoms']
print(f"  Total atoms: {len(atoms)}")

# Duplicate paths
paths = [a['path'] for a in atoms]
path_dupes = {p: c for p, c in Counter(paths).items() if c > 1}
print(f"  Duplicate paths: {len(path_dupes)}")

# Duplicate hashes
hashes = [a['hash'] for a in atoms]
hash_dupes = {h: c for h, c in Counter(hashes).items() if c > 1}
print(f"  Duplicate hashes: {len(hash_dupes)}")
for h, count in hash_dupes.items():
    print(f"    {h}: {count} occurrences")

# Descriptions with embedded 'description:'
desc_issues = [i for i, a in enumerate(atoms) if str(a.get('description', '')).startswith('description:')]
print(f"  Descriptions starting with 'description:': {len(desc_issues)}")

# Missing files
missing = []
for i, a in enumerate(atoms):
    p = a['path']
    if not os.path.exists(os.path.join(REPO_ROOT, p)):
        missing.append((i, p))
print(f"  Missing files: {len(missing)}")
for i, p in missing:
    print(f"    [{i}] {p}")

# ============================================================
# 3. Analyze designs/**/*.yaml
# ============================================================
print("\n=== 3. designs/**/*.yaml Analysis ===")
non_cp1252_map = {
    0x2012: '-', 0x2013: '-', 0x2014: '-',
    0x2192: '->', 0x2194: '<->', 0x2190: '<-',
    0x2026: '...', 0x00A0: ' ',
}
design_issues = []
for f in sorted(glob.glob('designs/**/*.yaml', recursive=True)):
    fpath = os.path.join(REPO_ROOT, f)
    with io.open(fpath, encoding='utf-8') as fh:
        content = fh.read()
    
    # Check non-CP1252
    non_cp1252 = [(i, c) for i, c in enumerate(content) if ord(c) > 127 and ord(c) not in range(0x80, 0x100)]
    if non_cp1252:
        unique_chars = sorted(set(hex(ord(c)) for _, c in non_cp1252))
        design_issues.append((f, 'non-CP1252', unique_chars))
    
    # Check YAML parse (already validated above, but double-check)
    try:
        yaml.safe_load(content)
    except Exception as e:
        design_issues.append((f, 'yaml-error', str(e)))

print(f"  Files with issues: {len(design_issues)}")
for f, issue_type, detail in design_issues:
    print(f"  {f}: {issue_type} - {detail}")

# ============================================================
# 4. Check worktrees
# ============================================================
print("\n=== 4. Worktree Check ===")
result = os.popen('git worktree list --porcelain').read()
print(result)

# ============================================================
# 5. Check stash
# ============================================================
print("\n=== 5. Stash Check ===")
result = os.popen('git stash list').read()
print(result if result else "(no stashes)")
