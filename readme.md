# 🐛 Smart Maggot Farming Dashboard — Wireless Sensor Network (WSN)

Proyek Akhir Praktikum Mata Kuliah **Mobile Computing (TIK403)**
**Program Studi D4 Teknik Informatika, Jurusan Teknik Informatika dan Komputer**
**Politeknik Negeri Jakarta (PNJ)**

---

## 📝 Deskripsi Proyek

Proyek ini merupakan implementasi prototipe **Smart Maggot Farming** berbasis **Internet of Things (IoT)** yang mengintegrasikan **Wireless Sensor Network (WSN)** skala edukasi dengan **Web Dashboard** interaktif.

Sistem dirancang untuk memonitor parameter lingkungan pada kandang pembesaran larva **Black Soldier Fly (BSF)** secara **real-time** guna mengoptimalkan proses biokonversi sampah organik dalam kerangka **Circular Economy**.

Sistem menggunakan **ESP32** sebagai node sensor nirkabel untuk mengakuisisi data suhu, kelembaban, dan intensitas cahaya, kemudian mengirimkannya ke server backend **Python Flask** melalui protokol **HTTP POST (REST API)** menggunakan jaringan Wi-Fi lokal.

Data sensor divisualisasikan secara dinamis menggunakan **Chart.js** dengan mekanisme **AJAX Polling** otomatis setiap 2 detik.

---

## ✨ Fitur Utama Sistem

### 1. Multi-Parameter Real-Time Monitoring

Membaca dan menampilkan data berikut secara simultan:

* Suhu udara (°C)
* Kelembaban udara (%)
* Status pencahayaan kandang

### 2. Dual-LED Hazard Indicator

#### 🔴 LED Merah (GPIO 18)

Menyala otomatis apabila:

* Suhu melebihi **28.5°C**
* Kelembaban kurang dari **50%**

#### 🟢 LED Hijau (GPIO 19)

Menyala otomatis apabila:

* Kandang terdeteksi terlalu terang
* Lingkungan tidak ideal bagi larva maggot yang bersifat fotofobik (menghindari cahaya)

### 3. Grafik Responsif dan Dinamis

* Visualisasi data menggunakan **Chart.js**
* Pembaruan data otomatis tanpa refresh halaman
* Menggunakan metode **Asynchronous AJAX Polling**

### 4. User Input / Data Manual

Form input untuk mencatat data operasional harian seperti:

* Berat sampah organik masuk (kg)
* Total hasil panen maggot (kg)

---

## 🛠️ Arsitektur Sistem

### 1. Perangkat Keras (Hardware)

| Komponen                  | Pin ESP32  | Deskripsi                      |
| ------------------------- | ---------- | ------------------------------ |
| ESP32 Development Board   | 3.3V & GND | Mikrokontroler dan modul Wi-Fi |
| Sensor DHT11              | GPIO 23    | Sensor suhu dan kelembaban     |
| Sensor Cahaya LDR (DO)    | GPIO 34    | Deteksi kondisi terang/gelap   |
| LED Merah + Resistor 100Ω | GPIO 18    | Indikator overheat/kering      |
| LED Hijau + Resistor 100Ω | GPIO 19    | Indikator cahaya berlebih      |

---

### 2. Perangkat Lunak (Software Stack)

| Komponen         | Teknologi                |
| ---------------- | ------------------------ |
| Firmware         | C++ (Arduino IDE)        |
| Backend          | Python Flask             |
| Frontend         | HTML5, CSS3, Bootstrap 5 |
| Visualisasi Data | Chart.js                 |
| Komunikasi Data  | REST API (HTTP POST)     |

---

## 📁 Struktur Direktori Proyek

```text
smart-maggot-uas/
│
├── smart-maggot-firmware/
│   └── smart_maggot_firmware.ino
│
└── smart-maggot-web-uas/
    ├── app.py
    ├── static/
    │
    └── templates/
        └── index.html
```

### Keterangan File

| File / Folder             | Fungsi                                               |
| ------------------------- | ---------------------------------------------------- |
| smart_maggot_firmware.ino | Program ESP32 untuk membaca sensor dan mengirim data |
| app.py                    | Backend Flask dan REST API                           |
| templates/index.html      | Dashboard monitoring berbasis web                    |
| static/                   | Penyimpanan aset CSS, JavaScript, dan gambar         |

---

## 🚀 Panduan Instalasi dan Pengoperasian

### 1. Upload Firmware ke ESP32

1. Buka file:

```text
smart_maggot_firmware.ino
```

menggunakan **Arduino IDE**.

2. Pastikan library berikut telah terinstal:

* DHT Sensor Library by Adafruit
* Adafruit Unified Sensor

3. Sesuaikan konfigurasi jaringan pada kode berikut:

```cpp
const char* ssid = "punya_dipa";
const char* password = "alhamdulillah";
const char* server_ip = "10.220.250.210";
```

> Ganti `server_ip` sesuai alamat IPv4 laptop Anda yang dapat dilihat menggunakan perintah:

```bash
ipconfig
```

4. Pilih board:

```text
DOIT ESP32 DEVKIT V1
```

5. Upload program ke ESP32.

6. Buka **Serial Monitor** dengan baud rate:

```text
115200
```

7. Pastikan muncul status:

```text
HTTP Response Code: 200
```

yang menandakan data berhasil dikirim ke server.

---

### 2. Menjalankan Web Dashboard

1. Masuk ke folder:

```text
smart-maggot-web-uas/
```

2. Install Flask:

```bash
pip install flask
```

3. Jalankan server:

```bash
python app.py
```

4. Jika berhasil, terminal akan menampilkan:

```text
* Running on http://0.0.0.0:5000/
```

---

### 3. Mengakses Dashboard

Buka browser kemudian akses:

http://localhost:5000

atau

```text
http://127.0.0.1:5000
```

Dashboard akan menampilkan:

* Data suhu real-time
* Data kelembaban real-time
* Status pencahayaan
* Grafik monitoring sensor
* Form input data produksi

---

## 🎯 Tujuan Pengembangan

* Menerapkan konsep Wireless Sensor Network (WSN).
* Mengintegrasikan perangkat IoT dengan web dashboard.
* Memonitor kondisi lingkungan budidaya maggot secara real-time.
* Mendukung pengelolaan budidaya maggot yang lebih efisien dan berkelanjutan.
