---
status: proposed
date: "2026-07-26"
intent_hash: 0xADR_HITL_SESSION_PROTOCOL_20260726
author: gerivdb
---

# ADR-030 : Protocole de Session HITL Obligatoire

## Contexte

La session du 2026-07-26 a révélé 6 erreurs récurrentes de l'assistant dues à l'absence de protocole formalisé :

1. **Ignorance des designs sources** - `meta-design.yaml` non consulte avant mutations (LLM-REPO, TOPOS ajoutes a posteriori)
2. **Non-respect consignes utilisateur** - GitHub Actions propose 3+ fois malgre KIVA-CLI impose (ADR-024)
3. **Manque validation prealable** - `kiva ci run` execute sans verifier pipeline existant
4. **Construction incrementale** - DAG ASCII produit apres corrections, pas comme guide initial
5. **Propagation sans audit** - `sync-scripts.sh` lance sans `--dry-run`
6. **Checkpoints a posteriori** - Mis a jour fin de session, jamais consultes avant action

Ces erreurs ont allongé la session de ~40% et généré des frictions inutiles.

## Décision

**Tout agent HITL opérant sur l'écosystème gerivdb DOIT suivre le Protocole de Session HITL (ATOM-HITL-SESSION-PROTOCOL) avant toute action mutante.**

Le protocole impose 5 étapes séquentielles obligatoires :

| Étape | Action | Outil | Critère de passage |
|-------|--------|-------|-------------------|
| **0. BOOT** | `kiva ci run --dry-run <repo>` + `cat meta-design.yaml \| grep strates` | KIVA-CLI + shell | Pipeline existe + strates connues |
| **1. DAG FIRST** | Produire DAG ASCII consolidé (macro + micro) | Assistant | DAG complet AVANT action |
| **2. CI SOUVERAINE** | Interdiction formelle CI externe si KIVA-CLI spécifié | ADR-024 | Aucune proposition GitHub Actions |
| **3. DRY-RUN OBLIGATOIRE** | `sync-scripts.sh --dry-run` + `kiva ci run --dry-run` | Scripts + KIVA-CLI | 0 divergence avant exécution réelle |
| **4. CHECKPOINT GUARD** | `kilo_local_recall` AVANT action critique -> écrire APRÈS validation | kilo_local_recall | Checkpoint lu avant, écrit après |

## Conséquences

- **Temps de session réduit** : Élimination cycles correction (gain estimé 40%)
- **Traçabilité totale** : Chaque mutation précédée de validation documentée
- **Souveraineté KIVA-CLI** : ADR-024 respectée sans exception
- **Auditabilité** : Checkpoints servent de garde-fou, pas seulement de journal

## Implémentation

1. **ATOM** : `atoms/hitl-session-protocol.yaml` (déclaration normative, 167ème atome)
2. **Convention** : `conventions/hitl/SESSION_WORKFLOW.md` (procédure pas-à-pas)
3. **Validation** : `kiva ci run unified-design` valide la présence de l'atome + registre

## Exceptions

- **Hotfix critique** (production down) : Étapes 0+1+4 obligatoires, 2+3 autorisés à posteriori (max 2h)
- **Session lecture-seule** (audit, recherche) : Étapes 2+3 non requises

## Références

- ADR-024 : KIVA-CLI Souveraineté Validation
- ATOM-HITL-GATE : Mécanisme blocage opérations sensibles
- ATOM-KIVA-AUTO-PR-WORKFLOW : Workflow PR automatique
- ATOM-HITL-SESSION-PROTOCOL : Déclaration normative (cet ADR)

## Phase d'Approbation HITL (GATE-5)

**NOUVEAU** : Avant passage de `proposed` -> `accepted`, une validation HITL explicite est requise :

```
GATE-5 : HITL APPROVAL
|-- Revue par l'utilisateur (humain dans la boucle)
|-- Confirmation explicite : "APPROUVE ADR-030"
|-- Signature : timestamp + identité
|-- Changement status: proposed -> accepted
```

### Critères d'approbation

- [ ] Protocole 5 étapes (BOOT -> DAG -> CI -> DRY-RUN -> CHECKPOINT) validé
- [ ] ATOM `hitl-session-protocol.yaml` présent et registre à jour
- [ ] Convention `SESSION_WORKFLOW.md` testée sur session réelle
- [ ] Aucune régression sur sessions lecture-seule / hotfix

### Traçabilité

```yaml
hitl_approval:
  adr: ADR-030
  status_before: proposed
  status_after: accepted
  approved_by: <identité>
  approved_at: <ISO8601>
  criteria_met: [BOOT, DAG_FIRST, CI_SOUVERAINE, DRY_RUN, CHECKPOINT_GUARD]
```

## Statut

**Proposed** - En attente de validation HITL (GATE-0 -> GATE-5) avant passage `accepted`.