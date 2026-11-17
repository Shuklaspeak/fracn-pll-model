"""
Placement-quiz Q1, answered with the model:
hold R, C1, C2 at the nominal design and sweep Icp from 0.5x to 4x.
Run from the repo root:   python scripts/sweep_icp.py
Saves docs/icp_sweep.png
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import numpy as np
import matplotlib.pyplot as plt
from pllmodel.loop import kvco_rad, phase_margin, design_filter

N, KVCO, ICP, FC, PM = 150, kvco_rad(100e6), 100e-6, 500e3, 60.0
R, C1, C2 = design_filter(FC, PM, ICP, KVCO, N)

scale = np.logspace(np.log10(0.5), np.log10(4), 25)
fcs, pms = [], []
for k in scale:
    fc, pm = phase_margin(k * ICP, KVCO, N, R, C1, C2)
    fcs.append(fc)
    pms.append(pm)
fcs, pms = np.array(fcs), np.array(pms)
:q
uuu
i2 = np.argmin(abs(scale - 2))
print(f"Icp x{scale[i2]:.2f}: fc = {fcs[i2]/1e3:.0f} kHz ({fcs[i2]/FC:.2f}x), PM = {pms[i2]:.1f} deg")

fig, ax1 = plt.subplots(figsize=(7, 4))
ax1.semilogx(scale, fcs / 1e3, "o-", label="fc")
ax1.set_xlabel("Icp / Icp,nominal")
ax1.set_ylabel("Crossover fc (kHz)")
ax1.grid(True, which="both", alpha=0.3)
ax2 = ax1.twinx()
ax2.semilogx(scale, pms, "s-", color="tab:red", label="PM")
ax2.set_ylabel("Phase margin (deg)", color="tab:red")
ax1.set_title("Fixed loop filter, scaled Icp: fc and PM")
fig.tight_layout()
out = pathlib.Path(__file__).resolve().parents[1] / "docs" / "icp_sweep.png"
fig.savefig(out, dpi=150)
print(f"saved {out}")
