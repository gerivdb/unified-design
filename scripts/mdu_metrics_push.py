#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MDU Metrics Push — Push métriques vers Prometheus Pushgateway.

Usage:
    python mdu_metrics_push.py --gateway http://localhost:9091
    python mdu_metrics_push.py --gateway http://pushgateway:9091 --job mdu-orchestration
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Optional

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    requests = None

# Add project paths
UNIFIED_DESIGN_ROOT = Path(r"D:\DO\WEB\TOOLS\L0-CANON\unified-design")
sys.path.insert(0, str(UNIFIED_DESIGN_ROOT / "scripts"))

try:
    from compliance_scanner import check_repo_compliance  # type: ignore
    from mdu_compliance_scanner import load_catalog_designs, discover_repos_from_catalog
except ImportError:
    check_repo_compliance = None
    load_catalog_designs = None
    discover_repos_from_catalog = None


class MDU_MetricsPusher:
    """Push métriques MDU vers Prometheus Pushgateway."""
    
    def __init__(self, gateway_url: str, job_name: str = "mdu-orchestration"):
        if not REQUESTS_AVAILABLE:
            raise RuntimeError("requests module required for metrics push")
        
        self.gateway_url = gateway_url.rstrip("/")
        self.job_name = job_name
        self.push_url = f"{self.gateway_url}/metrics/job/{self.job_name}"
        
        print(f"[METRICS PUSH] Gateway: {self.gateway_url}, Job: {self.job_name}")
    
    def collect_metrics(self) -> dict[str, str]:
        """Collecte les métriques MDU au format Prometheus text."""
        lines = []
        timestamp = int(time.time() * 1000)
        
        # Métriques de base (toujours disponibles)
        lines.append(f"# HELP mdu_orchestration_timestamp Orchestration timestamp")
        lines.append(f"# TYPE mdu_orchestration_timestamp gauge")
        lines.append(f"mdu_orchestration_timestamp {timestamp}")
        
        lines.append(f"# HELP mdu_orchestration_status Orchestration status (1=success, 0=failed)")
        lines.append(f"# TYPE mdu_orchestration_status gauge")
        
        if check_repo_compliance and load_catalog_designs and discover_repos_from_catalog:
            try:
                catalog_path = Path(r"D:\DO\WEB\TOOLS\L0-CANON\unified-design\catalog\designs.index.yaml")
                catalog_designs = load_catalog_designs(catalog_path)
                repos = discover_repos_from_catalog(catalog_designs)
                
                total_repos = len(repos)
                compliant_repos = 0
                gap_counts = {}
                
                for repo in repos:
                    result = check_repo_compliance(repo)
                    if result.get("compliant", False):
                        compliant_repos += 1
                    for gap in result.get("gaps", []):
                        gap_counts[gap] = gap_counts.get(gap, 0) + 1
                
                lines.append(f"mdu_total_repos {total_repos}")
                lines.append(f"mdu_compliant_repos {compliant_repos}")
                lines.append(f"mdu_non_compliant_repos {total_repos - compliant_repos}")
                
                for gap_type, count in gap_counts.items():
                    lines.append(f'mdu_gaps_total{{gap_type="{gap_type}"}} {count}')
                
                # Status global
                status = 1 if compliant_repos == total_repos else 0
                lines.append(f"mdu_orchestration_status {status}")
                
            except Exception as e:
                print(f"[METRICS PUSH] Error collecting compliance metrics: {e}")
                lines.append("mdu_orchestration_status 0")
        else:
            lines.append("mdu_orchestration_status 0")
        
        return "\n".join(lines) + "\n"
    
    def push(self, metrics_text: str) -> bool:
        """Pousse les métriques vers Pushgateway."""
        try:
            headers = {"Content-Type": "text/plain; version=0.0.4"}
            response = requests.put(
                self.push_url,
                data=metrics_text.encode("utf-8"),
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            print(f"[METRICS PUSH] Successfully pushed to {self.push_url}")
            return True
        except Exception as e:
            print(f"[METRICS PUSH ERROR] Failed to push: {e}")
            return False


def main():
    parser = argparse.ArgumentParser(description="MDU Metrics Push to Prometheus Pushgateway")
    parser.add_argument("--gateway", required=True, help="Pushgateway URL (e.g., http://localhost:9091)")
    parser.add_argument("--job", default="mdu-orchestration", help="Job name for metrics")
    parser.add_argument("--instance", help="Instance label (default: hostname)")
    parser.add_argument("--dry-run", action="store_true", help="Print metrics without pushing")
    args = parser.parse_args()
    
    if not REQUESTS_AVAILABLE:
        print("[METRICS PUSH] ERROR: requests module not available")
        return 1
    
    try:
        pusher = MDU_MetricsPusher(args.gateway, args.job)
    except Exception as e:
        print(f"[METRICS PUSH] ERROR: {e}")
        return 1
    
    metrics_text = pusher.collect_metrics()
    
    if args.dry_run:
        print("[METRICS PUSH] DRY-RUN - Metrics to push:")
        print(metrics_text)
        return 0
    
    success = pusher.push(metrics_text)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())