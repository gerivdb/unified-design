---
type: ADR
status: proposed
date: "2026-07-29"
intent_hash: 0xCTULU_L4_MASTER_INTENT_20260729
---

# CTULU L4 Master Intent - Exploitation Complete du Pipeline Anamorphique

## 1. Objectif Global
Creer un **intent magistral** qui orchestre l'ensemble du systeme d'ingenierie graphique (DAG-3) en s'appuyant sur le pipeline **CTULU L4** (anamorphique, multi-couches N+1/N+2/N+3/N+4). Cet intent doit :

1. **Unifier** les principes de la Graph Engineering (noeuds isoles, barriere, fixing agent) sous une gouvernance unique.
2. **Deployer** une feuille de route (roadmap) coherente sur 12 mois, incluant la creation d'ADR, d'PICS, de sous-intents, d'issues et de scenarios d'imprevus.
3. **Assurer** la traabilite et la conformite via des ADR, tout en prevoyant des mecanismes de mitigation pour les imprevus.

## 2. Vision a Haute Niveau (N+4)

```
N+1 - Gouvernance (GOVERNANCE-HUB)           ->  Decisions architecturales officielles
N+2 - Analyse des lacunes (ARGUS)             ->  Identification des gaps
N+3 - Orchestration (CTULU)                   ->  Execution parallelevia CTULU L4
N+4 - Assurance Meta (GOVERNANCE-HUB/NEXUS)   ->  Validation finale et gouvernance continue
```

## 3. Roadmap (12 mois)

| Mois | Jalons Cles | Livrables Principaux |
|------|-------------|----------------------|
| **M1** | Kickoff & audit | Adascan du depot - Rapport de gap analysis (ARGUS) |
| **M2** | Definition des sousintents | ADR001CTULUL4Scope - Catalogue des intents subalternes |
| **M3** | Prototypage du pipeline CTULU L4 | PoC "GraphEnginev1" - Validation via trixtest |
| **M4** | Creation des ADR de gouvernance | ADR002CTULUL4JUDGMENTRULE - ADR003CTULUL4SECONDOPINION |
| **M5** | Implementation des roles (detecteurs vs correcteurs) | Skillcreator pour "fixingagent" - CI gate "designcompliance" |
| **M6** | Lancement du **SecondOpinion** (`-p`) a grande echelle | Dashboard de scores de conformite (95%) |
| **M7-M8** | Optimisation du **Headless Shell** et reduction des tokens | Benchmark token/memory - Modifications dans `dispatch.zig` |
| **M9** | Deploiement des **Roadmap & EPIC** en production | ROADMAP-CTULU-L4.md - EPICS.md complet |
| **M10** | **Thermonuclear Review** prerelease | Execution du pipeline complet sur tags - Rapport d'incident & mitigation |
| **M11** | Bilan de maturite (N+4) | valuation Niveau4 -> 5 transition plan |
| **M12** | Publication officielle & archivage | Documentation finale (ADR, EPICS, issues) - Versionnage Git tag `v1.0-CTULU-L4` |

## 4. Sub-intents (SousObjectifs)

| Intent | Description | Owner | Priority |
|--------|-------------|-------|----------|
| **INTENTCTULUL4JUDGMENT** | Definir les regles d'utilisation du modele Opus pour les noeuds de jugement | Architecte | Critique |
| **INTENTCTULUL4SECONDOPINION** | Implementer le mecanisme `-p` avec isolation d'historique | Lead Engineer | Haute |
| **INTENTCTULUL4HEADLESSOPT** | Remplacer Chrome complet par chromeheadless-shell et documenter les parametres | DevOps | Moyenne |
| **INTENTCTULUL4FIXINGAGENT** | Creer l'agent de correction base sur le rapport unifie | Responsable Corrige | Haute |
| **INTENTCTULUL4ORCHESTRATOR** | Orchestration multi-specialistes (Security, Design, Simplify) | Chef d'Orchestration | Haute |
| **INTENTCTULUL4THERMONUCLEAR** | Procedure de revue thermonucleaire prerelease | QA Lead | Faible (decClenchee uniquement) |

## 5. ADR Relatifs au Projet

| ADR | Sujet | Statut |
|-----|-------|--------|
| **ADR20260729001CTULUL4JUDGMENTRULE** | Obligation d'utiliser Opus sur tout noeud de jugement | proposed |
| **ADR20260729002CTULUL4SECONDOPINION** | Formalisation du protocole `-p` et exigences de isolation | proposed |
| **ADR20260729003CTULUL4HEADLESSOPT** | Politique d'utilisation du headless shell pour la capture d'ecran | proposed |
| **ADR20260729004CTULUL4FIXINGAGENTROLE** | Separation stricte des roles detector / corrector | proposed |
| **ADR20260729005CTULUL4THERMONUCLEARGATE** | Processus de declenchement de la revue thermonucleaire | proposed |

*Tous les ADR doivent etre versionnes dans `gerivdb/GOVERNANCE-HUB/ADR/` et suivre le front-matter habituel.*

