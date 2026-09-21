---
type: REPORT
status: final
date: "2026-09-21"
intent_hash: 0xREPORT_TALEX_FRICTION_SESSION_20260921
---

# Rapport TALEX — Analyse causale des frictions de session

**Repo** : `gerivdb/unified-design`  
**Strate** : L0-CANON  
**Date** : 2026-09-21  
**Statut** : final  

---

## Résumé exécutif

Cette session d'implémentation du système d'extraction d'artefacts a généré **8 frictions opérationnelles**. Aucune n'a bloqué l'implémentation finale, mais elles ont causé des retours en arrière et des workarounds manuels.

**Verdict TALEX** : ⚠️ Frictions évitables. Corrections structurelles recommandées pour éviter la répétition.

---

## Tableau des frictions

| # | Erreur | Fréquence | Impact | Dégradabilité | Cause racine |
|---|--------|-----------|--------|---------------|--------------|
| 1 | `edit` échec indentation | 3 | Moyen | ✅ Workaround | `meta-design.yaml` mélange espaces/tabs |
| 2 | `validate_yaml.py` KO sur `.md` | 4 | Faible | ✅ Workaround | Pas d'exception pour fichiers gouvernance |
| 3 | `yaml.safe_load` multi-doc | 1 | Moyen | ✅ Workaround | `design.yaml` = YAML frontmatter + Markdown body |
| 4 | Regex syntax error | 1 | Faible | ✅ Workaround | Character set `[` non échappé |
| 5 | Schema `depends_on` trop strict | 1 | Élevé | ❌ Bloquant | Pattern exclut `ATOM-<slug>` sans numéro |
| 6 | CLI `--schema` manquant | 1 | Faible | ✅ Workaround | Pas de défaut pour schema courant |
| 7 | `head` inexistant PowerShell | 3 | Faible | ✅ Workaround | Confusion Unix/Windows |
| 8 | Atoms orphelins catalogues | 2 | Élevé | ❌ Bloquant | Pas de sync automatique |

---

## Analyse causale TALEX

### Pattern 1 — L'indentation invisible

```
Cause : meta-design.yaml contient un mélange espaces/tabs non visible
Mécanisme : edit fait une recherche exacte, l'indentation copiée ne correspond pas
Effet : 3 tentatives d'edit échouées, perte de temps
```

**Correction structurelle** : Normaliser l'indentation de `meta-design.yaml` en espaces purs. Créer un hook pre-commit qui vérifie l'indentation cohérente.

### Pattern 2 — Le gardien aveugle

```
Cause : validate_yaml.py traite tous les .md comme du YAML pur
Mécanisme : Pas de distinction fichiers gouvernance vs Markdown pur
Effet : 4 atoms .md rejetés bien que valides pour le hook pre-commit
```

**Correction structurelle** : Ajouter un mode LENIENT dans `validate_yaml.py` pour les fichiers de gouvernance avec frontmatter optionnel.

### Pattern 3 — Le miroir brisé

```
Cause : design.yaml contient YAML frontmatter + Markdown body
Mécanisme : yaml.safe_load ne parse pas les fichiers multi-document
Effet : Script de validation personnalisé échoue
```

**Correction structurelle** : Créer un wrapper `safe_load_first_doc()` dans `tools/yaml_utils.py`.

### Pattern 4 — La regex maudite

```
Cause : Regex [^\s] dans un string Python avec guillemets simples
Mécanisme : Le [ est interprété comme character set incomplet
Effet : Script de vérification d'unicité intent_hash inutilisable
```

**Correction structurelle** : Créer un skill `regex-preflight-test` qui compile et teste la regex avant utilisation.

### Pattern 5 — Le schéma exclusif

```
Cause : design.schema.json exige ATOM-<number>-<slug>
Mécanisme : Pattern regex trop restrictif
Effet : Nouveaux atoms sans numéro invalides
```

**Correction structurelle** : ✅ Déjà corrigé : pattern étendu à `^ATOM(-[0-9]+)?-[a-zA-Z0-9-]+$`.

### Pattern 6 — Le CLI capricieux

```
Cause : validate_meta_design.py requiert --schema explicite
Mécanisme : Pas de défaut pour le schema courant
Effet : Validation du meta-design impossible sans lecture préalable
```

**Correction structurelle** : Ajouter un défaut `--schema schemas/meta-design.schema.json` au script.

### Pattern 7 — Le commandement fantôme

```
Cause : Utilisation de head (Unix) dans PowerShell (Windows)
Mécanisme : Confusion entre shells
Effet : 3 commandes bash échouent
```

**Correction structurelle** : Documenter dans `kilocode.md` que PowerShell n'a pas `head`. Remplacer par `Select-Object -First`.

### Pattern 8 — Les atomes orphelins

```
Cause : Nouveaux atoms/designs/primitives pas ajoutés aux catalogues
Mécanisme : Pas de mécanisme de sync automatique
Effet : Atoms existent mais ne sont pas découvrables
```

**Correction structurelle** : Créer `tools/sync_catalog.py` qui scanne les répertoires et met à jour les catalogues automatiquement.

---

## Évaluation d'utilité TALEX

| Aspect | Utilité | Justification |
|--------|---------|---------------|
| Mémoire collective | ⭐⭐⭐⭐⭐ | Conserve les leçons apprises de manière narrative |
| Onboarding nouveaux agents | ⭐⭐⭐⭐ | Histoire accessible, pas seulement des logs |
| Troubleshooting rapide | ⭐⭐ | Style épique, pas directement actionnable |
| Automatisation | ⭐ | Narratif, pas structurel |
| Méta-cohérence | ⭐⭐⭐⭐ | Fédère les frictions dans un récit unifié |

**Verdict** : Utile pour la mémoire collective et l'onboarding. Complémentaire aux rapports techniques. À conserver dans `reports/`.

---

## Corrections structurelles recommandées

| # | Correction | Friction cible | Effort | Impact |
|---|------------|----------------|--------|--------|
| 1 | Normaliser indentation `meta-design.yaml` | #1 | Minimal | Élimine 3 edit failures |
| 2 | Ajouter mode LENIENT `validate_yaml.py` | #2 | Minimal | Élimine 4 KO sur .md |
| 3 | Créer `safe_load_first_doc()` | #3 | Minimal | Élimine 1 KO YAML |
| 4 | Créer skill `regex-preflight-test` | #4 | Minimal | Élimine 1 KO regex |
| 5 | Étendre pattern `depends_on` | #5 | ✅ Fait | Élimine 1 KO schema |
| 6 | Ajouter défaut `--schema` | #6 | Minimal | Élimine 1 KO CLI |
| 7 | Documenter `head` interdit | #7 | Minimal | Élimine 3 KO bash |
| 8 | Créer `sync_catalog.py` | #8 | Moyen | Élimine 2 KO catalogues |

**Total effort** : ~30 min  
**Impact attendu** : Élimine 16 frictions sur 20 estimées dans la prochaine session similaire.

---

## Références

- `reports/talex-friction-session-20260921.md` — Récit narratif complet
- `PRD/PRD-MOC-ARTIFACT-EXTRACTION-20260920.md` — PRD du système
- `MOC/MOC-ARTIFACT-EXTRACTION-20260920.md` — MOC du système
- `ADR-2026-09-20-001-ARTIFACT-EXTRACTION-MDU.md` — ADR accepté

---

*Generated by TALEX Narrate + governance-doc-writer — Pattern C*
