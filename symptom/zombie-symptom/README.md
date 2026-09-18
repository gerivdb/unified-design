# Zombie Symptom Pattern

Pattern générique de détection, classification, purge et audit des symptômes zombies
dans l'écosystème gerivdb.

## Structure

```
zombie-symptom/
├── README.md                 # Ce fichier
├── template/                 # Templates génériques (réutilisables)
│   ├── symptom.yaml          # Définition du pattern
│   ├── detector.yaml         # Détection des zombies
│   ├── classifier.yaml       # Classification par sévérité/type
│   ├── purger.yaml           # Stratégies de purge sécurisées
│   ├── auditor.yaml          # Vérification post-purge + reporting
│   └── hook.yaml             # Intégration workflows + hooks git
└── instances/                # Instances concrètes du pattern
    ├── process-zombie-proliferation/
    │   ├── symptom.yaml
    │   ├── detector.yaml
    │   ├── classifier.yaml
    │   ├── purger.yaml
    │   ├── auditor.yaml
    │   └── hook.yaml
    ├── worktree-lock-syndrome/
    │   └── symptom.yaml
    ├── cross-repo-conflict-syndrome/
    │   └── symptom.yaml
    ├── phi-cps-drift-syndrome/
    │   └── symptom.yaml
    ├── node-handle-leak-syndrome/
    │   └── symptom.yaml
    └── zig-compilation-hang-syndrome/
        └── symptom.yaml
```

## Instances

| Instance | Symptôme ciblé | Couche | Status |
|----------|---------------|--------|--------|
| process-zombie-proliferation | Processus zombies (node, electron, Code) | L2/L4 | proposed |
| worktree-lock-syndrome | Worktrees orphelins/bloqués | L2 | proposed |
| cross-repo-conflict-syndrome | Conflits cross-repo non résolus | L1/L2 | proposed |
| phi-cps-drift-syndrome | Dérive phi/CPS dans workflows | L3/L4 | proposed |
| node-handle-leak-syndrome | Fuites de handles Node.js | L4 | proposed |
| zig-compilation-hang-syndrome | Compilations Zig bloquées | L2/L4 | proposed |

## Usage

1. Copier le template souhaité depuis `template/`
2. Adapter les seuils et méthodes à l'instance spécifique
3. Enregistrer dans `instances/<nom-instance>/`
4. Intégrer via les hooks/workflows définis dans `hook.yaml`

## Référence ADR
- **ADR** : ADR-2026-08-09-001-GIT_HYGIENE_MECHANISMS
- **IntentHash** : 0xGIT_HYGIENE_RULES_20260809
- **Dépôt** : gerivdb/GeriCode
- **Statut ADR** : proposed
