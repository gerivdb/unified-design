#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MDU WAL Emitter Standalone — Émission événements WAL pour l'orchestration.

Usage:
    python mdu_wal_emitter.py --event MDU_ORCHESTRATION_COMPLETE --payload '{"status":"success"}'
    python mdu_wal_emitter.py --event MDU_DRIFT_DETECTED --payload-file /tmp/drift.json
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Optional

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


class MDU_WAL_Emitter:
    """Émetteur d'événements WAL standalone."""
    
    def __init__(self, config: Optional[dict] = None):
        self.config = config or {}
        wal_config = self.config.get("wal", {})
        
        self.enabled = wal_config.get("enabled", True)
        self.endpoint = wal_config.get("endpoint", "")
        self.wal_dir = Path(wal_config.get("wal_dir", r"D:\DO\WEB\TOOLS\L1-INFRA\ARGUS\wal"))
        self.wal_dir.mkdir(parents=True, exist_ok=True)
        
        self.session_id = f"mdu-orchestration-{int(time.time())}-{os.getpid()}"
        
        print(f"[WAL] Emitter initialized: session={self.session_id}, dir={self.wal_dir}")
        if self.endpoint:
            print(f"[WAL] Remote endpoint: {self.endpoint}")
    
    def emit(self, event_type: str, payload: dict, metadata: Optional[dict] = None) -> bool:
        """Émet un événement WAL."""
        if not self.enabled:
            print("[WAL] Emitter disabled")
            return True
        
        event = {
            "event_type": event_type,
            "source": "mdu-orchestration",
            "session_id": self.session_id,
            "timestamp": time.time(),
            "timestamp_iso": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "payload": payload,
            "metadata": metadata or {},
        }
        
        success = True
        
        # 1. File-based WAL (toujours)
        try:
            self._write_file_wal(event)
        except Exception as e:
            print(f"[WAL ERROR] File write failed: {e}")
            success = False
        
        # 2. Remote endpoint (si configuré)
        if self.endpoint and REQUESTS_AVAILABLE:
            try:
                self._post_remote(event)
            except Exception as e:
                print(f"[WAL WARN] Remote post failed: {e}")
        
        return success
    
    def _write_file_wal(self, event: dict):
        """Écrit l'événement dans un fichier WAL local (JSONL, rotation journalière)."""
        date_str = time.strftime("%Y-%m-%d", time.gmtime(event["timestamp"]))
        wal_file = self.wal_dir / f"mdu_events_{date_str}.jsonl"
        
        with wal_file.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")
        
        print(f"[WAL] Event written to {wal_file}: {event['event_type']}")
    
    def _post_remote(self, event: dict):
        """Poste l'événement vers l'endpoint remote."""
        import requests
        response = requests.post(
            self.endpoint,
            json=event,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        response.raise_for_status()
        print(f"[WAL] Event posted to {self.endpoint}")


def main():
    parser = argparse.ArgumentParser(description="MDU WAL Emitter Standalone")
    parser.add_argument("--event", required=True, help="Event type (e.g., MDU_ORCHESTRATION_COMPLETE)")
    parser.add_argument("--payload", help="JSON payload string")
    parser.add_argument("--payload-file", type=Path, help="Path to JSON payload file")
    parser.add_argument("--metadata", help="JSON metadata string")
    parser.add_argument("--config", type=Path, help="Config YAML file")
    parser.add_argument("--wal-dir", type=Path, help="WAL directory override")
    parser.add_argument("--endpoint", help="Remote endpoint override")
    parser.add_argument("--enabled", action="store_true", default=True, help="Enable WAL emitter")
    parser.add_argument("--disabled", action="store_true", help="Disable WAL emitter")
    args = parser.parse_args()
    
    # Load config
    config = {"wal": {"enabled": args.enabled and not args.disabled}}
    if args.config:
        import yaml
        with args.config.open("r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
    
    if args.wal_dir:
        config.setdefault("wal", {})["wal_dir"] = str(args.wal_dir)
    if args.endpoint:
        config.setdefault("wal", {})["endpoint"] = args.endpoint
    
    # Parse payload
    if args.payload_file:
        with args.payload_file.open("r", encoding="utf-8") as f:
            payload = json.load(f)
    elif args.payload:
        payload = json.loads(args.payload)
    else:
        payload = {}
    
    metadata = json.loads(args.metadata) if args.metadata else {}
    
    emitter = MDU_WAL_Emitter(config)
    success = emitter.emit(args.event, payload, metadata)
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())