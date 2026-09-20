---
name: jevx-backend-selector
description: >
  Sélectionne le backend JEVX optimal selon les contraintes matérielles,
  la latence cible et le cas d'usage. S'appuie sur la matrice
  `designs/jevx-backend-matrix.yaml` et les profils hardware du MDU.
version: "1.0.0"
status: active
intent_hash: 0xSKILL_JEVX_BACKEND_SELECTOR_20260920
layer: L4
triggers:
  - "sélectionner backend JEVX"
  - "choisir backend jevx"
  - "backend selector JEVX"
  - "matrice backend jevx"
inputs:
  - type: use_case
    description: "Cas d'usage : minimal / standard / scorer-custom / api-compat"
  - type: constraints
    description: "Contraintes : ram_max_gb, cpu_req, wsl1_required, latency_target_ms"
  - type: hardware_profile
    description: "Profil matériel : cpu, gpu, ram_max_gb, execution_mode"
outputs:
  - type: backend_selection
    description: "Backend recommandé + justification + alternatives"
  - type: compatibility_report
    description: "Rapport de compatibilité WSL1/AVX1/RAM"
tools:
  - yaml_parser
  - designs/jevx-backend-matrix.yaml
  - meta-design.yaml
artifacts:
  - path: reports/jevx-backend-selection-*.json
    format: json
  - path: reports/jevx-backend-selection-*.md
    format: markdown
governance:
  adr: ADR-0111-JEVX-SOVEREIGN-OVERLAY
  design: jevx-backend-matrix
  atom: typed-decision-api
---

# Skill : JEVX Backend Selector

## Description

Sélectionne le backend JEVX optimal selon les contraintes matérielles,
la latence cible et le cas d'usage. S'appuie sur la matrice
`designs/jevx-backend-matrix.yaml` et les profils hardware du MDU.

## When to use

- Avant de déployer JEVX sur un nouvel environnement
- Lorsque les contraintes matérielles changent (RAM, CPU, WSL)
- Pour valider qu'un backend existant est toujours adapté
- Lors de l'audit d'un environnement ENV2/Z600

## Process

### ÉTAPE-1 — Collecter les contraintes

1. Lire `designs/jevx-backend-matrix.yaml` pour obtenir la liste des backends
2. Collecter les contraintes utilisateur :
   - `ram_max_gb` : RAM disponible en Go
   - `cpu_req` : AVX1, AVX2, scalaire
   - `wsl1_required` : true/false
   - `latency_target_ms` : cible de latence en ms
   - `use_case` : minimal / standard / scorer-custom / api-compat

### ÉTAPE-2 — Filtrer les backends compatibles

Pour chaque backend dans la matrice :
1. Vérifier `ram_gb <= ram_max_gb`
2. Vérifier `cpu_req` compatible avec le CPU cible
3. Vérifier `wsl1_compat` si `wsl1_required = true`
4. Vérifier `expected_latency_ms <= latency_target_ms` si spécifié

### ÉTAPE-3 — Classer par priorité

1. `LEGACY_FIT` > `LEGACY_PATCHABLE` > `LEGACY_INSPIRE`
2. `confidence` décroissant
3. `expected_latency_ms` croissant

### ÉTAPE-4 — Recommander

1. Retourner le backend le plus prioritaire compatible
2. Documenter les alternatives classées
3. Signalier les backends incompatibles avec raisons

## Backends connus

| Backend | Repo | Licence | Modèle | RAM | Latence | WSL1 | Confiance | Usage |
|---------|------|---------|--------|-----|---------|------|-----------|-------|
| minojev | zeredy879/minojev | MIT | 547k params scalaire | < 100 Mo | 13–23 ms | ✅ | 90% | Décision minimale |
| kev-0.5b | jaredpalmer/kev | Apache-2.0 | Qwen2.5-0.5B + LoRA | ~400 Mo | 50–150 ms | ✅ | 90% | API TypeSafe-compatible, fork direct |
| laya | NandhaKishorM/laya | Apache-2.0 | ModernBERT-large 421M + PPO | ~400 Mo Q4 | 50–200 ms | ✅ | 85% | ModernBERT + PPO, CPU-only |
| nanojev | TianyuCodings/NanoJev | MIT | Qwen3-0.6B + 3 têtes | ~1.2 Go | 50–200 ms | ✅ | 85% | Décision standard |
| jevlike | vinnylarouge/jevlike | MIT | Embedding 40 Ko from scratch | < 10 Mo | 1–10 ms | ✅ | 95% | Prototypage minimaliste |
| bespoke-nimble | bespokelabsai/nimble | Apache-2.0 | Qwen3.5-9B + LoRA | ~5 Go Q4 | 5–15 s | ⚠️ patch | 60% | Scorer high-quality, latence CPU élevée |
| semif | TheoLeeCJ/SemIf | MIT (présumé) | Qwen3.5-4B + NLI 3-classes | ~2.5 Go Q4 | 2–5 s | ⚠️ patch | 65% | NLI sur Qwen3.5 |
| jev_local | Argos1111/jev_local | MIT (présumé) | LFM2.5-1.2B Q8_0 | ~1.3 Go | 200–500 ms | ⚠️ patch | 70% | API LocalJev, bridge upstream |
| localjev | githubnext/localjev | MIT | DiffusionGemma-26B-A4B | > 16 Go | — | ❌ | 20% | INCOMPATIBLE Z600 — pattern uniquement |
| typesafe-jev | TypeSafe AI | Propriétaire | Jev officiel | cloud | cloud | ❌ | — | REJETÉ — dépendance cloud, clé obligatoire |

## Exemples

### Exemple 1 — Z600/ENV2, décision standard

```
Constraints:
  ram_max_gb: 24
  cpu_req: AVX1
  wsl1_required: true
  latency_target_ms: 200
  use_case: standard

Résultat:
  Recommandé: NanoJev (confidence 85%, RAM ~1.2 Go, WSL1 ✅)
  Alternatives: minojev (plus rapide, moins précis), jev_local (patch requis)
  Incompatibles: localjev (RAM > 16 Go)
```

### Exemple 2 — Décision minimale < 100ms

```
Constraints:
  ram_max_gb: 24
  cpu_req: scalaire
  wsl1_required: true
  latency_target_ms: 100
  use_case: minimal

Résultat:
  Recommandé: minojev (confidence 90%, RAM < 100 Mo, 13–23 ms)
  Alternatives: NanoJev (plus précis, plus lent)
```

## Governance

- **ADR** : ADR-0111-JEVX-SOVEREIGN-OVERLAY
- **Design** : jevx-backend-matrix
- **Atom** : typed-decision-api
