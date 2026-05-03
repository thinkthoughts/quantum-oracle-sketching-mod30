# Wheel Pre-Oracle Filter Additions

These files add an optional classical pre-oracle filtering layer:

```text
raw classical candidates
    -> modwheel.py / pre_oracle_filter.py
    -> filtered candidates
    -> qos.py or qos_sampling.py
    -> qsvt.py / downstream task
```

## Added files

- `modwheel.py` — wheel modulus, admissible residues, density, reduction
- `pre_oracle_filter.py` — applies wheel filters before oracle construction
- `compare_wheels.py` — compares mod30, mod210, mod2310
- `benchmark_modwheel.py` — simple oracle-call proxy benchmark
- `test_modwheel.py` — pytest checks for residue counts and filtering behavior

## Run

```bash
python compare_wheels.py
python benchmark_modwheel.py --n 100000
pytest test_modwheel.py
```

## Core comparison

| Wheel | Primes | Residues | Density |
|---|---:|---:|---:|
| mod30 | 2·3·5 | 8/30 | 0.2667 |
| mod210 | 2·3·5·7 | 48/210 | 0.2286 |
| mod2310 | 2·3·5·7·11 | 480/2310 | 0.2078 |

---

## Notebooks

For full experiments, figures, and paper-ready results, see:

```text
notebooks/modwheel_notebooks_overview.md
```
This includes:

Notebook 01 — wheel density and tradeoff
Notebook 02 — synthetic row-ID adapter
Notebook 03 — 20news real dataset adapter
Notebook 04 — consolidated paper figure pack
