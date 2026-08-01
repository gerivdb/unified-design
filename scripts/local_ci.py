#!/usr/bin/env python3
"""
Local CI Runner - KIVA-CLI Native
Remplace GitHub Actions par exécution locale via KIVA-CLI
Zéro dépendance GitHub Actions - tout tourne en local
"""

import subprocess
import sys
import time
from pathlib import Path
from typing import List, Tuple

REPO_ROOT = Path(__file__).parent.parent


def run(cmd: List[str], cwd: Path = None, desc: str = "") -> Tuple[bool, str]:
    """Execute command and return (success, output)."""
    cwd = cwd or REPO_ROOT
    print(f"  > {desc or ' '.join(cmd)}")
    start = time.time()
    try:
        result = subprocess.run(
            cmd, cwd=cwd, capture_output=True, text=True, timeout=300
        )
        elapsed = time.time() - start
        if result.returncode == 0:
            print(f"    OK OK ({elapsed:.1f}s)")
            return True, result.stdout
        else:
            print(f"    FAIL FAIL ({elapsed:.1f}s)")
            print(f"    stderr: {result.stderr[:500]}")
            return False, result.stderr
    except subprocess.TimeoutExpired:
        print(f"    FAIL TIMEOUT (>{300}s)")
        return False, "Timeout"
    except Exception as e:
        print(f"    FAIL ERROR: {e}")
        return False, str(e)


def check_kiva_cli() -> bool:
    """Verifie que KIVA-CLI est disponible."""
    result = subprocess.run(["kiva", "--version"], capture_output=True)
    if result.returncode == 0:
        print(f"  OK KIVA-CLI: {result.stdout.strip()}")
        return True
    print("  FAIL KIVA-CLI non trouve - installez via ECOS-CLI")
    return False


def validate_meta_design() -> bool:
    """Valide meta-design.yaml contre schema."""
    ok, _ = run(
        ["python", "scripts/validate_meta_design.py", "meta-design.yaml"],
        desc="Validate meta-design.yaml"
    )
    return ok


def validate_atoms() -> bool:
    """Valide tous les atoms YAML."""
    ok, _ = run(
        ["python", "scripts/validate_yaml.py", "--assert", "name", "atoms/*.yaml"],
        desc="Validate atoms YAML structure"
    )
    return ok


def validate_atom_registry() -> bool:
    """Valide la registry d'atoms."""
    ok, _ = run(
        ["python", "scripts/validate_atom_registry.py"],
        desc="Validate atom registry"
    )
    return ok


def validate_schema() -> bool:
    """Valide meta-design.schema.json."""
    ok, _ = run(
        ["python", "-c", "import json; json.load(open('schemas/meta-design.schema.json')); print('Schema JSON valide')"],
        desc="Validate meta-design.schema.json"
    )
    return ok


def check_loops() -> bool:
    """Détection de boucles dans le graphe de dépendances."""
    ok, _ = run(
        ["python", "loop_engine/check_loops.py", "--path", ".", "--max-depth", "5"],
        desc="Check dependency loops"
    )
    return ok


def validate_adr_refs() -> bool:
    """Valide les références ADR."""
    ok, _ = run(
        ["python", "scripts/validate_adr_refs.py"],
        desc="Validate ADR references"
    )
    return ok


def simulate_atoms() -> bool:
    """Lance simulate.py sur tous les nouveaux atoms."""
    atoms = [
        "ATOM-049-symbol-retrieval-mcp.yaml",
        "ATOM-050-agent-worktree-isolation.yaml",
        "ATOM-051-beads-sql-memory.yaml",
        "ATOM-052-exit-interceptor.yaml",
        "ATOM-053-tdd-airain-law.yaml",
        "ATOM-054-trace-replay-proof.yaml",
    ]
    all_ok = True
    for atom in atoms:
        atom_path = f"atoms/{atom}"
        if Path(atom_path).exists():
            ok, _ = run(
                ["python", "loop_engine/simulate.py", atom_path, "--meta-design", "meta-design.yaml"],
                desc=f"Simulate {atom}"
            )
            all_ok = all_ok and ok
    return all_ok


def run_full_ci() -> bool:
    """Pipeline CI complète locale."""
    print("=" * 60)
    print("LOCAL CI PIPELINE (KIVA-CLI Native)")
    print("=" * 60)
    
    if not check_kiva_cli():
        return False
    
    checks = [
        ("Meta-design schema", validate_schema),
        ("Meta-design validation", validate_meta_design),
        ("Atoms YAML structure", validate_atoms),
        ("Atom registry", validate_atom_registry),
        ("Dependency loops", check_loops),
        ("ADR references", validate_adr_refs),
        ("Atom simulation", simulate_atoms),
    ]
    
    results = []
    for name, check_fn in checks:
        print(f"\n[{name}]")
        ok = check_fn()
        results.append((name, ok))
    
    print("\n" + "=" * 60)
    print("CI SUMMARY")
    print("=" * 60)
    all_passed = True
    for name, ok in results:
        status = "PASS" if ok else "FAIL"
        print(f"  {status}: {name}")
        all_passed = all_passed and ok
    
    print("=" * 60)
    return all_passed


if __name__ == "__main__":
    success = run_full_ci()
    sys.exit(0 if success else 1)
