"""
Optional classical filtering layer before QOS.

Intended integration:

raw classical data
→ pre_oracle_candidates(...)
→ qos.py / qos_sampling.py
→ oracle construction

Purpose:
- reduce candidate stream size
- introduce a classical vs oracle cost tradeoff

This layer is independent and does not alter QOS internals.
"""

from __future__ import annotations

from typing import Iterable

from modwheel import Wheel, STANDARD_WHEELS


def pre_oracle_candidates(values: Iterable[int], wheel: Wheel) -> list[int]:
    """Return values that pass the wheel constraint."""
    return wheel.filter(values)


def pre_oracle_candidates_by_name(values: Iterable[int], wheel_name: str) -> list[int]:
    """Filter values using one of: mod30, mod210, mod2310."""
    try:
        wheel = STANDARD_WHEELS[wheel_name]
    except KeyError as exc:
        available = ", ".join(STANDARD_WHEELS)
        raise ValueError(f"Unknown wheel_name={wheel_name!r}. Available: {available}") from exc
    return pre_oracle_candidates(values, wheel)


def oracle_call_proxy(values: Iterable[int], wheel: Wheel | None = None) -> int:
    """
    Simple proxy for oracle workload.

    Without a wheel, this equals len(values).
    With a wheel, this equals number of candidates entering oracle construction.
    """
    vals = list(values)
    if wheel is None:
        return len(vals)
    return len(pre_oracle_candidates(vals, wheel))
