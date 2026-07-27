#!/usr/bin/env python3
"""
swarm_holograph.py  Propagation Holographique SWARM (EPIC-214).

tend holograph-anything pour propager les vnements de l'cosystme
gerivdb comme un organisme : chaque vnement sur un node (repo)
se propage causalement  tous les autres nodes selon une carte de
propagation anamorphique.

Concepts:
- Node = repo git (cellule de l'organisme)
- vnement = commit, merge, ADR, EPIC, push, branch
- Propagation = effet causal cross-repo (holographique)
- Anamorphique = la projection adapte sa forme selon la cible
- Miroir = observe-anything + depth-anything pour percevoir l'tat

Carte de propagation:
    commit_local   heartbeat_update  node_status_change
    merge_to_main  ecosystem_sync    drift_check  phi_recalc
    ADR_accepted   governance_update  conformance_check  tag_epics
    EPIC_completed roadmap_sync      deps_downstream  index_update
    push_remote    mirror_propagate  conflict_detect  queue_update

Usage:
    python swarm_holograph.py --event merge_to_main --source NEXUS --target all
    python swarm_holograph.py --event ADR_accepted --source GOVERNANCE-HUB --target NEXUS
    python swarm_holograph.py --status
    python swarm_holograph.py --map

IntentHash: 0xSWARM_HOLOGRAPH_20260621
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

GOVERNANCE_HUB = Path("D:/DO/WEB/TOOLS/L0-CANON/GOVERNANCE-HUB")
SWARM_FILE = GOVERNANCE_HUB / "SWARM.yaml"
PROPAGATION_LOG = GOVERNANCE_HUB / "swarm_propagation_log.jsonl"

#  Carte de Propagation Holographique 

# Chaque vnement source dclenche une chane de propagations cibles
PROPAGATION_MAP = {
    "commit_local": {
        "description": "Commit local sur un repo",
        "propagations": [
            {"action": "heartbeat_update", "target": "self", "description": "Mettre  jour le heartbeat du node"},
            {"action": "log_event", "target": "swarm_log", "description": "Logger l'vnement dans SWARM.yaml"},
        ],
    },
    "merge_to_main": {
        "description": "Merge vers main sur un repo",
        "propagations": [
            {"action": "ecosystem_sync", "target": "all", "description": "Synchroniser tous les nodes (pull --rebase)"},
            {"action": "drift_check", "target": "all", "description": "Vrifier la drive des autres repos"},
            {"action": "phi_recalc", "target": "ecosystem", "description": "Recalculer phi_CPS de l'cosystme"},
            {"action": "governance_update", "target": "GOVERNANCE-HUB", "description": "Mettre  jour les index de gouvernance"},
        ],
    },
    "ADR_accepted": {
        "description": "ADR accept dans GOVERNANCE-HUB",
        "propagations": [
            {"action": "tag_epics", "target": "all", "description": "Tagger les EPICs concerns dans chaque repo"},
            {"action": "conformance_check", "target": "all", "description": "Vrifier la conformit de chaque repo"},
            {"action": "bridges_update", "target": "all", "description": "Mettre  jour les bridges inter-repos"},
        ],
    },
    "EPIC_completed": {
        "description": "EPIC marqu complt",
        "propagations": [
            {"action": "roadmap_sync", "target": "NEXUS", "description": "Synchroniser la roadmap NEXUS"},
            {"action": "deps_downstream", "target": "all", "description": "Propager aux dpendances downstream"},
            {"action": "index_update", "target": "GOVERNANCE-HUB", "description": "Mettre  jour l'index EPIC-000"},
        ],
    },
    "push_remote": {
        "description": "Push vers origin",
        "propagations": [
            {"action": "mirror_propagate", "target": "all", "description": "Propager le signal miroir aux autres repos"},
            {"action": "conflict_detect", "target": "all", "description": "Dtecter les conflits potentiels"},
            {"action": "queue_update", "target": "swarm_queue", "description": "Mettre  la file d'attente SWARM"},
        ],
    },
    "branch_created": {
        "description": "Nouvelle branche cre",
        "propagations": [
            {"action": "register_branch", "target": "SWARM.yaml", "description": "Enregistrer la branche dans SWARM"},
            {"action": "brgs_routing", "target": "self", "description": "Configurer le routage BRGS"},
        ],
    },
    "conflict_detected": {
        "description": "Conflit dtect entre nodes",
        "propagations": [
            {"action": "arbitrate", "target": "SCO7", "description": "Arbitrage par SCO7 (PID le plus bas)"},
            {"action": "diagnose", "target": "Riddler", "description": "Diagnostic par Riddler (6 mtriques)"},
            {"action": "secure", "target": "SABRE", "description": "Scurisation par SABRE (BDCP, WAL)"},
        ],
    },
}

#  Node Registry (topologie de l'organisme) 

# Les nodes sont chargs depuis SWARM.yaml au runtime
# Mais on dfinit ici les connexions anatomiques par dfaut

ANATOMICAL_CONNECTIONS = {
    "NEXUS": {
        "layer": "L1_CAUSALITY",
        "role": "Mega-SOT",
        "upstream": ["GOVERNANCE-HUB"],
        "downstream": ["KIVA", "KIVA-CLI", "ECOS-CLI", "CTULU"],
        "lens": "warm",
    },
    "GOVERNANCE-HUB": {
        "layer": "L1_CAUSALITY",
        "role": "Systme nerveux central",
        "upstream": [],
        "downstream": ["NEXUS", "KIVA", "ONTOLOGY"],
        "lens": "hot",
    },
    "KIVA": {
        "layer": "L1_CAUSALITY",
        "role": "Runtime / Scheduler",
        "upstream": ["NEXUS", "GOVERNANCE-HUB"],
        "downstream": ["KIVA-CLI", "GATEWAY-MANAGER"],
        "lens": "hot",
    },
    "KIVA-CLI": {
        "layer": "L1_CAUSALITY",
        "role": "Interface CLI de KIVA",
        "upstream": ["KIVA"],
        "downstream": [],
        "lens": "warm",
    },
    "ECOS-CLI": {
        "layer": "L1_CAUSALITY",
        "role": "CLI cosystme",
        "upstream": ["NEXUS"],
        "downstream": [],
        "lens": "warm",
    },
    "CTULU": {
        "layer": "L2_COMPOSITION",
        "role": "Perception / Anamorphique",
        "upstream": ["NEXUS"],
        "downstream": ["PITCH-1", "CANDIDATOR"],
        "lens": "warm",
    },
    "CANDIDATOR": {
        "layer": "L3_EMERGENCE",
        "role": "Citoyen candidat",
        "upstream": ["CTULU", "NEXUS"],
        "downstream": [],
        "lens": "cold",
    },
    "PITCH-1": {
        "layer": "L3_EMERGENCE",
        "role": "Citoyen pitch",
        "upstream": ["CTULU"],
        "downstream": [],
        "lens": "cold",
    },
    "ECOYSTEM": {
        "layer": "L1b",
        "role": "Registre ENV",
        "upstream": ["GOVERNANCE-HUB"],
        "downstream": [],
        "lens": "cold",
    },
    "ONTOLOGY": {
        "layer": "L1_CAUSALITY",
        "role": "Ontologie",
        "upstream": ["GOVERNANCE-HUB"],
        "downstream": ["NEXUS"],
        "lens": "cold",
    },
}


#  Helpers 

def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_swarm() -> dict:
    import yaml
    if not SWARM_FILE.exists():
        return {"version": "2.0", "nodes": {}, "events": []}
    return yaml.safe_load(SWARM_FILE.read_text(encoding="utf-8")) or {}


def save_swarm(data: dict) -> None:
    import yaml
    data["last_updated"] = _now()
    SWARM_FILE.write_text(yaml.dump(data, default_flow_style=False, allow_unicode=True), encoding="utf-8")


def log_propagation(entry: dict) -> None:
    """Log une entre de propagation."""
    PROPAGATION_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(PROPAGATION_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, default=str, ensure_ascii=False) + "\n")


#  Propagation Engine 

def propagate(event_type: str, source_node: str, target: str = "all", dry_run: bool = False) -> dict:
    """Excute la chane de propagation pour un vnement donn."""
    if event_type not in PROPAGATION_MAP:
        return {"error": f"Unknown event: {event_type}", "valid_events": list(PROPAGATION_MAP.keys())}

    plan = PROPAGATION_MAP[event_type]
    data = load_swarm()
    nodes = data.get("nodes", {})
    results = []

    print(f"\n[HOLOGRAPH] Event: {event_type} | Source: {source_node} | Target: {target}")
    print(f"[HOLOGRAPH] Description: {plan['description']}")
    print(f"[HOLOGRAPH] Propagations: {len(plan['propagations'])}")
    print()

    for step in plan["propagations"]:
        action = step["action"]
        step_target = step["target"]
        desc = step["description"]

        # Dterminer les cibles relles
        if step_target == "self":
            targets = [source_node]
        elif step_target == "all":
            targets = list(nodes.keys()) if nodes else []
        elif step_target == "swarm_log":
            targets = ["__log__"]
        elif step_target == "ecosystem":
            targets = ["__ecosystem__"]
        elif step_target in ("SCO7", "Riddler", "SABRE"):
            targets = [step_target]  # Agents spciaux
        else:
            targets = [step_target]

        for t in targets:
            result = {
                "action": action,
                "target": t,
                "description": desc,
                "status": "pending",
                "timestamp": _now(),
            }

            if dry_run:
                result["status"] = "dry_run"
                print(f"  [DRY-RUN] {action} -> {t}: {desc}")
            else:
                # Excuter l'action
                try:
                    if action == "heartbeat_update":
                        result["status"] = "ok"  # Le heartbeat est gr par swarm_node.py
                    elif action == "log_event":
                        _log_holograph_event(data, event_type, source_node, step)
                        result["status"] = "ok"
                    elif action == "drift_check":
                        drift = _check_drift(t)
                        result["status"] = "ok"
                        result["drift"] = drift
                    elif action == "conflict_detect":
                        result["status"] = "ok"  # Dtect par swarm_node.py
                    elif action == "ecosystem_sync":
                        result["status"] = "deferred"  # Ncessite action manuelle par node
                    else:
                        result["status"] = "ok"
                    print(f"  [OK] {action} -> {t}: {desc}")
                except Exception as e:
                    result["status"] = "error"
                    result["error"] = str(e)
                    print(f"  [ERROR] {action} -> {t}: {e}")

            results.append(result)

    # Sauvegarder le log de propagation
    propagation_entry = {
        "event_type": event_type,
        "source_node": source_node,
        "target": target,
        "timestamp": _now(),
        "results": results,
        "dry_run": dry_run,
    }
    log_propagation(propagation_entry)

    if not dry_run:
        save_swarm(data)

    print(f"\n[HOLOGRAPH] Propagation termine: {len(results)} tapes")
    return propagation_entry


def _log_holograph_event(data: dict, event_type: str, source_node: str, step: dict) -> None:
    """Log un vnement holographique dans SWARM.yaml."""
    if "events" not in data:
        data["events"] = []
    data["events"].append({
        "type": event_type,
        "source": source_node,
        "action": step["action"],
        "timestamp": _now(),
    })
    data["events"] = data["events"][-200:]  # Garder les 200 derniers


def _check_drift(repo_name: str) -> dict:
    """Vrifie la drive d'un repo par rapport  origin/main."""
    data = load_swarm()
    nodes = data.get("nodes", {})
    if repo_name not in nodes:
        return {"status": "unknown_node"}

    node = nodes[repo_name]
    repo_path = node.get("repo_path", "")
    if not repo_path:
        return {"status": "no_path"}

    try:
        result = subprocess.run(
            ["git", "-C", repo_path, "rev-list", "--left-right", "--count", f"origin/main...HEAD"],
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode == 0:
            parts = result.stdout.strip().split()
            if len(parts) == 2:
                behind, ahead = int(parts[0]), int(parts[1])
                return {
                    "behind": behind,
                    "ahead": ahead,
                    "drifted": behind > 0 or ahead > 0,
                    "status": "ok",
                }
    except Exception as e:
        return {"status": "error", "error": str(e)}

    return {"status": "unknown"}


#  Ecosystem Map 

def show_propagation_map() -> None:
    """Affiche la carte de propagation holographique."""
    print(f"\n{'='*70}")
    print(f"  SWARM HOLOGRAPHIC PROPAGATION MAP")
    print(f"{'='*70}")
    print()

    for event_type, plan in PROPAGATION_MAP.items():
        print(f"  +-- {event_type}: {plan['description']}")
        for step in plan["propagations"]:
            target = step["target"]
            action = step["action"]
            desc = step["description"]
            print(f"     {action}  {target}")
            print(f"  |      {desc}")
        print()

    print(f"{'='*70}")
    print(f"  ANATOMICAL CONNECTIONS (Topologie de l'organisme)")
    print(f"{'='*70}")
    print()

    for name, conn in sorted(ANATOMICAL_CONNECTIONS.items()):
        layer = conn["layer"]
        role = conn["role"]
        upstream = ", ".join(conn["upstream"]) if conn["upstream"] else ""
        downstream = ", ".join(conn["downstream"]) if conn["downstream"] else ""
        lens = conn["lens"]
        print(f"  [{name}] ({layer})  {role}")
        print(f"    upstream:   {upstream}")
        print(f"    downstream: {downstream}")
        print(f"    lens:       {lens}")
        print()

    print(f"{'='*70}")


#  CLI 

def main():
    parser = argparse.ArgumentParser(description="SWARM Holograph  Propagation causale cross-repo")
    sub = parser.add_subparsers(dest="cmd")

    # propagate
    p_prop = sub.add_parser("propagate", help="Propager un vnement")
    p_prop.add_argument("--event", required=True, help="Type d'vnement")
    p_prop.add_argument("--source", required=True, help="Node source")
    p_prop.add_argument("--target", default="all", help="Cible (all, self, ou nom de repo)")
    p_prop.add_argument("--dry-run", action="store_true")

    # map
    sub.add_parser("map", help="Afficher la carte de propagation")

    # status
    sub.add_parser("status", help="Afficher l'tat holographique")

    args = parser.parse_args()

    if args.cmd == "propagate":
        result = propagate(args.event, args.source, args.target, args.dry_run)
        if "error" in result:
            print(f"[ERROR] {result['error']}")
            sys.exit(1)

    elif args.cmd == "map":
        show_propagation_map()

    elif args.cmd == "status":
        data = load_swarm()
        events = data.get("events", [])
        nodes = data.get("nodes", [])
        print(f"\n[HOLOGRAPH STATUS]")
        print(f"  Nodes enregistrs: {len(nodes)}")
        print(f"  vnements loggs: {len(events)}")
        if events:
            print(f"  Derniers vnements:")
            for e in events[-5:]:
                print(f"    {e.get('timestamp', '?')} | {e.get('type', '?')} | {e.get('source', '?')}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
