# Primitive: transport-test-runner

## IntentHash
0xPRIMITIVE_TRANSPORT_TEST_RUNNER_20260930

## Contexte
ERR-TRANSPORT-001 : tests de transport répartis sur auto-dev et BOINC-LLM-P2P.
Nécessitent 2 runs pytest séparés. Pas de runner unifié pour agréger les résultats.

## Règle
Toute session de test transport DOIT utiliser un runner unifié qui exécute :
1. Tests auto-dev (tests/test_wazaa_transport.py, tests/test_boinc_transport.py, etc.)
2. Tests BOINC-LLM-P2P (tests/test_internal_endpoints.py)
3. Agrégation des résultats avec verdict PASS/FAIL global

## Check-list

### 1. Exécution auto-dev
```bash
pytest tests/test_wazaa_transport.py \
       tests/test_boinc_transport.py \
       tests/test_drift_alerter_wazaa.py \
       tests/test_wazaa_e2e.py \
       tests/test_boinc_e2e.py \
       tests/test_transport_fallback.py \
       -v --tb=short
```

### 2. Exécution BOINC-LLM-P2P
```bash
cd D:\DO\WEB\TOOLS\L1-INFRA\BOINC-LLM-P2P
pytest tests/test_internal_endpoints.py -v --tb=short
```

### 3. Agrégation
```python
# transport_test_runner.py :
# - Collecter les résultats des deux runs
# - Compter pass/fail par suite
# - Verdict : PASS si 100% pass, FAIL sinon
# - Sortie JSON : {auto_dev: {pass: N, fail: M}, boinc: {pass: K, fail: L}, verdict: "PASS|FAIL"}
```

### 4. Intégration CI
```yaml
# .gitlab-ci.yml ou équivalent :
# - stage: test
#   script:
#     - python tools/transport_test_runner.py
```

## Anti-patterns
- Exécuter les tests manuellement sans agrégation
- Ignorer les tests BOINC-LLM-P2P (uniquement auto-dev)
- Accepter un verdict FAIL pour continuer l'implémentation

## Sortie attendue
```
[TRANSPORT_TEST_RUNNER] auto_dev=PASS/FAIL boinc=PASS/FAIL verdict=PASS/FAIL
```
