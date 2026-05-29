"""
visualize.py
------------
Gambar graph "Gambar 1" beserta rute terbaik hasil ACO, lalu simpan
ke file 'hasil_rute.png'. Membutuhkan matplotlib.
"""

from __future__ import annotations

import matplotlib
matplotlib.use("Agg")  # backend non-interaktif (aman tanpa display)
import matplotlib.pyplot as plt

from aco import ACOParams, AntColonyTSP
from graph import COORDS, EDGES


def main() -> None:
    solver = AntColonyTSP(start="H", end="D", params=ACOParams())
    result = solver.run()
    walk = result.walk

    fig, ax = plt.subplots(figsize=(10, 5))

    # Gambar semua edge graph (abu-abu) + label bobot.
    for u, v, w in EDGES:
        x1, y1 = COORDS[u]
        x2, y2 = COORDS[v]
        ax.plot([x1, x2], [y1, y2], color="#bbbbbb", lw=2, zorder=1)
        ax.text((x1 + x2) / 2, (y1 + y2) / 2, str(w),
                fontsize=10, color="#444444",
                ha="center", va="center",
                bbox=dict(boxstyle="round,pad=0.1", fc="white", ec="none"))

    # Tandai rute terbaik (jalur fisik) dengan garis tebal berwarna.
    for a, b in zip(walk, walk[1:]):
        x1, y1 = COORDS[a]
        x2, y2 = COORDS[b]
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-|>", color="#e8590c",
                                    lw=3, shrinkA=14, shrinkB=14),
                    zorder=2)

    # Gambar simpul.
    for n, (x, y) in COORDS.items():
        is_endpoint = n in (solver.start, solver.end)
        is_hash = n == "#"
        color = "#c0392b" if is_hash else ("#2f9e44" if is_endpoint else "#6741d9")
        ax.scatter([x], [y], s=900, color=color, zorder=3, edgecolors="white", linewidths=2)
        ax.text(x, y, n, color="white", fontsize=13, fontweight="bold",
                ha="center", va="center", zorder=4)

    title = (f"Rute ACO: {' -> '.join(result.tour)}  |  Total jarak = {result.length:.0f}")
    ax.set_title(title, fontsize=12)
    ax.axis("off")
    fig.tight_layout()
    fig.savefig("hasil_rute.png", dpi=130)
    print("Tersimpan: hasil_rute.png")
    print(f"Rute  : {' -> '.join(result.tour)}  (jarak {result.length:.0f})")
    print(f"Jalur : {' -> '.join(walk)}")


if __name__ == "__main__":
    main()
