---
type: ATOM
status: active
date: "2026-08-05"
intent_hash: 0xATOM_MATHEME_M3_TRANSFORMATION_20260805
strate: L0-CANON
author: gerivdb
source_repo: gerivdb/unified-design
source_path: atoms/mathemes/ATOM-M3-TRANSFORMATION.md
math: M3
inherits:
  - unified-design
---

# ATOM-M3-TRANSFORMATION - Logique, Langage, Code, Exécution

## Rôle

M3 est l'attracteur de **transformation** : logique, langage, code, exécution,
réversibilité. Il répond à la question : "Comment transformer ?"

## Représentants L0

| Persona | Spécialité |
|---------|------------|
| Brouwer | Constructivisme, logique |
| Turing | Calculabilité, machines |
| von Neumann | Architecture, jeux |
| Feynman | Intégrales de chemin, QED |
| Hoare | Contrats, vérification |
| Milner | Types, pi-calcul, CCS |
| Sifakis | Systèmes synchrones, SCADE |
| McCarthy | IA, LISP, situations |
| Musk | Performance, contraintes ENV2 |
| Bellard | Code minimal, compilation |
| Gardien | Déploiement, compile, rollback |

## Patterns associés

| Pattern | Action |
|---------|--------|
| @feynman+@dimension | Dimensions, QED |
| @hoare_contract | Contrats |
| @milner_types | Types |
| @sifakis_components | Composants |
| @mccarthy_metalang | Métalangage |
| @numa | Architecture |
| @turing | Calculabilité |
| @feynman | QED |
| @deploy+@compile | Déploiement |
| @perf | Performance |
| @sse4_only+@zig_0.14 | ISA, compilation |
| @korx_372b+@kbin_context | Cache, contexte |
| @boinc_p2p | P2P |
| @rlm_243 | Format ternaire |
| @db_schema_v1.0 | Schéma |
| @acid_tx_v1.0 | Transactions |

## Repos associés

| Repo | Rôle |
|------|------|
| TRIX | Runtime, isolation |
| ECOS-CLI | Exécution locale |
| CTULU | Orchestration |
| DevTools | Hooks, configs |
| PLIX | Codec ternaire |
| PIANO | Modulation |

## Validation

- [ ] Rollback F-1 o F = id
- [ ] Perte < 10%
- [ ] Terminaison (Kleene)
- [ ] Contraintes ENV2 respectées

## Références

- **ADR** : ADR-MATHEMES-PERSONAS-ORCHESTRATION-2026-08-05