## 6. pics (Feature Sets)

```yaml
epics:
  - id: EPIC-CTULU-001
    title: "Graph Engine v1 - Parallel Node Execution"
    description: "Implementer le graphe de noeuds isoles avec barrier et fixing agent."
    priority: high
    labels: [graph, parallelism, ctulul4]
    
  - id: EPIC-CTULU-002
    title: "Second-Opinion Service"
    description: "Deployer le mecanisme `-p` avec des sessions independantes."
    priority: critical
    labels: [security, isolation, second-opinion]
    
  - id: EPIC-CTULU-003
    title: "Headless Shell Integration"
    description: "Optimiser la capture d'ecran via chromeheadlessshell."
    priority: medium
    labels: [performance, imaging]
    
  - id: EPIC-CTULU-004
    title: "Orchestrateur Multi-Specialist"
    description: "Coordonner security, design, simplify agents via meta-node."
    priority: high
    labels: [orchestration, specialization]
    
  - id: EPIC-CTULU-005
    title: "Thermonuclear Review Pipeline"
    description: "Processus de revue exhaustive avant toute tag release."
    priority: low
    labels: [release, thermonuclear]
```

## 7. Issues (Backlog)

| Issue | Description | Impact | Owner | Status |
|-------|-------------|--------|-------|--------|
| **ISSUE-CTULU-001** | Faux positifs elevee avec Haiku sur les noeuds de jugement | Perte de tokens | Engineer | Open |
| **ISSUE-CTULU-002** | Latence additionnelle du mecanisme `-p` (>500ms) | Degradation du debit | DevOps | Open |
| **ISSUE-CTULU-003** | Compatibilite du headless shell avec les futures mises a jour Windows | Risque de rupture | QA Lead | Open |
| **ISSUE-CTULU-004** | Conflits de version lorsqu multiple specialistes ecrivent dans le meme repertoire `design.md` | Corruption de guide de conception | Architecte | Open |
| **ISSUE-CTULU-005** | Gestion de la memoire lorsqu'on lance >4 instances headless simultanement | OOM crashes | DevOps | Open |

## 8. Impacts & Imprevus Anticipes

| Scenario | Probabilite | Consequence | Mitigation |
|----------|-------------|-------------|------------|
| Explosion du nombre de noeuds (ex. 10+ parallel tasks) | Moyenne | Saturation de la memoire (au-dela de 2,5 GB) | Limiter le nombre de taches paralleles a 4; mise en place d'un semaphore base sur le tag `max_concurrency=4` |
| Decouverte tardive d'un gap de securite (ex. CVE non detectees) | Basse | Vulnerabilite critique en production | Executer Security-Agent en parallele avec second-opinion et bloquer le merge tant que le score de securite < 90% |
| Modifications simultanees de `design.md` causing merge conflicts | levee | Blocage du pipeline CI | Instaurer un lock-file `design.lock` et forcer les PR a passer par l'Orchestrateur avant toute modification |
| Timeout du barrier node (agent ne rend pas de rapport) | Faible | Bloque l'ensemble du pipeline | Implementer un watchdog qui relance l'agent ou qui passe en mode fallback-sequential apres 30s |

## 9. Gouvernance & Conformite

1. **Toutes les modifications** au pipeline CTULU L4 doivent etre documentees dans un ADR et approuvees par le Architecture Review Board.
2. **Chaque intent subordonne** doit posseder un intent-hash unique, reference dans les metadonnees du pipeline (`ctulu-l4.json`).
3. **Les EPICs** sont traces dans le registre `EPICS.md` et lies a leurs ADR via `references:` afin d'assurer la traabilite de bout en bout.
4. **Les issues** sont gerees dans le backlog GitHub avec le label `CTULU-L4`; chaque fermeture doit etre accompagnee d'une note de release-note mis a jour.
5. **Les imprevus** sont consignes dans le fichier `UNEXPECTED.md` (format Markdown) et revises lors de chaque Thermonuclear Review.

## 10. Checklist de Validation avant Merge

- [ ] Tous les ADR crees ont ete **merged** dans `gerivdb/GOVERNANCE-HUB/ADR/` avec status `proposed` -> `accepted`.
- [ ] Le **pipeline CTULU L4** passe les verifications `design-compliance` (95% de conformite au fichier `design.md`).
- [ ] Le **Second-Opinion** est execute en mode `-p` et retourne un score de conformite 95%.
- [ ] Les tests de charge ne depassent pas **4 instances headless** simultanees.
- [ ] Aucun **ISSUECTULU*** bloquant n'est marque `open`.
- [ ] Le **Roadmap-CTULU-L4.md** est a jour et versionne sous tag Git `roadmap-v1.0`.
- [ ] Les **EPICs** sont listes dans `EPICS.md` avec leurs statuts respectifs.

## 11. Tous les ADR doivent etre versionnes dans `gerivdb/GOVERNANCE-HUB/ADR/` et suivre le front-matter habituel.

## 12. pics (Feature Sets)