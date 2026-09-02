#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MDU State — Modèle d'état global MDU.

Usage:
    from mdu_state import MDUGlobalStatus, MDUState
    
    status = MDUGlobalStatus(
        state=MDUState.HEALTHY,
        total_repos=71,
        compliant_repos=71,
        ...
    )
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Optional
import json


class MDUState(Enum):
    """États globaux possibles de la conformité MDU."""
    HEALTHY = "healthy"           # Tous repos compliant
    DEGRADED = "degraded"         # Certains repos non-compliant (warnings)
    CRITICAL = "critical"         # Repos critiques non-compliant (P0)
    REMEDIATING = "remediating"   # Auto-remediation en cours
    RECOVERING = "recovering"     # Post-remediation validation
    UNKNOWN = "unknown"           # État indéterminé


@dataclass
class MDUGlobalStatus:
    """État global de la conformité MDU."""
    state: MDUState
    timestamp: datetime = field(default_factory=datetime.utcnow)
    total_repos: int = 0
    compliant_repos: int = 0
    critical_gaps: list[str] = field(default_factory=list)
    warning_gaps: list[str] = field(default_factory=list)
    last_orchestration_run: Optional[datetime] = None
    last_successful_run: Optional[datetime] = None
    remediation_in_progress: bool = False
    orchestration_version: str = "1.0.0"
    
    def __post_init__(self):
        if isinstance(self.state, str):
            self.state = MDUState(self.state)
        if isinstance(self.timestamp, str):
            self.timestamp = datetime.fromisoformat(self.timestamp.replace("Z", "+00:00"))
        if self.last_orchestration_run and isinstance(self.last_orchestration_run, str):
            self.last_orchestration_run = datetime.fromisoformat(self.last_orchestration_run.replace("Z", "+00:00"))
        if self.last_successful_run and isinstance(self.last_successful_run, str):
            self.last_successful_run = datetime.fromisoformat(self.last_successful_run.replace("Z", "+00:00"))
    
    @property
    def compliance_rate(self) -> float:
        """Taux de conformité en pourcentage."""
        if self.total_repos == 0:
            return 0.0
        return (self.compliant_repos / self.total_repos) * 100
    
    @property
    def is_healthy(self) -> bool:
        return self.state == MDUState.HEALTHY
    
    @property
    def needs_attention(self) -> bool:
        return self.state in (MDUState.CRITICAL, MDUState.DEGRADED)
    
    def to_dict(self) -> dict:
        """Sérialise en dictionnaire."""
        return {
            "state": self.state.value,
            "timestamp": self.timestamp.isoformat() + "Z",
            "total_repos": self.total_repos,
            "compliant_repos": self.compliant_repos,
            "compliance_rate": self.compliance_rate,
            "critical_gaps": self.critical_gaps,
            "warning_gaps": self.warning_gaps,
            "last_orchestration_run": self.last_orchestration_run.isoformat() + "Z" if self.last_orchestration_run else None,
            "last_successful_run": self.last_successful_run.isoformat() + "Z" if self.last_successful_run else None,
            "remediation_in_progress": self.remediation_in_progress,
            "orchestration_version": self.orchestration_version,
        }
    
    def to_json(self) -> str:
        """Sérialise en JSON."""
        return json.dumps(self.to_dict(), ensure_ascii=False)
    
    @classmethod
    def from_dict(cls, data: dict) -> "MDUGlobalStatus":
        """Crée une instance depuis un dictionnaire."""
        return cls(**data)
    
    @classmethod
    def from_json(cls, json_str: str) -> "MDUGlobalStatus":
        """Crée une instance depuis JSON."""
        return cls.from_dict(json.loads(json_str))
    
    @classmethod
    def from_compliance_scan(cls, scan_result: dict) -> "MDUGlobalStatus":
        """Crée un état depuis un résultat de scan de conformité."""
        total = scan_result.get("total_repos", 0)
        compliant = scan_result.get("compliant_repos", 0)
        
        critical_gaps = []
        warning_gaps = []
        
        for repo, result in scan_result.get("results", {}).items():
            for gap in result.get("gaps", []):
                if gap in {"design_registered", "citizen_registered"}:
                    critical_gaps.append(f"{repo}:{gap}")
                else:
                    warning_gaps.append(f"{repo}:{gap}")
        
        if total == 0:
            state = MDUState.UNKNOWN
        elif compliant == total:
            state = MDUState.HEALTHY
        elif critical_gaps:
            state = MDUState.CRITICAL
        elif warning_gaps:
            state = MDUState.DEGRADED
        else:
            state = MDUState.HEALTHY
        
        return cls(
            state=state,
            total_repos=total,
            compliant_repos=compliant,
            critical_gaps=critical_gaps,
            warning_gaps=warning_gaps,
        )
    
    def save(self, path: Path):
        """Sauvegarde l'état dans un fichier JSON."""
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(self.to_json(), encoding="utf-8")
    
    @classmethod
    def load(cls, path: Path) -> Optional["MDUGlobalStatus"]:
        """Charge l'état depuis un fichier JSON."""
        if not path.exists():
            return None
        return cls.from_json(path.read_text(encoding="utf-8"))


# Fichier d'état par défaut
DEFAULT_STATE_PATH = Path(r"D:\DO\WEB\TOOLS\L0-CANON\unified-design\.mdu\state.json")


def get_current_state() -> MDUGlobalStatus:
    """Récupère l'état actuel (depuis fichier ou scan)."""
    # Essayer de charger depuis fichier
    state = MDUGlobalStatus.load(DEFAULT_STATE_PATH)
    if state:
        return state
    
    # Sinon générer depuis scan
    try:
        from compliance_scanner import check_repo_compliance  # type: ignore
        from mdu_compliance_scanner import load_catalog_designs, discover_repos_from_catalog
        
        catalog_path = Path(r"D:\DO\WEB\TOOLS\L0-CANON\unified-design\catalog\designs.index.yaml")
        catalog_designs = load_catalog_designs(catalog_path)
        repos = discover_repos_from_catalog(catalog_designs)
        
        scan_result = {"total_repos": len(repos), "compliant_repos": 0, "results": {}}
        for repo in repos:
            result = check_repo_compliance(repo)
            scan_result["results"][repo] = result
            if result.get("compliant", False):
                scan_result["compliant_repos"] += 1
        
        return MDUGlobalStatus.from_compliance_scan(scan_result)
    except Exception:
        return MDUGlobalStatus(
            state=MDUState.UNKNOWN,
            total_repos=0,
            compliant_repos=0,
        )


if __name__ == "__main__":
    # Test
    state = get_current_state()
    print(json.dumps(state.to_dict(), indent=2, ensure_ascii=False))