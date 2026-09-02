---
type: PRD
version: "1.0"
date: "2026-08-29"
status: approved
intent_hash: 0xPRD_CAUSAL_RESOLUTION_METHODOLOGY_20260829
---

# PRD-MOC — Causal Resolution Methodology for LLUX & Ecosystem

## Contexte

Le "silent fail" LLUX 7B .q243 (hang sans logs, tokens=0, timeout 900s) a révélé une **incohérence ontologique systémique** : les kernels invoqués ne correspondaient pas au domaine des données qu'ils traitaient.

**Cause racine identifiée** : `data.domain = Q4_0` (continues, `scale × nibble`) ⊄ `kernel.domain = ternary` (attend {-1,0,1}). Le fallback `matvec_simd` utilisait `@Vector(4,f32)` sur données potentiellement mal alignées → **Undefined Behavior silencieux** (hang sans traces, complet avec traces).

**Résolution causale** : Généralisation du kernel (`ternary → general_f32`), élimination de l'UB (`@Vector` → unroll×4 scalaire), outillage de la causalité (7 outils inédits).

## Objectif

Formaliser la **méthodologie Causal-First Dev** comme nouvelle norme de développement pour l'écosystème (LLUX, CTULU, KG-L, PIANO, PLIX, N243, etc.) :

1. **Domain First** : L'ontologie précède le code. `domain_links.json` déclare les contrats `kernel.domain ⊇ data.domain` avant toute ligne de code.
2. **UB as First-Class Risk** : L'Undefined Behavior n'est pas un bug rare — c'est le risque #1. Outillage : `kg-l-type-guard`, `ctulu-zig-debug-adapter`, `ctulu-zig-fmt-auto`.
3. **Trace as Mirror** : `std.debug.print` n'est pas du debug optionnel — c'est un miroir obligatoire. Sans traces, le compilateur optimise l'UB en hang silencieux.
4. **Kernel Versioning** : Les kernels sont des contrats de domaine versionnés. Remplacement = généralisation de domaine + migration fixtures + traçabilité cross-repo.
5. **Format as Gate** : Le format n'est pas du style — c'est une porte. Boucle auto-fix obligatoire (`ctulu-zig-fmt-auto`).
6. **Zombie Prevention** : Les processus zombies ne sont pas des soucis d'ops — ce sont des risques de correction de build. Hook pré-build obligatoire.
7. **Causal Traceability** : Chaque commit porte sa lignée causale : `intent_hash` → `domain_links.json` → `CAUSAL_DIFF.md`.

## Périmètre

### 1. Designs de référence (L0-CANON/unified-design/designs/)
- `llux/` — Design LLUX avec principes causal-first (mis à jour v2.0.0)
- `kg-l-type-guard/` — Garde-fou domaine kernel/donnée
- `ctulu-zig-debug-adapter/` — Adaptateur DAP Zig live Windows
- `kg-l-kernel-versioner` — Versioning sémantique kernels + migration fixtures
- `ctulu-zig-fmt-auto` — Boucle auto-fix zig fmt intégrée au validateur
- `kg-l-fixture-registry` — Registre canonique fixtures cross-repo
- `ctulu-auto-cleanup-hook` — Nettoyage zombies pré-build
- `kg-l-causal-diff` — Diff causal post-commit

### 2. PRD/MOC de gouvernance
- `PRD/PRD-CAUSAL-RESOLUTION-METHODOLOGY-2026-08-29.md` (ce document)
- `MOC/MOC-CAUSAL-RESOLUTION-METHODOLOGY-2026-08-29.md`

### 3. ADR de support
- `ADR/ADR-2026-08-29-001-CAUSAL-RESOLUTION-METHODOLOGY.md` — Méthodologie Causal-First Dev
- `ADR/ADR-2026-08-29-002-DOMAIN-FIRST-KERNEL-CONTRACTS.md` — Contrats domaine kernel/donnée
- `ADR/ADR-2026-08-29-003-UB-ELIMINATION-GUIDELINES.md` — Directives élimination UB
- `ADR/ADR-2026-08-29-004-CAUSAL-DEV-LOOP.md` — Boucle de dev causale
- `ADR/ADR-2026-08-29-005-KERNEL-VERSIONING-POLICY.md` — Politique versioning kernels

