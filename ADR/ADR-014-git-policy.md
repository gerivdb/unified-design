# ADR-014 : Politique Git du Meta-Design Unified

- **Statut** : accepted
- **Date** : 2026-07-15
- **IntentHash** : 0xGIT_POLICY_META_DESIGN_20260715
- **Dépôt** : gerivdb/unified-design
- **Piliers concernés** : Connard Design (CD) + Governance Hub (N+4)

---

## Contexte

Les dépôts de design (connard-design, morphohdl-anamorphic-growth, triadic-compound-eye, sonar-driven-design) ont été initialisés avec des commits directs sur `main`. Cela a rendu impossible la création de PRs de revue, et a contourné le workflow GitFlow cible du Meta-Design Unified (MDU).

Il faut donc :
1. Verrouiller `main` contre les pushes directs.
2. Standardiser la politique Git pour tous les dépôts de l’écosystème.
3. Prévenir les récidives par hook + validation + documentation.

---

## Décision

### Branches
- `main` : branche de production. Protégée. Aucun push direct autorisé.
- `feat/*` : branches de feature.
- `hotfix/*` : branches de correctif urgent.

### Règles
- Toute modification passe par une PR `feat/*` → `main`.
- La PR nécessite au moins 1 validation.
- Le hook `pre-push` bloque les pushes depuis `main` ou `master`.
- `meta-design.yaml` contient la section `git_policy` comme source de vérité.

### Outils
- Hook `pre-push` global via Git template (`init.templateDir`).
- `connard-validator` étendu pour valider `git_policy`.
- Protection de branche GitHub activée sur `main`.

---

## Alternatives considérées

- **Option A** : reset `main` + cherry-pick des commits d’initialisation. Retenue pour `connard-design`.
- **Option B** : commit placeholder sur branche `feat/*`. Retenue pour les 3 dépôts sans commit antérieur.
- **Option C** : accepter le statu quo. Écartée car elle ne résout pas la cause racine.

---

## Conséquences

- Historique Git régularisé.
- Workflow GitFlow respecté.
- Traçabilité des modifications garantie.
- Gouvernance MDU renforcée.

---

## Référence ADR

- **ADR** : ADR-014-git-policy-meta-design
- **IntentHash** : 0xGIT_POLICY_META_DESIGN_20260715
- **Dépôt** : gerivdb/unified-design
- **Statut ADR** : accepted
