---
type: MOC
version: "1.0"
date: "2026-08-29"
status: active
intent_hash: 0xMOC_CAUSAL_RESOLUTION_METHODOLOGY_20260829
---

# MOC — Causal Resolution Methodology

> Carte de contenu pour la méthodologie Causal-First Dev issue de la résolution du "silent fail" LLUX 7B .q243.

## PRD

- `PRD/PRD-CAUSAL-RESOLUTION-METHODOLOGY-2026-08-29.md` — Méthodologie Causal-First Dev complète

## ADR

- `ADR/ADR-2026-08-29-001-CAUSAL-RESOLUTION-METHODOLOGY.md` — Méthodologie Causal-First Dev
- `ADR/ADR-2026-08-29-002-DOMAIN-FIRST-KERNEL-CONTRACTS.md` — Contrats domaine kernel/donnée
- `ADR/ADR-2026-08-29-003-UB-ELIMINATION-GUIDELINES.md` — Directives élimination UB
- `ADR/ADR-2026-08-29-004-CAUSAL-DEV-LOOP.md` — Boucle de dev causale
- `ADR/ADR-2026-08-29-005-KERNEL-VERSIONING-POLICY.md` — Politique versioning kernels

## Designs (L0-CANON/unified-design/designs/)

### LLUX (mis à jour v2.0.0)
- `llux/design.yaml` — Principes causal-first, registre kernels, fixtures, causal loop, 7 outils dérivés

### Outils dérivés (7 inédits)
- `kg-l-type-guard/design.yaml` — Garde-fou domaine kernel/donnée (pre-commit + zig_validator)
- `ctulu-zig-debug-adapter/design.yaml` — Adaptateur DAP Zig live Windows (DWARF/CodeView ↔ cdb.exe ↔ VS Code)
- `kg-l-kernel-versioner/design.yaml` — Versioning sémantique kernels + migration fixtures + cross-repo
- `ctulu-zig-fmt-auto/design.yaml` — Boucle auto-fix zig fmt intégrée au validateur
- `kg-l-fixture-registry/design.yaml` — Registre canonique fixtures cross-repo (fixtures.yaml + pre-push)
- `ctulu-auto-cleanup-hook/design.yaml` — Nettoyage zombies pré-build (hook zig_validator + build.zig)
- `kg-l-causal-diff/design.yaml` — Diff causal post-commit (git diff + domain_links + intent_hash → CAUSAL_DIFF.md)

## Registres & Fixtures (KG-L)
- `KG-L/kernels.yaml` — Registre versionné kernels (gemv_ternary v1.0.0 deprecated, gemv_f32 v2.0.0 active)
- `KG-L/fixtures.yaml` — Registre canonique fixtures cross-repo (q40_block, q243_runnable, etc.)
- `KG-L/exports/domain_links.json` — Export BOOT-5ter (source de vérité domaines, IntentHash: 0xINTENT_Q243_NATIVE_INFERENCE_20260825)

## Outils CTULU/KG-L (Nouveaux)
- `CTULU/tools/kg-l-type-guard` — Garde-fou domaine pre-commit + extension zig_validator
- `CTULU/tools/ctulu-zig-debug-adapter` — MVP: cdb.exe wrapper + VS Code DAP
- `CTULU/tools/kg-l-kernel-versioner` — CLI + kernels.yaml + migration fixtures
- `CTULU/scripts/commands/dev/zig_validator.py` — Extension `--auto-fix` (boucle auto-fix zig fmt)
- `KG-L/fixtures.yaml` + hook pre-push — Registre canonique fixtures + validation checksum
- `CTULU/scripts/ctulu-auto-cleanup-hook.py` — Nettoyage zombies pré-build
- `CTULU/tools/kg-l-causal-diff` — Post-commit hook + CLI (CAUSAL_DIFF.md + intent_hash)

## Frictions identifiées & Résolues

| # | Friction | Cause Racine | Résolution | Outil/Design |
|---|----------|--------------|------------|--------------|
| 1 | Silent hang LLUX | Domain mismatch: Q4_0 ⊄ ternary | Generalize kernel domain | gemv_f32 (general_f32) ✅ |
| 2 | UB silencieux (@Vector) | @Vector(4,f32) unaligned → silent hang | Eliminate @Vector, unroll×4 scalar | matvec_simd → scalar unroll×4 ✅ |
| 3 | Hang sans traces | Traces empêchent UB optimization | Trace as Mirror principle | Mandatory trace gates ✅ |
| 4 | AccessDenied rebuild | llux.exe zombie locks binary | Pre-build cleanup hook | ctulu-auto-cleanup-hook ✅ |
| 5 | Manual zig fmt loop | Format ❌ → manual fmt → revalidate | Auto-fix loop | ctulu-zig-fmt-auto ✅ |
| 6 | No live Zig debug | No DWARF/CodeView adapter Windows | DAP adapter | ctulu-zig-debug-adapter (MVP) ✅ |
| 7 | Ad-hoc kernel replacement | No versioning, no fixture migration | Kernel versioner + fixture registry | kg-l-kernel-versioner + fixture-registry ✅ |
| 8 | Lost causal lineage | git diff shows what, not why | Causal diff post-commit | kg-l-causal-diff ✅ |
| 9 | Domain mismatch at source | No kernel.domain ⊇ data.domain check | Type guard pre-commit | kg-l-type-guard ✅ |
| 10 | Fixtures scattered | No canonical registry | Canonical fixtures.yaml | kg-l-fixture-registry ✅ |
| 11 | Kernel performance | SSE4.2 scalar fallback too slow on E5620 | Optimize with _mm_loadu_ps + vectorized tail | gemv_f32 SSE4.2 (WIP) 🔄 |

