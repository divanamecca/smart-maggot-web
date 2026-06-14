# 🐛 Smart Maggot Farming Dashboard
*Tugas Akhir Semester (UAS) - Berbasis Proposal PKML Sekolah Alam Indonesia Cibinong*

Aplikasi web cerdas ini merupakan sistem monitoring berbasis *Internet of Things* (IoT) untuk pengelolaan budidaya Maggot *Black Soldier Fly* (BSF) sebagai media edukasi *Circular Economy*.

## ✨ Fitur Utama
1. **Keamanan Ekstra (Secret Code Registration):** Sistem pendaftaran tertutup bagi pihak luar. Hanya siswa dan guru yang memiliki kode akses (`ALAMCIBINONG26`) yang dapat membuat akun dan mengakses sistem.
2. **Database Permanen (SQLite):** 
   - Merekam data sensor setiap 5 menit (`sensor_history`).
   - Menyimpan seluruh log produksi panen siswa secara aman (`production_logs`).
3. **Monitoring Sensor Real-Time:** Menampilkan Suhu, Kelembaban, dan intensitas Cahaya dari *hardware* ESP32 tanpa perlu *refresh* halaman.
6. **Modul Edukasi Interaktif:** Terdapat halaman khusus berisi panduan kurikulum *Circular Economy* dan siklus BSF yang *hardcoded* (aman dari modifikasi iseng).
7. **Mobile-First & Responsive Dashboard:** Antarmuka secara cerdas beradaptasi di layar HP. Grafik diprioritaskan tampil paling atas pada layar kecil, dengan menu navigasi yang otomatis menyesuaikan (*wrap*).
8. **Profil Akun & Ganti Password Aman:** Pengguna dapat memperbarui kata sandi, yang tentunya masih dilindungi secara ketat oleh "Kode Akses Sekolah".
9. **Ekspor CSV Ramah Excel:** Ekspor satu kali klik. Data dapat langsung dibaca dengan kolom sempurna di Microsoft Excel (mendukung BOM UTF-8 SIG).

## 🔌 Spesifikasi Hardware (IoT)
Sistem ini terintegrasi secara langsung dengan perangkat keras fisik:
- **Mikrokontroler:** ESP32 (sebagai otak utama pengirim data via WiFi).
- **Sensor Suhu & Kelembaban:** DHT11 / DHT22.
- **Sensor Cahaya:** LDR (Light Dependent Resistor) atau Modul Cahaya analog.
- **Indikator Aktuator (LED):**
  - 🟢 **Lampu Hijau (Indikator Suhu):** Akan menyala sebagai penanda/aktuasi bahwa suhu sedang dalam kondisi bahaya/panas.
  - 🔴 **Lampu Merah (Indikator Cahaya):** Akan menyala apabila kondisi kandang terlalu terang (maggot bersifat *fotofobik* / takut cahaya).

## 🛠️ Persyaratan Sistem (Prerequisites)
- Python 3.x
- Flask (`pip install Flask`)
- Werkzeug Security (Bawaan Flask)
- Modul SQLite3 (Bawaan Python)

## 🚀 Cara Menjalankan Aplikasi
1. Buka Terminal/Command Prompt di dalam direktori proyek ini.
2. Jalankan perintah berikut:
   ```bash
   flask run --host=0.0.0.0
   ```
   *(Penggunaan host 0.0.0.0 memungkinkan aplikasi untuk diakses dari HP melalui jaringan WiFi yang sama).*
3. Buka browser dan ketikkan alamat: `http://localhost:5000` (atau IP Address laptop jika mengakses dari HP).

## 🔐 Info Demo
- **Kode Akses Sekolah:** `ALAMCIBINONG26`
- **Cara Kerja:** ESP32 mengirim data via metode POST JSON ke *endpoint* `/api/kirim-data` secara terus menerus. Web menggunakan AJAX untuk mengambil data tersebut dari memori RAM (untuk *live update* tiap 2 detik) dan dari database SQLite (untuk memori jangka panjang grafik).

---
*Dikembangkan untuk memenuhi standar spesifikasi Sistem Smart Farming berbasis Project-Based Learning.*
