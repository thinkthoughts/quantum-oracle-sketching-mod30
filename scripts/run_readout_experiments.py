#!/usr/bin/env python3
"""
run_readout_experiments.py

Reproduce a compact readout-policy experiment from the command line.

Outputs:
- data/readout_policy_results.csv
- data/readout_policy_summary.csv
- figures/readout_accuracy_vs_coverage.png
- figures/readout_pareto.png

Usage:
    python scripts/run_readout_experiments.py

Optional:
    python scripts/run_readout_experiments.py --max-features 12000 --random-trials 30
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, balanced_accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC

# Ensure repo root and src are importable when script is run from repo root.
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from readout_policy import (  # noqa: E402
    class_balance_l1_shift,
    confidence_schedule,
    hybrid_modular_confidence_schedule,
    lane_coverage,
    modular_schedule,
    pareto_efficient,
    random_schedule,
)


def decision_margin_confidence(model: LinearSVC, X) -> np.ndarray:
    """Margin confidence for LinearSVC."""
    scores = model.decision_function(X)
    if scores.ndim == 1:
        return np.abs(scores)
    sorted_scores = np.sort(scores, axis=1)
    return sorted_scores[:, -1] - sorted_scores[:, -2]


def evaluate_subset(model, X_test, y_test, indices: np.ndarray) -> dict:
    pred = model.predict(X_test[indices])
    return {
        "accuracy": accuracy_score(y_test[indices], pred),
        "balanced_accuracy": balanced_accuracy_score(y_test[indices], pred),
        "class_balance_l1_shift": class_balance_l1_shift(y_test[indices], y_test),
        "lane_coverage_fraction": lane_coverage(indices, modulus=30),
    }


def progressive_curve(name, schedule_type, schedule, model, X_test, y_test, fractions, trial=-1):
    rows = []
    n_total = X_test.shape[0]

    for f in fractions:
        k = max(2, int(np.ceil(len(schedule) * f)))
        idx = schedule[:k]
        metrics = evaluate_subset(model, X_test, y_test, idx)

        rows.append(
            {
                "schedule_name": name,
                "schedule_type": schedule_type,
                "trial": trial,
                "schedule_fraction": f,
                "n_eval": len(idx),
                "fraction_of_all_queries": len(idx) / n_total,
                **metrics,
            }
        )

    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--random-state", type=int, default=9423)
    parser.add_argument("--random-trials", type=int, default=30)
    parser.add_argument("--max-features", type=int, default=12000)
    parser.add_argument("--output-dir", type=str, default=".")
    args = parser.parse_args()

    root = Path(args.output_dir)
    data_dir = root / "data"
    fig_dir = root / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    fig_dir.mkdir(parents=True, exist_ok=True)

    categories = [
        "comp.graphics",
        "rec.sport.baseball",
        "sci.space",
        "talk.politics.misc",
    ]

    dataset = fetch_20newsgroups(
        subset="all",
        categories=categories,
        remove=("headers", "footers", "quotes"),
        shuffle=True,
        random_state=args.random_state,
    )

    texts = np.array(dataset.data, dtype=object)
    y = np.array(dataset.target)

    texts_train, texts_test, y_train, y_test = train_test_split(
        texts,
        y,
        test_size=0.30,
        random_state=args.random_state,
        stratify=y,
    )

    vectorizer = TfidfVectorizer(
        max_features=args.max_features,
        min_df=2,
        stop_words="english",
    )
    X_train = vectorizer.fit_transform(texts_train)
    X_test = vectorizer.transform(texts_test)

    clf = LinearSVC(random_state=args.random_state, dual="auto")
    clf.fit(X_train, y_train)

    full_pred = clf.predict(X_test)
    full_bal_acc = balanced_accuracy_score(y_test, full_pred)

    confidence = decision_margin_confidence(clf, X_test)

    n_queries = X_test.shape[0]
    mod30 = modular_schedule(n_queries, modulus=30)
    n_keep = len(mod30)

    schedules = {
        "mod30": ("deterministic_mod30", mod30),
        "global_low_conf": (
            "global_low_confidence",
            confidence_schedule(confidence, n_keep=n_keep, low_confidence_first=True),
        ),
        "hybrid_lane_low_conf": (
            "hybrid_lane_low_confidence",
            hybrid_modular_confidence_schedule(
                confidence,
                modulus=30,
                n_keep=n_keep,
                low_confidence_first=True,
            ),
        ),
        "hybrid_lane_round_robin": (
            "hybrid_lane_round_robin",
            mod30,
        ),
    }

    fractions = np.linspace(0.05, 1.0, 20)
    rows = []

    for name, (stype, sched) in schedules.items():
        rows.extend(progressive_curve(name, stype, sched, clf, X_test, y_test, fractions))

    for trial in range(args.random_trials):
        sched = random_schedule(n_queries, n_keep, seed=args.random_state + 1009 * trial)
        rows.extend(
            progressive_curve(
                "random_matched",
                "random_matched",
                sched,
                clf,
                X_test,
                y_test,
                fractions,
                trial=trial,
            )
        )

    results = pd.DataFrame(rows)
    results_path = data_dir / "readout_policy_results.csv"
    results.to_csv(results_path, index=False)

    # Multi-objective costs
    results["cost_query_fraction"] = results["fraction_of_all_queries"]
    results["cost_accuracy_gap"] = np.maximum(0, full_bal_acc - results["balanced_accuracy"]) / max(full_bal_acc, 1e-9)
    results["cost_coverage_gap"] = 1 - results["lane_coverage_fraction"]
    max_shift = max(results["class_balance_l1_shift"].max(), 1e-9)
    results["cost_class_shift"] = results["class_balance_l1_shift"] / max_shift

    costs = results[
        [
            "cost_query_fraction",
            "cost_accuracy_gap",
            "cost_coverage_gap",
            "cost_class_shift",
        ]
    ].to_numpy()
    results["pareto_efficient"] = pareto_efficient(costs)

    summary = (
        results.groupby("schedule_type")
        .agg(
            best_balanced_accuracy=("balanced_accuracy", "max"),
            min_query_fraction=("fraction_of_all_queries", "min"),
            max_lane_coverage=("lane_coverage_fraction", "max"),
            min_class_balance_l1=("class_balance_l1_shift", "min"),
            pareto_points=("pareto_efficient", "sum"),
        )
        .reset_index()
    )

    summary_path = data_dir / "readout_policy_summary.csv"
    summary.to_csv(summary_path, index=False)

    # Figure 1: accuracy vs coverage
    fig, ax = plt.subplots(figsize=(8, 5))
    for stype, group in results[results["schedule_type"] != "random_matched"].groupby("schedule_type"):
        group = group.sort_values("lane_coverage_fraction")
        ax.plot(group["lane_coverage_fraction"], group["balanced_accuracy"], marker="o", label=stype)

    random_mean = (
        results[results["schedule_type"] == "random_matched"]
        .groupby("lane_coverage_fraction")["balanced_accuracy"]
        .mean()
        .reset_index()
    )
    ax.plot(random_mean["lane_coverage_fraction"], random_mean["balanced_accuracy"], label="random_mean")
    ax.axhline(0.95 * full_bal_acc, linestyle="--", linewidth=1, label="95% target")
    ax.set_title("Accuracy vs Lane Coverage")
    ax.set_xlabel("Lane coverage fraction")
    ax.set_ylabel("Balanced accuracy")
    ax.set_ylim(0.5, 1.0)
    ax.grid(True, alpha=0.35)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(fig_dir / "readout_accuracy_vs_coverage.png", dpi=220)
    fig.savefig(fig_dir / "readout_accuracy_vs_coverage.svg")
    plt.close(fig)

    # Figure 2: Pareto view
    fig, ax = plt.subplots(figsize=(8, 5))
    sc = ax.scatter(
        results["fraction_of_all_queries"],
        results["balanced_accuracy"],
        c=results["lane_coverage_fraction"],
        alpha=0.45,
    )
    pareto = results[results["pareto_efficient"]]
    ax.scatter(
        pareto["fraction_of_all_queries"],
        pareto["balanced_accuracy"],
        marker="D",
        facecolors="none",
        edgecolors="black",
        label="Pareto-efficient",
    )
    ax.axhline(0.95 * full_bal_acc, linestyle="--", linewidth=1, label="95% target")
    ax.set_title("Pareto View: Query Cost, Accuracy, Coverage")
    ax.set_xlabel("Fraction of all queries evaluated")
    ax.set_ylabel("Balanced accuracy")
    ax.set_ylim(0.5, 1.0)
    ax.grid(True, alpha=0.35)
    ax.legend(fontsize=8)
    fig.colorbar(sc, ax=ax, label="Lane coverage fraction")
    fig.tight_layout()
    fig.savefig(fig_dir / "readout_pareto.png", dpi=220)
    fig.savefig(fig_dir / "readout_pareto.svg")
    plt.close(fig)

    print("Saved:")
    print(f"  {results_path}")
    print(f"  {summary_path}")
    print(f"  {fig_dir / 'readout_accuracy_vs_coverage.png'}")
    print(f"  {fig_dir / 'readout_pareto.png'}")


if __name__ == "__main__":
    main()