### 4. Outils CTULU/KG-L (nouveaux)
- `CTULU/tools/kg-l-type-guard` — Garde-fou domaine pre-commit
- `CTULU/tools/ctulu-zig-debug-adapter` — Adaptateur DAP Zig live Windows
- `CTULU/tools/kg-l-kernel-versioner` — Versioning kernels + migration fixtures
- `CTULU/scripts/commands/dev/zig_validator.py` (extension `--auto-fix`)
- `KG-L/fixtures.yaml` + hook pre-push
- `CTULU/scripts/ctulu-auto-cleanup-hook.py`
- `CTULU/tools/kg-l-causal-diff`

### 5. Registres & Fixtures
- `KG-L/kernels.yaml` — Registre versionné kernels
- `KG-L/fixtures.yaml` — Registre canonique fixtures cross-repo
- `KG-L/exports/domain_links.json` — Export BOOT-5ter (source de vérité domaines)

## Critères d'acceptation

## Critères d'acceptation

### Niveau 1 — Résolution LLUX (validé)
- [x] Build Zig 0.15 westmere sans warning
- [x] CTULU `zig_validator --strict` : Build ✅, Warnings 0, Format ✅
- [x] Tests Zig passent
- [x] Inférence 7B .q243 fonctionnelle (4 tokens, < 900s)
- [x] **Déterminisme confirmé** : 2 runs → tokens identiques `14135 28957 9992 11287`
- [x] Push `gerivdb/LLUX:main` (commit 6cc7ebd)

### Niveau 1bis — Performance Kernel (implémenté, limité par hardware)
- [x] Kernel `gemv_f32` SSE4.2 avec `_mm_loadu_ps` (charges non-alignées) — implémenté
- [x] Suppression fallback scalaire `matvec_simd` → kernel C unique
- [x] Build Zig 0.15 westmere sans warning
- [x] CTULU `zig_validator --strict` : Build ✅, Warnings 0, Format ✅
- [x] **Déterminisme confirmé** : 2 runs → tokens identiques `14135`
- [ ] Inférence 1 token < 5s (limité par hardware E5620 — ~300s)
- [ ] Inférence 4 tokens < 20s
- [x] Tests de régression : déterminisme + build ✅

### Niveau 2 — Designs créés (L0-CANON/unified-design/designs/)
- [x] `llux/design.yaml` v2.0.0 — Principes causal-first + registre kernels + fixtures + causal loop
- [x] `kg-l-type-guard/design.yaml` — Garde-fou domaine kernel/donnée
- [x] `ctulu-zig-debug-adapter/design.yaml` — Adaptateur DAP Zig live Windows
- [x] `kg-l-kernel-versioner/design.yaml` — Versioning kernels + migration fixtures
- [x] `ctulu-zig-fmt-auto/design.yaml` — Boucle auto-fix zig fmt
- [x] `kg-l-fixture-registry/design.yaml` — Registre canonique fixtures cross-repo
- [x] `ctulu-auto-cleanup-hook/design.yaml` — Nettoyage zombies pré-build
- [x] `kg-l-causal-diff/design.yaml` — Diff causal post-commit

### Niveau 3 — PRD/MOC/ADR
- [ ] `PRD/PRD-CAUSAL-RESOLUTION-METHODOLOGY-2026-08-29.md` (ce doc → PRD)
- [ ] `MOC/MOC-CAUSAL-RESOLUTION-METHODOLOGY-2026-08-29.md` — Carte de contenu
- [ ] 5 ADR de support créés dans `ADR/`

### Niveau 4 — Outils CTULU/KG-L implémentés
- [ ] `CTULU/tools/kg-l-type-guard` — Hook pre-commit + extension zig_validator
- [ ] `CTULU/tools/ctulu-zig-debug-adapter` — MVP: cdb.exe wrapper + VS Code DAP
- [ ] `CTULU/tools/kg-l-kernel-versioner` — CLI + kernels.yaml + migration fixtures
- [ ] `CTULU/scripts/commands/dev/zig_validator.py` — Extension `--auto-fix`
- [ ] `KG-L/fixtures.yaml` + hook pre-push
- [ ] `CTULU/scripts/ctulu-auto-cleanup-hook.py`
- [ ] `CTULU/tools/kg-l-causal-diff` — Post-commit hook + CLI

