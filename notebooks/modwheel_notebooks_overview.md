# Modwheel Pre-Oracle Filtering Notebooks

This repository includes a sequence of notebooks that introduce, test, and consolidate a wheel-based pre-oracle filtering layer (mod30, mod210, mod2310).

The notebooks are designed to move from theory → adapter → real data → paper-ready results.

---

## Notebook 01 — Pre-Oracle Tradeoff

notebooks/01_modwheel_pre_oracle_tradeoff.ipynb

Purpose:
- Compare mod30, mod210, mod2310
- Show candidate density and reduction
- Generate the core tradeoff figure

Outputs:
- figures/modwheel_pre_oracle_tradeoff.svg
- figures/modwheel_pre_oracle_tradeoff.png

---

## Notebook 02 — Row-ID Adapter (Synthetic)

notebooks/02_real_dataset_row_id_prefilter_adapter.ipynb

Purpose:
- Demonstrate safe row-ID filtering on dataset-shaped matrices
- Validate that filtering reduces samples without breaking downstream workflows

Outputs:
- data/row_id_prefilter_retained_samples.csv
- data/row_id_prefilter_classifier_sanity.csv
- figures/row_id_prefilter_retained_fraction.svg
- figures/row_id_prefilter_classifier_sanity.svg

---

## Notebook 03 — 20news Real Dataset Adapter

notebooks/03_20news_row_id_prefilter_qos_adapter.ipynb

Purpose:
- Apply row-ID filtering to a real text dataset (20newsgroups)
- Measure:
  - retained samples
  - class balance
  - fit-time proxy
  - classifier behavior

Outputs:
- data/20news_row_id_prefilter_retained_samples.csv
- data/20news_row_id_prefilter_svc_sanity.csv
- figures/20news_row_id_prefilter_retained_fraction.svg
- figures/20news_row_id_prefilter_balanced_accuracy.svg
- figures/20news_row_id_prefilter_fit_time.svg

---

## Notebook 04 — Paper Figure Pack

notebooks/04_modwheel_paper_figure_pack.ipynb

Purpose:
- Consolidate results from Notebooks 1–3
- Generate publication-ready figures and tables
- Export Markdown + CSV summaries

Outputs:
- data/paper_results_summary.csv
- data/paper_retained_fraction_summary.csv
- data/paper_20news_behavior_summary.csv
- data/paper_results_summary.md

- figures/figure_01_wheel_candidate_fraction.svg
- figures/figure_02_adapter_retained_fraction.svg
- figures/figure_03a_20news_balanced_accuracy.svg
- figures/figure_03b_20news_fit_time_proxy.svg

---

## Running

### Local

Run from repository root:

jupyter notebook notebooks/

---

### Colab

https://colab.research.google.com/github/thinkthoughts/quantum-oracle-sketching-mod30/

Each notebook clones the repo and runs independently.

---

## Summary

Across mod30, mod210, and mod2310:

- candidate streams reduce by ~73–79%
- filtering can be applied safely at the row-ID level
- real-dataset behavior (20news) remains stable
- fit-time proxy decreases with reduced sample count

This supports:

classical pre-oracle filtering → smaller candidate stream → downstream QOS / ML workflow

---

## Guardrail

These notebooks:
- measure filtering behavior and workload proxies
- demonstrate adapter-level integration

They do NOT claim:
- quantum advantage
- accuracy improvement
