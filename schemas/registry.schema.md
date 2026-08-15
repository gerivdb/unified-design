---
name: registry-schema
description: "Schéma de validation pour registry.yaml. Définit les champs obligatoires et optionnels pour skills, workflows et citizens."
version: "1.0.0"
status: active
owner: gerivdb
parameters:
  registry_files:
    - "packages/kilocode-ecos-integration/src/skills/registry.yaml"
    - ".kilo/workflows/README.md"
    - "act-protocol/citizens.yaml"
intent_hash: 0xREGISTRY_SCHEMA_20260807
---

# Design — Registry Schema

> **Verdict** : **SCHÉMA DE VALIDATION** — Définit la structure obligatoire des registres skills/workflows/citizens.

---

## Objectif

Garantir que tous les registres de l'écosystème sont valides et conformes :
1. Schéma de validation pour `registry.yaml`
2. Champs obligatoires et optionnels
3. Règles de unicité (`intent_hash`, `name`, `path`)

---

## Principes

| Principe | Règle d'application |
|----------|---------------------|
| **Unicité** | `intent_hash` unique par élément |
| **Traçabilité** | `source_path` obligatoire pour chaque entrée |
| **Dépendances explicites** | `dependencies` liste les skills/workflows requis |
| **Status** | `active`, `draft`, `deprecated`, `archived` |

---

## Schéma skills

```yaml
skills:
  - name: string                    # Obligatoire, unique
    intent_hash: string              # Obligatoire, unique
    description: string              # Obligatoire
    version: string                  # Obligatoire
    status: active|draft|deprecated  # Obligatoire
    source_path: string              # Obligatoire
    entrypoint: string               # Optionnel
    dependencies: []                 # Optionnel
    stratum: L0|L1|L2|L3|L4|L5      # Obligatoire
    citizen: string                  # Optionnel
    layer: string                    # Optionnel
    capabilities: []                 # Optionnel
```

---

## Schéma workflows

```yaml
workflows:
  - name: string                    # Obligatoire, unique
    intent_hash: string              # Obligatoire, unique
    description: string              # Obligatoire
    file: string                     # Obligatoire
    triggers: []                     # Optionnel
    status: active|draft|deprecated  # Obligatoire
    source_path: string              # Obligatoire
```

---

## Schéma citizens

```yaml
citizens:
  - id: string                       # Obligatoire, unique
    intent_hash: string              # Obligatoire, unique
    role: string                     # Obligatoire
    responsibilities: []             # Obligatoire
    goals: []                        # Optionnel
    stratum: L0|L1|L2|L3|L4|L5      # Obligatoire
    status: active|draft|deprecated  # Obligatoire
    skills: []                       # Optionnel
    context_files: []                # Optionnel
```

---

## Règles de validation

| Règle | Description |
|-------|-------------|
| Unicité intent_hash | Pas de doublon dans tout le registre |
| Unicité name | Pas de doublon de nom dans skills/workflows |
| Unicité id | Pas de doublon d'id dans citizens |
| Source_path obligatoire | Chaque entrée doit avoir un `source_path` |
| Dependencies valides | Les dépendances doivent exister dans le registre |
| Status valide | `active`, `draft`, `deprecated`, `archived` uniquement |

---

## Rôles

| Rôle | Responsabilité |
|------|----------------|
| `NEXUS` | Maintenir les registres |
| `MOX` | Valider la conformité des registres |
| `ARGUS` | Détecter les incohérences |

---

## Probes

```ascii
+-----------------------------------------------------------------------------+
| PROBE    CONDITION → COMPORTEMENT ATTENDU                                   |
+-----------------------------------------------------------------------------+
| P-1101   Tous les intent_hash sont uniques                                  |
| P-1102   Tous les names sont uniques                                        |
| P-1103   Tous les source_path existent                                      |
| P-1104   Toutes les dependencies sont valides                               |
| P-1105   Tous les status sont valides                                       |
+-----------------------------------------------------------------------------+
```

---

## Critères

```ascii
+-----------------------------------------------------------------------------+
| CRITÈRE    DESCRIPTION                                                      |
+-----------------------------------------------------------------------------+
| ✓          intent_hash uniques                                              |
| ✓          names uniques                                                    |
| ✓          source_path existants                                            |
| ✓          dependencies valides                                             |
| ✓          status valides                                                   |
+-----------------------------------------------------------------------------+
```

---

## Rollback

1. Revenir au registre précédent.
2. Logger dans WAL.
3. Corriger via PR review MOX.

---

## Références

- `packages/kilocode-ecos-integration/src/skills/registry.yaml`
- `act-protocol/citizens.yaml`
- `PRD-MOC-N243-DEVELOPER-EXPERIENCE-CONVENTIONS-2026-08-07.md`