### Niveau 5 — Registres & Fixtures
- [ ] `KG-L/kernels.yaml` — Registre versionné kernels (gemv_ternary v1.0.0 deprecated, gemv_f32 v2.0.0 active)
- [ ] `KG-L/fixtures.yaml` — Registre canonique (q40_block, q243_runnable, etc.)
- [ ] `KG-L/exports/domain_links.json` — Refresh BOOT-5ter avec nouveaux termes

### Niveau 6 — Vérification méta-cohérence KG-L (continue)
- [ ] `domain_links.json` freshness < 30 jours
- [ ] `fixtures.yaml` checksums match disk
- [ ] `kernels.yaml` domain subsumption valid
- [ ] `fixtures.yaml` generator exists + consumers listed
- [ ] Every commit on main has `CAUSAL_DIFF.md` with `intent_hash`

## Livrables

| Artefact | Chemin | Statut |
|----------|--------|--------|
| PRD | `L0-CANON/unified-design/PRD/PRD-CAUSAL-RESOLUTION-METHODOLOGY-2026-08-29.md` | ✅ (ce doc) |
| MOC | `L0-CANON/unified-design/MOC/MOC-CAUSAL-RESOLUTION-METHODOLOGY-2026-08-29.md` | 🔄 |
| LLUX Design | `designs/llux/design.yaml` | ✅ v2.0.0 |
| 7 Tool Designs | `designs/<tool>/design.yaml` | ✅ 7/7 |
| ADR Methodology | `ADR/ADR-2026-08-29-001-*.md` | 🔄 |
| ADR Domain Contracts | `ADR/ADR-2026-08-29-002-*.md` | 🔄 |
| ADR UB Guidelines | `ADR/ADR-2026-08-29-003-*.md` | 🔄 |
| ADR Causal Dev Loop | `ADR/ADR-2026-08-29-004-*.md` | 🔄 |
| ADR Kernel Versioning | `ADR/ADR-2026-08-29-005-*.md` | 🔄 |
| kg-l-type-guard | `CTULU/tools/kg-l-type-guard/` | 🔄 |
| ctulu-zig-debug-adapter | `CTULU/tools/ctulu-zig-debug-adapter/` | 🔄 |
| kg-l-kernel-versioner | `CTULU/tools/kg-l-kernel-versioner/` | 🔄 |
| ctulu-zig-fmt-auto | `CTULU/scripts/commands/dev/zig_validator.py` | 🔄 |
| kg-l-fixture-registry | `KG-L/fixtures.yaml` + hook | 🔄 |
| ctulu-auto-cleanup-hook | `CTULU/scripts/ctulu-auto-cleanup-hook.py` | 🔄 |
| kg-l-causal-diff | `CTULU/tools/kg-l-causal-diff/` | 🔄 |
| kernels.yaml | `KG-L/kernels.yaml` | 🔄 |
| fixtures.yaml | `KG-L/fixtures.yaml` | 🔄 |

## Définition de "Fait" (Definition of Done)

Un artefact est **Done** quand :
1. Design.yaml existe dans `L0-CANON/unified-design/designs/<tool>/`
2. Design passe validation méta-cohérence KG-L (domain_links + ontology)
3. Code implémenté dans repo cible (CTULU/KG-L/LLUX)
4. Tests passent (unit + integration)
4. `zig_validator --strict` passe (Build ✅, Warnings 0, Format ✅)
5. `kg-l-type-guard` passe (kernel.domain ⊇ data.domain)
6. `kg-l-causal-diff` génère `CAUSAL_DIFF.md` avec `intent_hash`
7. Commit message inclut `intent_hash`
8. Push sur `main` avec CI verte

## Références

- **Rapport d'analyse causale** : `0xCAUSAL_RESOLUTION_LLUX_Q40_GEMV_20260829` (rapport TALEX/KG-L/CTULU synthèse)
- **Commit de résolution** : `6cc7ebd` (feat(LLUX): 7B .q243 operational + Zig 0.15 compat + I2_S kernel + scalar matvec)
- **Domain Links Export** : `KG-L/exports/domain_links.json` (IntentHash: `0xINTENT_Q243_NATIVE_INFERENCE_20260825`)
- **LLUX Design** : `L0-CANON/unified-design/designs/llux/design.yaml` (v2.0.0)
- **CTULU Validator** : `CTULU/scripts/commands/dev/zig_validator.py`

## IntentHash
**0xPRD_CAUSAL_RESOLUTION_METHODOLOGY_20260829**