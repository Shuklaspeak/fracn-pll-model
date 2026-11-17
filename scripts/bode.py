"""
Bode plot of the open-loop gain L(jw) at the nominal design point.
Run from the repo root:   python scripts/bode.py
Saves docs/bode_nominal.png
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import numpy as np
import matplotlib.pyplot as plt
from pllmodel.loop import kvco_rad, loop_gain, phase_margin, design_filter

N, KVCO, ICP, FC, PM = 150, kvco_rad(100e6), 100e-6, 500e3, 60.0

R, C1, C2 = design_filter(FC, PM, ICP, KVCO, N)
fc, pm = phase_margin(ICP, KVCO, N, R, C1, C2)
print(f"R = {R/1e3:.2f} kOhm, C1 = {C1*1e12:.2f} pF, C2 = {C2*1e12:.3f} pF")
print(f"fc = {fc/1e3:.1f} kHz, PM = {pm:.2f} deg")

f = np.logspace(3, 8, 2000)
L = loop_gain(f, ICP, KVCO, N, R, C1, C2)

fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(7, 6))
ax1.semilogx(f, 20 * np.log10(np.abs(L)))
ax1.axhline(0, color="gray", lw=0.8)
ax1.axvline(fc, color="gray", ls="--", lw=0.8)
ax1.set_ylabel("|L| (dB)")
ax1.set_title(f"Open-loop gain — fc = {fc/1e3:.0f} kHz, PM = {pm:.1f}°")
ax2.semilogx(f, np.degrees(np.unwrap(np.angle(L))))
ax2.axhline(-180, color="gray", lw=0.8)
ax2.axvline(fc, color="gray", ls="--", lw=0.8)
ax2.set_ylabel("∠L (deg)")
ax2.set_xlabel("Frequency (Hz)")
for ax in (ax1, ax2):
    ax.grid(True, which="both", alpha=0.3)
fig.tight_layout()
out = pathlib.Path(__file__).resolve().parents[1] / "docs" / "bode_nominal.png"
fig.savefig(out, dpi=150)
print(f"saved {out}")
