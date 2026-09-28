#!/usr/bin/env python3
"""Analyser les gaps ACT-024b"""

import json
from pathlib import Path
from collections import defaultdict

REPORT_PATH = Path("D:/DO/WEB/TOOLS/L0-CANON/unified-design/ACT-024b-final-scan-report.json")
with open(REPORT_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

missing = [r for r in data["details"] if r["status"] == "MISSING"]
prd_only = [r for r in data["details"] if r["status"] == "PRD_MOC_ONLY"]

print(f"=== GAPS ACT-024b ===")
print(f"Total checks: {data['total_checks']}")
print(f"Implemented: {data['implemented']} ({data['coverage_pct']}%)")
print(f"Missing: {len(missing)}")
print(f"PRD-MOC only: {len(prd_only)}")
print()

by_design = defaultdict(list)
for r in missing + prd_only:
    by_design[r["design"]].append(r["consumer"])

print("=== GAPS PAR DESIGN ===")
for design, consumers in sorted(by_design.items()):
    print(f"{design}: {len(consumers)} consumers")
    for c in consumers:
        print(f"  - {c}")
    print()
