# Modwheel + Readout Policy Notebooks

This repository contains two connected components for QOS-style pipelines:

---

## Part I — Pre-Oracle Filtering (Input Reduction)

These notebooks introduce and validate a deterministic wheel-based filtering layer (mod30, mod210, mod2310) applied **before oracle construction / feature extraction**.

Progression:

theory → adapter → real data → comparison → pipeline integration → robustness

---

### Notebook 01 — Pre-Oracle Tradeoff
notebooks/01_modwheel_pre_oracle_tradeoff.ipynb

Purpose:
- Compare mod30, mod210, mod2310
- Show candidate density and reduction

---

### Notebook 02 — Row-ID Adapter (Synthetic)
notebooks/02_real_dataset_row_id_prefilter_adapter.ipynb

Purpose:
- Validate safe filtering on dataset-shaped inputs

---

### Notebook 03 — 20news Real Dataset Adapter
notebooks/03_20news_row_id_prefilter_qos_adapter.ipynb

Purpose:
- Apply filtering to real dataset
- Measure retained samples, class balance, behavior

---

### Notebook 04 — Paper Figure Pack
notebooks/04_modwheel_paper_figure_pack.ipynb

Purpose:
- Consolidate 01–03 into publication-ready outputs

---

### Notebook 05 — Comparison with Random Subsampling
notebooks/05_modwheel_vs_random_subsampling.ipynb

Key Result:
- modwheel ≈ random subsampling

Interpretation:
- deterministic subsampling equivalent

---

### Notebook 06 — QOS-Style Wrapper (Pre-Feature Filtering)
notebooks/06_qos_real_datasets_wrapper_modwheel.ipynb

Key Result:
- reduced input → reduced preprocessing cost
- downstream behavior stable

---

### Notebook 07 — Row-Order Robustness
notebooks/07_row_order_robustness_modwheel.ipynb

Key Result:
- invariant to row permutation

---

## Part I Summary

deterministic pre-oracle filtering
→ ~73–79% input reduction
→ reduced preprocessing cost
→ stable downstream behavior

---

## Part II — Readout Scheduling & Inference Control

These notebooks study how to evaluate many sparse test queries efficiently and systematically after model construction.

Progression:

fixed schedule → early stopping → confidence → coverage → policy → optimization

---

### Notebook 08 — Readout Scheduling (mod30 vs random)
notebooks/08_readout_scheduling_mod30.ipynb

Purpose:
- Evaluate structured vs random query ordering

---

### Notebook 09 — Early Stopping
notebooks/09_early_stopping_readout.ipynb

Purpose:
- Stop evaluation once target behavior reached

---

### Notebook 10 — Confidence-Aware Scheduling
notebooks/10_confidence_readout_scheduling.ipynb

Purpose:
- Prioritize uncertain queries first

---

### Notebook 11 — Hybrid Scheduling (mod30 + confidence)
notebooks/11_hybrid_modwheel_confidence_readout.ipynb

Key Result:
- preserves modular coverage while prioritizing uncertainty

---

### Notebook 12 — Coverage-Constrained Stopping
notebooks/12_coverage_constrained_adaptive_readout.ipynb

Key Result:
- stopping requires both accuracy and coverage

---

### Notebook 13 — Multi-Objective Policy Optimization
notebooks/13_multi_objective_readout_policy.ipynb

Key Result:
- Pareto frontier defines tradeoffs between:
  - query cost
  - accuracy
  - coverage
  - distribution stability

---

## Part II Summary

structured readout scheduling
→ early stopping
→ confidence prioritization
→ coverage guarantees
→ multi-objective policy selection

---

## Combined Pipeline

raw data
→ (Part I) modwheel filtering
→ feature construction / QOS-style model
→ (Part II) structured readout scheduling
→ controlled stopping / policy selection

---

## Guardrail

These notebooks:
- evaluate classical preprocessing and inference behavior
- demonstrate QOS-compatible integration

They do NOT claim:
- quantum advantage
- improvements to QOS algorithms
- accuracy gains

---

## Key Contribution

A structured framework for controlling both input reduction and output evaluation in QOS-style pipelines.
