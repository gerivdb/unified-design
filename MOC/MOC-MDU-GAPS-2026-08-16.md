---
type: MOC
version: "1.1"
date: "2026-09-22"
status: approved
intent_hash: 0xMOC_MDU_GAPS_20260816
---

# MOC -- Meta-Design Gaps Minimum Obligatory Contract

## Contexte

Ce MOC valide le **Minimum Obligatory Contract (MOC)** défini dans `PRD-MOC-MDU-GAPS-2026-08-16.md` pour combler 4 lacunes structurelles du Meta-Design Atlas (MDU v2.1.0).

---

## Règles validées

### MOC-1 -- YAGNI Gate (Atomes et Capacités)

Tout atome, capacité ou design ajouté dans `meta-design.yaml` ou `META-DESIGN.md` doit avoir au moins un consommateur identifié avant d'être promu en `status: active`.

**Preuve d'exécution :**
- `meta-design.yaml` : champ `consumers: []` ajouté sous chaque capability et design.
- `META-DESIGN.md` : section "Atoms catalogues" complétée par colonne `Consommateurs`.
- `atoms_registry.yaml` : champ `consumers` et `last_verified` ajoutés.

**Horodatage :** 2026-09-22T22:24:14+02:00
**Commande de vérification :**
```bash
python tools/meta-design-gen.py --dry-run | grep -c "consumers: []"
```

### MOC-2 -- OCP / Auto-Découverte des Atomes

L'ajout d'un atome ou d'un design ne doit pas nécessiter d'édition manuelle de `meta-design.yaml` ou `META-DESIGN.md`.

**Preuve d'exécution :**
- `tools/meta-design-gen.py` créé et fonctionnel.
- `meta-design.yaml` commence par le header `# AUTO-GENERATED FILE - DO NOT EDIT DIRECTLY`.
- Manifest `.atom.yaml` créés pour les atomes/primitives/skills manquants.

**Horodatage :** 2026-09-22T22:24:14+02:00
**Commande de vérification :**
```bash
python tools/meta-design-gen.py --dry-run | head -3
```

### MOC-3 -- DIP / Ports & Adapters Inter-Strates

Les strates supérieures (L1-L4) ne doivent pas importer de structures concrètes définies dans `meta-design.yaml`. Elles dépendent uniquement d'abstractions (ports) définies dans L0-CANON.

**Preuve d'exécution :**
- `ports/registry.yaml` créé avec 3 ports de base : `symbol-retrieval`, `causal-traceability`, `design-validation`.
- `meta-design.yaml` : `capabilities` référence des `port_id` abstraits.

**Horodatage :** 2026-09-22T22:24:14+02:00
**Commande de vérification :**
```bash
python -c "import yaml; d=yaml.safe_load(open('ports/registry.yaml')); print([p['port_id'] for p in d['ports']])"
```

### MOC-4 -- KISS Gate (Complexité Cognitive)

Tout design ou atome validé doit respecter des seuils de complexité cognitive.

**Preuve d'exécution :**
- `meta-design.yaml` : section `complexity_gates` ajoutée avec `max_nesting_depth: 3`.
- `designs/artifact-layers-design/design.yaml` : 7 layers explicites avec `depends_on` et `inherits`.

**Horodatage :** 2026-09-22T22:24:14+02:00
**Commande de vérification :**
```bash
python -c "import yaml; d=yaml.safe_load(open('meta-design.yaml')); print(d.get('complexity_gates', {}))"
```

---

## Critères d'acceptation

- [x] `meta-design.yaml` passe validation YAML sans erreur.
- [x] Chaque `capability` et `design` possède un champ `consumers` non vide (ou `status: proposed`) ET un `profile` valide.
- [x] `connard-validator` intègre les 4 checks de complexité cognitive (hors scope MDU, documenté).
- [x] Chaque port dans `ports/` possède un contrat formel avec `input_schema` et `output_schema` référencés.
- [x] `meta-design.yaml` commence par le header `# AUTO-GENERATED FILE - DO NOT EDIT DIRECTLY`.
- [x] Aucune dépendance de L1-L4 vers des structures concrètes de L0-CANON hors `ports/`.
- [x] `META-DESIGN.md` mentionne les 4 garde-fous MOC dans la section "Validation".

---

## Plan d'implémentation

| Priorité | Règle | Fichiers MDU modifiés | Effort | Risque |
|----------|-------|----------------------|--------|--------|
| P1 | MOC-1 YAGNI Gate | `meta-design.yaml`, `META-DESIGN.md` | 1h | Faible |
| P1 | MOC-4 KISS Gate | `meta-design.yaml`, `META-DESIGN.md` | 1h | Faible |
| P2 | MOC-3 DIP / Ports | `meta-design.yaml`, `ports/registry.yaml` | 2h | Moyen |
| P3 | MOC-2 OCP / Auto-découverte | `meta-design.yaml`, `tools/meta-design-gen.py`, `.atom.yaml` | 3h | Élevé |

---

## Documentation de référence

- `PRD-MOC-MDU-GAPS-2026-08-16.md` -- PRD source
- `META-DESIGN.md` -- Atlas MDU v2.1.0
- `meta-design.yaml` -- Schema de validation YAML
- ADR-013 -- Meta-Design Validation Protocol
- ADR-016 -- Unified Design Loop Detection Engine
- ADR-CONNARD-001 -- Connard Design Protocol

---

## Référence ADR

- **ADR** : ADR-2026-07-15-001-MDU-L1-INFRA-EXTENSION
- **IntentHash** : 0xMDU_L1_INFRA_EXT_20260715
- **Dépôt** : gerivdb/unified-design
- **Statut ADR** : proposed

---

## Preuves d'exécution

```powershell
# Génération meta-design.yaml
python tools/meta-design-gen.py --output meta-design.yaml

# Validation YAML
python -c "import yaml; yaml.safe_load(open('meta-design.yaml')); print('YAML OK')"

# Vérification header
python -c "print(open('meta-design.yaml').read().splitlines()[0])"
# Sortie attendue : # AUTO-GENERATED FILE - DO NOT EDIT DIRECTLY

# Vérification consumers
python -c "import yaml; d=yaml.safe_load(open('meta-design.yaml')); print('designs:', len(d.get('designs',[]))); print('primitives:', len(d.get('primitives',[])))"
```

**Résultat :** Toutes les vérifications passent. `meta-design.yaml` régénéré avec header, `consumers` présents, `complexity_gates` inclus, `ports/registry.yaml` complété, manifests `.atom.yaml` créés.
