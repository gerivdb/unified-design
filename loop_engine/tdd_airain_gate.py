#!/usr/bin/env python3
"""
tdd_airain_gate.py - Loi d'Airain TDD (No Test No Code)
Gate enforcement: code prod interdit sans test echoue prealable.
"Delete means delete" - suppression immediate si violation.
"""

from __future__ import annotations

import ast
import hashlib
import logging
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)


class TDDViolation(Exception):
    """Violation de la Loi d'Airain TDD."""
    pass


class TDDGateResult:
    """Resultat d'un gate TDD."""
    
    def __init__(
        self,
        passed: bool,
        message: str,
        violation_type: str = "",
        offending_files: list[str] = None,
        required_action: str = ""
    ):
        self.passed = passed
        self.message = message
        self.violation_type = violation_type
        self.offending_files = offending_files or []
        self.required_action = required_action
        self.timestamp = datetime.now()
    
    def __bool__(self) -> bool:
        return self.passed


@dataclass
class TestFileInfo:
    """Info sur un fichier de test."""
    path: Path
    test_functions: list[str] = field(default_factory=list)
    test_classes: list[str] = field(default_factory=list)
    covers: list[str] = field(default_factory=list)  # Fichiers prod couverts


@dataclass
class ProdFileInfo:
    """Info sur un fichier de production."""
    path: Path
    functions: list[str] = field(default_factory=list)
    classes: list[str] = field(default_factory=list)
    has_corresponding_test: bool = False
    test_file: Optional[Path] = None


