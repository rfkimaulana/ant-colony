# Naskah Video Demo — ACO untuk TSP (Gambar 1)

> Estimasi durasi: **4–6 menit**. Bahasa santai, tetap jelas.
> Kolom kiri = yang diucapkan, kolom kanan = yang ditampilkan di layar.

---

## 0. Persiapan sebelum rekam
- Buka **VS Code / editor** dengan folder project (`graph.py`, `aco.py`, `visualize.py`, `README.md`).
- Buka **terminal** di folder yang sama.
- Siapkan **Gambar 1** dan **hasil_rute.png** biar gampang ditampilkan.
- Tips: rekam layar pakai OBS / Screen Recorder bawaan, mic dinyalakan.

---

## 1. Pembukaan (0:00 – 0:30)

**Ucapan:**
> "Halo, assalamualaikum. Perkenalkan, saya Rifki Maulana. Di video ini saya mau
> demoin tugas Kecerdasan Buatan, yaitu nyelesaiin *Traveling Salesman Problem*
> pakai algoritma *Ant Colony Optimization* atau ACO, dengan Python.
> Soalnya: cari rute dari titik **H** ke titik **D**, dan wajib lewat titik **pagar** (`#`).
> Yuk langsung aja kita bahas."

**Layar:** Tampilkan slide judul / folder project / README bagian atas.

---

## 2. Jelasin soalnya (0:30 – 1:30)

**Ucapan:**
> "Jadi ini graph-nya, Gambar 1. Ada 9 titik: pagar, A, B, C, D, E, F, G, H.
> Tiap garis punya bobot, anggap aja itu jarak antar titik.
> Nah tugasnya itu kayak tukang pos: berangkat dari H, harus keliling lewatin
> semua titik, terus berakhir di D. Syarat tambahannya, titik pagar wajib dilewatin.
> Tujuannya satu: total jaraknya sependek mungkin."

**Layar:** Tampilkan `gambar1.jpg`, tunjuk titik H, D, dan `#` pakai kursor.

---

## 3. Sedikit soal logika kodenya (1:30 – 2:45)

**Ucapan:**
> "Sebelum jalanin, aku jelasin dikit logikanya. Masalahnya, graph ini nggak
> semua titik nyambung langsung. Ada titik kayak A, B, F yang cuma punya dua
> jalan, jadi kalau dipaksa lewat sekali-sekali doang malah nggak ada solusinya.
>
> Makanya aku pakai trik standar: pertama, hitung dulu jarak terpendek antar
> semua titik pakai **Floyd–Warshall** — ini ada di file `graph.py`.
> Habis itu baru si **semut-semut ACO** jalan di atas jarak itu."

**Layar:** Buka `graph.py`, scroll ke fungsi `floyd_warshall`.

**Ucapan (lanjut):**
> "Nah ini inti ACO-nya di `aco.py`. Idenya niru semut beneran:
> tiap semut bikin rute dari H, milih titik selanjutnya berdasarkan dua hal —
> **feromon** (jejak yang ditinggalin semut lain) dan **heuristik** yaitu satu
> per jarak, jadi yang deket lebih dipilih.
> Tiap putaran, feromon nguap dikit, terus rute yang paling pendek dapet
> feromon paling banyak. Lama-lama semua semut ngumpul ke rute terbaik."

**Layar:** Buka `aco.py`, tunjuk method `_pick_next` (rumus probabilitas) dan
`_update_pheromone` (penguapan + deposit).

---

## 4. Jalanin programnya (2:45 – 4:00)

**Ucapan:**
> "Oke sekarang kita running. Cukup ketik `python aco.py`."

**Layar:** Di terminal, ketik dan jalankan:
```bash
python aco.py
```

**Ucapan (sambil nunjuk output):**
> "Nih hasilnya. Rutenya: **H → E → G → F → C → pagar → A → B → D**.
> Total jaraknya **36**. Dan bener, titik pagar dilewatin.
>
> Yang keren, di bawah ada **verifikasi pakai brute force** — jadi aku cek semua
> kemungkinan urutan, ada 5.040 kombinasi, dan jarak optimalnya juga **36**.
> Artinya hasil ACO-nya **udah optimal**, bukan cuma kira-kira."

**Layar:** Highlight baris `Total jarak : 36` dan `Status hasil ACO : OPTIMAL`.

---

## 5. Tampilin visualisasinya (4:00 – 5:00)

**Ucapan:**
> "Biar lebih kebayang, aku juga bikin visualisasinya. Tinggal jalanin
> `python visualize.py`, nanti dia bikin gambar rutenya."

**Layar:** Jalankan:
```bash
python visualize.py
```
Lalu buka `hasil_rute.png`.

**Ucapan:**
> "Nah ini gambarnya. Garis abu-abu itu graph aslinya, yang oranye tebal itu
> rute pilihan si semut. Mulai dari H di kanan bawah, naik ke E, G, balik lewat
> F, ke C, mampir ke pagar, ke A, turun ke B, dan finish di D.
> Titik hijau itu start sama finish, titik merah itu pagar yang wajib dilewatin."

**Layar:** Tunjukkan `hasil_rute.png` full screen, telusuri rutenya pakai kursor.

---

## 6. Penutup (5:00 – 5:30)

**Ucapan:**
> "Jadi kesimpulannya, pakai Ant Colony Optimization kita berhasil nemuin rute
> terpendek dari H ke D yang lewat pagar, dengan total jarak 36, dan itu udah
> kebukti optimal.
> Semua source code-nya ada di GitHub, link-nya aku taro di deskripsi.
> Sekian demo dari saya, makasih udah nonton. Wassalamualaikum."

**Layar:** Tampilkan halaman GitHub repo (`github.com/rfkimaulana/ant-colony`)
dan README.

---

## Catatan tambahan (kalau ditanya dosen)
- **Kenapa ada titik yang dilewati dua kali di jalur fisik** (mis. `...E → G → E...`)?
  Karena jaraknya pakai *shortest path*, jadi pas dijabarin ke jalan asli, kadang
  lewat titik penghubung lagi. Total jaraknya tetap minimum.
- **Parameter ACO** bisa diubah di `ACOParams` (`aco.py`): jumlah semut, iterasi,
  alpha, beta, rho. Defaultnya udah cukup buat konvergen ke optimal.
- **Reproducible**: pakai `seed=42`, jadi hasilnya konsisten tiap dijalankan.
