"""
graph.py
Data graph Gambar 1 (titik, garis penghubung, sama bobotnya) buat
tugas TSP pakai Ant Colony Optimization.

Di Gambar 1 nggak semua titik nyambung langsung, jadi di sini ada
fungsi buat ngitung jarak terdekat dari tiap titik ke titik lain
dulu, biar nanti ACO tau jaraknya.
"""

from __future__ import annotations

import math
from typing import Dict, List, Tuple

# Semua titik yang ada di Gambar 1.
NODES: List[str] = ["#", "A", "B", "C", "D", "E", "F", "G", "H"]

# Garis penghubung antar titik + bobotnya, dicatat dari Gambar 1.
EDGES: List[Tuple[str, str, int]] = [
    ("#", "A", 3),
    ("#", "C", 2),
    ("#", "G", 5),
    ("A", "C", 6),
    ("B", "C", 9),
    ("B", "D", 8),
    ("C", "F", 4),
    ("D", "E", 7),
    ("D", "H", 9),
    ("E", "F", 2),
    ("E", "G", 1),
    ("E", "H", 1),
    ("G", "H", 3),
]

# Posisi (x, y) tiap titik, cuma dipakai pas bikin gambar biar
# tata letaknya mirip Gambar 1.
COORDS: Dict[str, Tuple[float, float]] = {
    "#": (2.1, 3.0),
    "G": (6.2, 3.0),
    "A": (0.4, 2.0),
    "C": (1.9, 1.6),
    "F": (3.5, 2.3),
    "E": (4.8, 1.7),
    "B": (0.8, 0.5),
    "D": (3.25, 0.9),
    "H": (6.0, 0.4),
}


def adjacency():
    """Bikin daftar tetangga tiap titik dari EDGES (dicatat dua arah)."""
    adj = {n: {} for n in NODES}
    for u, v, w in EDGES:
        adj[u][v] = w
        adj[v][u] = w
    return adj


def hitung_jarak_terdekat():
    """
    Hitung jarak paling pendek dari tiap titik ke semua titik lain.
    Idenya: buat tiap pasang titik, dicoba lewat titik perantara,
    kalau ada yang lebih pendek dipakai.

    Ngembaliin 2 hal:
      dist[u][v] = jarak terdekat dari u ke v
      nxt[u][v]  = titik berikutnya kalau mau jalan dari u ke v
                   (dipakai buat nyusun jalur aslinya nanti)
    """
    adj = adjacency()
    dist = {u: {v: math.inf for v in NODES} for u in NODES}
    nxt = {u: {v: None for v in NODES} for u in NODES}

    # jarak titik ke dirinya sendiri = 0
    for u in NODES:
        dist[u][u] = 0.0
        nxt[u][u] = u
    # isi jarak yang nyambung langsung
    for u in NODES:
        for v, w in adj[u].items():
            dist[u][v] = float(w)
            nxt[u][v] = v

    # coba tiap titik k sebagai perantara, update kalau lebih pendek
    for k in NODES:
        for i in NODES:
            for j in NODES:
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    nxt[i][j] = nxt[i][k]
    return dist, nxt


def reconstruct_path(u, v, nxt):
    """Susun jalur asli dari u ke v pakai tabel nxt."""
    if nxt[u][v] is None:
        return []
    path = [u]
    while u != v:
        u = nxt[u][v]
        path.append(u)
    return path


def expand_tour(tour, nxt):
    """
    Ubah urutan titik (tour) jadi jalur asli yang beneran lewat garis
    di graph. Soalnya kadang dua titik berurutan di tour nggak nyambung
    langsung, jadi harus lewat titik lain dulu.
    """
    if not tour:
        return []
    walk = [tour[0]]
    for a, b in zip(tour, tour[1:]):
        seg = reconstruct_path(a, b, nxt)
        walk.extend(seg[1:])  # titik sambungannya jangan kehitung dobel
    return walk


if __name__ == "__main__":
    # buat ngecek jarak antar titik
    dist, nxt = hitung_jarak_terdekat()
    print("Jarak terdekat antar titik:")
    print("    " + "".join(f"{n:>5}" for n in NODES))
    for u in NODES:
        row = "".join(f"{dist[u][v]:>5.0f}" for v in NODES)
        print(f"{u:>3} {row}")