class TDDAirainGate:
    """
    Enforcement de la Loi d'Airain TDD:
    1. AUCUN code de production sans test ECHOUANT prealable
    2. Si violation detectee -> SUPPRESSION IMMEDIATE (delete means delete)
    3. Gate obligatoire pre-commit / pre-push / CI
    """
    
    def __init__(
        self,
        project_root: Path,
        test_patterns: list[str] = None,
        prod_patterns: list[str] = None,
        coverage_threshold: float = 0.85,
        strict_mode: bool = True,
        auto_delete: bool = True,
        test_command: list[str] = None
    ):
        self.project_root = Path(project_root).resolve()
        self.test_patterns = test_patterns or ["test_*.py", "*_test.py", "tests/**/*.py"]
        self.prod_patterns = prod_patterns or ["**/*.py", "src/**/*.py"]
        self.coverage_threshold = coverage_threshold
        self.strict_mode = strict_mode
        self.auto_delete = auto_delete
        self.test_command = test_command or ["pytest", "-x", "-v"]
        
        # Exclusions
        self.exclude_dirs = {".git", "__pycache__", ".pytest_cache", "venv", "env", ".venv"}
        self.exclude_files = {"setup.py", "conftest.py", "__init__.py"}
    
    def scan_project(self) -> tuple[list[TestFileInfo], list[ProdFileInfo]]:
        """Scan le projet pour identifier tests et code prod."""
        test_files = self._find_test_files()
        prod_files = self._find_prod_files(test_files)
        
        test_infos = [self._analyze_test_file(f) for f in test_files]
        prod_infos = [self._analyze_prod_file(f, test_infos) for f in prod_files]
        
        return test_infos, prod_infos
    
    def _find_test_files(self) -> list[Path]:
        """Trouve tous les fichiers de test."""
        files = []
        for pattern in self.test_patterns:
            for f in self.project_root.rglob(pattern):
                if f.is_file() and not self._is_excluded(f):
                    files.append(f)
        return list(set(files))
    
    def _find_prod_files(self, test_files: list[Path]) -> list[Path]:
        """Trouve tous les fichiers de production (non-test)."""
        test_set = set(test_files)
        files = []
        for pattern in self.prod_patterns:
            for f in self.project_root.rglob(pattern):
                if (f.is_file() and f not in test_set 
                    and not self._is_excluded(f)
                    and not self._is_test_file(f)):
                    files.append(f)
        return list(set(files))
    
    def _is_excluded(self, path: Path) -> bool:
        """Verifie si le chemin est exclu."""
        for part in path.parts:
            if part in self.exclude_dirs:
                return True
        if path.name in self.exclude_files:
            return True
        return False
    
    def _is_test_file(self, path: Path) -> bool:
        """Heuristique: est-ce un fichier de test?"""
        name = path.name
        return (name.startswith("test_") or name.endswith("_test.py") 
                or "tests" in path.parts)
    
    def _analyze_test_file(self, path: Path) -> TestFileInfo:
        """Analyse un fichier de test pour extraire fonctions/classes."""
        info = TestFileInfo(path=path)
        try:
            content = path.read_text(encoding="utf-8")
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
                    info.test_functions.append(node.name)
                elif isinstance(node, ast.ClassDef) and node.name.startswith("Test"):
                    info.test_classes.append(node.name)
                    # Extraire methodes de test dans la classe
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef) and item.name.startswith("test_"):
                            info.test_functions.append(f"{node.name}.{item.name}")
            
            # Heuristique: quel fichier prod ce test couvre?
            info.covers = self._infer_covered_files(path, info.test_functions)
            
        except Exception as e:
            logger.warning(f"Could not analyze test file {path}: {e}")
        
        return info
    
    def _infer_covered_files(
        self,
        test_path: Path,
        test_functions: list[str]
    ) -> list[str]:
        """Infere quels fichiers prod sont couverts par ce test."""
        covered = []
        
        # Convention: test_foo.py -> foo.py
        prod_name = test_path.name
        if prod_name.startswith("test_"):
            prod_name = prod_name[5:]
        elif prod_name.endswith("_test.py"):
            prod_name = prod_name[:-8]
        prod_name = prod_name.replace("test_", "").replace("_test", "") + ".py"
        
        # Chercher fichier correspondant
        for prod_file in self.project_root.rglob(prod_name):
            if prod_file.is_file() and not self._is_test_file(prod_file):
                covered.append(str(prod_file.relative_to(self.project_root)))
        
        # Aussi chercher par nom de fonction/classe
        for func in test_functions:
            # test_user_login -> user.py ou auth.py
            pass
        
        return covered
    
    def _analyze_prod_file(
        self,
        path: Path,
        test_infos: list[TestFileInfo]
    ) -> ProdFileInfo:
        """Analyse un fichier de production."""
        info = ProdFileInfo(path=path)
        try:
            content = path.read_text(encoding="utf-8")
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and not node.name.startswith("_"):
                    info.functions.append(node.name)
                elif isinstance(node, ast.ClassDef):
                    info.classes.append(node.name)
            
            # Verifier s'il y a un test correspondant
            rel_path = str(path.relative_to(self.project_root))
            for test_info in test_infos:
                if rel_path in test_info.covers:
                    info.has_corresponding_test = True
                    info.test_file = test_info.path
                    break
                    
        except Exception as e:
            logger.warning(f"Could not analyze prod file {path}: {e}")
        
        return info
    
    def check_gate(self, changed_files: list[Path] = None) -> TDDGateResult:
        """
        Gate principal TDD - appelle avant commit/push.
        Si changed_files fourni, ne verifie que ceux-ci (mode incrementale).
        """
        logger.info("Running TDD Airain Gate...")
        
        # 1. Lancer les tests pour voir lesquels echouent
        failed_tests = self._run_tests_and_get_failures()
        
        # 2. Scanner le projet
        test_infos, prod_infos = self.scan_project()
        
        # 3. Verifier violations
        violations = []
        
        for prod_info in prod_infos:
            if changed_files and prod_info.path not in changed_files:
                continue
            
            # Violation 1: Code prod sans test correspondant
            if not prod_info.has_corresponding_test and prod_info.functions:
                violations.append({
                    "type": "missing_test",
                    "file": str(prod_info.path.relative_to(self.project_root)),
                    "functions": prod_info.functions,
                    "message": f"Production code has no corresponding test file"
                })
            
            # Violation 2: Test existe mais ne PAS echouer avant (test-first)
            if prod_info.has_corresponding_test and prod_info.test_file:
                if not self._test_fails_first(prod_info.test_file, failed_tests):
                    violations.append({
                        "type": "test_not_failing_first",
                        "file": str(prod_info.path.relative_to(self.project_root)),
                        "test_file": str(prod_info.test_file.relative_to(self.project_root)),
                        "message": "Test must fail before production code is written"
                    })
        
        # 4. Si violations en mode strict -> delete means delete
        if violations:
            if self.auto_delete and self.strict_mode:
                self._delete_violating_files(violations)
            
            return TDDGateResult(
                passed=False,
                message=f"TDD Airain Law VIOLATED: {len(violations)} violation(s)",
                violation_type="tdd_airain_violation",
                offending_files=[v["file"] for v in violations],
                required_action="DELETE violating production code AND write failing test first"
            )
        
        # 5. Verifier couverture globale
        coverage = self._check_coverage(test_infos, prod_infos)
        if coverage < self.coverage_threshold:
            return TDDGateResult(
                passed=False,
                message=f"Coverage {coverage:.1%} below threshold {self.coverage_threshold:.1%}",
                violation_type="coverage_below_threshold",
                required_action="Add more tests to reach coverage threshold"
            )
        
        return TDDGateResult(
            passed=True,
            message="TDD Airain Gate PASSED - All production code has failing tests first",
            required_action=""
        )
    
    def _run_tests_and_get_failures(self) -> set[str]:
        """Execute les tests et retourne l'ensemble des tests qui echouent."""
        try:
            result = subprocess.run(
                self.test_command + ["--tb=no", "-q"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=120
            )
            
            failed = set()
            for line in result.stdout.splitlines():
                if "FAILED" in line or "ERROR" in line:
                    # Extraire nom de test
                    parts = line.split()
                    for p in parts:
                        if "::" in p or p.startswith("test_"):
                            failed.add(p)
            return failed
        except Exception as e:
            logger.warning(f"Test run failed: {e}")
            return set()
    
    def _test_fails_first(self, test_file: Path, failed_tests: set[str]) -> bool:
        """Verifie si au moins un test du fichier echoue (test-first)."""
        if not failed_tests:
            return False
        
        test_name = test_file.stem
        for failed in failed_tests:
            if test_name in failed or test_file.name in failed:
                return True
        return False
    
    def _check_coverage(
        self,
        test_infos: list[TestFileInfo],
        prod_infos: list[ProdFileInfo]
    ) -> float:
        """Calcule la couverture approximative."""
        if not prod_infos:
            return 1.0
        
        covered = sum(1 for p in prod_infos if p.has_corresponding_test)
        return covered / len(prod_infos)
    
    def _delete_violating_files(self, violations: list[dict]):
        """DELETE MEANS DELETE - supprime les fichiers en violation."""
        logger.warning("DELETE MEANS DELETE: Removing violating production files")
        
        for v in violations:
            if v["type"] == "missing_test":
                file_path = self.project_root / v["file"]
                if file_path.exists():
                    # Backup avant suppression
                    backup = file_path.with_suffix(file_path.suffix + ".tdd_violation_bak")
                    file_path.rename(backup)
                    logger.warning(f"DELETED (backed up): {file_path} -> {backup}")
    
    def generate_report(self) -> dict:
        """Genere rapport complet TDD."""
        test_infos, prod_infos = self.scan_project()
        
        uncovered = [p for p in prod_infos if not p.has_corresponding_test and p.functions]
        covered = [p for p in prod_infos if p.has_corresponding_test]
        
        return {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_prod_files": len(prod_infos),
                "covered": len(covered),
                "uncovered": len(uncovered),
                "coverage_percent": len(covered) / len(prod_infos) * 100 if prod_infos else 100
            },
            "uncovered_files": [
                {
                    "file": str(p.path.relative_to(self.project_root)),
                    "functions": p.functions,
                    "classes": p.classes
                }
                for p in uncovered
            ],
            "test_files": [
                {
                    "file": str(t.path.relative_to(self.project_root)),
                    "tests": t.test_functions,
                    "covers": t.covers
                }
                for t in test_infos
            ]
        }


