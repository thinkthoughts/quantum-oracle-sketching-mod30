"""
Compare mod30, mod210, and mod2310 as pre-oracle wheel filters.

Run:
    python compare_wheels.py
"""

from __future__ import annotations

from modwheel import STANDARD_WHEELS, wheel_summary


def main() -> None:
    print("wheel,primes,modulus,residues,density,reduction")
    for name, wheel in STANDARD_WHEELS.items():
        s = wheel_summary(wheel)
        primes = "·".join(str(p) for p in s["primes"])
        print(
            f"{name},{primes},{s['modulus']},{s['residue_count']},"
            f"{s['density']:.6f},{s['reduction']:.6f}"
        )


if __name__ == "__main__":
    main()
