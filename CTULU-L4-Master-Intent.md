---
type: ADR
status: proposed
date: "2026-07-29"
intent_hash: 0xCTULU_L4_MASTER_INTENT_20260729
---

<<<<<<< HEAD
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
=======
# CTULU L4 Master Intent - Exploitation Complte du Pipeline Anamorphique

## 1. Objectif Global
Crer un **intent magistral** qui orchestre lensemble du systme dingnierie graphique (DAG3) en sappuyant sur le pipeline **CTULU L4** (anamorphique, multicouches N+1/N+2/N+3/N+4).  
Cet intent doit :

1. **Unifier** les principes de la Graph Engineering (nuds isols, barrire, fixing agent) sous une gouvernance unique.  
2. **Dployer** une feuille de route (roadmap) cohrente sur 12mois, incluant la cration dADR, dPICS, de sousintents, dissues et de scnarios dimprvus.  
3. **Assurer** la traabilit et la conformit via des ADR, tout en prvoyant des mcanismes de mitigation pour les imprvus.

## 2. Vision  Haute Niveau (N+4)

```
N+1 - Gouvernance (GOVERNANCE-HUB)          ->  Dcisions architecturales officielles
N+2 - Analyse des lacunes (ARGUS)           ->  Identification des gaps
N+3 - Orchestration (CTULU)                 ->  Excution paralllevia CTULU L4
N+4 - Assurance Meta (GOVERNANCE-HUB/NEXUS)  ->  Validation finale et gouvernance continue
```

## 3. Roadmap (12mois)

| Mois | Jalons Cls | Livrables Principaux |
|------|-------------|----------------------|
| **M1** | Kickoff & audit | - Adascan du dpt <br> - Rapport de gap analysis (ARGUS) |
| **M2** | Dfinition des sousintents | - ADR001CTULUL4Scope <br> - Catalogue des intents subalternes |
| **M3** | Prototypage du pipeline CTULU L4 | - PoC GraphEnginev1 <br> - Validation via **trixtest** |
| **M4** | Cration des ADR de gouvernance | - ADR002CTULUL4JUDGMENTRULE <br> - ADR003CTULUL4SECONDOPINION |
| **M5** | Implmentation des rles (detecteurs vs correcteurs) | - Skillcreator pour fixingagent <br> - CI gate designcompliance |
| **M6** | Lancement du **SecondOpinion** (`-p`)  grande chelle | - Dashboard de scores de conformit (95%) |
| **M7M8** | Optimisation du **Headless Shell** et rduction des tokens | - Benchmark token/memory <br> - Modifications dans `dispatch.zig` |
| **M9** | Dploiement des **Roadmap & EPIC** en production | - `ROADMAP-CTULU-L4.md` <br> - `EPICS.md` complet |
| **M10** | **Thermonuclear Review** prrelease | - Excution du pipeline complet sur tags <br> - Rapport dincident & mitigation |
| **M11** | Bilan de maturit (N+4) | - valuation Niveau4 -> 5 transition plan |
| **M12** | Publication officielle & archivage | - Documentation finale (ADR, EPICS, issues) <br> - Versionnage Git tag `v1.0-CTULU-L4` |

## 4. Intents Subalternes (SousObjectifs)

| Intent | Description | Owner | Priorit |
|--------|-------------|-------|----------|
| **INTENTCTULUL4JUDGMENT** | Dfinir les rgles dutilisation du modle Opus pour les nuds de jugement | Architecte | Critique |
| **INTENTCTULUL4SECONDOPINION** | Mettre en place le mcanisme `-p` avec isolation dhistorique | Lead Engineer | Haute |
| **INTENTCTULUL4HEADLESSOPT** | Remplacer Chrome complet par `chromeheadlessshell` et documenter les paramtres | DevOps | Moyenne |
| **INTENTCTULUL4FIXINGAGENT** | Crer lagent de correction bas sur le rapport unifi | Responsable Corrige | Haute |
| **INTENTCTULUL4ORCHESTRATOR** | Orchestration multispcialistes (Security, Design, Simplify) | Chef dOrchestration | Haute |
| **INTENTCTULUL4THERMONUCLEAR** | Procdure de revue thermonuclaire prrelease | QA Lead | Faible (dclenche uniquement) |
>>>>>>> 88da000 (feat(ge): implement DAG-3 Graph Engineering design with CTULU L4 master intent)

