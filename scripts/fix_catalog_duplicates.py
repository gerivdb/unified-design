#!/usr/bin/env python3
"""
Correction des catalogues YAML : fusionne les sections entries dupliquées.
"""

import yaml
from pathlib import Path

REPO = Path(r"D:\DO\WEB\TOOLS\L0-CANON\unified-design")
CATALOG = REPO / "catalog" / "designs.index.yaml"

def fix_catalog(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Charger avec yaml.safe_load pour récupérer toutes les entrées
    data = yaml.safe_load(content)
    if not data or "entries" not in data:
        print(f"[SKIP] {path.name}: pas de section 'entries'")
        return

    entries = data["entries"]
    # Dédupliquer par (id, source_path)
    seen = set()
    unique_entries = []
    for entry in entries:
        key = (entry.get("id", "").lower(), entry.get("source_path", "").lower())
        if key not in seen:
            seen.add(key)
            unique_entries.append(entry)

    # Réécrire proprement
    data["entries"] = unique_entries
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False, default_flow_style=False)

    print(f"[FIX] {path.name}: {len(entries)} entrées -> {len(unique_entries)} uniques")


def main():
    print("Correction des catalogues YAML...")
    fix_catalog(CATALOG)


if __name__ == "__main__":
    main()
