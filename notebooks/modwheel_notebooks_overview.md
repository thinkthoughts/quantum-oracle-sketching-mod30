# Modwheel Pre-Oracle Filtering Notebooks

This repository includes a sequence of notebooks that introduce, validate, and integrate a deterministic wheel-based pre-oracle filtering layer (mod30, mod210, mod2310) for **Quantum Oracle Sketching (QOS)-style pipelines**.

The notebooks progress:

```text
theory → adapter → real data → comparison → pipeline integration → robustness
```

---

## Notebook 01 — Pre-Oracle Tradeoff

```
notebooks/01_modwheel_pre_oracle_tradeoff.ipynb
```

**Purpose:**

* Compare mod30, mod210, mod2310
* Show candidate density and reduction
* Establish theoretical tradeoff

**Outputs:**

* figures/modwheel_pre_oracle_tradeoff.svg
* figures/modwheel_pre_oracle_tradeoff.png

---

## Notebook 02 — Row-ID Adapter (Synthetic)

```
notebooks/02_real_dataset_row_id_prefilter_adapter.ipynb
```

**Purpose:**

* Demonstrate safe row-ID filtering on dataset-shaped inputs
* Validate structural correctness of filtering

**Outputs:**

* data/row_id_prefilter_retained_samples.csv
* data/row_id_prefilter_classifier_sanity.csv
* figures/row_id_prefilter_retained_fraction.svg
* figures/row_id_prefilter_classifier_sanity.svg

---

## Notebook 03 — 20news Real Dataset Adapter

```
notebooks/03_20news_row_id_prefilter_qos_adapter.ipynb
```

**Purpose:**

* Apply filtering to a real dataset
* Measure:

  * retained samples
  * class balance
  * fit-time proxy
  * classifier behavior

**Outputs:**

* data/20news_row_id_prefilter_retained_samples.csv
* data/20news_row_id_prefilter_svc_sanity.csv
* figures/20news_row_id_prefilter_retained_fraction.svg
* figures/20news_row_id_prefilter_balanced_accuracy.svg
* figures/20news_row_id_prefilter_fit_time.svg

---

## Notebook 04 — Paper Figure Pack

```
notebooks/04_modwheel_paper_figure_pack.ipynb
```

**Purpose:**

* Consolidate results from Notebooks 1–3
* Generate publication-ready figures and summaries

**Outputs:**

* data/paper_results_summary.csv

* data/paper_retained_fraction_summary.csv

* data/paper_20news_behavior_summary.csv

* data/paper_results_summary.md

* figures/figure_01_wheel_candidate_fraction.svg

* figures/figure_02_adapter_retained_fraction.svg

* figures/figure_03a_20news_balanced_accuracy.svg

* figures/figure_03b_20news_fit_time_proxy.svg

---

## Notebook 05 — Comparison with Random Subsampling

```
notebooks/05_modwheel_vs_random_subsampling.ipynb
```

**Purpose:**

* Compare wheel filtering with random subsampling at matched retained fractions
* Establish baseline equivalence

**Key Result:**

* wheel ≈ random (within noise)

**Interpretation:**

* wheel filtering behaves like deterministic subsampling

**Outputs:**

* figures/figure_05a_balanced_accuracy_wheel_vs_random.svg
* figures/figure_05b_random_distribution_boxplot.svg
* figures/figure_05c_accuracy_delta.svg

---

## Notebook 06 — QOS-Style Wrapper (Pre-Feature Filtering)

```
notebooks/06_qos_real_datasets_wrapper_modwheel.ipynb
```

**Purpose:**

* Apply filtering before feature construction (correct pipeline placement)
* Simulate a QOS-style preprocessing stage

**Key Result:**

* reduced input → reduced preprocessing cost (TF-IDF, etc.)
* downstream behavior remains stable

**Interpretation:**

* valid **pre-oracle / pre-feature layer**

**Outputs:**

* data/06_qos_style_wrapper_results.csv
* figures/figure_06a_wrapper_retained_fraction.svg
* figures/figure_06b_wrapper_vectorize_time.svg
* figures/figure_06c_wrapper_balanced_accuracy.svg
* figures/figure_06d_wrapper_class_balance_shift.svg

---

## Notebook 07 — Row-Order Robustness

```
notebooks/07_row_order_robustness_modwheel.ipynb
```

**Purpose:**

* Test whether filtering depends on dataset ordering
* Compare original vs shuffled row order

**Key Result:**

* results remain stable under permutation

**Interpretation:**

* filtering is **not driven by row-order artifacts**

**Outputs:**

* data/07_row_order_robustness_results.csv
* data/07_row_order_robustness_delta_summary.csv
* figures/figure_07a_row_order_balanced_accuracy.svg
* figures/figure_07b_row_order_balanced_accuracy_delta.svg
* figures/figure_07c_row_order_class_balance_shift.svg

---

## Running

### Local

Run from repository root:

```
jupyter notebook notebooks/
```

---

### Colab

```
https://colab.research.google.com/github/thinkthoughts/quantum-oracle-sketching-mod30/
```

Each notebook clones the repo and runs independently.

---

## Summary

Across mod30, mod210, and mod2310:

* candidate streams reduce by ~73–79%
* behavior matches random subsampling
* preprocessing cost decreases (Notebook 06)
* results are robust to row ordering (Notebook 07)

This supports:

```text
deterministic pre-oracle filtering
→ reduced input stream
→ lower preprocessing cost
→ stable downstream behavior
```

---

## Guardrail

These notebooks:

* evaluate classical preprocessing behavior
* demonstrate QOS-compatible adapter integration

They do NOT claim:

* quantum advantage
* improvement to QOS algorithms
* accuracy gains

---

## Overall Interpretation

This work introduces:

> a deterministic front-end filtering layer for reducing classical input before QOS-style pipelines

---
