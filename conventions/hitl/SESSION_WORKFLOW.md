# SESSION_WORKFLOW.md — Procédure Opératoire HITL Session
# Version: 1.0.0
# IntentHash: 0xSESSION_WORKFLOW_HITL_20260726
# Source: ADR-030-hitl-session-protocol.md
# Gouvernance: HITL Gate requis

---

## 🔴 RÈGLE ZÉRO — Rien ne démarre sans Phase 0

**Avant le premier token d'action mutante**, l'agent HITL **doit** exécuter :

```bash
# 0.1 Pipeline KIVA-CLI cible existe et valide
kiva ci run --dry-run <target_repo>

# 0.2 Strates consultées
cat meta-design.yaml | grep -A5 "strates:"

# 0.3 Checkpoints lus (kilo_local_recall)
kilo_local_recall search --query "<action_critique>"
```

> **Échec = BLOCK**. Aucune excuse. Cette phase coûte < 30 secondes et évite 40% d'erreurs.

---

## PHASE 1 — DAG ASCII PREMIER (Non Négociable)

Le DAG consolidé **macro (REPO-STANDARDS) + micro (unified-design)** doit exister **avant** :

- Création de fichier (write)
- Modification de code (edit)
- Exécution de script mutatif
- Proposition d'architecture

**Livrable** : `DAG_ASCII.md` consolidé avec :
- Strates physiques L0-L5 (macro)
- Couches logiques N+1 à N+4 (macro)
- Atoms + Dependencies + Conventions + Design Instances (micro)
- Pipelines KIVA-CLI + Validation (micro)

---

## PHASE 2 — VALIDATION LOCALE SEULE (ADR-024)

| ❌ INTERDIT | ✅ REQUIS |
|-------------|-----------|
| GitHub Actions pour valider design | `kiva ci run <repo>` |
| GitLab CI / Jenkins / CircleCI | Pipeline `.kiva/pipelines/<repo>.yaml` |
| "Je vais créer un workflow CI" | `kiva ci run --dry-run` d'abord |

> **Rappel ADR-024** : KIVA-CLI est l'**unique** outil de validation design. Toute proposition externe = violation.

---

## PHASE 3 — DRY-RUN SYSTÉMATIQUE

**Tout script mutatif** doit avoir passé `--dry-run` avec succès avant exécution réelle :

```bash
# Scripts de synchronisation
sync-scripts.sh --dry-run

# Pipelines KIVA
kiva ci run --dry-run <repo>

# Tout script custom mutatif
<mon_script>.ps1 --dry-run
<mon_script>.py --dry-run
```

> **Règle** : Si le script n'a pas d'option `--dry-run`, l'agent **doit** l'ajouter avant de proposer son exécution.

---

## PHASE 4 — CHECKPOINT POST-VALIDATION

Le checkpoint s'écrit **après** la validation réussie, **jamais** après correction d'erreur.

**Format checkpoint** :
```yaml
session_id: <kilo_session_id>
action: <description_courte>
validation_status: SUCCESS
dag_hash: <sha256_du_DAG_ASCII>
timestamp: <ISO8601>
```

**Outil** : `kilo_local_recall` pour lecture/écriture.

---

## 📋 CHECKLIST RAPIDE (Copier-coller au début de session)

```markdown
## HITL SESSION CHECKLIST
- [ ] Phase 0.1 : `kiva ci run --dry-run <target>` ✅
- [ ] Phase 0.2 : Strates consultées (`meta-design.yaml`) ✅
- [ ] Phase 0.3 : Checkpoints lus (`kilo_local_recall`) ✅
- [ ] Phase 1 : DAG ASCII consolidé produit & validé ✅
- [ ] Phase 2 : Aucune CI externe proposée (ADR-024) ✅
- [ ] Phase 3 : Tous dry-run passés avant exécution ✅
- [ ] Phase 4 : Checkpoint post-validation écrit ✅
```

---

## SANCTIONS

| Violation | Conséquence |
|-----------|-------------|
| Phase 0 omise | STOP immédiat — session en violation ADR-030 |
| DAG après mutation | REVERT — refaire avec DAG d'abord |
| CI externe proposée | REJET — violation ADR-024 + ADR-030 |
| Dry-run absent | BLOCK — exécution interdite |
| Checkpoint pré-validation | INVALID — réécrire post-validation |

---

## RÉFÉRENCES

- **ADR** : `ADR-030-hitl-session-protocol.md`
- **ATOM** : `atoms/hitl-session-protocol.yaml`
- **ADR lié** : `ADR-024-kiva-cli-souverainete-validation.md`
- **ATOM lié** : `atoms/hitl-gate.yaml`
- **INTENT** : `INTENT-030-hitl-session-protocol.md`