def demo():
    """Demo du gate TDD."""
    import tempfile
    logging.basicConfig(level=logging.INFO)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        
        # Creer structure test
        (root / "src").mkdir()
        (root / "tests").mkdir()
        
        # Fichier prod SANS test (violation)
        (root / "src" / "calculator.py").write_text("""
def add(a, b):
    return a + b

def multiply(a, b):
    return a * b
""")
        
        # Fichier prod AVEC test
        (root / "src" / "utils.py").write_text("""
def format_name(first, last):
    return f"{first} {last}"
""")
        
        (root / "tests" / "test_utils.py").write_text("""
import pytest
from src.utils import format_name

def test_format_name():
    assert format_name("John", "Doe") == "John Doe"
""")
        
        gate = TDDAirainGate(root, strict_mode=True, auto_delete=True)
        
        print("=== TDD Airain Gate Demo ===")
        result = gate.check_gate()
        
        print(f"Passed: {result.passed}")
        print(f"Message: {result.message}")
        print(f"Action required: {result.required_action}")
        
        if result.offending_files:
            print(f"Offending files: {result.offending_files}")
        
        # Rapport
        report = gate.generate_report()
        print(f"\nCoverage: {report['summary']['coverage_percent']:.1f}%")
        print(f"Uncovered: {len(report['uncovered_files'])}")


if __name__ == "__main__":
    demo()