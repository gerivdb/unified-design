"""CLI for auto-design: analyze|generate|deploy|verify|report."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.engines.auto_design.analyzer import analyze_repo
from src.engines.auto_design.generator import generate_repo
from src.engines.auto_design.industrializer import deploy_repo
from src.engines.auto_design.reporter import report_global
from src.engines.auto_design.verifier import verify_repo


def _json(result: dict[str, object]) -> str:
    return json.dumps(result, ensure_ascii=False, indent=2)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Auto-design CLI")
    sub = parser.add_subparsers(dest="command")

    analyze = sub.add_parser("analyze")
    analyze.add_argument("repo", type=Path)

    generate = sub.add_parser("generate")
    generate.add_argument("repo", type=Path)
    generate.add_argument("--apply", action="store_true")

    deploy = sub.add_parser("deploy")
    deploy.add_argument("repo", type=Path)

    verify = sub.add_parser("verify")
    verify.add_argument("repo", type=Path)

    report = sub.add_parser("report")
    report.add_argument("--known-repos", type=Path, default=Path(__file__).resolve().parents[2] / "GOVERNANCE-HUB" / "known_repositories.yaml")

    args = parser.parse_args(argv)

    if args.command == "analyze":
        print(_json(analyze_repo(args.repo)))
        return 0

    if args.command == "generate":
        print(_json(generate_repo(args.repo, apply=args.apply)))
        return 0

    if args.command == "deploy":
        print(_json(deploy_repo(args.repo)))
        return 0

    if args.command == "verify":
        print(_json(verify_repo(args.repo)))
        return 0

    if args.command == "report":
        print(_json(report_global(args.known_repos)))
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
