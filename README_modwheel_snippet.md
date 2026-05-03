# Wheel Pre-Oracle Filter Additions

These files add an optional classical pre-oracle filtering layer before Quantum Oracle Sketching (QOS).

## Pipeline

```text
raw classical candidates
    -> modwheel.py / pre_oracle_filter.py
    -> filtered candidates
    -> qos.py or qos_sampling.py
    -> qsvt.py / downstream task
```

This layer is:
- optional
- non-invasive (does not modify core QOS files)
- designed to reduce the candidate stream before oracle construction

---

## Added Files

- `modwheel.py` — wheel modulus, admissible residues, density, reduction
- `pre_oracle_filter.py` — applies wheel filters before oracle construction
- `compare_wheels.py` — compares mod30, mod210, mod2310
- `benchmark_modwheel.py` — simple oracle-call proxy benchmark
- `test_modwheel.py` — pytest checks for residue counts and filtering behavior

---

## Run

```bash
python compare_wheels.py
python benchmark_modwheel.py --n 100000
pytest test_modwheel.py
```

---

## Core Comparison

| Wheel | Primes | Residues | Density |
|------|--------|----------|---------|
| mod30 | 2·3·5 | 8/30 | 0.2667 |
| mod210 | 2·3·5·7 | 48/210 | 0.2286 |
| mod2310 | 2·3·5·7·11 | 480/2310 | 0.2078 |

Key observation:
- most reduction occurs at mod30
- deeper wheels provide diminishing returns

---

## Notebooks

For full experiments, figures, and paper-ready results:

```text
notebooks/README.md
```

Notebook sequence:

- Notebook 01 — wheel density and tradeoff  
- Notebook 02 — synthetic row-ID adapter  
- Notebook 03 — 20news real dataset adapter  
- Notebook 04 — consolidated paper figure pack  

---

## Summary

Across mod30, mod210, and mod2310:

- candidate streams reduce by ~73–79%
- filtering can be applied safely at the row-ID level
- real-dataset behavior (20news) remains stable
- fit-time proxy decreases with reduced sample count

This supports:

```text
classical pre-oracle filtering -> smaller candidate stream -> downstream QOS / ML workflow
```

---

## Guardrail

This layer:
- measures filtering behavior and workload proxies
- demonstrates adapter-level integration

It does **not** claim:
- quantum advantage
- accuracy improvement
