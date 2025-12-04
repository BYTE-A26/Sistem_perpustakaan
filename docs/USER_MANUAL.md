# User Manual - Sistem Perpustakaan Digital

## 📖 Panduan Pengguna Lengkap

### 1. Getting Started

#### 1.1 Instalasi dan Setup

1. **Install Python 3.8+** dari https://www.python.org

2. **Clone/Download Project**
   ```
   Pastikan folder proyek ada di: c:\Users\ASUS\Documents\TUGAS\Proyek\Proyek
   ```

3. **Install Dependencies**
   ```bash
   cd c:\Users\ASUS\Documents\TUGAS\Proyek\Proyek
   pip install -r requirements.txt
   ```

4. **Jalankan Aplikasi**
   ```bash
   python main.py
   ```

### 2. Login & Registration

#### 2.1 Membuat Akun Baru (Register)

1. Klik tombol "Registrasi Member Baru" di layar login
2. Isi form dengan data berikut:
   - **Username**: Nama unik untuk login (min 1 karakter)
   - **Password**: Min 8 karakter (gunakan kombinasi huruf & angka)
   - **Nama Lengkap**: Nama lengkap Anda
   - **Email**: Email yang valid
   - **Nomor Telepon**: Nomor HP Anda
   - **Alamat**: Alamat lengkap
3. Klik tombol "Registrasi"
4. Setelah sukses, kembali ke layar login untuk login

#### 2.2 Login

1. Masukkan username Anda
2. Masukkan password
3. Klik tombol "Login"
4. Jika berhasil, Anda akan masuk ke menu utama

**Catatan Keamanan:**
- Jangan pernah bagikan password Anda
- Gunakan password yang kuat
- Logout sebelum meninggalkan komputer

### 3. Menu Utama

Setelah login, Anda akan melihat menu dengan opsi berbeda tergantung role Anda:

#### 3.1 Menu Common (Semua User)
- **Cari Buku**: Cari buku dengan berbagai kriteria
- **Lihat Daftar Buku**: Lihat semua buku yang tersedia
- **Buku Rekomendasi**: Lihat buku yang direkomendasikan
- **Lihat Transaksi Saya**: Lihat riwayat peminjaman

#### 3.2 Menu Librarian/Admin
- **Tambah Buku**: Menambah buku baru ke sistem
- **Kelola Buku**: Mengelola data buku yang ada
- **Proses Peminjaman**: Memproses peminjaman buku
- **Proses Pengembalian**: Memproses pengembalian buku
- **Kelola Reservasi**: Mengelola reservasi buku

#### 3.3 Menu Admin
- **Kelola User**: Mengelola akun pengguna
- **Statistik & Laporan**: Melihat statistik perpustakaan

#### 3.4 Menu Member
- **Ajukan Peminjaman**: Meminjam buku (dapat juga dari daftar buku)
- **Lihat Reservasi Saya**: Lihat reservasi buku
- **Beri Rating & Review**: Memberikan rating dan review buku

### 4. Operasi Umum

#### 4.1 Mencari Buku

1. Dari menu utama, klik "Cari Buku"
2. Isi kriteria pencarian:
   - **Judul**: Masukkan judul atau bagian dari judul (opsional)
   - **Author**: Masukkan nama pengarang (opsional)
   - **Kategori**: Masukkan kategori buku (opsional)
3. Klik tombol "Cari"
4. Hasil pencarian akan ditampilkan

**Cara menggunakan hasil:**
- Klik "Pinjam" untuk meminjam buku (jika tersedia)
- Klik "Lihat Detail" untuk informasi lengkap buku

#### 4.2 Meminjam Buku (Member)

**Cara 1: Dari daftar buku**
1. Klik "Lihat Daftar Buku"
2. Lihat tabel buku yang tersedia
3. Jika ada tombol "Pinjam", klik untuk meminjam

**Cara 2: Dari halaman detail**
1. Cari buku menggunakan "Cari Buku"
2. Klik "Lihat Detail" pada buku yang diinginkan
3. Jika tersedia, akan ada opsi untuk meminjam

**Durasi Peminjaman:**
- Default: 7 hari
- Librarian dapat menyesuaikan durasi

#### 4.3 Melihat Transaksi Saya

1. Dari menu utama, klik "Lihat Transaksi Saya"
2. Akan ditampilkan tabel dengan:
   - ID Transaksi
   - Tipe (Peminjaman/Pengembalian)
   - Nama Buku
   - Tanggal Transaksi
   - Deadline/Tanggal Kembali
   - Status (Aktif/Selesai)

#### 4.4 Memberikan Rating & Review (Member)

1. Dari menu utama, klik "Beri Rating & Review"
2. Masukkan Book ID buku yang ingin di-review
3. Pilih rating (1-5 bintang)
4. Tulis review/komentar tentang buku
5. Klik "Submit Review"

### 5. Operasi Librarian

#### 5.1 Menambah Buku Baru

1. Dari menu utama, klik "Tambah Buku"
2. Isi form berikut:
   - **Judul**: Judul buku
   - **Author**: Nama pengarang
   - **Publisher**: Penerbit
   - **ISBN**: Nomor ISBN buku
   - **Tahun Publikasi**: Tahun terbit
   - **Kategori**: Kategori buku (misal: Fiction, Programming, History)
   - **Lokasi**: Lokasi penyimpanan di perpustakaan (misal: Rak A1)
   - **Total Salinan**: Jumlah salinan yang ditambah
   - **Halaman**: Jumlah halaman
   - **Deskripsi**: Deskripsi/ringkasan buku
3. Klik "Tambah Buku"

#### 5.2 Mengelola Buku

