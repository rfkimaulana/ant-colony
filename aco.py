"""
aco.py
------
Penyelesaian Traveling Salesman Problem (TSP) dengan Ant Colony
Optimization (ACO) untuk graph "Gambar 1".

Kasus: cari rute terpendek yang BERANGKAT dari titik H, BERAKHIR di
titik D, dan WAJIB melewati titik '#'. Karena ini TSP, rute harus
mengunjungi SELURUH titik tepat satu kali (sehingga '#' otomatis
ikut dilalui).

Karena graph bersifat sparse, jarak antar-titik memakai jarak
terpendek (Floyd-Warshall). Rute hasil ACO kemudian dijabarkan
kembali menjadi jalur fisik edge-per-edge pada graph asli.

Referensi algoritma:
- M. Dorigo, "Ant Colony Optimization", aturan transisi probabilistik
  dan pembaruan feromon dengan penguapan (evaporation).
- Paper tugas: "Solving Traveling Salesman Problem Using Ant Colony
  Optimization Algorithm".
"""

from __future__ import annotations

import itertools
import random
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

from graph import NODES, adjacency, expand_tour, floyd_warshall


@dataclass
class ACOParams:
    n_ants: int = 20          # jumlah semut per iterasi
    n_iterations: int = 200   # jumlah iterasi
    alpha: float = 1.0        # bobot pengaruh feromon
    beta: float = 3.0         # bobot pengaruh heuristik (1/jarak)
    rho: float = 0.5          # laju penguapan feromon
    q: float = 100.0          # konstanta deposit feromon
    tau0: float = 1.0         # feromon awal
    seed: int = 42            # seed RNG agar hasil reproducible


@dataclass
class ACOResult:
    tour: List[str]                 # urutan kunjungan titik (H ... D)
    length: float                   # total jarak rute
    walk: List[str]                 # jalur fisik edge-per-edge
    history: List[float] = field(default_factory=list)  # jarak terbaik tiap iterasi


class AntColonyTSP:
    """ACO untuk TSP open-path dengan titik awal & akhir tetap."""

    def __init__(self, start: str = "H", end: str = "D", params: ACOParams | None = None):
        self.start = start
        self.end = end
        self.params = params or ACOParams()
        self.dist, self.nxt = floyd_warshall()

        # Titik perantara yang harus dikunjungi di antara start dan end.
        self.intermediates = [n for n in NODES if n not in (start, end)]

        # Inisialisasi feromon pada graph lengkap (matriks jarak).
        self.tau: Dict[str, Dict[str, float]] = {
            u: {v: self.params.tau0 for v in NODES} for u in NODES
        }
        self.rng = random.Random(self.params.seed)

    # ----------------------------- inti ACO ----------------------------- #
    def _eta(self, u: str, v: str) -> float:
        """Nilai heuristik = 1 / jarak (semakin dekat semakin menarik)."""
        d = self.dist[u][v]
        return 1.0 / d if d > 0 else 0.0

    def _pick_next(self, current: str, candidates: List[str]) -> str:
        """Pilih titik berikutnya secara probabilistik (aturan transisi ACO)."""
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

    def _build_tour(self) -> Tuple[List[str], float]:
        """Satu semut membangun rute: start -> semua perantara -> end."""
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

    def _tour_length(self, tour: List[str]) -> float:
        return sum(self.dist[a][b] for a, b in zip(tour, tour[1:]))

    def _update_pheromone(self, ant_tours: List[Tuple[List[str], float]]) -> None:
        # Penguapan.
        for u in NODES:
            for v in NODES:
                self.tau[u][v] *= (1.0 - self.params.rho)
        # Deposit oleh tiap semut, berbanding terbalik dengan panjang rute.
        for tour, length in ant_tours:
            if length <= 0:
                continue
            deposit = self.params.q / length
            for a, b in zip(tour, tour[1:]):
                self.tau[a][b] += deposit
                self.tau[b][a] += deposit

    def run(self) -> ACOResult:
        best_tour: List[str] = []
        best_len = float("inf")
        history: List[float] = []

        for _ in range(self.params.n_iterations):
            ant_tours = [self._build_tour() for _ in range(self.params.n_ants)]
            for tour, length in ant_tours:
                if length < best_len:
                    best_len, best_tour = length, tour
            self._update_pheromone(ant_tours)
            # Reinforcement elitist: rute terbaik global diperkuat.
            if best_tour:
                deposit = self.params.q / best_len
                for a, b in zip(best_tour, best_tour[1:]):
                    self.tau[a][b] += deposit
                    self.tau[b][a] += deposit
            history.append(best_len)

        walk = expand_tour(best_tour, self.nxt)
        return ACOResult(tour=best_tour, length=best_len, walk=walk, history=history)

    # --------------------------- verifikasi ---------------------------- #
    def brute_force_optimum(self) -> Tuple[List[str], float]:
        """Cari solusi optimal eksak via brute force (untuk verifikasi)."""
        best_tour: List[str] = []
        best_len = float("inf")
        for perm in itertools.permutations(self.intermediates):
            tour = [self.start, *perm, self.end]
            length = self._tour_length(tour)
            if length < best_len:
                best_len, best_tour = length, tour
        return best_tour, best_len