## 5. ADR Relatifs au Projet

| ADR | Sujet | Statut |
|-----|-------|--------|
<<<<<<< HEAD
| **ADR20260729001CTULUL4JUDGMENTRULE** | Obligation d'utiliser Opus sur tout noeud de jugement | proposed |
| **ADR20260729002CTULUL4SECONDOPINION** | Formalisation du protocole `-p` et exigences de isolation | proposed |
| **ADR20260729003CTULUL4HEADLESSOPT** | Politique d'utilisation du headless shell pour la capture d'ecran | proposed |
| **ADR20260729004CTULUL4FIXINGAGENTROLE** | Separation stricte des roles detector / corrector | proposed |
| **ADR20260729005CTULUL4THERMONUCLEARGATE** | Processus de declenchement de la revue thermonucleaire | proposed |

*Tous les ADR doivent etre versionnes dans `gerivdb/GOVERNANCE-HUB/ADR/` et suivre le front-matter habituel.*
=======
| **ADR20260729001CTULUL4JUDGMENTRULE** | Obligation dutiliser Opus sur tout nud de jugement | proposed |
| **ADR20260729002CTULUL4SECONDOPINION** | Formalisation du protocole `-p` et exigences de isolation | proposed |
| **ADR20260729003CTULUL4HEADLESSOPT** | Politique dutilisation du headless shell pour le capture dcran | proposed |
| **ADR20260729004CTULUL4FIXINGAGENTROLE** | Sparation stricte des rles detector / corrector | proposed |
| **ADR20260729005CTULUL4THERMONUCLEARGATE** | Processus de dclenchement de la revue thermonuclaire | proposed |

*Tous les ADR doivent tre versionns dans `gerivdb/GOVERNANCE-HUB/ADR/` et suivre le frontmatter habituel.*
>>>>>>> 88da000 (feat(ge): implement DAG-3 Graph Engineering design with CTULU L4 master intent)

## 6. pics (Feature Sets)

```yaml
epics:
  - id: EPIC-CTULU-001
    title: "Graph Engine v1 - Parallel Node Execution"
<<<<<<< HEAD
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
    
=======
    description: "Implmenter le graphe de nuds isols avec barrier et fixing agent."
    priority: high
    labels: [graph, parallelism, ctulul4]

  - id: EPIC-CTULU-002
    title: "SecondOpinion Service"
    description: "Dployer le mcanisme `-p` avec des sessions indpendantes."
    priority: critical
    labels: [security, isolation, second-opinion]

  - id: EPIC-CTULU-003
    title: "Headless Shell Integration"
    description: "Optimiser la capture dcran via chromeheadlessshell."
    priority: medium
    labels: [performance, imaging]

  - id: EPIC-CTULU-004
    title: "Orchestrateur MultiSpecialist"
    description: "Coordonner security, design, simplify agents via metanode."
    priority: high
    labels: [orchestration, specialization]

>>>>>>> 88da000 (feat(ge): implement DAG-3 Graph Engineering design with CTULU L4 master intent)
  - id: EPIC-CTULU-005
    title: "Thermonuclear Review Pipeline"
    description: "Processus de revue exhaustive avant toute tag release."
    priority: low
    labels: [release, thermonuclear]
```

<<<<<<< HEAD
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
=======
## 7. Issues Cohrentes (Backlog)

