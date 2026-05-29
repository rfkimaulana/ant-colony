"""
graph.py
--------
Definisi graph "Gambar 1" untuk tugas Traveling Salesman Problem (TSP)
dengan Ant Colony Optimization (ACO).

Graph aslinya bersifat sparse (tidak semua titik terhubung langsung),
sehingga jarak antar-titik dihitung dengan algoritma shortest-path
(Floyd-Warshall). Hasilnya berupa matriks jarak lengkap + tabel
"next-hop" untuk merekonstruksi jalur fisik antar dua titik.
"""

from __future__ import annotations

import math
from typing import Dict, List, Tuple

# Daftar simpul (node) pada Gambar 1.
NODES: List[str] = ["#", "A", "B", "C", "D", "E", "F", "G", "H"]

# Daftar sisi (edge) beserta bobotnya, dibaca langsung dari Gambar 1.
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

# Koordinat (x, y) untuk visualisasi, mendekati tata letak pada Gambar 1.
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


def adjacency() -> Dict[str, Dict[str, int]]:
    """Bangun adjacency list (graph tak-berarah) dari EDGES."""
    adj: Dict[str, Dict[str, int]] = {n: {} for n in NODES}
    for u, v, w in EDGES:
        adj[u][v] = w
        adj[v][u] = w
    return adj


def floyd_warshall() -> Tuple[Dict[str, Dict[str, float]], Dict[str, Dict[str, str | None]]]:
    """
    Hitung jarak terpendek antar semua pasang titik (Floyd-Warshall).

    Returns:
        dist: dist[u][v] = panjang jalur terpendek u->v.
        nxt:  nxt[u][v]  = titik berikutnya pada jalur terpendek u->v
              (untuk rekonstruksi jalur fisik).
    """
    adj = adjacency()
    dist: Dict[str, Dict[str, float]] = {
        u: {v: math.inf for v in NODES} for u in NODES
    }
    nxt: Dict[str, Dict[str, str | None]] = {
        u: {v: None for v in NODES} for u in NODES
    }

    for u in NODES:
        dist[u][u] = 0.0
        nxt[u][u] = u
    for u in NODES:
        for v, w in adj[u].items():
            dist[u][v] = float(w)
            nxt[u][v] = v

    for k in NODES:
        for i in NODES:
            for j in NODES:
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    nxt[i][j] = nxt[i][k]
    return dist, nxt


def reconstruct_path(u: str, v: str, nxt: Dict[str, Dict[str, str | None]]) -> List[str]:
    """Rekonstruksi jalur fisik terpendek dari u ke v menggunakan tabel next-hop."""
    if nxt[u][v] is None:
        return []
    path = [u]
    while u != v:
        u = nxt[u][v]  # type: ignore[assignment]
        path.append(u)
    return path


def expand_tour(tour: List[str], nxt: Dict[str, Dict[str, str | None]]) -> List[str]:
    """
    Ubah urutan kunjungan titik (tour) menjadi jalur fisik lengkap
    edge-per-edge di graph asli.
    """
    if not tour:
        return []
    walk: List[str] = [tour[0]]
    for a, b in zip(tour, tour[1:]):
        seg = reconstruct_path(a, b, nxt)
        walk.extend(seg[1:])  # hindari duplikasi titik sambungan
    return walk


if __name__ == "__main__":
    dist, nxt = floyd_warshall()
    print("Matriks jarak terpendek antar titik:")
    header = "    " + "".join(f"{n:>5}" for n in NODES)
    print(header)
    for u in NODES:
        row = "".join(f"{dist[u][v]:>5.0f}" for v in NODES)
        print(f"{u:>3} {row}")
