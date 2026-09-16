# 📱💻 TechMate

Sebuah platform web berbasis komunitas untuk mendukung gaya hidup berkelanjutan (*Sustainable Living*) melalui pencegahan limbah elektronik (*E-Waste Prevention*). Platform ini membantu mahasiswa dan masyarakat cerdas dalam memilih, merawat, dan memperpanjang masa pakai gadget (HP, Laptop, Tablet) melalui filter kebutuhan tepat sasaran, direktori perbaikan mandiri, forum komunitas, dan jual-beli gadget seken.

---

## 1. Latar Belakang & Deskripsi Masalah 🔍

Limbah elektronik (*e-waste*) merupakan salah satu kategori limbah dengan pertumbuhan paling pesat di dunia. Di kalangan mahasiswa dan masyarakat umum, pergantian perangkat elektronik sering kali terjadi secara prematur akibat:
1. **Ketidaksesuaian Pembelian**: Pengguna membeli perangkat yang spesifikasinya kurang atau terlalu berlebihan karena bingung membaca istilah teknis.
2. **Ketiadaan Panduan Kerusakan Ringan**: Masalah sepele (seperti baterai bocor atau sistem lambat) langsung memicu keputusan membuang/mengganti perangkat baru ketimbang melakukan servis atau peningkatan komponen (*upgrade*).
3. **Minimnya Sirkulasi Gadget Bekas Terpercaya**: Sulitnya menemukan wadah jual-beli perangkat *second-hand* lokal yang berorientasi pada transparansi kondisi barang.

Proyek ini hadir di dengan tema **Sustainable Living (Sub-tema: Waste Management & Conscious Shopping)** untuk mempromosikan prinsip ekonomi sirkular pada produk elektronik konsumen: *Choose Right, Fix First, Pass It On*.

---

## 2. Peran Pengguna (*User Roles*) 👥

Aplikasi membagi hak akses ke dalam 2 kategori:

1. **Pengguna Belum Login (*Guest / Public*)**:
   - Menjelajah katalog spesifikasi perangkat (HP, Laptop, Tablet).
   - Menggunakan fitur filter kebutuhan (berdasarkan harga, kebutuhan aplikasi, dan batas spesifikasi).
   - Membaca artikel diagnosis pada modul *Troubleshooting*.
   - Melihat forum diskusi tanya-jawab dan ulasan komunitas.
   - Melihat daftar listing gadget bekas di marketplace.

2. **Pengguna Terotentikasi (*Authenticated User*)**:
   - Memberikan rating dan ulasan perangkat (*Review*).
   - Membuat *thread* pertanyaan baru atau menjawab pertanyaan di forum komunitas.
   - Mengunggah postingan penjualan gadget bekas di marketplace (termasuk foto kondisi fisik dan titik lokasi COD).
   - Menyimpan perangkat incaran ke daftar favorit (*Watchlist*).

---

## 3. Pemakaian API (Public & Mungkin Mock API) 🌐

API yang akan dipakai dalam aplikasi ini, tapi mungkin akan bertambah:

1. **Public Mobile Specs API**:
   - **Sumber**: Phone Specifications API seperti [phone-specs-api](https://github.com/azharimm/phone-specs-api) atau [gsmarena-scraper](https://github.com/dbeley/gsmarena-scraper)(API berdasarkan GSMArena).
   - **Kegunaan**: Mengambil data dinamis merek, model, spesifikasi baterai, tipe layar, dan tahun rilis smartphone/tablet.
2. **Laptop API**:
   - Untuk laptop belum ketemu API yang benar-benar khusus, paling ada [techspecs.io](https://developer.techspecs.io) (berisi banyak perangkat seperti hp laptop) atau [noteb](https://noteb.com/?public/api.php). Dan terdapat batasan waktu pada API ini, jadi belum tentu.
3. **Search API**
    - COMING SOON

---

##  4. Daftar Modul Rencana & Pembagian Tugas 📝



| No | Nama Modul | Tanggung Jawab & Deskripsi Fitur | Anggota Penanggung Jawab |
| :---: | :--- | :--- | :--- |
| **1** | **Authentication & User Profile Management** | - Registrasi, login, logout, dan manajemen sesi berbasis otentikasi.<br>- Halaman profil pengguna (menampilkan riwayat listing barang bekas, reputasi komunitas, dan perangkat tersimpan).<br>- Pengaturan hak akses (middleware/guard) antara Guest dan Registered User. | **Vebian** |
| **2** | **Device Explorer** | - Konsumsi API spesifikasi HP/Laptop/Tablet.<br>- Filter pencarian multi-parameter: rentang harga, spesifikasi minimal (RAM, CPU, Storage), dan preset kebutuhan komputasi (misal: *Coding/VM*, *Desain*, *Harian*).<br>- Halaman detail perbandingan spesifikasi gadget. | **Ahmad** |
| **3** | **Community Forum & Reviews** | - Sistem rating dan ulasan perangkat dengan fokus durabilitas (apakah awet dipakai >2 tahun).<br>- Forum diskusi tanya-jawab (Q&A) seputar rekomendasi dan troubleshooting gadget.<br>- Fitur upvote/like dan komentar balasan pada thread forum. | **Rasya** |
| **4** | **Troubleshooting** | - Modul pencarian dan penanganan gejala kerusakan umum (baterai cepat habis, overheating, layar bergaris).<br>- Edukasi kelayakan servis mandiri vs tukar tambah.<br>- Tautan cerdas yang menghubungkan artikel gejala kerusakan ke topik thread forum terkait. | **Naufal** |
| **5** | **Marketplace** | - Form pembuatan listing jual gadget bekas (kondisi baterai/fisik, kelengkapan, harga, area COD).<br>- Katalog penjelajahan bursa barang bekas dengan filter lokasi terdekat.<br>- Tombol integrasi kontak langsung ke penjual (*Direct WhatsApp link*). | **Raya** |

---

## Anggota

- **Ahmad Shanahan Zorya** - 2506541894
- **Muhammad Ghaisan Raya** - 2506624493
- **Muhammad Naufal Rizki Fadhlurrahman** - 2506623490
- **Rasya Al Hawari** - 2506534176
- **Vebian Francois Ariftya Manurung** - 2506543363