1. Dari menu utama, klik "Kelola Buku"
2. Akan ditampilkan daftar semua buku
3. Lihat informasi: Book ID, Judul, Author, Kategori, Tersedia/Total, Rating

#### 5.3 Proses Peminjaman

1. Dari menu utama, klik "Proses Peminjaman"
2. Masukkan:
   - **User ID**: ID atau username pembaca
   - **Book ID**: ID buku yang akan dipinjam
3. Klik "Proses Peminjaman"
4. Sistem akan memberikan ID transaksi dan deadline

#### 5.4 Proses Pengembalian

1. Dari menu utama, klik "Proses Pengembalian"
2. Masukkan **Transaction ID** (dari proses peminjaman)
3. Klik "Proses Pengembalian"
4. Sistem akan:
   - Menandai transaksi sebagai selesai
   - Mengembalikan buku ke stok
   - Menghitung denda (jika terlambat)

#### 5.5 Mengelola Reservasi

1. Dari menu utama, klik "Kelola Reservasi"
2. Lihat daftar reservasi:
   - ID Reservasi
   - User ID yang mereservasi
   - Book ID yang dipesan
   - Tanggal reservasi
   - Status (Aktif/Siap/Dibatalkan)

### 6. Operasi Admin

#### 6.1 Mengelola User

1. Dari menu utama, klik "Kelola User"
2. Lihat daftar semua pengguna dengan:
   - Username
   - Nama Lengkap
   - Email
   - Role (Member/Librarian/Admin)
   - Status Aktif (Ya/Tidak)

#### 6.2 Melihat Statistik & Laporan

1. Dari menu utama, klik "Statistik & Laporan"
2. Lihat informasi:
   - **Total Buku**: Jumlah buku di sistem
   - **Buku Tersedia**: Jumlah buku yang dapat dipinjam
   - **Buku Dipinjam**: Jumlah buku yang sedang dipinjam
   - **Total Transaksi**: Jumlah transaksi yang telah dilakukan
   - **Total Denda**: Jumlah denda yang terkumpul
   - **Rating Rata-rata**: Rating buku secara keseluruhan
   - **Buku Paling Banyak Dipinjam**: Buku yang paling populer
   - **Kategori Paling Populer**: Kategori buku yang diminati

### 7. Fitur Khusus

#### 7.1 Sistem Rekomendasi

- Sistem otomatis merekomendasikan buku berdasarkan:
  - Buku yang sering dipinjam
  - Buku dengan rating tinggi
  - Hubungan antar buku (similar books)

#### 7.2 Reservasi Buku

- Jika buku tidak tersedia, member dapat mereservasi
- Reservasi berlaku selama 7 hari
- Ketika buku dikembalikan, member akan mendapat giliran

#### 7.3 Sistem Denda

- Denda dihitung otomatis jika buku dikembalikan terlambat
- Tarif denda: Rp 5.000 per hari keterlambatan
- Denda akan ditampilkan saat pengembalian

#### 7.4 Rating & Review

- Member dapat memberi rating 1-5 bintang
- Rating buku akan diupdate secara otomatis
- Review membantu member lain memilih buku

### 8. Tips & Tricks

✅ **Best Practices:**
- Selalu logout setelah selesai menggunakan sistem
- Catat ID transaksi saat meminjam untuk referensi
- Kembalikan buku tepat waktu untuk menghindari denda
- Gunakan pencarian multi-kriteria untuk hasil optimal
- Review buku untuk membantu member lain

⚠️ **Hal yang Harus Dihindari:**
- Jangan bagikan password dengan orang lain
- Jangan meninggalkan komputer tanpa logout
- Jangan meminjam buku melebihi kapasitas yang diizinkan
- Jangan merusak atau mencoret buku

### 9. FAQ (Frequently Asked Questions)

**Q: Berapa lama saya bisa meminjam buku?**
A: Default 7 hari, tetapi librarian dapat menyesuaikan durasi.

**Q: Apakah ada biaya pendaftaran?**
A: Tidak, registrasi gratis.

**Q: Bagaimana jika saya mengembalikan buku terlambat?**
A: Akan ada denda sebesar Rp 5.000 per hari keterlambatan.

**Q: Bisakah saya meminjam buku yang tidak tersedia?**
A: Ya, Anda dapat membuat reservasi. Anda akan mendapat notifikasi ketika buku tersedia.

**Q: Bagaimana cara mengubah password?**
A: Hubungi admin atau librarian untuk mengubah password.

**Q: Berapa maksimal buku yang bisa dipinjam?**
A: Tidak ada batasan jumlah, tetapi librarian dapat membuat kebijakan.

### 10. Troubleshooting

**Masalah: Tidak bisa login**
- Pastikan username dan password benar (case-sensitive)
- Jika lupa password, hubungi admin
- Tunggu 5 menit jika login gagal 5x (cooldown)

**Masalah: Buku tidak tersedia di pencarian**
- Coba gunakan kata kunci yang lebih umum
- Coba cari dengan criteria lain (author, kategori)
- Pastikan buku sudah ditambahkan ke sistem oleh librarian

**Masalah: Tidak bisa meminjam buku**
- Pastikan buku tersedia (available_copies > 0)
- Hubungi librarian jika ada masalah teknis
- Check apakah status buku adalah "Tersedia"

**Masalah: Aplikasi crash/tidak responsif**
- Close aplikasi dan restart
- Pastikan Python terinstall dengan benar
- Check console untuk error messages

### 11. Kontak & Support

Jika mengalami masalah atau memiliki pertanyaan:
1. Hubungi **Librarian** di desk perpustakaan
2. Hubungi **Admin** untuk masalah teknis
3. Lihat dokumentasi di folder `docs/`

---

**Last Updated**: December 4, 2024
**Version**: 1.0.0
