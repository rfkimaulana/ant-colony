"""
aco.py
Nyelesaiin Traveling Salesman Problem (TSP) di graph Gambar 1 pakai
Ant Colony Optimization (ACO).

Soalnya: cari rute dari titik H ke titik D yang harus lewat titik '#'.
Karena ini TSP, semutnya disuruh ngunjungin semua titik, jadi '#'
pasti kelewat.

Karena di Gambar 1 nggak semua titik nyambung langsung, jaraknya
diambil dari jarak terdekat antar titik (dihitung di graph.py).
"""

from __future__ import annotations

import itertools
import random
from dataclasses import dataclass, field
from typing import List

from graph import NODES, adjacency, expand_tour, hitung_jarak_terdekat


@dataclass
class ACOParams:
    n_ants: int = 20          # jumlah semut tiap iterasi
    n_iterations: int = 200   # berapa kali diulang
    alpha: float = 1.0        # seberapa ngaruh feromon
    beta: float = 3.0         # seberapa ngaruh jarak (1/jarak)
    rho: float = 0.5          # seberapa cepat feromon nguap
    q: float = 100.0          # konstanta buat nambah feromon
    tau0: float = 1.0         # feromon awal
    seed: int = 42            # biar hasilnya tetap sama tiap dijalanin


@dataclass
class ACOResult:
    tour: List[str]                 # urutan titik yang dikunjungi (H ... D)
    length: float                   # total jaraknya
    walk: List[str]                 # jalur aslinya di graph
    history: List[float] = field(default_factory=list)  # jarak terbaik tiap iterasi


class AntColonyTSP:
    """ACO buat cari rute H ke D yang lewat semua titik."""

    def __init__(self, start="H", end="D", params=None):
        self.start = start
        self.end = end
        self.params = params or ACOParams()
        self.dist, self.nxt = hitung_jarak_terdekat()

        # titik-titik yang harus dikunjungi di antara H dan D
        self.intermediates = [n for n in NODES if n not in (start, end)]

        # feromon awal, semua sisi dikasih nilai sama
        self.tau = {u: {v: self.params.tau0 for v in NODES} for u in NODES}
        self.rng = random.Random(self.params.seed)

    def _eta(self, u, v):
        """Makin deket titiknya makin gede nilainya (1 / jarak)."""
        d = self.dist[u][v]
        return 1.0 / d if d > 0 else 0.0

    def _pick_next(self, current, candidates):
        """Pilih titik berikutnya secara acak tapi dibobotin feromon & jarak."""
        weights = []
        for v in candidates:
            tau = self.tau[current][v] ** self.params.alpha
            eta = self._eta(current, v) ** self.params.beta
            weights.append(tau * eta)
        total = sum(weights)
        if total <= 0:
            return self.rng.choice(candidates)
        r = self.rng.uniform(0, total)
        upto = 0.0
        for v, w in zip(candidates, weights):
            upto += w
            if upto >= r:
                return v
        return candidates[-1]

    def _build_tour(self):
        """Satu semut bikin rute: dari H, keliling semua titik, terus ke D."""
        tour = [self.start]
        unvisited = list(self.intermediates)
        current = self.start
        while unvisited:
            nxt = self._pick_next(current, unvisited)
            tour.append(nxt)
            unvisited.remove(nxt)
            current = nxt
        tour.append(self.end)
        return tour, self._tour_length(tour)

    def _tour_length(self, tour):
        return sum(self.dist[a][b] for a, b in zip(tour, tour[1:]))

    def _update_pheromone(self, ant_tours):
        # feromon nguap dulu
        for u in NODES:
            for v in NODES:
                self.tau[u][v] *= (1.0 - self.params.rho)
        # terus ditambah, rute yang lebih pendek dapet tambahan lebih banyak
        for tour, length in ant_tours:
            if length <= 0:
                continue
            tambah = self.params.q / length
            for a, b in zip(tour, tour[1:]):
                self.tau[a][b] += tambah
                self.tau[b][a] += tambah

    def run(self):
        best_tour = []
        best_len = float("inf")
        history = []

        for _ in range(self.params.n_iterations):
            ant_tours = [self._build_tour() for _ in range(self.params.n_ants)]
            for tour, length in ant_tours:
                if length < best_len:
                    best_len, best_tour = length, tour
            self._update_pheromone(ant_tours)
            # rute terbaik sejauh ini dikasih feromon ekstra biar makin kuat
            if best_tour:
                tambah = self.params.q / best_len
                for a, b in zip(best_tour, best_tour[1:]):
                    self.tau[a][b] += tambah
                    self.tau[b][a] += tambah
            history.append(best_len)

        walk = expand_tour(best_tour, self.nxt)
        return ACOResult(tour=best_tour, length=best_len, walk=walk, history=history)

    def brute_force_optimum(self):
        """Cek semua kemungkinan urutan, buat mastiin hasil ACO udah paling kecil."""
        best_tour = []
        best_len = float("inf")
        for perm in itertools.permutations(self.intermediates):
            tour = [self.start, *perm, self.end]
            length = self._tour_length(tour)
            if length < best_len:
                best_len, best_tour = length, tour
        return best_tour, best_len