def shortest_path_via_waypoint(start: str, end: str, waypoint: str) -> Tuple[List[str], float]:
    """
    Cari jalur SEDERHANA terpendek (tanpa mengunjungi titik dua kali)
    dari start ke end yang wajib melewati waypoint, memakai sisi ASLI graph.

    Dipakai untuk interpretasi kedua: "cari rute H->D yang lewat # saja"
    (titik A & B tidak wajib). Pencarian eksak via DFS, aman karena graph kecil.
    """
    adj = adjacency()
    best_len = float("inf")
    best_path: List[str] = []

    def dfs(node: str, visited: set, path: List[str], cost: float) -> None:
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


def main() -> None:
    print("=" * 64)
    print("  ANT COLONY OPTIMIZATION - TSP (Gambar 1)")
    print("  Rute dari H ke D, wajib melewati '#'")
    print("=" * 64)

    # --- Tafsir 1: TSP PENUH (kunjungi SEMUA titik) ---
    solver = AntColonyTSP(start="H", end="D", params=ACOParams())
    result = solver.run()
    bf_tour, bf_len = solver.brute_force_optimum()
    status = "OPTIMAL" if abs(result.length - bf_len) < 1e-9 else "BELUM OPTIMAL"

    print("\n[1] TSP PENUH - kunjungi SEMUA titik (# otomatis dilewati)")
    print(f"    Rute (urutan titik)  : {' -> '.join(result.tour)}")
    print(f"    Jalur fisik (edge)   : {' -> '.join(result.walk)}")
    print(f"    Total jarak (ACO)    : {result.length:.0f}")
    print(f"    Verifikasi bruteforce: {bf_len:.0f}  -> {status}")

    # --- Tafsir 2: shortest path H->D lewat # (A & B tidak wajib) ---
    sp_path, sp_len = shortest_path_via_waypoint("H", "D", "#")
    print("\n[2] SHORTEST PATH - dari H ke D wajib lewat # (A & B TIDAK wajib)")
    print(f"    Rute                 : {' -> '.join(sp_path)}")
    print(f"    Total jarak          : {sp_len:.0f}")

    print("\n" + "-" * 64)
    print("Catatan: struktur graph Gambar 1 membuat Hamiltonian path murni")
    print("H->D mustahil (A, B, F hanya terhubung lewat C). Karena itu ada")
    print("dua tafsir: 36 (TSP, kunjungi semua) atau 23 (jalur terpendek")
    print("H->D lewat # saja). Penjelasan ada di readme.txt bagian Analisis.")


if __name__ == "__main__":
    main()
