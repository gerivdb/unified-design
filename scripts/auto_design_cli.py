"""CLI for auto-design: analyze|generate|deploy|verify|report|promote."""

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
from scripts.auto_promote import promote_adr, promote_design, promote_intent, check_adr_can_be_promoted, check_design_can_be_promoted, check_intent_can_be_promoted, DESIGN_ADR_MAP, DESIGN_SLUGS


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

    promote = sub.add_parser("promote")
    promote.add_argument("--dry-run", action="store_true", help="Simulate without applying changes")
    promote.add_argument("--apply", action="store_true", help="Apply promotions")
    promote.add_argument("repo", type=Path, nargs="?", default=Path(__file__).resolve().parents[1])

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

    if args.command == "promote":
        if not args.dry_run and not args.apply:
            print("Error: --dry-run or --apply required for promote command")
            return 1
        apply = args.apply
        repo_root = args.repo
        
        results = {
            "timestamp": Path(__file__).resolve().stat().st_mtime,
            "mode": "APPLY" if apply else "DRY-RUN",
            "adr_promotions": [],
            "design_promotions": [],
            "intent_promotions": [],
            "summary": {"adr_total": 0, "adr_promoted": 0, "design_total": 0, "design_promoted": 0, "intent_total": 0, "intent_promoted": 0},
        }
        
        # ADR
        for design_name, adr_name in DESIGN_ADR_MAP.items():
            check = check_adr_can_be_promoted(adr_name)
            results["summary"]["adr_total"] += 1
            if check.get("can_promote"):
                result = promote_adr(adr_name, dry_run=not apply)
                results["adr_promotions"].append({"adr": adr_name, "design": design_name, "check": check, "result": result})
                if result["status"] in ("promoted", "would_promote"):
                    results["summary"]["adr_promoted"] += 1
        
        # Designs
        for design_name in DESIGN_SLUGS.keys():
            check = check_design_can_be_promoted(design_name)
            results["summary"]["design_total"] += 1
            if check.get("can_promote"):
                result = promote_design(design_name, dry_run=not apply)
                results["design_promotions"].append({"design": design_name, "check": check, "result": result})
                if result["status"] in ("promoted", "would_promote"):
                    results["summary"]["design_promoted"] += 1
        
        # INTENTS
        intent_dir = repo_root / "INTENTS"
        if intent_dir.exists():
            for intent_file in intent_dir.glob("INTENT-*.md"):
                if intent_file.name == "INTENTS-000-index.md":
                    continue
                check = check_intent_can_be_promoted(intent_file.name)
                results["summary"]["intent_total"] += 1
                if check.get("can_promote"):
                    result = promote_intent(intent_file.name, dry_run=not apply)
                    results["intent_promotions"].append({"intent": intent_file.name, "check": check, "result": result})
                    if result["status"] in ("promoted", "would_promote"):
                        results["summary"]["intent_promoted"] += 1
        
        print(_json(results))
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
