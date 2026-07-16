---
type: ATOM
id: ATOM-005-interface-contract
version: 1.0.0
date: 2026-07-16
title: "Interface Contract — Formalisation explicite des exports C pour FFI"
intent_hash: 0xATOM_INTERFACE_CONTRACT_20260716
status: approved
strate: L1b
---

# ATOM-005 — Interface Contract

## Contexte

Les interfaces entre langages (FFI) sont souvent sous-spécifiées, entraînant des bugs difficiles à diagnostiquer. Un contrat formel des exports C permet de valider l'interface avant compilation.

## Loi fondamentale

**Chaque module FFI doit avoir un fichier de contrat (YAML ou JSON) décrivant explicitement chaque export C avec ses paramètres, types de retour, et contraintes ABI.**

### Format de contrat (exemple YAML)

```yaml
module: trix_runtime
exports:
  - name: handle_kiva_run
    signature: "fn(*const u8, usize) -> i32"
    abi_constraint: "scalars_first"
    description: "Handle KIVA container run request"
  
  - name: handle_stop_container
    signature: "fn(*const u8, u32) -> void"
    abi_constraint: "u32_for_size"
    description: "Stop a running container"
```

## Conséquences

- **Bugs d'ABI silencieux** : Le code compile mais plante à l'exécution
- **Documentation insuffisante** : Impossible de connaître l'interface sans lire le code source
- **Maintenance coûteuse** : Chaque modification d'interface est une source de bugs

## Recommandations

1. Créer un fichier `interface_contract.yaml` pour chaque module FFI
2. Valider le contrat avec un outil avant compilation
3. Générer automatiquement les wrappers à partir du contrat (EPIC-312)
4. Maintenir le contrat en parallèle du code source

## Références

- ADR-20260621-001-zig-015-api-compatibility
- EPIC-312: Générateur automatique de wrappers FFI

## Référence ADR
- **ADR** : ADR-2026-07-16-005-ATOM-INTERFACE-CONTRACT
- **IntentHash** : 0xADR_INTERFACE_CONTRACT_20260716
- **Dépôt** : gerivdb/LLM-REPO
- **Statut ADR** : proposed
- **Màj requise si** : statut ADR → deprecated ou superseded