---
intent_hash: 0xEPIC_ASSIMILATION_20260801
status: active
priority: P0
owner: gerivdb
repo: gerivdb/GOVERNANCE-HUB
---

# EPIC-ASSIMILATION-2026-08-01 -- Phase D : GERICODE KILOCODE ASSIMILATION

## 📋 Résumé Exécutif

La Phase C a été terminée avec succès. Les benchmarks dépassent les objectifs, la conformité ONTOLOGY est à 100%, et les livrables sont validés. La Phase D vise à préparer l'assimilation complète du système GERICODE dans l'écosystème KILOCODE.

**IntentHash** : `0xEPIC_ASSIMILATION_20260801`  
**Date de création** : 2026-08-01  
**Statut** : active (P0)

---

## 🔍 Contexte & Justification

### Phase C Complétée
- Benchmarks validés avec latence 65-72ms (cible 75ms)
- Taux d'erreur 0.1-0.3% (cible <1%)
- Throughput 92-128 ops/sec (cible 50 ops/sec)
- Conformité ONTOLOGY 100%

### Problématique de la Phase D
La migration du nommage `L2-PLATFORM` -> `L3-CITIZENS` necessite une coordination cross-repo et l'implementation d'un service d'etat dynamique (`psy_state_machine`).

---

## 🎯 Objectifs de la Phase D

### O1. Création du Service `psy_state_machine` (P1)
- **Type** : Service d'état cognitif dynamique
- **Localisation** : `ONTOLOGY/psy_state_machine.yaml`
- **Fonction** : Gestion des états des citoyens via machine à états finis

### O2. Migration du Nommage L2-PLATFORM → L3-CITIZENS (P1)
- **Portée** : Tous les fichiers et répertoires sous `L2-PLATFORM`
- **Cible** : Renommer en `L3-CITIZENS` conformément à l'architecture stratifiée
- **Impact** : Synchronisation croisée-repo nécessaire

### O3. Mise à jour de REGISTRY.yaml (P0)
- **Mapping** : `ONTOLOGY-FILL-SCHEMA`
- **Source** : `gerivdb/ONTOLOGY`
- **Destination** : `config/REGISTRY.yaml`

---

## 📊 Scope & Dépendances

### In Scope
- [ ] Création fichier `ONTOLOGY/psy_state_machine.yaml`
- [ ] Migration répertoires `L2-PLATFORM` → `L3-CITIZENS`
- [ ] Mise à jour `REGISTRY.yaml` avec mapping schema
- [ ] Validation BDCP compliance

### Out of Scope
- Modifications du code métier existant
- Changements de schéma de base de données

### Dépendances
- ADR-2026-08-01-001 (GERICODE KILOCODE ASSIMILATION)
- ADR-091-HITL-GATE-FOR-CLONE
- ADR-093-ZIG-015-API-COMPATIBILITY

---

## 🛠️ Architecture Technique

### Structure Cible
```
ONTOLOGY/
├── psy_state_machine.yaml    # Nouveau service
├── L3-CITIZENS/              # Migré depuis L2-PLATFORM
│   ├── citizens/
│   └── schemas/
└── L4_TOOLS/                 # Existant
```

### Fichier de Configuration
```yaml
# config/REGISTRY.yaml
ontology_fill_schema:
  version: "1.0"
  sources:
    - gerivdb/ONTOLOGY/psy_state_machine.yaml
    - gerivdb/BRAIN/citizen_registry.json
  mappings:
    L2-PLATFORM: L3-CITIZENS
    schema_version: "2.1"
```

---

## 📈 Métriques de Succès

| Métrique | Cible | Validation |
|----------|-------|------------|
| `psy_state_machine.yaml` créé | ✅ | PR merge |
| Migration L2→L3 complète | 100% | 0 fichiers L2-PLATFORM |
| REGISTRY.yaml mis à jour | ✅ | Commit validé |
| BDCP compliance | Maintenu | Audit OK |

---

## 📅 Planning

| Sprint | Tâches | Statut |
|--------|--------|--------|
| Sprint 1 | EPIC création + psy_state_machine.yaml | 🔄 En cours |
| Sprint 2 | Migration L2→L3 + REGISTRY.yaml | ⏳ À venir |
| Sprint 3 | Validation + Documentation | ⏳ À venir |

---

## 🔐 Sécurité & Compliance

### BDCP Mode
- ✅ Conformité maintenue
- ✅ Aucun accès non autorisé
- ✅ Logging complet des opérations

### Git Safety
- [ ] Vérification `git remote -v` avant push
- [ ] Commits atomiques (<3 fichiers)
- [ ] Pas de force push sans autorisation

---

## 📚 Références

- **ADR** : ADR-2026-08-01-001 (GERICODE KILOCODE ASSIMILATION)
- **ONTOLOGY** : ONTOLOGY_DECLARATION.yaml
- **Phase C** : benchmark-analysis.json
- **Pattern Router** : ADR-2026-06-28-001

---

## ⚠️ Risques & Mitigations

| Risque | Probabilité | Impact | Mitigation |
|--------|-------------|--------|------------|
| Conflits de merge L2→L3 | Moyen | Élevé | Branche feature dédiée |
| Perte de traçabilité | Faible | Élevé | WAL journalisation |
| BDCP violation | Très faible | Critique | Guard watchdog 300s |