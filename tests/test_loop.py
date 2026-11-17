"""
Tests for pllmodel.loop.  Run from the repo root with:   pytest -v

A test passes silently and fails loudly. The goal: all green.
"""

import numpy as np
import pytest

from pllmodel.loop import kvco_rad, loop_gain, phase_margin, design_filter

# Nominal design point (matches README spec table)
N = 150
KVCO = kvco_rad(100e6)   # 100 MHz/V -> rad/s/V
ICP = 100e-6             # 100 uA
FC = 500e3               # 500 kHz
PM = 60.0                # degrees


def test_kvco_units():
    assert KVCO == pytest.approx(2 * np.pi * 100e6)


def test_design_filter_oracle():
    """Hand-checked values for the nominal design point (within 1%)."""
    R, C1, C2 = design_filter(FC, PM, ICP, KVCO, N)
    assert C1 == pytest.approx(23.4e-12, rel=0.01)
    assert C2 == pytest.approx(1.81e-12, rel=0.01)
    assert R == pytest.approx(50.8e3, rel=0.01)


def test_cap_ratio_for_60deg():
    """For 60 deg, b = (2+sqrt(3))^2, so C1/C2 = b - 1."""
    _, C1, C2 = design_filter(FC, PM, ICP, KVCO, N)
    b = (2 + np.sqrt(3)) ** 2
    assert C1 / C2 == pytest.approx(b - 1, rel=1e-6)


def test_unity_gain_at_fc():
    """|L| must be exactly 1 at the design crossover."""
    R, C1, C2 = design_filter(FC, PM, ICP, KVCO, N)
    assert abs(loop_gain(FC, ICP, KVCO, N, R, C1, C2)) == pytest.approx(1.0, rel=1e-6)


def test_round_trip():
    """design_filter -> phase_margin must give back the spec (forward and inverse agree)."""
    R, C1, C2 = design_filter(FC, PM, ICP, KVCO, N)
    fc, pm = phase_margin(ICP, KVCO, N, R, C1, C2)
    assert fc == pytest.approx(FC, rel=0.01)
    assert pm == pytest.approx(PM, abs=0.5)


def test_pm_is_maximum_at_design_point():
    """Moving crossover off the geometric mean (by scaling Icp) must LOWER the PM."""
    R, C1, C2 = design_filter(FC, PM, ICP, KVCO, N)
    _, pm_nom = phase_margin(ICP, KVCO, N, R, C1, C2)
    _, pm_lo = phase_margin(0.5 * ICP, KVCO, N, R, C1, C2)
    _, pm_hi = phase_margin(2.0 * ICP, KVCO, N, R, C1, C2)
    assert pm_lo < pm_nom and pm_hi < pm_nom
