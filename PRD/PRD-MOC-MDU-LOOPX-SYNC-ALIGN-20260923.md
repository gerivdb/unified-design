---
type: PRD-MOC
version: "1.0.0"
date: "2026-09-23"
status: proposed
intent_hash: 0xPRD_MOC_MDU_LOOPX_SYNC_ALIGN_20260923
author: gerivdb
source_repo: gerivdb/unified-design
ontology:
  concepts:
    - mdu-sync
    - loopx-routine
    - design-applier
    - registry-sync
  repo: gerivdb/ONTOLOGY
---

# PRD-MOC — MDU Design Sync + LOOPX Routine Alignment

> **Périmètre** : audit, mise à jour et alignement des designs MDU (`unified-design`) avec les routines LOOPX disponibles. Garantir que chaque design MDU fonctionnel est couvert par une routine LOOPX exécutable, et que les routines LOOPX reflètent les designs à jour.
> **Coordination transverse** : voir `designs/*.yaml`, `workflows/*.md`, `LOOPX/routines/`.

---

## 1. Objectif

1. Vérifier que tous les designs MDU de `unified-design` sont **réellement fonctionnels** (YAML valide, références complètes, pas de draft orphelin).
2. Vérifier que chaque design MDU fonctionnel dispose **d'une routine LOOPX correspondante** (ou d'un plan de création).
3. Mettre à jour les designs obsolètes, corriger les chemins/références, et créer les routines LOOPX manquantes.
4. Maximiser le nombre de routines LOOPX couvrant les designs MDU.
5. Produire un rapport de synchronisation MDU ↔ LOOPX avec gaps et actions.

---

## 2. Livrables assignés

| ID | Livrable | Chemin cible | Type | Statut |
|---|---|---|---|---|
| L1 | Audit MDU designs | `reports/mdu-loopx-audit-20260923.md` | Créer | ⏳ |
| L2 | Corrections designs | `designs/*.yaml` | Mettre à jour | ⏳ |
| L3 | Matrice MDU → LOOPX | `reports/mdu-loopx-matrix-20260923.csv` | Créer | ⏳ |
| L4 | Routines LOOPX manquantes | `LOOPX/routines/*.yaml` | Créer | ⏳ |
| L5 | Mise à jour registry | `catalog/designs.index.yaml`, `atoms_registry.yaml` | Mettre à jour | ⏳ |
| L6 | Validation finale | `reports/mdu-loopx-validation-20260923.md` | Créer | ⏳ |

---

## 3. Tâches

### Phase A — Audit MDU

1. **A1** : Scanner tous les `designs/*.yaml` et vérifier :
   - YAML valide
   - `status` ≠ `draft` orphelin (sauf intention)
   - `intent_hash` présent
   - `adr` référencé
   - `depends_on` / `inherits` cohérents
2. **A2** : Vérifier la cohérence `catalog/designs.index.yaml` ↔ `designs/`
3. **A3** : Vérifier la cohérence `atoms_registry.yaml` ↔ `atoms/methodology/git/`

### Phase B — Matrice MDU → LOOPX

4. **B1** : Lister les routines LOOPX existantes (`LOOPX/routines/*.yaml`)
5. **B2** : Pour chaque design MDU fonctionnel, vérifier s'il existe une routine LOOPX correspondante (mapping par nom/intent_hash)
6. **B3** : Identifier les gaps (designs sans routine LOOPX)
7. **B4** : Pour chaque routine LOOPX existante, vérifier si elle correspond à un design MDU (détection d'orphelines)

### Phase C — Corrections

8. **C1** : Corriger les designs défaillants (YAML, références, status)
9. **C2** : Mettre à jour `catalog/designs.index.yaml` et `atoms_registry.yaml`
10. **C3** : Créer les routines LOOPX manquantes pour les designs sans couverture

### Phase D — Validation

11. **D1** : Exécuter `mdu-lint --strict` (ou équivalent) pour valider la couverture
12. **D2** : Exécuter un dryrun causal : vérifier que chaque routine LOOPX peut être invoquée et produit un résultat
13. **D3** : Générer le rapport final avec taux de couverture MDU → LOOPX

---

## 4. Contraintes

- **Atomicité** : chaque correction = commit séparé (max 3 fichiers, max 30 min)
- **MDU prioritaire** : si un design est en conflit avec une routine LOOPX, le design MDU fait foi (SOT)
- **LOOPX max** : créer une routine LOOPX pour TOUT design MDU fonctionnel sauf exception documentée
- **Validation YAML** : tout design YAML doit passer `check-yaml` et `mdu-lint --strict`
- **Dryrun causal** : la validation finale passe par un script dryrun qui simule l'invocation de chaque routine LOOPX

---

## 5. Plan de commits proposé

| Commit | Fichiers | Description |
|---|---|---|
| `chore(mdu): audit MDU designs and LOOPX routines` | `reports/mdu-loopx-audit-20260923.md` | Phase A |
| `fix(mdu): correct design YAML and references` | `designs/*.yaml` | Phase C (corrections) |
| `feat(loopx): add missing routine for <design>` | `LOOPX/routines/<routine>.yaml` | Phase C (1 par routine) |
| `chore(mdu): update registry and matrix` | `catalog/*`, `atoms_registry.yaml`, `reports/mdu-loopx-matrix-20260923.csv` | Phase B/D |
| `chore(mdu): validate MDU-LOOPX alignment` | `reports/mdu-loopx-validation-20260923.md` | Phase D |

---

## 6. Critères d'acceptation

1. `reports/mdu-loopx-audit-20260923.md` créé avec liste complète des designs et routines.
2. Tous les designs MDU ont `status: active` ou `status: approved` (pas de draft orphelin).
3. `catalog/designs.index.yaml` et `atoms_registry.yaml` sont cohérents avec `designs/` et `atoms/`.
4. Pour chaque design MDU fonctionnel, une routine LOOPX existe **ou** un gap documenté avec raison.
5. `reports/mdu-loopx-matrix-20260923.csv` contient le mapping complet design → routine LOOPX.
6. `mdu-lint --strict` passe avec 0 erreur, 0 warning.
7. Dryrun causal : chaque routine LOOPX référencée peut être invoquée et retourne un statut connu.

---

## 7. Proof-of-Life

- [ ] 2026-09-23T03:33:50+02:00 — Création PRD-MOC MDU-LOOPX Sync Align
- [ ] 2026-09-23T03:40:00+02:00 — Audit MDU designs terminé
- [ ] 2026-09-23T03:50:00+02:00 — Matrice MDU → LOOPX créée
- [ ] 2026-09-23T04:00:00+02:00 — Corrections designs appliquées
- [ ] 2026-09-23T04:10:00+02:00 — Routines LOOPX manquantes créées
- [ ] 2026-09-23T04:15:00+02:00 — Validation finale dryrun causal OK

---

## 8. Références

- `designs/` — designs MDU
- `workflows/` — workflows MDU
- `LOOPX/routines/` — routines LOOPX
- `catalog/designs.index.yaml` — index designs
- `atoms_registry.yaml` — registre atoms
- `reports/mdu-loopx-audit-20260923.md` — rapport d'audit