def shortest_path_via_waypoint(start, end, waypoint):
    """
    Cari jalur terpendek dari start ke end yang harus lewat waypoint,
    tanpa ngunjungin titik yang sama dua kali, pakai garis asli di graph.

    Dipakai buat tafsir kedua: cari rute H->D yang cukup lewat # aja
    (titik A & B nggak wajib). Dicari dengan nyoba semua jalur (graph kecil).
    """
    adj = adjacency()
    best_len = float("inf")
    best_path = []

    def dfs(node, visited, path, cost):
        nonlocal best_len, best_path
        if cost >= best_len:
            return
        if node == end:
            if waypoint in path:
                best_len = cost
                best_path = list(path)
            return
        for nb, w in adj[node].items():
            if nb not in visited:
                visited.add(nb)
                path.append(nb)
                dfs(nb, visited, path, cost + w)
                path.pop()
                visited.remove(nb)

    dfs(start, {start}, [start], 0.0)
    return best_path, best_len


def main():
    print("=" * 64)
    print("  ANT COLONY OPTIMIZATION - TSP (Gambar 1)")
    print("  Rute dari H ke D, wajib melewati '#'")
    print("=" * 64)

    # --- Tafsir 1: kunjungi SEMUA titik ---
    solver = AntColonyTSP(start="H", end="D", params=ACOParams())
    result = solver.run()
    bf_tour, bf_len = solver.brute_force_optimum()
    status = "OPTIMAL" if abs(result.length - bf_len) < 1e-9 else "BELUM OPTIMAL"

    print("\n[1] TSP PENUH - kunjungi SEMUA titik (# otomatis dilewati)")
    print(f"    Rute (urutan titik)  : {' -> '.join(result.tour)}")
    print(f"    Jalur asli di graph  : {' -> '.join(result.walk)}")
    print(f"    Total jarak (ACO)    : {result.length:.0f}")
    print(f"    Dicek semua urutan   : {bf_len:.0f}  -> {status}")

    # --- Tafsir 2: cukup lewat # aja (A & B nggak wajib) ---
    sp_path, sp_len = shortest_path_via_waypoint("H", "D", "#")
    print("\n[2] SHORTEST PATH - dari H ke D wajib lewat # (A & B TIDAK wajib)")
    print(f"    Rute                 : {' -> '.join(sp_path)}")
    print(f"    Total jarak          : {sp_len:.0f}")

    print("\n" + "-" * 64)
    print("Catatan: di graph ini nggak ada rute yang bisa lewat tiap titik")
    print("tepat sekali dari H ke D (A, B, F cuma nyambung lewat C). Makanya")
    print("ada dua tafsir: 36 (kunjungi semua) atau 23 (cukup lewat # aja).")
    print("Penjelasan lengkap ada di readme.txt bagian Analisis.")


if __name__ == "__main__":
    main()
