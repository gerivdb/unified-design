"""Design validator for unified-design."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


class DesignValidator:
    def __init__(self, root: Path):
        self.root = root
        self.schema_path = self.root / "schemas" / "design.schema.json"
        self._schema = None
        self._atom_cache: set[str] | None = None

    @property
    def schema(self) -> dict[str, Any]:
        if self._schema is None and self.schema_path.exists():
            with open(self.schema_path, "r", encoding="utf-8") as f:
                self._schema = json.load(f)
        return self._schema or {}

    def _get_atom_stems(self) -> set[str]:
        if self._atom_cache is None:
            atoms_dir = self.root / "atoms"
            self._atom_cache = set()
            if atoms_dir.exists():
                for path in atoms_dir.rglob("*"):
                    if path.is_file() and path.suffix in (".md", ".yaml", ".yml"):
                        self._atom_cache.add(path.stem)
        return self._atom_cache

    def validate(self, design: dict[str, Any]) -> list[str]:
        errors: list[str] = []

        # Basic required fields
        if "name" not in design:
            errors.append("missing required field: name")
        if "version" not in design:
            errors.append("missing required field: version")
        if "status" not in design:
            errors.append("missing required field: status")
        if "layer" not in design:
            errors.append("missing required field: layer")
        if "intent_hash" not in design:
            errors.append("missing required field: intent_hash")

        # Universal naming: name must be lowercase + hyphens only
        name = design.get("name", "")
        if name and not re.fullmatch(r"[a-z0-9-]+", name):
            errors.append(
                f"non-universal design name: '{name}' (must be lowercase + hyphens only)"
            )

        # No repo-specific references in name
        if "/" in name or "\\" in name:
            errors.append(
                f"repo-specific path in design name: '{name}'"
            )

        # depends_on validation
        depends_on = design.get("depends_on", [])
        if not isinstance(depends_on, list):
            errors.append("depends_on must be a list")
        else:
            atom_stems = self._get_atom_stems()
            for dep in depends_on:
                if not isinstance(dep, str):
                    errors.append(f"depends_on entry must be string: {dep}")
                    continue
                if not re.fullmatch(r"ATOM-[0-9]+-[a-z0-9-]+", dep):
                    errors.append(
                        f"invalid depends_on atom id: '{dep}' (expected ATOM-NNN-slug)"
                    )
                elif dep not in atom_stems:
                    errors.append(f"depends_on atom not found: {dep}")

        # bridges validation
        bridges = design.get("bridges", [])
        if not isinstance(bridges, list):
            errors.append("bridges must be a list")
        else:
            for bridge in bridges:
                if not isinstance(bridge, dict):
                    errors.append(f"bridge entry must be object: {bridge}")
                    continue
                if "target" not in bridge:
                    errors.append("bridge missing required field: target")
                if "role" not in bridge:
                    errors.append("bridge missing required field: role")
                if "protocol" not in bridge:
                    errors.append("bridge missing required field: protocol")
                role = bridge.get("role", "")
                if role and role not in ("consumer", "provider", "bidirectional"):
                    errors.append(
                        f"invalid bridge role: '{role}' (expected consumer|provider|bidirectional)"
                    )

        # inherits validation
        inherits = design.get("inherits", [])
        if isinstance(inherits, list):
            atom_stems = self._get_atom_stems()
            for parent in inherits:
                if parent not in atom_stems:
                    errors.append(f"inherited atom not found: {parent}")

        # intent_hash format
        intent_hash = design.get("intent_hash", "")
        if intent_hash and not re.fullmatch(r"0x[a-zA-Z0-9_]+", intent_hash):
            errors.append(
                f"invalid intent_hash format: '{intent_hash}' (expected 0xHEX)"
            )

        return errors
