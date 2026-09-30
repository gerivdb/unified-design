#!/usr/bin/env python3
"""
ACT-039: Batch integration — 126/126 functional integrations.
Génère les modules d'intégration et tests pour tous les couples design/consumer
manquants.

Usage:
    python ACT-039-batch-integrations.py [--dry-run] [--consumer CONSUMER] [--design DESIGN]
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime, timezone
import argparse

UNIFIED_DESIGN_ROOT = Path("D:/DO/WEB/TOOLS/L0-CANON/unified-design")
ACT_026_REPORT = UNIFIED_DESIGN_ROOT / "ACT-026-final-coverage-100.json"
REPORT_PATH = UNIFIED_DESIGN_ROOT / "ACT-039-batch-integration-report.json"

# Mapping design -> (module_name, class_name, module_level_func)
DESIGN_API_MAP = {
    "safe-action-pattern": ("safe_action_pattern", "SafeActionGate", "run_safe_action"),
    "safe-action-gate": ("safe_action_gate", "SafeActionGate", "verify_safe_action_gate"),
    "ecosystem-meta-coherence": ("ecosystem_meta_coherence", "EcosystemMetaCoherence", "verify_meta_coherence"),
    "ecosystem-meta-coherence-gate": ("ecosystem_meta_coherence_gate", "EcosystemMetaCoherenceGate", "verify_meta_coherence_gate"),
    "meta-design-self-healing": ("meta_design_self_healing", "MetaDesignSelfHealing", "scan_self_healing"),
    "design-ops-loop": ("design_ops_loop", "DesignOpsLoop", "run_design_ops_loop"),
    "session-boot-design": ("session_boot_design", "SessionBoot", "run_session_boot"),
    "artifact-layers-design": ("artifact_layers_design", "ArtifactLayers", "validate_artifact_layers"),
    "talex-friction-analyzer": ("talex_friction_analyzer", "TalexFrictionAnalyzer", "analyze_friction"),
}

# Mapping consumer -> (repo_path, integration_package_dir, prd_dir_name)
# integration_package_dir: where to put the integration wrapper module (None = use integrations/)
CONSUMER_MAP = {
    "KIVA-CLI": {
        "path": Path("D:/DO/WEB/TOOLS/L1-INFRA/KIVA-CLI"),
        "pkg_dir": "kiva_cli",
        "prd_dir": "PRD",
    },
    "ECOS-CLI": {
        "path": Path("D:/DO/WEB/TOOLS/L1-INFRA/ECOS-CLI"),
        "pkg_dir": "ecos_cli",
        "prd_dir": "PRD",
    },
    "ARGUS": {
        "path": Path("D:/DO/WEB/TOOLS/L1-INFRA/ARGUS"),
        "pkg_dir": None,
        "prd_dir": "PRD",
    },
    "CTULU": {
        "path": Path("D:/DO/WEB/TOOLS/L4-TOOLS/CTULU"),
        "pkg_dir": None,
        "prd_dir": "PRD",
    },
    "KG-CAUSAL": {
        "path": Path("D:/DO/WEB/TOOLS/L4-TOOLS/KG-CAUSAL"),
        "pkg_dir": "src",
        "prd_dir": "PRD-MOC",
    },
    "KG-L": {
        "path": Path("D:/DO/WEB/TOOLS/L4-TOOLS/KG-L"),
        "pkg_dir": "kg_l",
        "prd_dir": "PRD",
    },
    "KIX": {
        "path": Path("D:/DO/WEB/TOOLS/L2-PLATFORM/KIX"),
        "pkg_dir": "kix",
        "prd_dir": "PRD-MOC",
    },
    "LOOPX": {
        "path": Path("D:/DO/WEB/TOOLS/L3-CITIZENS/LOOPX"),
        "pkg_dir": None,
        "prd_dir": "PRD",
    },
    "NEXUS": {
        "path": Path("D:/DO/WEB/TOOLS/L1-INFRA/NEXUS"),
        "pkg_dir": None,
        "prd_dir": "PRD-MOC",
    },
    "TALEX": {
        "path": Path("D:/DO/WEB/TOOLS/L4-TOOLS/TALEX"),
        "pkg_dir": None,
        "prd_dir": "PRD",
    },
    "TRIX": {
        "path": Path("D:/DO/WEB/TOOLS/L4-TOOLS/TRIX"),
        "pkg_dir": None,
        "prd_dir": "PRD",
    },
    "VERSES": {
        "path": Path("D:/DO/WEB/TOOLS/L4-TOOLS/VERSES"),
        "pkg_dir": "verses",
        "prd_dir": "PRD",
    },
    "VOLTX": {
        "path": Path("D:/DO/WEB/TOOLS/L0-CANON/VOLTX"),
        "pkg_dir": None,
        "prd_dir": "PRD-MOC",
    },
    "WAZAA": {
        "path": Path("D:/DO/WEB/TOOLS/L4-TOOLS/WAZAA"),
        "pkg_dir": "wazaa",
        "prd_dir": "PRD",
    },
}

# Already done pairs (functional integrations, not just standalone modules)
DONE_PAIRS = {
    ("safe-action-pattern", "KIVA-CLI"),
    ("safe-action-gate", "KIVA-CLI"),
    ("design-ops-loop", "KIVA-CLI"),
}


def design_to_slug(design_name: str) -> str:
    return design_name.replace("-", "_")


def get_integration_dir(consumer: str, consumer_info: dict) -> Path:
    pkg_dir = consumer_info["pkg_dir"]
    if pkg_dir:
        return consumer_info["path"] / pkg_dir
    else:
        integrations_dir = consumer_info["path"] / "integrations"
        integrations_dir.mkdir(parents=True, exist_ok=True)
        # Create __init__.py if it doesn't exist
        init_file = integrations_dir / "__init__.py"
        if not init_file.exists():
            init_file.write_text('"""Unified-design integrations."""\n', encoding="utf-8")
        return integrations_dir


def get_test_dir(consumer: str, consumer_info: dict) -> Path:
    tests_dir = consumer_info["path"] / "tests"
    tests_dir.mkdir(parents=True, exist_ok=True)
    return tests_dir


def create_integration_module(consumer: str, design_name: str, consumer_info: dict, dry_run: bool = False) -> dict:
    module_name, class_name, module_func = DESIGN_API_MAP[design_name]
    slug = design_to_slug(design_name)
    
    integration_dir = get_integration_dir(consumer, consumer_info)
    module_path = integration_dir / f"{slug}_integration.py"
    
    # Determine PRD relative path
    # If pkg_dir is set, integration is at pkg_dir/slug_integration.py, PRD is at ../PRD or ../PRD-MOC
    # If pkg_dir is None, integration is at integrations/slug_integration.py, PRD is at ../PRD or ../PRD-MOC
    prd_dir_name = consumer_info["prd_dir"]
    prd_rel = f".. / \"{prd_dir_name}\""
    
    # Determine import path for integration module in tests
    if consumer_info["pkg_dir"]:
        pkg_import = consumer_info["pkg_dir"].replace("-", "_")
        test_import_line = f"from {pkg_import}.{slug}_integration import get_{slug}_integration"
    else:
        test_import_line = f"from integrations.{slug}_integration import get_{slug}_integration"
    
    content = f'''#!/usr/bin/env python3
"""
Integration module for {design_name} design in {consumer}.
Wraps the standalone implementation for use in {consumer} commands.
"""

import sys
from pathlib import Path

# Add PRD directory to path for imports
prd_dir = Path(__file__).parent.parent / "{prd_dir_name}"
sys.path.insert(0, str(prd_dir))

from {module_name} import {class_name}, {module_func}


class {class_name}Integration:
    """Integration wrapper for {design_name}."""

    def __init__(self):
        self.{slug} = {class_name}()

    def validate(self, context: dict) -> dict:
        """Validate using {design_name}."""
        return self.{slug}.verify(context)

    def check_and_execute(self, context: dict, action_func) -> dict:
        """Check {design_name} then execute action if allowed."""
        validation = self.validate(context)
        if validation.get("state") == "ALLOW":
            result = action_func(context)
            return {{"validation": validation, "execution": result}}
        else:
            return {{"validation": validation, "execution": None}}


# Singleton
_{slug}_integration = None


def get_{slug}_integration() -> {class_name}Integration:
    """Get or create singleton instance."""
    global _{slug}_integration
    if _{slug}_integration is None:
        _{slug}_integration = {class_name}Integration()
    return _{slug}_integration
'''
    
    if dry_run:
        return {
            "module_path": str(module_path),
            "created": False,
            "dry_run": True,
            "content": content,
        }
    
    if not module_path.exists():
        module_path.write_text(content, encoding="utf-8")
        created = True
    else:
        created = False
    
    return {
        "module_path": str(module_path),
        "created": created,
        "dry_run": False,
        "content": content,
    }


def create_test_module(consumer: str, design_name: str, consumer_info: dict, dry_run: bool = False) -> dict:
    module_name, class_name, module_func = DESIGN_API_MAP[design_name]
    slug = design_to_slug(design_name)
    
    tests_dir = get_test_dir(consumer, consumer_info)
    test_path = tests_dir / f"test_{slug}_integration.py"
    
    # Determine import line for integration module
    if consumer_info["pkg_dir"]:
        pkg_import = consumer_info["pkg_dir"].replace("-", "_")
        integration_import = f"from {pkg_import}.{slug}_integration import get_{slug}_integration"
        pkg_path_line = f'sys.path.insert(0, str(Path(__file__).parent.parent / "{consumer_info["pkg_dir"]}"))'
    else:
        integration_import = f"from integrations.{slug}_integration import get_{slug}_integration"
        pkg_path_line = ''
    
    content = f'''#!/usr/bin/env python3
"""
Integration tests for {design_name} in {consumer}.
"""

import pytest
from pathlib import Path
import sys

# Add paths for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "{consumer_info["prd_dir"]}"))
{pkg_path_line}

{integration_import}


def test_{slug}_integration_allow():
    """Test that valid context is allowed."""
    integration = get_{slug}_integration()
    context = {{
        "intent_hash": "0xTEST_20260928",
        "consumer": "{consumer}",
    }}
    result = integration.validate(context)
    assert result.get("state") == "ALLOW"


def test_{slug}_integration_deny_missing_hash():
    """Test that context without intent_hash is denied."""
    integration = get_{slug}_integration()
    context = {{"consumer": "{consumer}"}}
    result = integration.validate(context)
    assert result.get("state") == "DENY"


def test_{slug}_integration_singleton():
    """Test that singleton pattern works."""
    integration1 = get_{slug}_integration()
    integration2 = get_{slug}_integration()
    assert integration1 is integration2
'''
    
    if dry_run:
        return {
            "test_path": str(test_path),
            "created": False,
            "dry_run": True,
            "content": content,
        }
    
    if not test_path.exists():
        test_path.write_text(content, encoding="utf-8")
        created = True
    else:
        created = False
    
    return {
        "test_path": str(test_path),
        "created": created,
        "dry_run": False,
        "content": content,
    }


def run_pytest(consumer: str, test_path: Path) -> dict:
    """Run pytest for a specific test file."""
    import subprocess
    result = {
        "consumer": consumer,
        "test_file": str(test_path),
        "passed": False,
        "output": "",
        "error": None,
    }
    
    if not test_path.exists():
        result["error"] = "Test file does not exist"
        return result
    
    try:
        proc = subprocess.run(
            [sys.executable, "-m", "pytest", str(test_path), "-v", "--tb=short"],
            capture_output=True,
            text=True,
            timeout=60,
            cwd=str(test_path.parent.parent),
        )
        result["output"] = proc.stdout + proc.stderr
        result["passed"] = proc.returncode == 0
    except Exception as e:
        result["error"] = str(e)
    
    return result


def main():
    parser = argparse.ArgumentParser(description="ACT-039: Batch integration 126/126")
    parser.add_argument("--dry-run", action="store_true", help="Preview only, do not write files")
    parser.add_argument("--consumer", type=str, help="Process only this consumer")
    parser.add_argument("--design", type=str, help="Process only this design")
    parser.add_argument("--skip-tests", action="store_true", help="Skip pytest execution")
    args = parser.parse_args()
    
    # Load ACT-026 data
    with open(ACT_026_REPORT, "r", encoding="utf-8") as f:
        act_026_data = json.load(f)
    
    pairs = act_026_data["details"]
    
    # Filter remaining pairs
    remaining = [p for p in pairs if (p["design"], p["consumer"]) not in DONE_PAIRS]
    
    if args.consumer:
        remaining = [p for p in remaining if p["consumer"] == args.consumer]
    
    if args.design:
        remaining = [p for p in remaining if p["design"] == args.design]
    
    results = []
    tests_passed = 0
    tests_failed = 0
    
    for pair in remaining:
        design = pair["design"]
        consumer = pair["consumer"]
        
        if design not in DESIGN_API_MAP:
            results.append({
                "design": design,
                "consumer": consumer,
                "status": "SKIPPED",
                "reason": f"Unknown design: {design}",
            })
            continue
        
        if consumer not in CONSUMER_MAP:
            results.append({
                "design": design,
                "consumer": consumer,
                "status": "SKIPPED",
                "reason": f"Unknown consumer: {consumer}",
            })
            continue
        
        consumer_info = CONSUMER_MAP[consumer]
        
        # Create integration module
        try:
            module_result = create_integration_module(consumer, design, consumer_info, dry_run=args.dry_run)
        except Exception as e:
            results.append({
                "design": design,
                "consumer": consumer,
                "status": "FAILED",
                "step": "create_module",
                "error": str(e),
            })
            tests_failed += 1
            continue
        
        # Create test module
        try:
            test_result = create_test_module(consumer, design, consumer_info, dry_run=args.dry_run)
        except Exception as e:
            results.append({
                "design": design,
                "consumer": consumer,
                "status": "FAILED",
                "step": "create_test",
                "error": str(e),
            })
            tests_failed += 1
            continue
        
        # Run pytest unless skipped
        pytest_passed = False
        pytest_output = ""
        if not args.dry_run and not args.skip_tests:
            pytest_result = run_pytest(consumer, Path(test_result["test_path"]))
            pytest_passed = pytest_result["passed"]
            pytest_output = pytest_result["output"][:500] if pytest_result["output"] else ""
            
            if pytest_passed:
                tests_passed += 1
            else:
                tests_failed += 1
        
        if pytest_passed or args.dry_run or args.skip_tests:
            status = "INTEGRATED"
        else:
            status = "TEST_FAILED"
        
        results.append({
            "design": design,
            "consumer": consumer,
            "status": status,
            "module_path": module_result["module_path"],
            "test_path": test_result["test_path"],
            "module_created": module_result["created"],
            "test_created": test_result["created"],
            "pytest_passed": pytest_passed,
            "pytest_output": pytest_output,
            "error": None,
        })
    
    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "task": "ACT-039",
        "dry_run": args.dry_run,
        "total_pairs": len(remaining),
        "integrated": sum(1 for r in results if r["status"] == "INTEGRATED"),
        "test_failed": sum(1 for r in results if r["status"] == "TEST_FAILED"),
        "failed": sum(1 for r in results if r["status"] == "FAILED"),
        "skipped": sum(1 for r in results if r["status"] == "SKIPPED"),
        "tests_passed": tests_passed,
        "tests_failed": tests_failed,
        "results": results,
    }
    
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    
    print(f"[ACT-039] Batch integration: {report['integrated']}/{report['total_pairs']} integrated")
    print(f"[ACT-039] Tests passed: {tests_passed}, failed: {tests_failed}")
    print(f"[ACT-039] Report: {REPORT_PATH}")
    
    # Print summary by consumer
    by_consumer = {}
    for r in results:
        c = r["consumer"]
        if c not in by_consumer:
            by_consumer[c] = {"integrated": 0, "failed": 0, "skipped": 0}
        if r["status"] == "INTEGRATED":
            by_consumer[c]["integrated"] += 1
        elif r["status"] == "TEST_FAILED":
            by_consumer[c]["failed"] += 1
        else:
            by_consumer[c]["skipped"] += 1
    
    print("\nSummary by consumer:")
    for c in sorted(by_consumer.keys()):
        s = by_consumer[c]
        print(f"  {c}: {s['integrated']} integrated, {s['failed']} failed, {s['skipped']} skipped")
    
    return report


if __name__ == "__main__":
    main()
