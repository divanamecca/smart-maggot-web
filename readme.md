# 🐛 Smart Maggot Farming Dashboard — Wireless Sensor Network (WSN)

Proyek Akhir Praktikum Mata Kuliah **Mobile Computing (TIK403)**
**Program Studi D4 Teknik Informatika, Jurusan Teknik Informatika dan Komputer**
**Politeknik Negeri Jakarta (PNJ)**

---

## 📝 Deskripsi Proyek

Proyek ini merupakan implementasi prototipe **Smart Maggot Farming** berbasis _Internet of Things_ (IoT) yang mengintegrasikan _Wireless Sensor Network_ (WSN) skala edukasi dengan _Web Dashboard_ interaktif. Sistem dirancang khusus untuk memonitor parameter lingkungan pada kandang pembesaran larva _Black Soldier Fly_ (BSF) secara _real-time_ guna mengoptimalkan proses biokonversi sampah organik dalam kerangka _Circular Economy_.
Sistem menggunakan **ESP32** sebagai _node_ sensor nirkabel untuk mengakuisisi data suhu, kelembaban, dan intensitas cahaya, lalu mengirimkannya ke server backend **Python Flask** melalui protokol **HTTP POST (REST API)** menggunakan jaringan Wi-Fi lokal. Data divisualisasikan secara dinamis menggunakan **Chart.js** dengan sistem _AJAX Polling_ otomatis setiap 2 detik.

---

## ✨ Fitur Utama Sistem

1. **Multi-Parameter Real-Time Monitoring:** Membaca suhu (°C), kelembaban udara (%), dan status pencahayaan secara simultan.
2. **Dual-LED Hazard Indicator:**
   - **LED Merah (GPIO 18):** Menyala otomatis sebagai alarm fisik jika terjadi kondisi _overheat_ (suhu > 28.5°C) atau kelembaban terlalu kering (< 50%).
   - **LED Hijau (GPIO 19):** Menyala otomatis jika kandang mendeteksi cahaya berlebih (karena larva maggot bersifat fotofobik/takut cahaya dan membutuhkan kondisi teduh agar optimal).
3. **Grafik Responsif & Dinamis:** Visualisasi pergerakan data sensor menggunakan Chart.js yang ter-update otomatis tanpa perlu me-refresh halaman (_Asynchronous AJAX_).
4. **User Input / Data Manual:** Form penginputan data harian untuk mencatat parameter non-sensor seperti berat sampah masuk (kg) dan total produksi panen maggot (kg).

---

## 🛠️ Spesifikasi Arsitektur Sistem

### 1. Perangkat Keras (Hardware) & Pin Mapping

Komponen utama yang digunakan beserta konfigurasinya pada _breadboard_:
| Komponen | Pin ESP32 | Deskripsi |
| :--- | :--- | :--- |
| **ESP32 Development Board** | VCC (3.3V) & GND | Otak pengolah data & modul Wi-Fi bawaan |
| **Sensor DHT11** | **GPIO 23** | Akuisisi data Suhu dan Kelembaban Udara |
| **Sensor Cahaya LDR (Digital Output/DO)** | **GPIO 34** | Deteksi kondisi gelap/terang kandang |
| **LED Merah + Resistor 100 Ω** | **GPIO 18** | Indikator Bahaya _Overheat_ / Kering |
| **LED Hijau + Resistor 100 Ω** | **GPIO 19** | Indikator Bahaya Kandang Terlalu Terang |

### 2. Perangkat Lunak (Software Stack)

- **Firmware:** C++ (Arduino IDE)
- **Backend Framework:** Python 3 (Flask REST API)
- **Frontend UI:** HTML5, CSS3, Bootstrap 5 (Responsive Layout)
- **Data Visualization:** JavaScript (Chart.js via AJAX Polling)

---

## 📁 Struktur Direktori Repositori

smart-maggot-uas/
│
├── 📁 smart-maggot-firmware/
│ └── 📄 smart_maggot_firmware.ino # Source code C++ untuk ESP32 (Arduino IDE)
│
└── 📁 smart-maggot-web-uas/
├── 📄 app.py # Server Backend Flask (REST API & Routing)
├── 📁 static/ # Tempat file aset statis (CSS/JS jika diperlukan)
└── 📁 templates/
└── 📄 index.html # Frontend Web Dashboard (Bootstrap + Chart.js)

🚀 Panduan Instalasi & Pengoperasian

1. Konfigurasi & Upload Firmware (ESP32)
   Buka file smart_maggot_firmware.ino menggunakan Arduino IDE.
   Pastikan pustaka DHT sensor library oleh Adafruit sudah terinstal.
   Sesuaikan kredensial Wi-Fi Hotspot dan IP Laptop Anda pada baris kode berikut:
   C++
   const char* ssid = "punya_dipa";
   const char* password = "alhamdulillah";
   const char\* server_ip = "10.220.250.210"; // Sesuaikan dengan IPv4 Wi-Fi laptop Anda (cek via cmd: ipconfig)
   Pilih Board DOIT ESP32 DEVKIT V1, lalu lakukan Upload.
   Buka Serial Monitor (Baud rate: 115200) untuk memantau status koneksi dan respon HTTP (200 jika sukses).

2. Setup Server Web Dashboard (Python Flask)
   Buka folder smart-maggot-web-uas/ menggunakan VS Code.
   Buka terminal baru di VS Code, lalu instal dependensi Flask melalui pip:
   Bash
   pip install flask
   Jalankan server lokal Flask dengan mengetik perintah berikut:
   Bash
   python app.py
   Pastikan terminal memunculkan log aktif yang menandakan server membuka gerbang jaringan:

- Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)

3. Akses Dashboard
   Buka web browser (Google Chrome/Microsoft Edge) di laptop Anda, lalu akses tautan berikut:
   Plaintext
   http://localhost:5000
