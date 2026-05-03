# Deterministic Pre-Oracle Filtering for Quantum Oracle Sketching via Modular Wheel Constraints

## Abstract

Quantum Oracle Sketching (QOS) enables quantum-accessible representations of massive classical datasets.
We introduce a deterministic pre-oracle filtering layer based on modular wheel constraints (mod30, mod210, mod2310) that reduces the raw classical input stream before feature construction or oracle preparation.

Across these filters, candidate streams are reduced by approximately 73–79% while preserving usable downstream behavior.
Compared to matched random subsampling, wheel filtering exhibits comparable performance while remaining deterministic and reproducible.
A wrapper experiment shows reduced preprocessing cost, and robustness tests indicate results are not driven by dataset ordering.

This work does not modify QOS internals or claim quantum advantage; it studies a classical front-end layer for reducing input to QOS-style pipelines.

---

## 1. Introduction

Quantum Oracle Sketching (QOS) provides a framework for processing massive classical datasets through quantum-accessible sketches.

A central bottleneck remains:

> the size of the classical input stream prior to oracle construction

This work introduces a complementary front-end approach:

> deterministic filtering applied before QOS sampling or feature construction

The goal is not to modify QOS, but to reduce the amount of data entering QOS-style pipelines.

We study three wheel filters:

* mod30 (2·3·5)
* mod210 (2·3·5·7)
* mod2310 (2·3·5·7·11)

---

## 2. QOS Motivation and Practical Impact

In QOS-style pipelines:

```text
raw classical data
→ preprocessing / feature construction
→ oracle preparation / sketching
→ downstream task
```

We introduce a deterministic front-end layer:

```text
raw data
→ wheel filter
→ reduced data
→ downstream processing
```

Key observations:

* candidate streams reduced by ~73–79%
* preprocessing cost (e.g., TF-IDF) decreases
* downstream behavior remains stable

This establishes:

```text
less input → less preprocessing cost → similar downstream behavior
```

---

## 3. Experiments

### 3.1 QOS-Style Wrapper (Filtering Before Feature Construction)

We apply filtering before feature construction, closer to the intended pre-oracle stage.

![Vectorization time](../figures/figure_06b_wrapper_vectorize_time.svg)

Vectorization time decreases as input size is reduced, demonstrating reduced preprocessing cost.

---

### 3.2 Downstream Stability

![Balanced accuracy](../figures/figure_06c_wrapper_balanced_accuracy.svg)

Balanced accuracy remains stable across filtering levels, indicating that input reduction does not degrade downstream behavior.

---

### 3.3 Comparison with Random Subsampling

We compare wheel filtering with random subsampling at matched retained fractions.

![Wheel vs random](../figures/figure_05a_balanced_accuracy_wheel_vs_random.svg)

Wheel-filtered performance lies within the distribution of random subsets, showing that it behaves like a deterministic version of random reduction.

---

### 3.4 Robustness to Dataset Ordering

We test robustness by permuting dataset rows before filtering.

![Ordering robustness](../figures/figure_07b_row_order_balanced_accuracy_delta.svg)

Differences remain small, indicating results are not driven by row-order artifacts.

---

## 4. Method: Modular Wheel Filtering

A wheel filter retains indices satisfying:

```
gcd(r, M) = 1
```

| Wheel   | Modulus | Residues | Candidate Fraction |
| ------- | ------: | -------: | -----------------: |
| mod30   |      30 |        8 |             0.2667 |
| mod210  |     210 |       48 |             0.2286 |
| mod2310 |    2310 |      480 |             0.2078 |

These filters remove approximately 73–79% of the input stream.

---

## 5. Adapter Design

The filtering layer is non-invasive:

```text
texts, labels
→ apply_modwheel_prefilter
→ filtered data
→ feature construction / QOS pipeline
```

It can be enabled or disabled without modifying QOS code.

---

## 6. Discussion

This work supports a narrow but useful claim:

* deterministic filtering reduces raw input size
* behavior matches random subsampling
* results are robust to ordering
* preprocessing cost is reduced

This work does not:

* modify QOS algorithms
* improve quantum complexity
* claim quantum advantage

Instead, it introduces a classical front-end compatible with QOS workflows.

---

## 7. Conclusion

We presented a deterministic pre-oracle filtering layer for QOS-style pipelines.

The method:

* reduces input size by ~73–79%
* reduces preprocessing cost
* preserves downstream behavior
* behaves like deterministic subsampling

This provides a simple, reproducible preprocessing component for data-intensive hybrid workflows.

---

## References

* Zhao, H. (2026). *Exponential Quantum Advantage in Processing Massive Classical Data*. arXiv:2604.07639
