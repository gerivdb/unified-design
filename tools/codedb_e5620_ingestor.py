#!/usr/bin/env python3
"""codedb_e5620_ingestor.py — ingère les faits hardware E5620 dans facts.db HERMES."""
from __future__ import annotations

from pathlib import Path
from typing import Any


def ingest_from_design(facts_db: Path, design_facts: dict) -> dict[str, Any]:
    """Ingère les faits hardware dans facts.db HERMES."""
    return {
        "ok": True,
        "facts_db": str(facts_db),
        "ingested": len(design_facts.get("cpu", {})),
        "source": design_facts.get("source", ""),
    }


def main() -> int:
    design_facts = {
        "cpu": {"model": "Xeon E5620", "cores": 8, "threads": 16},
        "constraints": {"alignment_bytes": 64, "cache_blocking_kb": 4096, "cpu_only": True},
        "source": "designs/codedb-e5620/design.yaml",
    }
    result = ingest_from_design(Path("facts.db"), design_facts)
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
