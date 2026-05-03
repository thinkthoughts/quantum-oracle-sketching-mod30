"""
pytest tests for wheel-based pre-oracle filtering.

Run:
    pytest test_modwheel.py
"""

from modwheel import STANDARD_WHEELS, make_wheel
from pre_oracle_filter import pre_oracle_candidates_by_name, oracle_call_proxy


def test_standard_residue_counts():
    assert STANDARD_WHEELS["mod30"].residue_count == 8
    assert STANDARD_WHEELS["mod210"].residue_count == 48
    assert STANDARD_WHEELS["mod2310"].residue_count == 480


def test_standard_densities():
    assert STANDARD_WHEELS["mod30"].density == 8 / 30
    assert STANDARD_WHEELS["mod210"].density == 48 / 210
    assert STANDARD_WHEELS["mod2310"].density == 480 / 2310


def test_mod30_accepts_expected_residues():
    residues = set(STANDARD_WHEELS["mod30"].residues)
    assert residues == {1, 7, 11, 13, 17, 19, 23, 29}


def test_pre_oracle_filter_mod30_small_range():
    values = list(range(1, 31))
    filtered = pre_oracle_candidates_by_name(values, "mod30")
    assert filtered == [1, 7, 11, 13, 17, 19, 23, 29]


def test_oracle_call_proxy_reduces_candidates():
    values = range(1, 31)
    assert oracle_call_proxy(values) == 30
    assert oracle_call_proxy(values, STANDARD_WHEELS["mod30"]) == 8


def test_make_wheel_rejects_duplicate_primes():
    try:
        make_wheel((2, 3, 3))
    except ValueError:
        return
    raise AssertionError("duplicate primes should raise ValueError")
