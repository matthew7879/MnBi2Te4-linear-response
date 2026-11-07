import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
mpl.rcdefaults()

mpl.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Times New Roman"],

    "text.latex.preamble": r"""
    \usepackage{amsmath}
    \usepackage{amssymb}
    """,

    "axes.labelsize": 25,
    "xtick.labelsize": 20,
    "ytick.labelsize": 20,
})

# ============================================================
# Load file
#
# columns:
# ell   ell'   Re_chi_nm   Im_chi_nm   Abs_chi_nm
# ============================================================

data = np.loadtxt("chi_layer_resolved.dat")

ell    = data[:, 0].astype(int)
ellp   = data[:, 1].astype(int)
chi_re = data[:, 2]

# ============================================================
# Build matrix chi_{ell ell'}
#
# first index  ell  = row    = y-axis
# second index ell' = column = x-axis
# ============================================================

layers = np.arange(1, 12)

chi = np.zeros((11, 11))

for l, lp, value in zip(ell, ellp, chi_re):
    chi[l - 1, lp - 1] = value

# ============================================================
# Plot
# ============================================================

fig, ax = plt.subplots(figsize=(7, 6.5))

edges = np.arange(0.5, 12.5, 1)

im = ax.pcolormesh(
    edges,
    edges,
    chi,
    shading="flat",
    cmap="viridis",
    edgecolors="white",
    linewidth=0.5
)

ax.set_aspect("equal")

# Matrix convention:
# horizontal = column index ell'
# vertical   = row index ell
ax.set_xlabel(r"$\ell'$")
ax.set_ylabel(r"$\ell$")

ax.set_xticks(layers)
ax.set_yticks(layers)

ax.set_xlim(0.5, 11.5)
ax.set_ylim(0.5, 11.5)


divider = make_axes_locatable(ax)

cax = divider.append_axes(
    "right",
    size="4%",
    pad=0.12
)

cbar = fig.colorbar(
    im,
    cax=cax
)

cbar.set_label(
    r"$\mathcal{R}\,\chi^{xx}_{\ell\ell'}(0)$ (nm)",
    fontsize=22
)

cbar.ax.tick_params(labelsize=18)

plt.tight_layout()

plt.savefig(
    "chi_layer_heatmap.pdf",
    bbox_inches="tight",
    dpi=600
)

plt.savefig(
    "chi_layer_heatmap.png",
    bbox_inches="tight",
    dpi=600
)

plt.show()
