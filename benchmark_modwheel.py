"""
Tiny benchmark/proxy experiment for pre-oracle filtering.

This is intentionally simple: it measures how many integer candidates remain
after mod30, mod210, and mod2310 filtering.

Run:
    python benchmark_modwheel.py --n 100000
"""

from __future__ import annotations

import argparse

from modwheel import STANDARD_WHEELS
from pre_oracle_filter import oracle_call_proxy


def run(n: int) -> None:
    values = range(1, n + 1)
    baseline = oracle_call_proxy(values)

    print(f"baseline_candidates,{baseline}")
    print("wheel,remaining,remaining_fraction,reduction_fraction")

    for name, wheel in STANDARD_WHEELS.items():
        remaining = oracle_call_proxy(range(1, n + 1), wheel)
        remaining_fraction = remaining / baseline
        reduction_fraction = 1.0 - remaining_fraction
        print(f"{name},{remaining},{remaining_fraction:.6f},{reduction_fraction:.6f}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=100_000, help="Candidate range: 1..n")
    args = parser.parse_args()
    run(args.n)


if __name__ == "__main__":
    main()
