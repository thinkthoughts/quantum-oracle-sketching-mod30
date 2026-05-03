"""
modwheel.py

Wheel-based residue filters for classical pre-oracle filtering.

This module is intentionally independent of the core QOS implementation:
it computes admissible residue classes modulo M = product(primes), where
admissible means gcd(r, M) = 1.

Examples:
    mod30   = primes [2, 3, 5]       -> 8 / 30 candidates
    mod210  = primes [2, 3, 5, 7]    -> 48 / 210 candidates
    mod2310 = primes [2, 3, 5, 7, 11]-> 480 / 2310 candidates
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd, prod
from typing import Iterable, Sequence


@dataclass(frozen=True)
class Wheel:
    """Finite wheel filter defined by a list of small primes."""
    primes: tuple[int, ...]

    @property
    def modulus(self) -> int:
        return prod(self.primes)

    @property
    def residues(self) -> tuple[int, ...]:
        m = self.modulus
        return tuple(r for r in range(m) if gcd(r, m) == 1)

    @property
    def residue_count(self) -> int:
        return len(self.residues)

    @property
    def density(self) -> float:
        return self.residue_count / self.modulus

    @property
    def reduction(self) -> float:
        """Fraction excluded by the wheel."""
        return 1.0 - self.density

    def accepts(self, n: int) -> bool:
        return gcd(n % self.modulus, self.modulus) == 1

    def filter(self, values: Iterable[int]) -> list[int]:
        return [n for n in values if self.accepts(n)]


def make_wheel(primes: Sequence[int]) -> Wheel:
    """Construct a Wheel from small primes."""
    if not primes:
        raise ValueError("Wheel requires at least one prime.")
    if any(p <= 1 for p in primes):
        raise ValueError("Wheel primes must be integers greater than 1.")
    if len(set(primes)) != len(primes):
        raise ValueError("Wheel primes must be unique.")
    return Wheel(tuple(int(p) for p in primes))


STANDARD_WHEELS: dict[str, Wheel] = {
    "mod30": make_wheel((2, 3, 5)),
    "mod210": make_wheel((2, 3, 5, 7)),
    "mod2310": make_wheel((2, 3, 5, 7, 11)),
}


def wheel_summary(wheel: Wheel) -> dict[str, float | int | tuple[int, ...]]:
    """Return a compact summary useful for tables and benchmarks."""
    return {
        "primes": wheel.primes,
        "modulus": wheel.modulus,
        "residue_count": wheel.residue_count,
        "density": wheel.density,
        "reduction": wheel.reduction,
    }
