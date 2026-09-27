import glob, os, yaml, json, sys, shutil, argparse
from collections import deque, defaultdict
from datetime import datetime, timezone

ROOT = r"D:\DO\WEB\TOOLS\L0-CANON\unified-design"
REPORT_DIR = os.path.join(ROOT, "reports", "meta-coherence")
FIX_BACKUP_DIR = os.path.join(REPORT_DIR, "backups")
ALIASES_PATH = os.path.join(ROOT, ".kilo", "meta_coherence_aliases.yaml")

parser = argparse.ArgumentParser(description="Unified-design structural metacoherence checker")
parser.add_argument("--mode", choices=["check", "plan", "apply", "strict"], default="check", help="Execution mode")
parser.add_argument("--strict", action="store_true", help="Strict mode: exit 1 if any issue or bad yaml")
args = parser.parse_args()
mode = args.mode
strict = args.strict or mode == "strict"

def write_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)

def write_text(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

def backup_file(path):
    os.makedirs(FIX_BACKUP_DIR, exist_ok=True)
    rel = os.path.relpath(path, ROOT)
    dest = os.path.join(FIX_BACKUP_DIR, rel.replace(os.sep, "_"))
    shutil.copy2(path, dest)
    return dest

def load_yaml(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return list(yaml.safe_load_all(f))[0] or {}
    except Exception:
        return None

def save_yaml(path, doc):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        yaml.safe_dump(doc, f, sort_keys=False, allow_unicode=True, default_flow_style=False)
    os.replace(tmp, path)

def load_aliases():
    if not os.path.exists(ALIASES_PATH):
        return {}
    doc = load_yaml(ALIASES_PATH)
    if not isinstance(doc, dict):
        return {}
    return doc.get("aliases", {})

def is_protected(doc):
    layer = (doc.get("layer") or "").upper()
    status = (doc.get("status") or "").lower()
    if layer in {"L0", "L0_CANON", "L0_CONSTITUTIONAL", "L0-INFRASTRUCTURE"}:
        return True
    if status == "active" and doc.get("intent_hash"):
        return False
    return False

def resolve_ref(ref, by_slug, aliases):
    if ref in by_slug:
        return ref
    alias = aliases.get(ref)
    if alias and alias in by_slug:
        return alias
    return None

def compute_depth(slug, by_slug, aliases):
    depth = 0
    q = deque([(slug, 0)])
    visited = set()
    while q:
        cur, d = q.popleft()
        if cur in visited:
            continue
        visited.add(cur)
        if d > depth:
            depth = d
        if depth > 3:
            break
        target = cur
        path = by_slug.get(target)
        if not path:
            continue
        doc = load_yaml(path)
        if not doc:
            continue
        for parent in (doc.get("inherits") or []):
            resolved = resolve_ref(parent, by_slug, aliases)
            if resolved:
                q.append((resolved, d + 1))
    return depth

# Chargement aliases
aliases = load_aliases()

# Chargement designs
paths = glob.glob(os.path.join(ROOT, "designs/**/*.yaml"), recursive=True) + \
        glob.glob(os.path.join(ROOT, "designs/**/*.yml"), recursive=True)

data = {}
bad = []
for p in paths:
    doc = load_yaml(p)
    if doc is None:
        bad.append(p)
        continue
    slug = doc.get("name")
    if slug:
        data[slug] = {"path": p, "doc": doc}

by_slug = {slug: v["path"] for slug, v in data.items()}

# Analyse
issues = []
auto_fixes = []
manual_fixes = []

for slug, meta in data.items():
    p = meta["path"]
    doc = meta["doc"]
    inherits = doc.get("inherits") or []
    depends = doc.get("depends_on") or []
    if isinstance(inherits, str):
        inherits = [inherits]
    if isinstance(depends, str):
        depends = [depends]
    for parent in inherits:
        resolved = resolve_ref(parent, by_slug, aliases)
        if resolved is None:
            issues.append({"slug": slug, "type": "missing_parent", "ref": parent, "file": p})
            if not is_protected(doc):
                manual_fixes.append({"slug": slug, "ref": parent, "file": p, "action": "remove_missing_parent"})
    for dep in depends:
        resolved = resolve_ref(dep, by_slug, aliases)
        if resolved is None:
            issues.append({"slug": slug, "type": "missing_dependency", "ref": dep, "file": p})
            if not is_protected(doc):
                manual_fixes.append({"slug": slug, "ref": dep, "file": p, "action": "remove_missing_dependency"})
    depth = compute_depth(slug, by_slug, aliases)
    if depth > 3:
        issues.append({"slug": slug, "type": "depth", "ref": str(depth), "file": p})
        if not is_protected(doc):
            auto_fixes.append({"slug": slug, "file": p, "action": "cap_depth", "value": 3})

def utcnow_iso():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

summary = {
    "timestamp": utcnow_iso(),
    "files": len(data),
    "bad_yaml": len(bad),
    "issues_total": len(issues),
    "missing_parents": len([i for i in issues if i["type"] == "missing_parent"]),
    "missing_dependencies": len([i for i in issues if i["type"] == "missing_dependency"]),
    "depth_violations": len([i for i in issues if i["type"] == "depth"]),
    "bad_yaml_files": bad,
    "sample_issues": issues[:50],
}

report_path = os.path.join(REPORT_DIR, f"meta-coherence-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.json")
write_json(report_path, summary)
latest_path = os.path.join(REPORT_DIR, "latest.json")
write_json(latest_path, summary)

fix_plan = []
for fix in auto_fixes + manual_fixes:
    fix_plan.append(fix)

fix_plan_path = os.path.join(REPORT_DIR, f"fix-plan-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.json")
write_json(fix_plan_path, fix_plan)
write_json(os.path.join(REPORT_DIR, "latest-fix-plan.json"), fix_plan)

# Mode --plan : sortie plan uniquement, pas d'apply
if mode == "plan":
    print(json.dumps({
        "mode": "plan",
        "report": report_path,
        "fix_plan": fix_plan_path,
        "auto_fixes": len(auto_fixes),
        "manual_fixes": len(manual_fixes),
        "issues_total": summary["issues_total"]
    }, ensure_ascii=False, indent=2))
    sys.exit(0)

# Mode --apply : applique les auto_fixes seulement
applied = []
skipped = []
if mode == "apply":
    for fix in auto_fixes:
        p = fix["file"]
        doc = load_yaml(p)
        if doc is None:
            skipped.append({"file": p, "reason": "bad_yaml"})
            continue
        if fix["action"] == "cap_depth":
            # strategy: remove all but 3 inherited ancestors by breadth-first truncation
            inherits = doc.get("inherits") or []
            if isinstance(inherits, str):
                inherits = [inherits]
            resolved_inherits = []
            for parent in inherits:
                r = resolve_ref(parent, by_slug, aliases)
                if r:
                    resolved_inherits.append(r)
            if len(resolved_inherits) > 3:
                new_inherits = resolved_inherits[:3]
                backup_file(p)
                doc["inherits"] = new_inherits
                save_yaml(p, doc)
                applied.append({"file": p, "action": "cap_depth", "from": resolved_inherits, "to": new_inherits})
            else:
                skipped.append({"file": p, "reason": "depth_ok"})
        elif fix["action"] == "remove_missing_parent":
            # handled in manual_fixes only for safety
            skipped.append({"file": p, "reason": "manual_only"})
    apply_report = {
        "timestamp": utcnow_iso(),
        "applied": applied,
        "skipped": skipped,
    }
    apply_path = os.path.join(REPORT_DIR, f"apply-report-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.json")
    write_json(apply_path, apply_report)
    print(json.dumps({
        "mode": "apply",
        "applied": len(applied),
        "skipped": len(skipped),
        "report": apply_path
    }, ensure_ascii=False, indent=2))
    sys.exit(0)

# Mode --strict : bloque si issues non vides
if strict:
    if summary["issues_total"] > 0 or summary["bad_yaml"] > 0:
        print(json.dumps({
            "mode": "strict",
            "status": "BLOCKED",
            "issues_total": summary["issues_total"],
            "bad_yaml": summary["bad_yaml"]
        }, ensure_ascii=False, indent=2))
        sys.exit(1)
    print(json.dumps({
        "mode": "strict",
        "status": "PASS",
        "issues_total": 0,
        "bad_yaml": 0
    }, ensure_ascii=False, indent=2))
    sys.exit(0)

# Mode --check par défaut
print(json.dumps({
    "mode": "check",
    "report": report_path,
    "fix_plan": fix_plan_path,
    "issues_total": summary["issues_total"],
    "bad_yaml": summary["bad_yaml"],
    "depth_violations": summary["depth_violations"],
    "missing_parents": summary["missing_parents"],
    "missing_dependencies": summary["missing_dependencies"]
}, ensure_ascii=False, indent=2))
