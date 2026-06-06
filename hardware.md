### 1. Tabel Pemetaan Pin Utama (Pinout Mapping)

Berikut adalah tabel konfigurasi pinout antara mikrokontroler ESP32 dengan seluruh komponen sensor dan aktuator yang digunakan pada sistem _Smart Maggot Farming_:

| Perangkat / Komponen    | Kaki / Pin Komponen                 | Pin Digital ESP32          | Tipe Arus / Sinyal               | Fungsi Teknis                                                                     |
| :---------------------- | :---------------------------------- | :------------------------- | :------------------------------- | :-------------------------------------------------------------------------------- |
| **Sensor DHT11**        | VCC<br>GND<br>DATA                  | 3.3V<br>GND<br>**GPIO 23** | Power<br>Ground<br>Digital Input | Menyalurkan daya.<br>Jalur massa.<br>Mengirimkan data suhu & kelembaban.          |
| **Sensor Cahaya LDR**   | VCC<br>GND<br>DO (Digital Output)   | 3.3V<br>GND<br>**GPIO 34** | Power<br>Ground<br>Digital Input | Menyalurkan daya.<br>Jalur massa.<br>Mengirimkan status cahaya (0 atau 1).        |
| **LED Indikator Merah** | Kaki Panjang (+)<br>Kaki Pendek (-) | **GPIO 18**<br>GND         | Digital Output<br>Ground         | Menerima arus setruman saat _overheat_.<br>Menyalurkan arus kembali ke massa.     |
| **LED Indikator Hijau** | Kaki Panjang (+)<br>Kaki Pendek (-) | **GPIO 19**<br>GND         | Digital Output<br>Ground         | Menerima arus setruman saat terlalu terang.<br>Menyalurkan arus kembali ke massa. |

---

### 2. Panduan Langkah-Demi-Langkah Perakitan Rangkaian (Wiring Guide)

Proses perakitan jalur sirkuit pada _breadboard_ dibagi menjadi 4 bagian integrasi utama:

#### A. Jalur Distribusi Daya Utama (Power & Ground)

- Pin **3.3V** pada bodi ESP32 dihubungkan menggunakan kabel jumper ke jalur panjang bertanda **plus (+/garis merah)** di pinggiran _breadboard_ untuk bertindak sebagai jalur distribusi daya sensor.
- Pin **GND** pada bodi ESP32 dihubungkan menggunakan kabel jumper ke jalur panjang bertanda **minus (-/garis biru)** di pinggiran _breadboard_ untuk bertindak sebagai jalur massa (arus negatif) bersama.

#### B. Rangkaian Sensor Suhu & Kelembaban (DHT11)

- Kaki **VCC** pada modul sensor DHT11 ditancapkan ke jalur positif (+) _breadboard_.
- Kaki **GND** pada modul sensor DHT11 ditancapkan ke jalur negatif (-) _breadboard_.
- Kaki **DATA / OUT** pada modul sensor DHT11 dihubungkan menggunakan kabel jumper _Female-to-Male_ langsung menuju pin **GPIO 23** pada papan ESP32.

#### C. Rangkaian Sensor Cahaya (Modul Digital LDR)

- Kaki **VCC** pada modul sensor cahaya ditancapkan ke jalur positif (+) _breadboard_.
- Kaki **GND** pada modul sensor cahaya ditancapkan ke jalur negatif (-) _breadboard_.
- Kaki **DO (Digital Output)** pada modul sensor cahaya dihubungkan menggunakan kabel jumper langsung menuju pin **GPIO 34** pada papan ESP32 untuk mendeteksi ambang batas intensitas cahaya secara digital.

#### D. Rangkaian Aktuator Dual-LED Berbasis Resistor Penahan Arus

Untuk mencegah lampu LED putus akibat tegangan berlebih, rangkaian memanfaatkan resistor 100 Ohm sebagai pembatas arus:

1. **Jalur LED Merah (Indikator Suhu/Kelembaban):**
   - Kaki panjang (Anoda) LED Merah ditempatkan pada baris tertentu (misalnya Baris 22).
   - Sebuah **Resistor 100 Ohm** dipasang untuk menjembatani arus dari Baris 22 ke jalur kabel data yang terhubung ke pin **GPIO 18** ESP32.
   - Kaki pendek (Katoda) LED Merah ditancapkan langsung ke jalur negatif (-) warna biru di _breadboard_ menggunakan kawat konduktor.

2. **Jalur LED Hijau (Indikator Intensitas Cahaya Maggot):**
   - Kaki panjang (Anoda) LED Hijau ditempatkan pada **Baris 25**, sedangkan kaki pendeknya (Katoda) ditempatkan pada **Baris 26**.
   - Sebuah **Resistor 100 Ohm** dipasang secara mandiri untuk menjembatani dan mengalirkan arus dari **Baris 25** menuju **Baris 24** (isolasi jalur agar tidak bercampur dengan LED Merah).
   - Kabel data _Female-to-Male_ dipasang dari pin **GPIO 19** ESP32 menuju **Baris 24** untuk mengontrol aktivitas LED Hijau secara mandiri lewat program.
   - Kaki pendek LED Hijau pada **Baris 26** dihubungkan ke jalur bumi/negatif (-) warna biru di pinggiran _breadboard_ menggunakan kawat tiarap jembatan untuk menutup siklus arus listrik.
