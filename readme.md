# 🐛 Smart Maggot Farming Dashboard — Wireless Sensor Network (WSN)

Proyek Akhir Praktikum Mata Kuliah **Mobile Computing (TIK403)**
Program Studi D4 Teknik Informatika
Jurusan Teknik Informatika dan Komputer
Politeknik Negeri Jakarta (PNJ)

---

# 📖 Deskripsi Proyek

Smart Maggot Farming Dashboard merupakan sistem monitoring dan pengelolaan budidaya maggot berbasis Wireless Sensor Network (WSN) yang memanfaatkan mikrokontroler ESP32 sebagai node sensor dan Flask sebagai web server.

Sistem memungkinkan pengguna untuk:

* Memantau kondisi lingkungan kandang maggot secara real-time.
* Melihat data suhu, kelembaban, dan intensitas cahaya.
* Mengelola data budidaya melalui dashboard web.
* Mengakses halaman edukasi budidaya maggot.
* Melakukan autentikasi pengguna (login dan registrasi).
* Menyimpan data ke database SQLite.
* Mengintegrasikan komunikasi data antara ESP32 dan server menggunakan REST API.

---

# 🎯 Tujuan Sistem

Sistem ini dikembangkan untuk membantu proses pengelolaan budidaya maggot Black Soldier Fly (BSF) melalui pemantauan kondisi lingkungan secara digital sehingga proses budidaya menjadi lebih efektif, efisien, dan terukur.

---

# ⚙️ Teknologi yang Digunakan

## Backend

* Python 3
* Flask
* SQLite
* REST API

## Frontend

* HTML5
* CSS3
* JavaScript

## Hardware

* ESP32
* Sensor Suhu
* Sensor Kelembaban
* Sensor Cahaya

---

# 🏗️ Arsitektur Sistem

```text
ESP32 + Sensor
       │
       ▼
REST API (Flask)
       │
       ▼
Database SQLite
       │
       ▼
Dashboard Web
       │
       ▼
Pengguna
```

ESP32 membaca data sensor kemudian mengirimkannya ke server Flask melalui REST API. Data diproses dan disimpan ke database SQLite sebelum ditampilkan pada dashboard web.

---

# 📂 Struktur Proyek

```text
SMART-MAGGOT-WEB/
│
├── codingan-esp32-arduinoIDE/
│   └── code.txt
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   └── img/
│       └── login_illustration.png
│
├── templates/
│   ├── edukasi.html
│   ├── index.html
│   ├── login.html
│   ├── profile.html
│   └── register.html
│
├── .gitignore
├── app.py
├── database.db
├── old_index.html
├── readme.md
└── requirements.txt
```

---

# 📁 Penjelasan Struktur Folder

| Folder / File                | Keterangan                                             |
| ---------------------------- | ------------------------------------------------------ |
| `app.py`                     | File utama aplikasi Flask.                             |
| `database.db`                | Database SQLite yang digunakan sistem.                 |
| `templates/`                 | Berisi halaman HTML yang dirender Flask.               |
| `static/`                    | Berisi aset statis seperti CSS dan gambar.             |
| `codingan-esp32-arduinoIDE/` | Source code ESP32 untuk komunikasi sensor.             |
| `requirements.txt`           | Daftar dependensi Python yang dibutuhkan.              |
| `old_index.html`             | File dashboard versi lama yang disimpan sebagai arsip. |
| `.gitignore`                 | Konfigurasi file yang tidak diunggah ke GitHub.        |
| `readme.md`                  | Dokumentasi proyek.                                    |

---

# 🌐 Fitur Utama

## Dashboard Monitoring

Menampilkan data kondisi lingkungan kandang maggot secara real-time.

## Login dan Registrasi

Menyediakan sistem autentikasi pengguna.

## Profil Pengguna

Menampilkan informasi akun pengguna yang sedang login.

## Edukasi Maggot

Memberikan informasi dan edukasi mengenai budidaya maggot serta pengelolaan sampah organik.

## Integrasi Sensor ESP32

Menerima data sensor melalui REST API untuk ditampilkan pada dashboard.

---

# 🔌 REST API

## Kirim Data Sensor

```http
POST /api/kirim-data
```

Contoh JSON:

```json
{
  "suhu": 30,
  "kelembaban": 75,
  "cahaya": 450
}
```

Fungsi:

* Menerima data dari ESP32.
* Memvalidasi data sensor.
* Menyimpan data ke sistem.

---

## Ambil Data Terbaru

```http
GET /api/data-terbaru
```

Response:

```json
{
  "suhu": 30,
  "kelembaban": 75,
  "cahaya": 450
}
```

Fungsi:

* Menyediakan data terbaru kepada dashboard web.

---

# 🗄️ Database

Sistem menggunakan SQLite sebagai media penyimpanan data.

Keuntungan:

* Ringan.
* Tidak memerlukan instalasi server database tambahan.
* Cocok untuk kebutuhan prototipe dan pengembangan akademik.

File database:

```text
database.db
```

---

# 🚀 Cara Menjalankan Proyek

## 1. Clone Repository

```bash
git clone <repository-url>
```

## 2. Masuk ke Folder Proyek

```bash
cd SMART-MAGGOT-WEB
```

## 3. Install Dependensi

```bash
pip install -r requirements.txt
```

## 4. Jalankan Flask

```bash
python app.py
```

## 5. Akses Aplikasi

```text
http://127.0.0.1:5000
```

---

# 📡 Integrasi ESP32

Source code ESP32 tersedia pada folder:

```text
codingan-esp32-arduinoIDE/
```

ESP32 bertugas untuk:

1. Membaca data sensor.
2. Menghubungkan perangkat ke jaringan Wi-Fi.
3. Mengirimkan data sensor ke Flask menggunakan HTTP POST.
4. Memperbarui data monitoring secara berkala.
