#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Auto operator orchestrating full auto-design lifecycle from any repo."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .analyzer import AutoDesignAnalyzer
from .generator import AutoDesignGenerator
from .industrializer import AutoDesignIndustrializer
from .pr_review_auto import auto_pr_workflow
from .verifier import AutoDesignVerifier


class AutoOperator:
    def __init__(self, repo_root: Path) -> None:
        self.repo_root = Path(repo_root)

    def run_full_cycle(self, apply: bool = False) -> dict[str, Any]:
        analyzer = AutoDesignAnalyzer(self.repo_root)
        generator = AutoDesignGenerator(self.repo_root)
        verifier = AutoDesignVerifier(self.repo_root)
        industrializer = AutoDesignIndustrializer(self.repo_root)

        analysis = analyzer.analyze()
        generated = generator.generate(apply=apply)
        verification = verifier.verify()
        deployed = industrializer.deploy()

        pr_result: dict[str, Any] = {}
        if apply and generated.get("design_yaml"):
            pr_result = auto_pr_workflow(
                self.repo_root,
                slug="full-cycle",
                title="auto-design full cycle",
                body="Automated auto-design cycle: analyze, generate, verify, deploy, PR, merge.",
            )

        return {
            "repo": str(self.repo_root),
            "analysis": analysis,
            "generated": generated,
            "verification": verification,
            "deployed": deployed,
            "pr": pr_result,
        }


def run_full_cycle(repo_root: Path, apply: bool = False) -> dict[str, Any]:
    return AutoOperator(repo_root).run_full_cycle(apply=apply)