## Principes Causal-First (Extraits LLUX design.yaml)

1. **Domain First** : Ontologie avant code. `domain_links.json` déclare contrats `kernel.domain ⊇ data.domain`.
2. **UB as First-Class Risk** : UB = risque #1. Outils : `kg-l-type-guard`, `ctulu-zig-debug-adapter`, `ctulu-zig-fmt-auto`.
3. **Trace as Mirror** : `std.debug.print` = miroir obligatoire. Sans traces, compilateur optimise UB en hang.
4. **Kernel Versioning** : Kernels = contrats de domaine versionnés. Remplacement = généralisation + migration fixtures + traçabilité.
5. **Format as Gate** : Format = porte. Boucle auto-fix obligatoire (`ctulu-zig-fmt-auto`).
6. **Zombie Prevention** : Processus zombies = risque correction build. Hook pré-build obligatoire.
7. **Causal Traceability** : Chaque commit porte lignée causale : `intent_hash` → `domain_links.json` → `CAUSAL_DIFF.md`.

## Boucle Causal Dev Loop (7 étapes)

1. **Intent → Domain Links** : `domain_links.json` (data.domain, kernel.domain, intent_hash)
2. **KG-L Type Guard** (pre-commit) : Vérifie `kernel.domain ⊇ data.domain`
3. **CTULU Zig Validator** (`--strict --auto-fix`) : Build + Warnings 0 + Format auto-fix
4. **CTULU Auto Cleanup** (pre-build) : Kill zombies, free locks
5. **Live Debug** : `ctulu-zig-debug-adapter` (DWARF/CodeView live, breakpoints, watch @Vector)
6. **Causal Diff** (post-commit) : Génère `CAUSAL_DIFF.md` + `intent_hash`
7. **Kernel Versioner + Fixture Registry** : Bump version, update fixtures.yaml, link cross-repo

## Vérification Méta-Cohérence KG-L (Continue)

- [ ] `domain_links.json` freshness < 30 jours
- [ ] `fixtures.yaml` checksums match disk
- [ ] `kernels.yaml` domain subsumption valid
- [ ] `fixtures.yaml` generator exists + consumers listed
- [ ] Every commit on main has `CAUSAL_DIFF.md` with `intent_hash`

## IntentHashs de référence

| Artefact | IntentHash |
|----------|------------|
| PRD Methodology | 0xPRD_CAUSAL_RESOLUTION_METHODOLOGY_20260829 |
| MOC | 0xMOC_CAUSAL_RESOLUTION_METHODOLOGY_20260829 |
| LLUX Design v2.0.0 | 0xLLUX_CAUSAL_RESOLUTION_DESIGN_20260829 |
| kg-l-type-guard | 0xKG_L_TYPE_GUARD_20260829 |
| ctulu-zig-debug-adapter | 0xCTULU_ZIG_DEBUG_ADAPTER_20260829 |
| kg-l-kernel-versioner | 0xKG_L_KERNEL_VERSIONER_20260829 |
| ctulu-zig-fmt-auto | 0xCTULU_ZIG_FMT_AUTO_20260829 |
| kg-l-fixture-registry | 0xKG_L_FIXTURE_REGISTRY_20260829 |
| ctulu-auto-cleanup-hook | 0xCTULU_AUTO_CLEANUP_HOOK_20260829 |
| kg-l-causal-diff | 0xKG_L_CAUSAL_DIFF_20260829 |
| Resolution Commit | 0xCAUSAL_RESOLUTION_LLUX_Q40_GEMV_20260829 |
| Domain Links Export | 0xINTENT_Q243_NATIVE_INFERENCE_20260825 |

## Navigation

- **PRD Principal** : `PRD/PRD-CAUSAL-RESOLUTION-METHODOLOGY-2026-08-29.md`
- **Designs** : `designs/<tool>/design.yaml`
- **Registres** : `KG-L/kernels.yaml`, `KG-L/fixtures.yaml`, `KG-L/exports/domain_links.json`
- **Outils** : `CTULU/tools/<tool>/`, `CTULU/scripts/`
- **LLUX Implémentation** : `D:\DO\WEB\TOOLS\L3-CITIZENS\LLUX\` (commit 6cc7ebd)