# Worktree Engineering — Spécification de Conception

**Dépôt** : unified-design (L0)  
**Worktree** : `feat/wt-worktree-engineering-docs`  
**Date** : 2026-10-26  
**IntentHash** : 0xDESIGN_WTE_20261026

---

## 1. Définition — Qu'est-ce que le Worktree Engineering ?

Le **Worktree Engineering** est la discipline qui transforme un *worktree Git* (copie de travail) en un **isolat programmable et opératoire** dont le cycle de vie est entièrement maîtrisé par des scripts d'infrastructure.

Dans l'écosystème gerivdb, ce principe est incarné par le **Hook de Naissance** (`setup-script.ps1`) qui s'exécute à la création de chaque worktree managé par l'Agent Manager Kilo Code. Avant même que l'agent ne lise son premier prompt, ce script configure l'environnement :

| Étape | Action | Résultat |
|-------|--------|----------|
| **Hydratation** | Jonctions NTFS vers caches partagés (node_modules, .venv) | Prêt en < 200 ms, zéro duplication disque |
| **Contrat** | Génération `WORKTREE_MISSION.md` | Périmètre strict, IntentHash, commande de test |
| **Enrôlement** | Création `.kilo/bus/`, signal `session-spawned.json` | Visibilité immédiate dans WAZAA |
| **Armement** | `core.hooksPath` → `.githooks` du repo maître | CP1252, fichiers interdits, index propre |
| **Réaper** | Teardown auto : merge check, nettoyage jonctions, bail WAL | Clôture propre garantie |

---

## 2. Ontologie — Les Trois Couches

| Couche | Terme | Définition | Focus |
|--------|-------|------------|-------|
| **L0 — Ontologie** | **Worktree-Managed** | État d'un worktree déclaré, suivi, géré par un système d'orchestration (Agent Manager) | État, métadonnées, cycle de vie, statut |
| **L1 — Design** | **Worktree-Design** | Architecture du conteneur : structure dossiers, fichiers config, hooks, jonctions, identité | Forme, contenu, organisation |
| **L2 — Engineering** | **Worktree-Engineering** | Mise en œuvre technique : scripts, jonctions NTFS, bus signaux, tests, procédures | Mécanismes, outils, exécution |

**Hiérarchie** : L'ontologie définit *ce qu'est* un worktree managé ; le design définit *à quoi il ressemble* ; l'ingénierie définit *comment il fonctionne*.

---

## 3. Le Principe : Relatif au "worktree", Indépendant de l'Outil

Le **Worktree Engineering** n'est pas lié à Kilo Code, ni à GeriCode, ni à VS Code. C'est un principe applicable à **tout outil utilisant des worktrees Git** (`git worktree add`, `git worktree remove`, etc.).

| Transposable (universel) | Outil-spécifique |
|--------------------------|------------------|
| Hook de naissance (script à la création) | Syntaxe `setup-script.ps1` (PowerShell) |
| Jonctions ressources partagées (zero-copy) | Emplacement `.kilo/bus/` |
| Enrôlement dans un bus de signaux | Format `agent-manager.json` |
| Armement des garde-fous (hooks pré-commit) | Format `agent-manager.json` |
| Protocole clôture (réaper, baux, WAL) | Format `agent-manager.json` |

**Conclusion** : Le *Worktree Engineering* est une discipline générique ; son implémentation dans gerivdb est une instance concrète.

---

## 4. Les 5 Skills Worktree Engineering (Implémentés)

| # | Skill | Opération | Script | Effet |
|---|-------|-----------|--------|-------|
| 1 | `worktree-zero-copy-hydrator` | Hydratation zero-copy | `hydrate.ps1` | Jonctions NTFS node_modules/.venv en <200ms |
| 2 | `worktree-genetic-contractor` | Contrat `WORKTREE_MISSION.md` | `contract.ps1` | Périmètre, IntentHash, test unitaire |
| 3 | `worktree-synaptic-bus-joiner` | Enrôlement bus `.kilo/bus/` | `join_bus.ps1` | Visibilité WAZAA immédiate |
| 4 | `worktree-precommit-armorer` | Armement `core.hooksPath` | `armor.ps1` | CP1252, fichiers interdits, index propre |
| 5 | `worktree-lifecycle-reaper` | Teardown auto : merge check, nettoyage, bail WAL | `reap.ps1` | Clôture propre garantie |

---

## 6. Implémentation de Référence (gerivdb)

| Composant | Localisation | Rôle |
|-----------|--------------|------|
| Hook de naissance | `D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\.kilo\setup-script.ps1` | Point d'entrée unique |
| Skills Worktree Engineering | `D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\skills\worktree-*` | 5 skills atomiques |
| Opérateur unifié | `D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\skills\kilo-worktree-operator\scripts\wt_operator.py` | 6 super-pouvoirs CLI |
| Bus inter-worktrees | `.kilo/bus/` + `session-spawned.json` | Communication via WAZAA |

---

## 7. Références ADR & SSoT

| ADR | Titre | Statut |
|-------|-------|--------|
| ADR-2026-06-28-001 | Logical Architecture N1-N4 | proposed |
| ADR-2026-05-14-004 | KILO-CODE-HOTL-OPERATIONAL-STD | proposed |
| ADR-2026-06-28-001 | PR-LIFECYCLE-GATE | proposed |
| ADR-2026-05-28-001 | WSL1-RUNTIME-Z600 | proposed |

---

## 8. Conclusion

Le **Worktree Engineering** est une discipline générique applicable à **tout outil utilisant des worktrees Git**. Dans gerivdb, il est incarné par 5 skills atomiques + 1 opérateur unifié (`kilo-worktree-operator`), déployés dans `L4-TOOLS/SKILLS` et opérationnels via l'Agent Manager.

**EXIT CODE : 0** — Spécification complète et cohérente.

---

*Document généré dans le dépôt `unified-design` (L0).*