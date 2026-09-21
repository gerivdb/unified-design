---
type: PRD
version: "1.0"
date: "2026-09-22"
status: in_review
intent_hash: 0xPRD_MOC_SYMBIOSE_REVERSIBLE_PLUGIN_ARCHITECTURE_20260922
---

# PRD-MOC — Symbiose Reversible Plugin Architecture

**Repo** : `gerivdb/unified-design`  
**Strate** : L0-CANON  
**Statut** : in_review  
**Date** : 2026-09-22  
**Version** : 1.0 (création design + tensions assumées)

---

## Contexte

L'analyse du paradigme "Everything is a Plugin" (Cordis / DeepSeek Harness) révèle une convergence structurelle avec l'écosystème gerivdb :

- **Composition spatiale** : Cordis utilise des Fiber scopes pour isoler la visibilité des services ; gerivdb utilise `repo × périmètre(-Paths)` + WAZAA channels.
- **Composition temporelle** : Cordis garantit que toute inscription est réversible ; gerivdb dispose de `swarm lease` (SL4) et de WAL, mais sans invariant de réversibilité explicite pour les symbiotes.
- **Résolution dynamique** : Cordis utilise `ctx.<service>` + Proxy ; gerivdb utilise KG-L + WAZAA + TOPOS, mais sans point d'entrée unifié.

Il manque un **design formel** qui :
1. Mappe explicitement les concepts Cordis vers les mécanismes gerivdb existants ;
2. Établisse la réversibilité comme invariant de premier ordre pour les symbiotes ;
3. Identifie les tensions structurelles (réversibilité ↔ durabilité, hot-reload ↔ trans-repo, noyau non privilégié ↔ BDCP) et les résolve explicitement.

## Mission

Créer un design d'architecture `symbiose-reversible-plugin-architecture` qui formalise la convergence Cordis → gerivdb, avec :
- mapping Cordis → gerivdb explicite ;
- 5 principes d'architecture (dont noyau minimal explicite) ;
- contrat de symbiose comme relation réversible (formation → maintenance → dissolution) ;
- 3 tensions assumées documentées ;
- primitive de cycle de vie réversible ;
- workflow de reconfiguration coordonnée.

## Évaluation d'utilité

| Composant | Utilité | Impact | Effort | Justification |
|-----------|---------|--------|--------|---------------|
| Design architecture mapping | ⭐⭐⭐⭐⭐ | P0 | Minimal | Évite réinvention silencieuse ; base ADR-ready |
| Principe noyau minimal explicite | ⭐⭐⭐⭐⭐ | P0 | Minimal | Protège BDCP, swarm lease, IntentHash du "plugging" |
| Contrat symbiose réversible | ⭐⭐⭐⭐⭐ | P0 | Minimal | Garantit dissolution propre + traçabilité |
| Tensions assumées documentées | ⭐⭐⭐⭐ | P1 | Minimal | Transforme 3 faux-amis en choix de design explicités |
| Primitive lifecycle | ⭐⭐⭐⭐ | P1 | Minimal | Cycle formation/maintenance/dissolution avec rollback |
| Workflow reconfiguration | ⭐⭐⭐⭐ | P1 | Minimal | Reconfiguration coordonnée avec garanties dérivées |

**Verdict** : 4 P0 + 2 P1. Effort minimal, valeur architecturale élevée. Comble le gap entre modularité statique et composition dynamique.

## Périmètre

| Inclut | Exclut |
|--------|--------|
| Design `symbiose-reversible-plugin-architecture.yaml` | Implémentation runtime Cordis-like |
| Primitive `reversible-symbiose-lifecycle.yaml` | Moteur de résolution `ctx.<service>` |
| Workflow `symbiose-coordinated-reload.yaml` | Hot-reload atomique intra-processus |
| Mapping Cordis → gerivdb | Plugin system pour Flask/KIX |
| Tensions assumées + résolutions | Suppression de BDCP/swarm lease/IntentHash |

## Livrables

