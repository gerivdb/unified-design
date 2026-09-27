import glob, os, tempfile, json, pytest

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_check(args):
    import importlib.util
    spec = importlib.util.spec_from_file_location("check_meta_coherence", os.path.join(ROOT, ".kilo", "check_meta_coherence.py"))
    mod = importlib.util.module_from_spec(spec)
    # inject args manually by monkeypatching sys.argv
    import sys
    old_argv = sys.argv
    sys.argv = [old_argv[0]] + args
    try:
        spec.loader.exec_module(mod)
    finally:
        sys.argv = old_argv
    return mod

def test_check_mode_returns_json():
    mod = run_check(["--mode", "check"])
    # stdout is printed, but we can inspect latest.json
    latest = os.path.join(ROOT, "reports", "meta-coherence", "latest.json")
    assert os.path.exists(latest)
    data = json.load(open(latest, encoding="utf-8"))
    assert "issues_total" in data
    assert "files" in data

def test_strict_mode_blocks_on_issues():
    with pytest.raises(SystemExit) as excinfo:
        run_check(["--mode", "strict"])
    assert excinfo.value.code == 1

def test_apply_mode_skips_protected_and_bad_yaml():
    with pytest.raises(SystemExit) as excinfo:
        run_check(["--mode", "apply"])
    assert excinfo.value.code == 0
    apply_report = os.path.join(ROOT, "reports", "meta-coherence", "latest-fix-plan.json")
    assert os.path.exists(apply_report)

def test_plan_mode_returns_summary():
    with pytest.raises(SystemExit) as excinfo:
        run_check(["--mode", "plan"])
    assert excinfo.value.code == 0
    latest = os.path.join(ROOT, "reports", "meta-coherence", "latest.json")
    data = json.load(open(latest, encoding="utf-8"))
    assert "issues_total" in data
    assert data["files"] > 0

def test_aliases_loaded():
    aliases_path = os.path.join(ROOT, ".kilo", "meta_coherence_aliases.yaml")
    assert os.path.exists(aliases_path)
    import yaml
    data = yaml.safe_load(open(aliases_path, encoding="utf-8"))
    assert "aliases" in data