| Issue | Description | Impact | Owner | Status |
|-------|-------------|--------|-------|--------|
| **ISSUE-CTULU-001** | Faux positifs leve avec Haiku sur les nuds de jugement | Perte de tokens | Engineer | Open |
| **ISSUE-CTULU-002** | Latence additionnelle du mcanisme `-p` (>500ms) | Dgradation du dbit | DevOps | Open |
| **ISSUE-CTULU-003** |Compatibilit du headless shell avec les futures mises  jour Windows | Risque de rupture | QA Lead | Open |
| **ISSUE-CTULU-004** | Conflits de version lorsqu plusieurs spcialistes crivent dans le mme rpertoire `design.md` | Corruption de design guide | Architecte | Open |
| **ISSUE-CTULU-005** | Gestion de la mmoire lorsquon lance >4 instances headless simultanment | OOM crashes | DevOps | Open |

## 8. Impacts & Imprvus Anticips

| Scnario | Probabilit | Consquence | Mitigation |
|----------|-------------|-------------|------------|
| **Explosion du nombre de nuds** (ex. 10+parallel tasks) | Moyenne | Saturation de la mmoire (audel de 2,5GB) | Limiter le nombre de tches parallles  4; mise en place dun semaphore bas sur le tag `max_concurrency=4` |
| **Dcouverte tardive dun gap de scurit** (ex. CVEs non dtectes) | Basse | Vulnrabilit critique en production | Excuter **SecurityAgent** en parallle avec *secondopinion* et bloquer le merge tant que le score de scurit <90% |
| **Modifications simultanes de `design.md`** causing merge conflicts | leve | Blocage du pipeline CI | Instaurer un **lockfile** `design.lock` et forcer les PR  passer par le **Orchestrateur** avant toute modification |
| **Timeout du barrier node** (agent ne rend pas de rapport) | Faible | Bloque lensemble du pipeline | Implmenter un watchdog qui relance lagent ou qui passe en mode *fallbacksequential* aprs 30s |

## 9. Gouvernance & Conformit

1. **Toutes les modifications** au pipeline CTULU L4 doivent tre documentes dans un ADR et approuves par le **Architecture Review Board**.  
2. **Chaque intent subordonn** doit possder un **intenthash** unique, rfrenc dans les mtadonnes du pipeline (`ctulu-l4.json`).  
3. **Les EPICs** sont tracs dans le registre `EPICS.md` et lis  leurs ADR via `references:` afin dassurer la traabilit de bout en bout.  
4. **Les issues** sont gres dans le backlog GitHub avec le label `CTULU-L4`; chaque fermeture doit tre accompagne dune note de **releasenote** mise  jour.  
5. **Les imprvus** sont consigns dans le fichier `UNEXPECTED.md` (format Markdown) et rviss lors de chaque **Thermonuclear Review**.

## 10. Checklist de Validation avant Merge

- [ ] Tous les ADR crs ont t **merged** dans `gerivdb/GOVERNANCE-HUB/ADR/` avec status `proposed` -> `accepted`.  
- [ ] Le **pipeline CTULU L4** passe les vrifications `designcompliance` (95% de conformit au fichier `design.md`).  
- [ ] Le **SecondOpinion** est excut en mode `-p` et retourne un score de conformit 95%.  
- [ ] Les tests de charge ne dpassent pas **4 instances headless** simultanes.  
- [ ] Aucun **ISSUECTULU*** bloquant nest marqu `open`.  
- [ ] Le **Roadmap-CTULU-L4.md** est  jour et versionn sous tag Git `roadmap-v1.0`.  
- [ ] Les **EPICS** sont lists dans `EPICS.md` avec leurs statuts respectifs.  

---  

*Ce document constitue le **Intent Magistral** pour lexploitation complte du pipeline anamorphique CTULU L4. Il servira de rfrence unique pour toutes les quipes dingnierie, de gouvernance et de QA lors de la conception, du dploiement et de la maintenance du systme graphique DAG3.*
>>>>>>> 88da000 (feat(ge): implement DAG-3 Graph Engineering design with CTULU L4 master intent)
