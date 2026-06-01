Tugas Kecerdasan Buatan - Ant Colony Optimization (ACO)
Traveling Salesman Problem pada Gambar 1
========================================================

Soal:
Cari rute dari titik H ke titik D yang harus melewati titik #,
menggunakan algoritma Ant Colony Optimization (ACO).


Penjelasan singkat:
Graph di gambar 1 sifatnya sparse (nggak semua titik nyambung
langsung). Jadi sebelum ACO dijalanin, jarak antar titik dihitung
dulu pakai shortest path (Floyd-Warshall) biar jadi matriks jarak
lengkap. Setelah itu ACO nyari urutan kunjungan titik dari H ke D
dengan total jarak paling kecil. Karena ini TSP, semua titik
dikunjungi sehingga titik # otomatis ikut dilewati.


Cara kerja ACO (singkatnya):
- Tiap "semut" bikin rute mulai dari H, milih titik berikutnya
  secara probabilistik berdasarkan feromon dan jarak (titik yang
  lebih dekat + feromonnya banyak, peluang dipilih lebih besar).
- Setelah semua semut jalan, feromon menguap lalu diperkuat di
  jalur yang lebih pendek. Lama-lama semut ngumpul ke rute terbaik.


Hasil:
Program menampilkan DUA tafsir hasil (lihat bagian Analisis):
[1] TSP penuh (kunjungi semua titik):
    H -> E -> G -> F -> C -> # -> A -> B -> D   = 36  (dicek brute force, optimal)
[2] Shortest path H->D lewat # (A & B tidak wajib):
    H -> G -> # -> C -> F -> E -> D             = 23


Analisis (kenapa ada 2 jawaban):
Graph Gambar 1 ini ternyata bukan TSP biasa. Titik A, B, dan F
masing-masing CUMA nyambung lewat C. Akibatnya, rute yang mengunjungi
semua titik tepat satu kali (Hamiltonian path) dari H ke D itu MUSTAHIL
secara matematis. Jadi soalnya bisa dibaca dua cara:

- Kalau dianggap "TSP" (kunjungi semua titik), karena nggak bisa lewat
  tiap titik sekali, dipakai jarak terpendek antar titik (Floyd-Warshall).
  Konsekuensinya beberapa titik (E, C, #) terpaksa dilewati dua kali.
  Hasil = 36.

- Kalau dibaca literal "cari rute dari H ke D yang harus melewati #",
  maka A dan B tidak wajib dikunjungi. Hasilnya jalur terpendek biasa
  H->D yang lewat # = 23. Menariknya titik # ditandai khusus (bukan
  huruf) seakan jadi satu-satunya titik yang wajib.

Catatan soal ACO: ACO selalu konvergen ke rute terpendek, tapi
"terpendek dari kumpulan rute mana" tergantung aturan yang dikasih ke
semut. Kalau semut diwajibkan kunjungi semua titik -> ketemu 36. Kalau
semut bebas asal lewat # -> ketemu 23. Jadi 36 vs 23 bukan soal ACO
benar/salah, tapi soal masalah mana yang diselesaikan.


Cara jalanin:
1. Pastikan Python sudah terinstall.
2. Install matplotlib buat visualisasi:  pip install matplotlib
3. Jalanin solver:                       python aco.py
4. (opsional) bikin gambar rute:         python visualize.py


File:
- graph.py      : data graph gambar 1 + Floyd-Warshall
- aco.py        : algoritma ACO + verifikasi brute force (file utama)
- visualize.py  : gambar graph & rute terbaik (hasil_rute.png)
- gambar1.jpg   : soal (gambar 1)
