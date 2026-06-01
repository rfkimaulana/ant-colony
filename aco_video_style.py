"""
aco_video_style.py
------------------
Ant Colony Optimization (ACO) untuk Traveling Salesman Problem,
ditulis MENGIKUTI GAYA video YouTube materi tugas
(channel "Vamboi Creates" - ACO Using Python):

  - matriks jarak (d) di-HARDCODE,
  - pakai numpy + faktor pheromone^beta * visibility^alpha,
  - pemilihan kota via probabilitas kumulatif + bilangan acak R,
  - update feromon: evaporasi lalu deposit 1/cost,
  - OUTPUT hanya: rute semua semut + best path + cost.

Bedanya dengan video: kasus tugas ini OPEN-PATH dengan titik awal &
akhir TETAP -> berangkat dari H, berakhir di D, dan wajib melewati '#'
(otomatis terpenuhi karena semua titik dikunjungi). Matriks jarak
memakai jarak terpendek antar-titik pada graph "Gambar 1"
(hasil Floyd-Warshall) agar berbentuk matriks lengkap seperti di video.
"""

import numpy as np

# Label kota sesuai urutan baris/kolom matriks d.
# Indeks 0 = H (start), indeks 8 = D (end), sisanya titik perantara.
CITIES = ["H", "#", "A", "B", "C", "E", "F", "G", "D"]
START = 0   # H
END = 8     # D

# Matriks jarak antar-kota (HARDCODE), simetris.
# Diagonal diisi angka besar (INF) agar visibility = 1/d -> 0.
INF = 1e9
d = np.array([
    # H     #     A     B     C     E     F     G     D
    [INF,   7,   10,   16,    7,    1,    3,    2,    8],  # H
    [  7, INF,    3,   11,    2,    6,    6,    5,   13],  # #
    [ 10,   3,  INF,   14,    5,    9,    9,    8,   16],  # A
    [ 16,  11,   14,  INF,    9,   15,   13,   16,    8],  # B
    [  7,   2,    5,    9,  INF,    6,    4,    7,   13],  # C
    [  1,   6,    9,   15,    6,  INF,    2,    1,    7],  # E
    [  3,   6,    9,   13,    4,    2,  INF,    3,    9],  # F
    [  2,   5,    8,   16,    7,    1,    3,  INF,    8],  # G
    [  8,  13,   16,    8,   13,    7,    9,    8,  INF],  # D
], dtype=float)

# ----------------------------- parameter ----------------------------- #
iteration = 100      # jumlah iterasi
n_ants = 20          # jumlah semut
n_citys = len(CITIES)

e = 0.5              # laju penguapan (evaporation rate)
alpha = 1            # bobot feromon
beta = 2             # bobot visibility

np.random.seed(42)   # agar hasil reproducible

# visibility = 1 / jarak (semakin dekat semakin terlihat).
visibility = 1.0 / d
visibility[visibility == 1.0 / INF] = 0.0

# feromon awal sama rata di semua sisi.
pheromone = 0.1 * np.ones((n_citys, n_citys))

# Titik perantara yang harus dikunjungi di antara START dan END.
intermediates = [c for c in range(n_citys) if c not in (START, END)]
n_inter = len(intermediates)

best_route_global = None
best_cost_global = float("inf")
last_routes = None  # rute semua semut pada iterasi terakhir

for ite in range(iteration):
    # rute tiap semut: kolom 0 = START(H), kolom terakhir = END(D).
    rute = np.zeros((n_ants, n_citys), dtype=int)
    rute[:, 0] = START
    rute[:, -1] = END

    for i in range(n_ants):
        temp_vis = np.array(visibility)
        temp_vis[:, START] = 0.0   # START tidak dikunjungi ulang
        temp_vis[:, END] = 0.0     # END hanya di akhir, bukan perantara

        cur = START
        # Pilih (n_inter - 1) perantara secara probabilistik,
        # perantara terakhir diisi sisa (mengikuti trik di video).
        for j in range(n_inter - 1):
            temp_vis[:, cur] = 0.0
            p_feature = np.power(pheromone[cur, :], beta)
            v_feature = np.power(temp_vis[cur, :], alpha)
            combine = p_feature * v_feature

            total = np.sum(combine)
            probs = combine / total
            cum_prob = np.cumsum(probs)

            r = np.random.random_sample()
            nxt = int(np.nonzero(cum_prob > r)[0][0])
            rute[i, j + 1] = nxt
            cur = nxt

        # Perantara yang belum terpilih -> isi di posisi sebelum END.
        chosen = set(rute[i, : n_inter].tolist())
        left = list(set(intermediates) - chosen)[0]
        rute[i, n_inter] = left  # kolom sebelum END

    # ---- hitung cost tiap rute ---- #
    dist_cost = np.zeros(n_ants)
    for i in range(n_ants):
        s = 0.0
        for j in range(n_citys - 1):
            s += d[rute[i, j], rute[i, j + 1]]
        dist_cost[i] = s

    # ---- rute terbaik iterasi ini ---- #
    min_loc = int(np.argmin(dist_cost))
    if dist_cost[min_loc] < best_cost_global:
        best_cost_global = dist_cost[min_loc]
        best_route_global = rute[min_loc].copy()

    # ---- update feromon: evaporasi lalu deposit 1/cost ---- #
    pheromone = (1.0 - e) * pheromone
    for i in range(n_ants):
        dt = 1.0 / dist_cost[i]
        for j in range(n_citys - 1):
            pheromone[rute[i, j], rute[i, j + 1]] += dt

    last_routes = rute  # simpan untuk ditampilkan di akhir


def to_labels(idx_route):
    return " -> ".join(CITIES[c] for c in idx_route)


# ----------------------------- OUTPUT ----------------------------- #
# (mengikuti video: tampilkan rute semua semut + best path + cost)
print("Rute semua semut pada iterasi terakhir:")
for i in range(n_ants):
    print(f"  semut {i + 1:>2}: {to_labels(last_routes[i])}")

print("\nBest path :", to_labels(best_route_global))
print("Cost      :", f"{best_cost_global:.0f}")
