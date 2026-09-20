#!/usr/bin/env python3
"""
Audit complet des artefacts inédits : skills, citizens, pipelines, primitives,
workflows, designs/atoms à déduire de la conversation et/ou à mettre à jour.
Compare les fichiers du filesystem avec les catalogues index.
"""

import yaml
from pathlib import Path

REPO = Path(r"D:\DO\WEB\TOOLS\L0-CANON\unified-design")

def load_catalog(name):
    path = REPO / "catalog" / name
    if not path.exists():
        print(f"[WARN] Catalogue manquant: {path}")
        return {}
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data if data else {}

def get_registered_ids(catalog_data, source_repo="unified-design"):
    """Extrait tous les IDs enregistrés pour un repo donné."""
    ids = set()
    for entry in catalog_data.get("entries", []):
        if entry.get("source_repo") == source_repo:
            ids.add(entry.get("id", "").lower())
    return ids

def get_registered_paths(catalog_data, source_repo="unified-design"):
    """Extrait tous les source_path enregistrés pour un repo donné."""
    paths = set()
    for entry in catalog_data.get("entries", []):
        if entry.get("source_repo") == source_repo:
            paths.add(entry.get("source_path", "").lower())
    return paths

def scan_filesystem(directory, pattern="*"):
    """Scanne le filesystem et retourne les chemins relatifs."""
    files = set()
    for p in sorted(directory.glob(pattern)):
        if p.is_file():
            rel = p.relative_to(REPO)
            files.add(str(rel).lower())
    return files

def scan_subdirs(directory):
    """Scanne tous les sous-dossiers et retourne les chemins relatifs des fichiers."""
    files = set()
    if not directory.exists():
        return files
    for p in sorted(directory.rglob("*")):
        if p.is_file():
            rel = p.relative_to(REPO)
            files.add(str(rel).lower())
    return files

