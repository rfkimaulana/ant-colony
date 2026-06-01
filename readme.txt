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
Rute        : H -> E -> G -> F -> C -> # -> A -> B -> D
Total jarak : 36
Hasil ini udah dicek pakai brute force dan terbukti optimal.


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
