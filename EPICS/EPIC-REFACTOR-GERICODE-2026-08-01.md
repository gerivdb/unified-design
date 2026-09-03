---
intent_hash: 0xEPIC_REFACTOR_GERICODE_20260801
status: active
priority: P0
owner: gerivdb
repo: gerivdb/GOVERNANCE-HUB
---

# EPIC-REFACTOR-GERICODE-2026-08-01 -- Phase E : Refactoring GeriCode vers L3-CITIZENS

## Resumexecutif

La Phase D a ete completee avec succes. La migration L2-PLATFORM vers L3-CITIZENS est validee,le service psy_state_machine est deploye, et les artefacts sont commites. La Phase E visearefactoriser GeriCode pour qu ilconforme pleinement aux normes L3-CITIZENS et valider l authentification CDS + CID.

**IntentHash**: 0xEPIC_REFACTOR_GERICODE_20260801
**Date de creation**: 2026-08-01
**Statut**: active (P0)

---

## Contexte et Justification

### Phase D Completee
- Migration L2-PLATFORM vers L3-CITIZENS executee
- psy_state_machine.yaml deploie et valide
- REGISTRY.yaml mis a jour avec ONTOLOGY-FILL-SCHEMA
- Tous les artefacts de Phase D commites

### Problematique Phase E
GeriCode reside actuellement dans D:\DO\WEB\TOOLS\L2-PLATFORM\GeriCode. Il doit etrerefactore pour etre conforme a l architecture L3-CITIZENS et valider l authentificationCDS (Credential Delegation Service) et CID (Cross-Repo Identity Delegation).

---

## Objectifs Phase E

### O1. Refactoring GeriCode vers L3-CITIZENS (P0)
- **Source**: D:\DO\WEB\TOOLS\L2-PLATFORM\GeriCode
- **Cible**: D:\DO\WEB\TOOLS\L3-CITIZENS\GeriCode\refactored
- **Action**: Deplacer et restructurer GeriCode selon les normes L3-CITIZENS

### O2. Validation CDS + CID Authentication (P1)
- **CDS**: Credential Delegation Service - credential delegation
- **CID**: Cross-Repo Identity Delegation - cross-repo identity
- **Validation**: S assurer que GeriCode peut deleguer les credentiels et l identitecross-repo

### O3. Mise a jour du pattern-router (P1)
- Ajouter les mots-cles GeriCode au pattern-router
- Ajouter le routage pour les operations GeriCode dans le systeme GERICODE/KILOCODE

### O4. Validation finale et documentation (P2)
- Verifier la conformite avec ONTOLOGY_DECLARATION.yaml
- Documenter les changements dans le rapport de phase

---

## Scope et Dependances

### In Scope
- [ ] Deplacer GeriCode de L2-PLATFORM vers L3-CITIZENS
- [ ] Refactoring GeriCode pour conformite L3-CITIZENS
- [ ] Validation CDS authentication
- [ ] Validation CID cross-repo identity delegation
- [ ] Mise a jour pattern-router avec mots-cles GeriCode
- [ ] Validation conformite ONTOLOGY

### Out of Scope
- Modification du code metier existant des autres services
- Changement de schema de base de donnees

### Dependances
- ADR-2026-08-01-001 (GERICODE KILOCODE ASSIMILATION)
- ADR-2026-06-28-001 (ARCHITECTURE LOGIQUE N1-N4)
- ADR-091-HITL-GATE-FOR-CLONE
- ADR-093-ZIG-015-API-COMPATIBILITY
- Phase D artifacts (EPIC-ASSIMILATION-2026-08-01.md)

---

## Architecture Technique

### Structure Cible Phase E
```
L3-CITIZENS/
|-- GeriCode/
|   |-- refactored/
|   |   |-- package.json         # Avec _kilo frontmatter
|   |   |-- extension.ts         # Refactore en modules
|   |   |-- bat-family-chat/     # Module bat-family-chat
|   |   |-- ecos-cli-bridge/     # Module ecos-cli-bridge
|   |   `-- quality-check-runner/# Module quality-check-runner
|   `-- design.yaml              # Design GeriCode L3
```

### Fichier de Configuration Phase E
```yaml
# config/PHASE_E.yaml
phase_e:
  refactoring:
    source: "D:/DO/WEB/TOOLS/L2-PLATFORM/GeriCode"
    target: "D:/DO/WEB/TOOLS/L3-CITIZENS/GeriCode/refactored"
    type: "full_refactor"
    
  authentication:
    cds:
      enabled: true
      validation: "credential_delegation"
      target: "L3-CITIZENS"
    cid:
      enabled: true
      validation: "cross_repo_identity"
      target: "L3-CITIZENS"
```

---

## Methriques de Succes

| Metrique | Cible | Validation |
|----------|-------|------------|
| GeriCode migre vers L3-CITIZENS | 100% | PR merge |
| CDS authentication validee | Pass | Integration test |
| CID identity delegation validee | Pass | Cross-repo test |
| pattern-router mis a jour | Complete | Routing test |
| Conformite ONTOLOGY | 100% | Audit OK |

---

## Planning

| Sprint | Taches | Statut |
|--------|--------|--------|
| Sprint 1 | EPIC creation + Refactoring plan | En cours |
| Sprint 2 | GeriCode migration vers L3-CITIZENS | A venir |
| Sprint 3 | CDS + CID authentication validation | A venir |
| Sprint 4 | Pattern-router update + Finalisation | A venir |

---

## Securite et Compliance

### BDCP Mode
- Conformite maintenue
- Aucun acces non autorise
- Logging complet des operations

### Git Safety
- Verification git remote -v avant push
- Commits atomiques (<3 fichiers)
- Pas de force push sans autorisation

---

## References

- **ADR**: ADR-2026-08-01-001 (GERICODE KILOCODE ASSIMILATION)
- **ADR**: ADR-2026-06-28-001 (ARCHITECTURE LOGIQUE N1-N4)
- **Phase C**: benchmark-analysis.json
- **Phase D**: EPIC-ASSIMILATION-2026-08-01.md
- **Pattern Router**: ADR-2026-06-28-001

---

## Risques et Mitigations

| Risque | Probabilite | Impact | Mitigation |
|--------|-------------|--------|------------|
| Conflits de migration GeriCode | Moyen | Eleve | Feature branch dediee |
| Perte de fonctionnalites Bat-Family | Faible | Eleve | Tests integration completes |
| CDS authentication failure | Faible | Critique | Validation pre-migration |
| CID delegation failure | Faible | Critique | Cross-repo test pre-migration |
| BDCP violation | Tres faible | Critique | Guard watchdog 300s |
---

*Phase E: Refactoring GeriCode vers L3-CITIZENS*
*Version: 1.0*
*Date: 2026-08-01*
