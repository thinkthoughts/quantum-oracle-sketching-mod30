# Wheel Pre-Oracle Filter Additions

These files add an optional deterministic pre-oracle filtering layer before Quantum Oracle Sketching (QOS).

---

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
- deterministic (no sampling variance)  
- non-invasive (does not modify core QOS files)  
- designed to reduce the candidate stream before oracle construction  

---

## Added Files

- `modwheel.py` — wheel modulus, admissible residues, density, reduction  
- `pre_oracle_filter.py` — applies wheel filters before oracle construction  
- `compare_wheels.py` — compares mod30, mod210, mod2310  
- `benchmark_modwheel.py` — oracle-call proxy benchmark (input reduction)  
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

| Wheel   | Primes         | Residues | Density |
|--------|----------------|----------|---------|
| mod30   | 2·3·5          | 8/30     | 0.2667  |
| mod210  | 2·3·5·7        | 48/210   | 0.2286  |
| mod2310 | 2·3·5·7·11     | 480/2310 | 0.2078  |

**Key observations:**

- ~73–79% candidate reduction across wheels  
- most reduction occurs at mod30  
- deeper wheels provide diminishing returns  

---

## Notebooks

For full experiments, figures, and paper-ready results, see:

👉 [notebooks/README.md](notebooks/modwheel_notebooks_overview.md)

Includes:

- Notebook 01 — wheel density and tradeoff  
- Notebook 02 — synthetic row-ID adapter  
- Notebook 03 — 20news real dataset adapter  
- Notebook 04 — consolidated paper figure pack  
- Notebook 05 — comparison with random subsampling  
- Notebook 06 — QOS-style wrapper (pre-feature filtering)  
- Notebook 07 — row-order robustness  

Together these establish:

- deterministic reduction ≈ random subsampling behavior  
- reduced preprocessing cost (Notebook 06)  
- stability under dataset reordering (Notebook 07)  

---

## Paper

Full write-up of the modwheel pre-oracle filtering layer:

👉 [paper/paper.pdf](paper/paper.pdf)

Highlights:

- ~73–79% candidate reduction before oracle construction  
- deterministic alternative to random subsampling  
- reduced preprocessing cost in QOS-style wrapper experiments  
- robustness to dataset ordering  
- non-invasive integration (no QOS modifications)  

This work positions modwheel filtering as a:

> deterministic front-end layer for reducing classical input in QOS-style pipelines

---

## Summary

Across mod30, mod210, and mod2310:

- candidate streams reduce by ~73–79%  
- behavior matches random subsampling at equal size  
- preprocessing cost decreases when filtering is applied before feature construction  
- results remain stable under dataset reordering  

This supports:

```text
deterministic pre-oracle filtering
    -> reduced input stream
    -> lower preprocessing cost
    -> stable downstream QOS / ML workflow
```

---

## Guardrail

This layer:

- evaluates classical preprocessing behavior  
- demonstrates QOS-compatible adapter integration  

It does **not** claim:

- quantum advantage  
- improvements to QOS algorithms  
- accuracy gains  