| # | Livrable | Chemin cible | Statut | Preuve d'exécution |
|---|----------|--------------|--------|-------------------|
| L1 | Design architecture | `designs/symbiose-reversible-plugin-architecture.yaml` | ✅ Créé | Commit `7720f29` — 2026-09-22 |
| L2 | Primitive lifecycle | `primitives/reversible-symbiose-lifecycle.yaml` | ✅ Créé | Commit `7720f29` — 2026-09-22 |
| L3 | Workflow reconfiguration | `workflows/symbiose-coordinated-reload.yaml` | ✅ Créé | Commit `7720f29` — 2026-09-22 |
| L4 | Catalogue index | `catalog/designs.index.yaml` | ✅ Mis à jour | Commit `7720f29` — 2026-09-22 |
| L5 | ADR backing | `GOVERNANCE-HUB/ADR/ADR-SYMBIOSE-REVERSIBLE-ARCHITECTURE-20260922.md` | ⏳ À créer | — |
| L6 | MOC orchestration | `MOC/MOC-SYMBIOSE-REVERSIBLE-ARCHITECTURE-20260922.md` | ⏳ À créer | — |

## Dépendances

| Dépendance | Type | Raison |
|------------|------|--------|
| `designs/swarm-lease.yaml` | amont | Coordination primitive |
| `designs/safe-action-pattern.yaml` | amont | Contraintes exécutables |
| `designs/design-ops-loop.yaml` | amont | Boucle opérationnelle |
| `designs/kg-l-causal-diff.yaml` | pair | Traçabilité causale |
| `designs/agent-observability-architecture.yaml` | pair | Observabilité |
| `GOVERNANCE-HUB/ADR/ADR-2026-08-28-001` | pair | ADR swarm lease |

## Gates et critères d'acceptation

| Gate | Critère formel | Validation | Statut |
|------|---------------|------------|--------|
| **G1** | Design validé par pre-commit hook (frontmatter + IntentHash) | `git commit` | ✅ Passe |
| **G2** | 5 principes documentés + tensions assumées | Review ADR | ⏳ En attente |
| **G3** | Primitive lifecycle avec rollback explicite | Review ADR | ⏳ En attente |
| **G4** | Workflow avec garanties dérivées (lease TTL / 2) | Review ADR | ⏳ En attente |
| **G5** | ADR backing créé | GOVERNANCE-HUB | ⏳ À créer |

## Critères d'acceptation

- [x] Design `symbiose-reversible-plugin-architecture.yaml` créé avec 5 principes + mapping Cordis → gerivdb + tensions assumées
- [x] Primitive `reversible-symbiose-lifecycle.yaml` créée avec dissolution_cost + rollback
- [x] Workflow `symbiose-coordinated-reload.yaml` créé avec garanties dérivées + drain inbound
- [x] Catalogue `catalog/designs.index.yaml` mis à jour
- [ ] ADR `ADR-SYMBIOSE-REVERSIBLE-ARCHITECTURE-20260922.md` créé dans GOVERNANCE-HUB
- [ ] MOC `MOC-SYMBIOSE-REVERSIBLE-ARCHITECTURE-20260922.md` créé

## Risques

| Risque | Impact | Mitigation |
|--------|--------|------------|
| Faux-ami Cordis → gerivdb | Élevé | Tensions assumées documentées + ADR review |
| Résolution `ctx.<service>` divergente | Élevé | À trancher avant ADR : WAZAA ? KG-L ? Les deux ? |
| Rollback sans borne dérivée | Moyen | Borne = lease TTL / 2, pas valeur arbitraire |
| Noyau privilégié caché | Moyen | 3 invariants non-négociables listés explicitement |

## Références

- `designs/swarm-lease.yaml` — Coordination primitive
- `designs/safe-action-pattern.yaml` — Contraintes exécutables
- `designs/design-ops-loop.yaml` — Boucle opérationnelle
- `designs/kg-l-causal-diff.yaml` — Traçabilité causale
- `designs/agent-observability-architecture.yaml` — Observabilité
- `GOVERNANCE-HUB/ADR/ADR-2026-08-28-001` — ADR swarm lease
- DeepSeek Harness / Cordis — Inspiration paradigme EIP

## Preuves d'exécution

| Action | Date | Commit | Référence |
|--------|------|--------|-----------|
| Création design | 2026-09-22 | `7720f29` | `designs/symbiose-reversible-plugin-architecture.yaml` |
| Création primitive | 2026-09-22 | `7720f29` | `primitives/reversible-symbiose-lifecycle.yaml` |
| Création workflow | 2026-09-22 | `7720f29` | `workflows/symbiose-coordinated-reload.yaml` |
| Mise à jour catalogue | 2026-09-22 | `7720f29` | `catalog/designs.index.yaml` |
