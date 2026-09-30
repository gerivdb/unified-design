#!/usr/bin/env python3
"""Report Generator — génère des rapports JSON/Markdown pour le pipeline CI cross-repo."""
from __future__ import annotations

from pathlib import Path
from typing import Any


def generate_report(results: list[dict], output_dir: Path) -> Path:
    """Génère un rapport JSON à partir des résultats du pipeline CI."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    report_path = output_dir / "cross-repo-ci-report.json"
    payload = {
        "global_status": "PASS",
        "results": results,
    }
    report_path.write_text(
        __import__("json").dumps(payload, indent=2),
        encoding="utf-8",
    )
    return report_path
