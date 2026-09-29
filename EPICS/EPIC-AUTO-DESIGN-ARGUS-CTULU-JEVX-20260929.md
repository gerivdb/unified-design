---
type: EPIC
version: "1.0.0"
date: "2026-09-29"
status: proposed
priority: P1
owner: gerivdb
repo: gerivdb/unified-design
---

# EPIC — Auto-Design ARGUS/CTULU/JEVX Integration

## Contexte

`auto-design` est fonctionnel mais isolé. Il ne bénéficie pas des capacités existantes d'ARGUS (validation sémantique), CTULU (traçabilité, commits, gouvernance) et JEVX (projection/synchronisation). Cet EPIC intègre ces trois composants pour transformer auto-design en validateur écosystémique complet.

## Objectif

Exploiter ARGUS, CTULU et JEVX pour :
1. Ajouter la validation sémantique des bridges et cross-refs
2. Automatiser la gestion des commits (conventional commits, atomic commits, auto-commit)
3. Intégrer la traçabilité cross-repo
4. Ajouter la projection/synchronisation JEVX
5. Améliorer la classification des composants via KG-L

## Scope

### Inclus

- **P0** : Conventional commits, atomic commits, commit messages, ARGUS bridge/crossref validation
- **P1** : Templates commit, auto-commit on deploy, branch/commit coupling, tests intégration
- **P2** : Meta-coherence gate, traceability validation, NODEX classification, JEVX projection, governance synthesizer
- **Subalternes** : TASKs par livrable atomique
- **Documentation** : README intégration, exemples, troubleshooting

### Exclu

- Refonte architecturale d'auto-design
- Modification des scanners ARGUS existants
- Modification des outils CTULU existants
- Création de nouveaux repos

## Critères d'acceptation

- [ ] `_score_conventional_commit_adherence()` retourne score 0-100
- [ ] `_check_atomic_commits()` détecte commits >3 fichiers
- [ ] `generate_commit_message()` génère messages conventionnels
- [ ] `_validate_bridges_argus()` retourne findings GAP/DRIFT/VOID/UNPROVEN
- [ ] `_validate_crossrefs_argus()` retourne findings ORPHAN/GAP/STALE/BROKEN
- [ ] Templates commit déployés dans `scripts/`
- [ ] `deploy_with_auto_commit()` commit et push automatiquement
- [ ] `create_pr()` vérifie cohérence branch → commit → PR
- [ ] `_check_meta_coherence()` bloque si `status != OK`
- [ ] `_validate_traceability()` retourne violations
- [ ] `_detect_components()` utilise NODEX + KG-L
- [ ] Templates JEVX projection fonctionnels
- [ ] `auto_promote.py` génère 6 artifacts + commit via CTULU
- [ ] Tests intégration passent (couverture 80%)
- [ ] Documentation intégration complète

## Livrables

| ID | Livrable | Priorité | Effort |
|---|---|---|---|
| L1 | Conventional commit scoring | P0 | 1h |
| L2 | Atomic commit checking | P0 | 30min |
| L3 | Commit message generation | P0 | 30min |
| L4 | ARGUS bridge validation | P0 | 1h |
| L5 | ARGUS crossref validation | P0 | 1h |
| L6 | Commit templates | P1 | 1h |
| L7 | Auto-commit on deploy | P1 | 1h |
| L8 | Branch/commit coupling | P1 | 30min |
| L9 | Tests intégration | P1 | 2h |
| L10 | Meta-coherence gate | P2 | 2h |
| L11 | Traceability validation | P2 | 3h |
| L12 | NODEX classification | P2 | 2h |
| L13 | JEVX projection templates | P2 | 2h |
| L14 | Governance synthesizer integration | P2 | 2h |

## Références

- **INTENT** : `INTENT-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md`
- **PRD** : `PRD-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md`
- **MOC** : `MOC-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md`
- **ADR** : `ADR-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md`
- **Repo ARGUS** : `gerivdb/ARGUS`
- **Repo CTULU** : `gerivdb/CTULU`
- **Repo JEVX** : mécanisme intégré à CTULU/TALEX
- **Repo KG-L** : `gerivdb/KG-L`
