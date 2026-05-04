# Wheel Pre-Oracle Filter Additions

These files add an optional deterministic pre-oracle filtering layer before Quantum Oracle Sketching (QOS), along with a complementary readout-side evaluation framework.

---

## Pipeline

```text
raw classical candidates
    -> modwheel.py / pre_oracle_filter.py
    -> filtered candidates
    -> qos.py or qos_sampling.py
    -> qsvt.py / downstream task
    -> structured readout scheduling (Notebooks 08–13)
```

This system now includes:

- input-side filtering (Part I)  
- output-side readout control (Part II)  

---

## Part I — Pre-Oracle Filtering (Input Reduction)

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

👉 notebooks/modwheel_notebooks_overview.md

---

### Part I — Pre-Oracle Filtering (01–07)

- Notebook 01 — wheel density and tradeoff  
- Notebook 02 — synthetic row-ID adapter  
- Notebook 03 — 20news real dataset adapter  
- Notebook 04 — consolidated paper figure pack  
- Notebook 05 — comparison with random subsampling  
- Notebook 06 — QOS-style wrapper (pre-feature filtering)  
- Notebook 07 — row-order robustness  

**Establishes:**

- deterministic reduction ≈ random subsampling  
- reduced preprocessing cost (Notebook 06)  
- stability under dataset reordering (Notebook 07)  

---

### Part II — Readout Scheduling & Inference Control (08–13)

- Notebook 08 — structured vs random readout scheduling  
- Notebook 09 — early stopping  
- Notebook 10 — confidence-aware scheduling  
- Notebook 11 — hybrid scheduling (mod30 + confidence)  
- Notebook 12 — coverage-constrained stopping  
- Notebook 13 — multi-objective policy optimization  

**Establishes:**

- structured evaluation of sparse queries  
- early stopping based on target behavior  
- coverage-aware scheduling (mod30 lanes)  
- explicit stopping policies (accuracy + coverage)  
- Pareto tradeoffs between:
  - query cost  
  - accuracy  
  - coverage  
  - distribution stability  

---

## Paper

Full write-up of the modwheel pre-oracle filtering layer:

👉 paper/paper.pdf

Highlights:

- ~73–79% candidate reduction before oracle construction  
- deterministic alternative to random subsampling  
- reduced preprocessing cost in QOS-style wrapper experiments  
- robustness to dataset ordering  
- non-invasive integration (no QOS modifications)  

Extended results (Notebooks 08–13) introduce:

- structured readout scheduling  
- coverage-aware inference  
- multi-objective policy selection  

---

## Summary

This repository introduces two complementary layers:

### Input-side (Part I)

deterministic pre-oracle filtering  
    -> reduced input stream  
    -> lower preprocessing cost  

### Output-side (Part II)

structured readout scheduling  
    -> controlled evaluation of sparse queries  
    -> early stopping + coverage constraints  
    -> policy selection via multi-objective optimization  

---

## Combined View

```text
raw data
    -> modwheel filtering (input reduction)
    -> feature construction / QOS-style model
    -> structured readout scheduling
    -> controlled stopping / policy selection
```

---

## Guardrail

This work:

- evaluates classical preprocessing and inference behavior  
- demonstrates QOS-compatible integration patterns  

It does NOT claim:

- quantum advantage  
- improvements to QOS algorithms  
- accuracy gains  
