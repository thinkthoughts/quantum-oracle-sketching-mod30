"""
readout_policy.py

Reusable scheduling and stopping utilities for structured readout experiments.

This module is intentionally classical and non-invasive:
- no QOS internals are modified
- no quantum advantage is claimed
- schedules are used to control query evaluation order and stopping behavior
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Mapping, Optional, Sequence

import numpy as np


MOD30_RESIDUES = (1, 7, 11, 13, 17, 19, 23, 29)


@dataclass(frozen=True)
class StopResult:
    """Result returned by a stopping rule."""

    reached: bool
    reason: str
    n_eval: int
    fraction: float
    accuracy: float
    coverage: float


def wheel_residues(modulus: int) -> tuple[int, ...]:
    """Return residues r in [0, modulus) satisfying gcd(r, modulus) = 1."""
    return tuple(r for r in range(modulus) if np.gcd(r, modulus) == 1)


def modular_schedule(
    n_queries: int,
    modulus: int = 30,
    residues: Optional[Sequence[int]] = None,
) -> np.ndarray:
    """Return deterministic indices whose residues are admissible."""
    if n_queries <= 0:
        return np.array([], dtype=int)

    if residues is None:
        residues = wheel_residues(modulus)

    residue_set = set(int(r) for r in residues)
    return np.array([i for i in range(n_queries) if i % modulus in residue_set], dtype=int)


def random_schedule(n_queries: int, n_keep: int, seed: int = 0) -> np.ndarray:
    """Return random query indices without replacement."""
    if n_queries <= 0:
        return np.array([], dtype=int)

    n_keep = min(max(int(n_keep), 0), n_queries)
    rng = np.random.default_rng(seed)
    return np.array(rng.choice(np.arange(n_queries), size=n_keep, replace=False), dtype=int)


def confidence_schedule(
    confidence: np.ndarray,
    n_keep: Optional[int] = None,
    low_confidence_first: bool = True,
) -> np.ndarray:
    """
    Return indices sorted by confidence.

    Lower confidence first prioritizes uncertain queries.
    Higher confidence first is useful as a diagnostic contrast.
    """
    confidence = np.asarray(confidence)
    order = np.argsort(confidence)
    if not low_confidence_first:
        order = order[::-1]

    if n_keep is None:
        return order.astype(int)
    return order[:n_keep].astype(int)


def split_lanes(
    indices: Sequence[int],
    modulus: int = 30,
    residues: Optional[Sequence[int]] = None,
) -> Dict[int, List[int]]:
    """Split indices into modular lanes."""
    if residues is None:
        residues = wheel_residues(modulus)

    lanes: Dict[int, List[int]] = {int(r): [] for r in residues}
    for i in indices:
        r = int(i) % modulus
        if r in lanes:
            lanes[r].append(int(i))
    return lanes


def interleave_lanes(lanes: Mapping[int, Sequence[int]]) -> np.ndarray:
    """Round-robin interleave modular lanes."""
    if not lanes:
        return np.array([], dtype=int)

    keys = list(lanes.keys())
    max_len = max((len(lanes[k]) for k in keys), default=0)

    out: List[int] = []
    for j in range(max_len):
        for k in keys:
            if j < len(lanes[k]):
                out.append(int(lanes[k][j]))
    return np.array(out, dtype=int)


def hybrid_modular_confidence_schedule(
    confidence: np.ndarray,
    modulus: int = 30,
    residues: Optional[Sequence[int]] = None,
    n_keep: Optional[int] = None,
    low_confidence_first: bool = True,
) -> np.ndarray:
    """
    Split admissible modular indices into lanes, sort each lane by confidence,
    then interleave lanes.
    """
    confidence = np.asarray(confidence)
    n_queries = len(confidence)

    base = modular_schedule(n_queries, modulus=modulus, residues=residues)
    lanes = split_lanes(base, modulus=modulus, residues=residues)

    for r, idxs in lanes.items():
        arr = np.array(idxs, dtype=int)
        if len(arr) == 0:
            lanes[r] = []
            continue
        order = np.argsort(confidence[arr])
        if not low_confidence_first:
            order = order[::-1]
        lanes[r] = arr[order].astype(int).tolist()

    schedule = interleave_lanes(lanes)
    if n_keep is not None:
        schedule = schedule[:n_keep]
    return schedule.astype(int)


def lane_coverage(
    evaluated_indices: Sequence[int],
    modulus: int = 30,
    residues: Optional[Sequence[int]] = None,
) -> float:
    """Return fraction of admissible modular lanes touched by evaluated indices."""
    if residues is None:
        residues = wheel_residues(modulus)

    residue_set = set(int(r) for r in residues)
    if len(residue_set) == 0:
        return 0.0

    covered = {int(i) % modulus for i in evaluated_indices if int(i) % modulus in residue_set}
    return len(covered) / len(residue_set)


def class_balance_l1_shift(y_subset: np.ndarray, y_reference: np.ndarray) -> float:
    """L1 shift between subset and reference label distributions."""
    y_subset = np.asarray(y_subset)
    y_reference = np.asarray(y_reference)

    if len(y_subset) == 0:
        return float("nan")

    n_classes = int(max(np.max(y_reference), np.max(y_subset))) + 1
    subset_counts = np.bincount(y_subset, minlength=n_classes)
    ref_counts = np.bincount(y_reference, minlength=n_classes)

    subset_frac = subset_counts / subset_counts.sum()
    ref_frac = ref_counts / ref_counts.sum()

    return float(np.sum(np.abs(subset_frac - ref_frac)))


def should_stop(
    accuracy: float,
    coverage: float,
    accuracy_threshold: float,
    coverage_threshold: float = 0.0,
) -> bool:
    """Joint stopping rule."""
    return bool(accuracy >= accuracy_threshold and coverage >= coverage_threshold)


def first_stop(
    rows: Sequence[Mapping[str, float]],
    accuracy_threshold: float,
    coverage_threshold: float = 0.0,
) -> StopResult:
    """
    Find first row satisfying accuracy and coverage thresholds.

    Each row must include:
    - n_eval
    - fraction_of_all_queries
    - balanced_accuracy
    - lane_coverage_fraction
    """
    if len(rows) == 0:
        return StopResult(False, "empty", 0, 0.0, float("nan"), float("nan"))

    for row in rows:
        acc = float(row["balanced_accuracy"])
        cov = float(row["lane_coverage_fraction"])
        if should_stop(acc, cov, accuracy_threshold, coverage_threshold):
            return StopResult(
                reached=True,
                reason="reached",
                n_eval=int(row["n_eval"]),
                fraction=float(row["fraction_of_all_queries"]),
                accuracy=acc,
                coverage=cov,
            )

    last = rows[-1]
    return StopResult(
        reached=False,
        reason="not_reached",
        n_eval=int(last["n_eval"]),
        fraction=float(last["fraction_of_all_queries"]),
        accuracy=float(last["balanced_accuracy"]),
        coverage=float(last["lane_coverage_fraction"]),
    )


def pareto_efficient(costs: np.ndarray) -> np.ndarray:
    """
    Return boolean mask for Pareto-efficient rows.

    All columns are minimized.
    """
    costs = np.asarray(costs, dtype=float)
    n = costs.shape[0]
    is_eff = np.ones(n, dtype=bool)

    for i in range(n):
        if not is_eff[i]:
            continue
        dominated = np.all(costs <= costs[i], axis=1) & np.any(costs < costs[i], axis=1)
        if np.any(dominated):
            is_eff[i] = False

    return is_eff
