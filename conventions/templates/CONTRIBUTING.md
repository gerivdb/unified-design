---
type: GUI
version: 1.0.0
status: active
intent_hash: 0xATOM_024_TEMPLATES
---

# ATOM-024 : Templates de contribution

## Fichiers obligatoires

| Fichier | Description | Où le placer |
|---------|-------------|--------------|
| `CONTRIBUTING.md` | Guide de contribution | Racine du repo |
| `PULL_REQUEST_TEMPLATE.md` | Template PR | `.github/` |
| `ISSUE_TEMPLATE.md` | Template issue | `.github/` |

## CONTRIBUTING.md

```markdown
# Contribuer

Merci de contribuer ! Ce projet suit les conventions MDU (ATOM).

## Workflow standard

1. **Lire l'issue** ou créer une nouvelle issue pour discuter
2. **Brancher** depuis `main` avec le bon préfixe :
   - `feat/` pour une nouvelle fonctionnalité
   - `fix/` pour une correction de bug
   - `docs/` pour de la documentation
   - `chore/` pour du ménage/CI
3. **Travailler localement** :
   - Faire les tests passer
   - Formater le code (`ruff format .` ou `zig fmt .`)
   - Vérifier le lint (`ruff check .` ou `zig fmt --check .`)
4. **Committer** avec un message conventionnel :
   ```
   feat(scope): description concise
   
   Corps du message optionnel...
   ```
5. **Pousser** la branche
6. **Créer une PR** en suivant le template
7. **Attendre les checks CI** et les reviews

## Conventions

- **Conventional Commits** : https://www.conventionalcommits.org/
- **SemVer** : https://semver.org/
- **Lint/Format** : Voir `conventions/lint/CODE_QUALITY.md`
- **CI** : Voir `conventions/ci/MINIMAL_CI.md`

## Questions fréquentes

**Q : Comment tester localement ?**
R : `pytest` pour Python, `zig test` pour Zig, `cargo test` pour Rust.

**Q : Comment formater le code ?**
R : `ruff format .` ou `zig fmt .`

**Q : Combien de temps avant de créer une PR ?**
R : Pas de délai, mais préférez des commits petits et atomiques.
```

## PULL_REQUEST_TEMPLATE.md

```markdown
## 📋 Description

<!-- Décrivez les changements apportés -->

## 🎯 Type de changement

- [ ] Nouvelle fonctionnalité (`feat`)
- [ ] Correction de bug (`fix`)
- [ ] Amélioration de performance (`perf`)
- [ ] Refactoring (`refactor`)
- [ ] Mise à jour de documentation (`docs`)
- [ ] Ajout de tests (`test`)
- [ ] Changement de CI/Infrastructure (`chore`)

## ✅ Checklist

- [ ] Le code compile/constructe
- [ ] Les tests passent localement
- [ ] Le formatage est appliqué
- [ ] Le lint est propre
- [ ] Les commits suivent Conventional Commits
- [ ] La documentation est mise à jour (si nécessaire)
- [ ] Le changelog sera mis à jour (si nécessaire)

## 📊 Tests

<!-- Décrivez les tests ajoutés/modifiés -->

## 📦 Impact

<!-- Indiquez les impacts (breaking change, dépendances, etc.) -->

## 🔗 Liens

- Issue: #
- ADR: (si applicable)