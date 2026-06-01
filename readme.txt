Tugas Kecerdasan Buatan - Ant Colony Optimization (ACO)
Traveling Salesman Problem pada Gambar 1
========================================================

Soal:
Cari rute dari titik H ke titik D yang harus melewati titik #,
menggunakan algoritma Ant Colony Optimization (ACO).


Penjelasan singkat:
Di gambar 1, nggak semua titik nyambung langsung satu sama lain.
Jadi sebelum ACO dijalanin, dihitung dulu jarak terdekat antar tiap
titik biar lengkap. Setelah itu ACO nyari urutan kunjungan titik dari
H ke D dengan total jarak paling kecil. Karena ini TSP, semua titik
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
semua titik tepat satu kali dari H ke D itu nggak mungkin dibuat.
Jadi soalnya bisa dibaca dua cara:

- Kalau dianggap "TSP" (kunjungi semua titik), karena nggak bisa lewat
  tiap titik sekali, dipakai jarak terdekat antar titik. Konsekuensinya
  beberapa titik (E, C, #) terpaksa dilewati dua kali. Hasil = 36.

- Kalau dibaca literal "cari rute dari H ke D yang harus melewati #",
  maka A dan B tidak wajib dikunjungi. Hasilnya jalur terpendek biasa
  H->D yang lewat # = 23. Menariknya titik # ditandai khusus (bukan
  huruf) seakan jadi satu-satunya titik yang wajib.

Catatan soal ACO: ACO selalu konvergen ke rute terpendek, tapi
"terpendek dari kumpulan rute mana" tergantung aturan yang dikasih ke
semut. Kalau semut diwajibkan kunjungi semua titik -> ketemu 36. Kalau
semut bebas asal lewat # -> ketemu 23. Jadi 36 vs 23 bukan soal ACO
benar/salah, tapi soal masalah mana yang diselesaikan.


Cara jalanin (Google Colab):
1. Buka Google Colab (colab.research.google.com), bikin notebook baru.
2. Upload file graph.py, aco.py, dan visualize.py.
   (klik ikon folder di panel kiri -> tombol Upload)
3. Di sebuah cell, ketik lalu jalankan:   !python aco.py
4. (opsional) buat gambar rute:           !python visualize.py