def main():
    # Charger les catalogues
    skills_catalog = load_catalog("skills.index.yaml")
    primitives_catalog = load_catalog("primitives.index.yaml")
    citizens_catalog = load_catalog("citizens.index.yaml")
    designs_catalog = load_catalog("designs.index.yaml")
    atoms_catalog = load_catalog("atoms.index.yaml")
    pipelines_catalog = load_catalog("pipelines.index.yaml")
    workflows_catalog = load_catalog("workflows.index.yaml")

    # IDs et chemins enregistrés
    registered_skill_ids = get_registered_ids(skills_catalog)
    registered_skill_paths = get_registered_paths(skills_catalog)
    registered_primitive_ids = get_registered_ids(primitives_catalog)
    registered_primitive_paths = get_registered_paths(primitives_catalog)
    registered_citizen_ids = get_registered_ids(citizens_catalog)
    registered_citizen_paths = get_registered_paths(citizens_catalog)
    registered_design_ids = get_registered_ids(designs_catalog)
    registered_design_paths = get_registered_paths(designs_catalog)
    registered_atom_ids = get_registered_ids(atoms_catalog)
    registered_atom_paths = get_registered_paths(atoms_catalog)
    registered_pipeline_ids = get_registered_ids(pipelines_catalog)
    registered_pipeline_paths = get_registered_paths(pipelines_catalog)
    registered_workflow_ids = get_registered_ids(workflows_catalog)
    registered_workflow_paths = get_registered_paths(workflows_catalog)

    # Fichiers filesystem
    fs_skills = scan_subdirs(REPO / "skills")
    fs_primitives = scan_subdirs(REPO / "primitives")
    fs_citizens = scan_subdirs(REPO / "citizens")
    fs_designs = scan_subdirs(REPO / "designs")
    fs_atoms = scan_subdirs(REPO / "atoms")
    fs_pipelines = scan_subdirs(REPO / "pipelines")
    fs_workflows = scan_subdirs(REPO / "workflows")

    print("=" * 80)
    print("AUDIT ARTEFACTS INÉDITS — unified-design")
    print("=" * 80)

    # 1. Skills
    print("\n### SKILLS ###")
    missing_skills = []
    for skill_path in sorted(fs_skills):
        if skill_path not in registered_skill_paths:
            missing_skills.append(skill_path)
            print(f"  [MANQUANT CATALOGUE] {skill_path}")

    # Vérifier les skills connus
    known_skills = [
        "skills/ecosystem-meta-coherence-analyzer/skill.md",
        "skills/dryrun-causal-auditor/skill.md",
    ]
    for ks in known_skills:
        if ks.lower() not in registered_skill_paths:
            print(f"  [À ENREGISTRER] {ks}")

    if not missing_skills:
        print("  [OK] Tous les skills filesystem sont catalogués")

    # 2. Primitives
    print("\n### PRIMITIVES ###")
    missing_prims = []
    for prim_path in sorted(fs_primitives):
        if prim_path not in registered_primitive_paths:
            missing_prims.append(prim_path)
            print(f"  [MANQUANT CATALOGUE] {prim_path}")

    known_prims = [
        "primitives/ecosystem-meta-coherence.yaml",
    ]
    for kp in known_prims:
        if kp.lower() not in registered_primitive_paths:
            print(f"  [À ENREGISTRER] {kp}")

    if not missing_prims:
        print("  [OK] Toutes les primitives filesystem sont cataloguées")

    # 3. Citizens
    print("\n### CITIZENS ###")
    missing_citizens = []
    for cit_path in sorted(fs_citizens):
        if cit_path not in registered_citizen_paths:
            missing_citizens.append(cit_path)
            print(f"  [MANQUANT CATALOGUE] {cit_path}")

    known_citizens = [
        "citizens/meta-coherence-auditor/citizen.yaml",
        "citizens.yaml",
    ]
    for kc in known_citizens:
        if kc.lower() not in registered_citizen_paths:
            print(f"  [À ENREGISTRER] {kc}")

    if not missing_citizens:
        print("  [OK] Tous les citizens filesystem sont catalogués")

    # 4. Designs / Atoms
    print("\n### DESIGNS & ATOMS ###")
    missing_designs = []
    for des_path in sorted(fs_designs):
        if des_path not in registered_design_paths:
            missing_designs.append(des_path)
            print(f"  [MANQUANT CATALOGUE] {des_path}")

    for atom_path in sorted(fs_atoms):
        if atom_path not in registered_atom_paths:
            print(f"  [MANQUANT CATALOGUE ATOM] {atom_path}")

    known_designs = [
        "designs/ecosystem-meta-coherence/design.yaml",
        "designs/jevx.yaml",
        "designs/jevx-engineering.yaml",
    ]
    for kd in known_designs:
        if kd.lower() not in registered_design_paths:
            print(f"  [À ENREGISTRER] {kd}")

    known_atoms = [
        "atoms/ecosystem-meta-coherence-gate.md",
        "atoms/typed-decision-api.yaml",
    ]
    for ka in known_atoms:
        if ka.lower() not in registered_atom_paths:
            print(f"  [À ENREGISTRER ATOM] {ka}")

    if not missing_designs:
        print("  [OK] Tous les designs/atoms filesystem sont catalogués")

    # 5. Pipelines
    print("\n### PIPELINES ###")
    missing_pipelines = []
    for pipe_path in sorted(fs_pipelines):
        if pipe_path not in registered_pipeline_paths:
            missing_pipelines.append(pipe_path)
            print(f"  [MANQUANT CATALOGUE] {pipe_path}")

    known_pipelines = [
        "pipelines/mdu-validation.yaml",
    ]
    for kp in known_pipelines:
        if kp.lower() not in registered_pipeline_paths:
            print(f"  [À ENREGISTRER] {kp}")

    if not missing_pipelines:
        print("  [OK] Tous les pipelines filesystem sont catalogués")

    # 6. Workflows
    print("\n### WORKFLOWS ###")
    missing_workflows = []
    for wf_path in sorted(fs_workflows):
        if wf_path not in registered_workflow_paths:
            missing_workflows.append(wf_path)
            print(f"  [MANQUANT CATALOGUE] {wf_path}")

    known_workflows = [
        "workflows/dryrun-causal-audit.md",
        "workflows/structural-fix-pipeline.md",
    ]
    for kw in known_workflows:
        if kw.lower() not in registered_workflow_paths:
            print(f"  [À ENREGISTRER] {kw}")

    if not missing_workflows:
        print("  [OK] Tous les workflows filesystem sont catalogués")

    # 7. Designs L2-PLATFORM migrés
    print("\n### DESIGNS L2-PLATFORM MIGRÉS (ajoutés le 2026-09-20) ###")
    l2_designs = [
        "designs/L2-PLATFORM/agent-manager-v99.yaml",
        "designs/L2-PLATFORM/agentic-git-branching.yaml",
        "designs/L2-PLATFORM/agentic-swarm-git-coordination.yaml",
        "designs/L2-PLATFORM/certified-execution-m5.yaml",
        "designs/L2-PLATFORM/conversation-semantic-layer.yaml",
        "designs/L2-PLATFORM/gericode.yaml",
        "designs/L2-PLATFORM/git-hygiene-architecture.yaml",
        "designs/L2-PLATFORM/global-branch-monitoring.yaml",
        "designs/L2-PLATFORM/m5-production-ontologique.yaml",
        "designs/L2-PLATFORM/rlm-243-laplace-optimization.yaml",
        "designs/L2-PLATFORM/ssm-ternary-spectrum.yaml",
        "designs/L2-PLATFORM/worktree-closure-protocol.yaml",
    ]
    for l2d in l2_designs:
        if l2d.lower() not in registered_design_paths:
            print(f"  [MANQUANT L2-PLATFORM] {l2d}")
        else:
            print(f"  [OK] {l2d}")

    # 8. Résumé des actions requises
    print("\n" + "=" * 80)
    print("RÉSUMÉ DES ACTIONS REQUISES")
    print("=" * 80)

    actions = []
    for kp in known_prims:
        if kp.lower() not in registered_primitive_paths:
            actions.append(f"Enregistrer primitive: {kp}")
    for ks in known_skills:
        if ks.lower() not in registered_skill_paths:
            actions.append(f"Enregistrer skill: {ks}")
    for kc in known_citizens:
        if kc.lower() not in registered_citizen_paths:
            actions.append(f"Enregistrer citizen: {kc}")
    for kd in known_designs:
        if kd.lower() not in registered_design_paths:
            actions.append(f"Enregistrer design: {kd}")
    for ka in known_atoms:
        if ka.lower() not in registered_atom_paths:
            actions.append(f"Enregistrer atom: {ka}")
    for kp in known_pipelines:
        if kp.lower() not in registered_pipeline_paths:
            actions.append(f"Enregistrer pipeline: {kp}")
    for kw in known_workflows:
        if kw.lower() not in registered_workflow_paths:
            actions.append(f"Enregistrer workflow: {kw}")

    if actions:
        for i, action in enumerate(actions, 1):
            print(f"  {i}. {action}")
    else:
        print("  [OK] Aucune action requise — tous les artefacts sont catalogués")

    # 9. Statistiques
    print("\n" + "=" * 80)
    print("STATISTIQUES")
    print("=" * 80)
    print(f"  Skills filesystem: {len(fs_skills)} | Catalogués: {len(registered_skill_paths)}")
    print(f"  Primitives filesystem: {len(fs_primitives)} | Catalogués: {len(registered_primitive_paths)}")
    print(f"  Citizens filesystem: {len(fs_citizens)} | Catalogués: {len(registered_citizen_paths)}")
    print(f"  Designs filesystem: {len(fs_designs)} | Catalogués: {len(registered_design_paths)}")
    print(f"  Atoms filesystem: {len(fs_atoms)} | Catalogués: {len(registered_atom_paths)}")
    print(f"  Pipelines filesystem: {len(fs_pipelines)} | Catalogués: {len(registered_pipeline_paths)}")
    print(f"  Workflows filesystem: {len(fs_workflows)} | Catalogués: {len(registered_workflow_paths)}")

if __name__ == "__main__":
    main()
