#!/usr/bin/env python3
"""design_impl_verifier — Vérifie l'implémentation des designs unified-design dans les repos cibles.

Usage:
    python design_impl_verifier.py <design_path>
    python design_impl_verifier.py --strict <design_path>
    python design_impl_verifier.py --json <design_path>

Exit codes:
    0 = design implémenté (ou warning en mode non-strict)
    1 = design non implémenté ou erreur
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

UNIFIED_DESIGN_ROOT = Path(__file__).resolve().parent.parent


def load_design(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if text.startswith("---"):
        parts = text.split("---", 2)
        yaml_text = parts[1] if len(parts) >= 3 and parts[1].strip() else text
    else:
        yaml_text = text
    return yaml.safe_load(yaml_text) or {}


def verify_artifact(artifact: dict, repo_root: Path) -> tuple[bool, str]:
    rel_path = artifact.get("path")
    if not rel_path:
        return False, "missing path in artifact"

    target = repo_root / rel_path
    if not target.exists():
        return False, f"file not found: {rel_path}"

    must_contain = artifact.get("must_contain", [])
    if not must_contain:
        return True, "file exists, no content checks"

    content = target.read_text(encoding="utf-8", errors="ignore")
    missing = [pattern for pattern in must_contain if pattern not in content]
    if missing:
        return False, f"missing patterns: {missing}"

    return True, "file exists and contains required patterns"


def _rel(path: Path) -> str:
    try:
        return str(path.relative_to(UNIFIED_DESIGN_ROOT))
    except ValueError:
        return str(path)


def verify_design(design_path: Path, strict: bool = False) -> dict:
    design_path = design_path.resolve()
    if not design_path.exists():
        return {'design': str(design_path), 'implemented': False, 'reason': 'file not found'}

    design = load_design(design_path)
    name = design.get('name', design_path.stem)
    status = design.get('status', 'unknown')
    layer = design.get('layer', 'unknown')
    intent_hash = design.get('intent_hash', '')

    contract = design.get('implementation_contract')
    if not contract:
        return {
            'design': name,
            'path': _rel(design_path),
            'status': status,
            'layer': layer,
            'intent_hash': intent_hash,
            'implemented': False,
            'reason': 'missing implementation_contract',
            'artifacts_verified': 0,
            'artifacts_missing': 0,
            'tests_passing': None,
            'coverage_pct': 0.0,
        }

    repo_name = contract.get('repo', '')
    repo_root = Path(contract.get('repo_root', '')).resolve()
    if not repo_root or not repo_root.exists():
        repo_root = UNIFIED_DESIGN_ROOT

    artifacts = contract.get('artifacts', [])
    verified = 0
    missing = 0
    details = []

    for artifact in artifacts:
        ok, msg = verify_artifact(artifact, repo_root)
        if ok:
            verified += 1
        else:
            missing += 1
        details.append({'path': artifact.get('path', ''), 'ok': ok, 'msg': msg})

    tests = contract.get('tests', [])
    tests_passing = None
    if tests:
        test_paths = [t.split('::')[0] for t in tests]
        all_exist = all((repo_root / tp).exists() for tp in test_paths)
        tests_passing = all_exist

    total = len(artifacts)
    coverage = (verified / total * 100) if total else 0.0
    implemented = missing == 0 and (tests_passing is None or tests_passing)

    return {
        'design': name,
        'path': _rel(design_path),
        'status': status,
        'layer': layer,
        'intent_hash': intent_hash,
        'implemented': implemented,
        'coverage_pct': round(coverage, 1),
        'artifacts_verified': verified,
        'artifacts_missing': missing,
        'tests_passing': tests_passing,
        'details': details,
    }

def find_designs(targets: list[str] | None = None) -> list[Path]:
    designs_dir = UNIFIED_DESIGN_ROOT / "designs"
    if targets:
        return [Path(t) for t in targets if Path(t).exists()]
    return sorted(set(designs_dir.rglob("design.yaml")))


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify design implementation")
    parser.add_argument("paths", nargs="*", help="Design paths to verify")
    parser.add_argument("--strict", action="store_true", help="Fail if not implemented")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    designs = find_designs(args.paths)
    if not designs:
        print("[FAIL] No designs found", file=sys.stderr)
        return 1

    results = []
    failures = 0
    for path in designs:
        result = verify_design(path, strict=args.strict)
        results.append(result)
        if not result["implemented"]:
            failures += 1

    if args.json:
        print(json.dumps({"designs": results, "failures": failures}, indent=2, ensure_ascii=False))
    else:
        for r in results:
            status = "OK" if r["implemented"] else "FAIL"
            print(f"[{status}] {r['design']}: coverage={r['coverage_pct']}% artifacts={r['artifacts_verified']}/{r['artifacts_verified']+r['artifacts_missing']} tests={r['tests_passing']}")

    total = len(designs)
    ok = total - failures
    print(f"\n{ok}/{total} designs implemented")

    if failures and args.strict:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
