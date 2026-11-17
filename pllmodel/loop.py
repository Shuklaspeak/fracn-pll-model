"""
Linear (continuous-time) model of a type-II, third-order charge-pump PLL.

Loop filter: R in series with C1, all in parallel with C2.

UNITS (the #1 source of bugs in PLL models):
    f      : Hz
    Icp    : A
    Kvco   : rad/s/V   <-- NOT Hz/V. Use kvco_rad(...) to convert.
    R      : ohm
    C1, C2 : F
    angles : degrees at the API boundary
"""

import numpy as np


def kvco_rad(kvco_hz_per_v):
    """Convert a VCO gain given in Hz/V (e.g. 100e6 for 100 MHz/V) to rad/s/V."""
    return 2 * np.pi * kvco_hz_per_v


# ---------------------------------------------------------------------------
# Forward model: components -> loop behaviour
# ---------------------------------------------------------------------------

def loop_gain(f, Icp, Kvco, N, R, C1, C2):
    """
    Open-loop gain L(j*2*pi*f) of the PLL, in the phase domain.

    L(s) = (Icp / 2pi) * Z_LF(s) * (Kvco / s) * (1 / N)

    Parameters
    ----------
    f : float or numpy array of frequencies in Hz

    Returns
    -------
    complex numpy array, same shape as f

    TODO (yours):
      1. s = 1j * 2 * np.pi * f
      2. Write Z_LF(s) for R+C1 in parallel with C2.
         (Impedance of a capacitor is 1/(s*C). Parallel: Za*Zb/(Za+Zb).)
      3. Combine the four blocks above and return L.
    numpy note: if f is an array, every line works element-wise automatically.
    """
    
    s = 1j * 2 * np.pi * f
    z = (1 + s*C1*R)/(s*(C1 + C2*(1+s*C1*R)))
    L = (Icp / (2 * np.pi)) * z * (Kvco / s) * (1 / N)
    return L




def closed_loop(f, Icp, Kvco, N, R, C1, C2):
    """Closed-loop transfer function from reference phase to output phase: N*L/(1+L)."""
    L = loop_gain(f, Icp, Kvco, N, R, C1, C2)
    return N * L / (1 + L)


def phase_margin(Icp, Kvco, N, R, C1, C2, fmin=1e2, fmax=1e9, npts=200_001):
    """
    Find the crossover frequency fc (|L| = 1) and the phase margin at fc.

    Returns
    -------
    (fc_hz, pm_deg)

    TODO (yours):
      1. Make a log-spaced frequency grid:  f = np.logspace(np.log10(fmin), np.log10(fmax), npts)
      2. L = loop_gain(f, ...);  mag = np.abs(L)
      3. Find the first index i where mag drops below 1.
         Hint: np.argmax(mag < 1) returns the first True index.
      4. fc = f[i]   (optional upgrade: interpolate between f[i-1] and f[i] on a log scale)
      5. Phase in degrees: np.degrees(np.unwrap(np.angle(L)))
         -> np.angle alone wraps to (-180, 180]; unwrap keeps it continuous.
      6. PM = 180 + phase[i]
    """
    f = np.logspace(np.log10(fmin), np.log10(fmax), npts)
    L = loop_gain(f, Icp, Kvco, N, R, C1, C2)
    Lmag = np.abs(L)
    i_fc = np.argmax(Lmag < 1)
    if i_fc == 0:
        raise ValueError("crossover is below fmin (or |L| never drops below 1): widen the grid")
    fc_hz = f[i_fc]
    phase = np.degrees(np.unwrap(np.angle(L)))
    pm_deg = 180 + phase[i_fc]
    return fc_hz, pm_deg

# ---------------------------------------------------------------------------
# Inverse model: spec -> components  (this is how loop filters are designed)
# ---------------------------------------------------------------------------

def design_filter(fc, pm_deg, Icp, Kvco, N):
    """
    Choose R, C1, C2 so the loop crosses over at fc with phase margin pm_deg,
    placing crossover at the PM-optimal point wc = sqrt(wz * wp3).

    Returns
    -------
    (R, C1, C2)

    TODO (yours) — your derivation from this morning, as code:
      1. PM -> b  (b = wp3/wz). Generalize the quadratic you solved for 60 deg:
         sqrt(b) as a function of tan(PM). Check: 60 deg must give sqrt(b) = 2 + sqrt(3).
         numpy: np.tan / np.cos take radians -> np.radians(pm_deg)
      2. wc = 2*pi*fc;  wz = wc / sqrt(b)
      3. K = wc**2 / sqrt(b), and K = Icp*Kvco / (2*pi*N*(C1+C2))  ->  C1 + C2
      4. b = 1 + C1/C2  ->  split into C1 and C2
      5. R = 1 / (wz * C1)
    """
    p = np.radians(pm_deg)
    x = np.tan(p) + 1 / np.cos(p)   # sqrt(b): positive root of x^2 - 2*tan(PM)*x - 1 = 0
    b = x**2
    wc = 2 * np.pi * fc
    wz = wc / x
    K = wc**2 / x
    Ctot = (Icp * Kvco) / (2 * np.pi * N * K)
    C1 = (b - 1) / b * Ctot
    C2 = C1 / (b - 1)
    R = 1 / (wz * C1)
    return R, C1, C2
