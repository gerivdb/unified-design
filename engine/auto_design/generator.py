"""Generate design.yaml, implementation_contract and bridges for a target repo."""

from __future__ import annotations

import yaml
from pathlib import Path
from typing import Any

TEMPLATE_DESIGN_YAML = """\
name: {repo_name}
version: "1.0.0"
status: active
intent_hash: 0x{intent_hash}
auto_design:
  components: {components}
  auto_debug_pathways:
    - observability
    - automation
    - infrastructure
  scientific_reflection_protocols: []
  cycle_runner_path: scripts/cycle_runner.py
  bridge_executor_path: scripts/bridge_executor.py
"""

TEMPLATE_IMPLEMENTATION_CONTRACT = """\
repo: {repo}
artifacts: []
verification:
  - command: python -m pytest tests/ -q
    expected: "passed"
"""

TEMPLATE_BRIDGE = """\
from: {from_repo}
to: {to_repo}
type: declarative
status: active
intent_hash: 0xBRIDGE_{from_slug}_{to_slug}
"""


class AutoDesignGenerator:
    def __init__(self, repo_root: Path) -> None:
        self.repo_root = Path(repo_root)
        self.repo_name = self.repo_root.name

    def generate(self, apply: bool = False) -> dict[str, Any]:
        components = self._detect_components()
        design_yaml = self._build_design_yaml(components)
        contracts = self._build_contracts(components)
        bridges = self._build_bridges(components)
        result = {
            "repo": str(self.repo_root),
            "design_yaml": design_yaml,
            "contracts": contracts,
            "bridges": bridges,
        }
        if apply:
            self._apply(result)
        return result

    def _detect_components(self) -> list[str]:
        components: list[str] = []
        for pattern in ("agents/*.py", "src/*.py", "scripts/*.py", "tools/**/*.py"):
            for path in self.repo_root.glob(pattern):
                if path.is_file():
                    components.append(path.stem)
        return sorted(set(components))[:20]

    def _classify_components_noded(self) -> dict[str, str]:
        """Classifie les composants via NODEX + KG-L, avec fallback heuristique."""
        try:
            import importlib.util
            script = r"D:\DO\WEB\TOOLS\L1-INFRA\ARGUS\scanners\nodex.py"
            spec = importlib.util.spec_from_file_location("nodex", script)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                classified = module.classify(str(self.repo_root))
                if isinstance(classified, dict):
                    return classified
        except Exception:
            pass

        components = self._detect_components()
        return {name: "unknown" for name in components}

    def _build_design_yaml(self, components: list[str]) -> str:
        intent_hash = f"{self.repo_name.upper()}_AUTO_DESIGN".replace("-", "_")
        return TEMPLATE_DESIGN_YAML.format(
            repo_name=self.repo_name,
            intent_hash=intent_hash,
            components=yaml.safe_dump(components, default_flow_style=False),
        )

    def _build_contracts(self, components: list[str]) -> dict[str, str]:
        return {name: TEMPLATE_IMPLEMENTATION_CONTRACT.format(repo=self.repo_name) for name in components}

    def _build_bridges(self, components: list[str]) -> list[str]:
        bridges: list[str] = []
        for i in range(min(len(components) - 1, 3)):
            bridges.append(
                TEMPLATE_BRIDGE.format(
                    from_repo=self.repo_name,
                    to_repo=self.repo_name,
                    from_slug=components[i].upper()[:10],
                    to_slug=components[i + 1].upper()[:10],
                )
            )
        return bridges

    @staticmethod
    def generate_commit_message(change_type: str, scope: str, description: str) -> str:
        """Génère un message de commit conventionnel."""
        valid_types = {"feat", "fix", "docs", "test", "refactor", "chore", "ci", "build", "revert", "style", "perf"}
        change_type = change_type.lower().strip()
        if change_type not in valid_types:
            raise ValueError(f"Invalid change_type: {change_type}. Must be one of {sorted(valid_types)}")
        scope = scope.strip()
        if scope:
            return f"{change_type}({scope}): {description.strip()}"
        return f"{change_type}: {description.strip()}"

    def generate_crm_tasks(self, registry_path: Path | None = None) -> list[dict[str, Any]]:
        """Génère des tickets CRM exploitables depuis le registry de dette."""
        registry = registry_path or Path(__file__).resolve().parents[3] / "crm" / "tech_debt_registry.yaml"
        if not registry.exists():
            return []
        try:
            with registry.open("r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
        except Exception:
            return []
        items = data.get("items", [])
        tickets: list[dict[str, Any]] = []
        for item in items:
            if item.get("status") != "open":
                continue
            tickets.append({
                "id": item.get("id"),
                "repo": item.get("repo"),
                "component": item.get("component"),
                "description": item.get("description"),
                "severity": item.get("severity"),
                "score": item.get("score"),
                "assignee": item.get("assignee"),
                "labels": item.get("labels", []),
                "type": "tech_debt",
                "created_at": item.get("created_at"),
            })
        return tickets

    def _apply(self, result: dict[str, Any]) -> None:
        design_path = self.repo_root / "design.yaml"
        design_path.parent.mkdir(parents=True, exist_ok=True)
        design_path.write_text(result["design_yaml"], encoding="utf-8")
        contracts_dir = self.repo_root / "implementation_contracts"
        contracts_dir.mkdir(parents=True, exist_ok=True)
        for name, content in result["contracts"].items():
            (contracts_dir / f"{name}.yaml").write_text(content, encoding="utf-8")
        bridges_dir = self.repo_root / "bridges"
        bridges_dir.mkdir(parents=True, exist_ok=True)
        for idx, content in enumerate(result["bridges"], start=1):
            (bridges_dir / f"bridge-{idx:03d}.yaml").write_text(content, encoding="utf-8")


def generate_repo(repo_root: Path, apply: bool = False) -> dict[str, Any]:
    return AutoDesignGenerator(repo_root).generate(apply=apply)
