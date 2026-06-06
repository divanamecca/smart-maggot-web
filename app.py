from flask import Flask, render_template, request, jsonify, redirect, make_response
import csv
from io import StringIO

app = Flask(__name__)

# Koleksi penampung data di RAM
data_kandang = {"suhu": 0.0, "kelembaban": 0.0, "cahaya": 0}
data_manual_list = [] # Menyimpan riwayat input harian sampah & maggot

@app.route('/')
def home():
    # Mengirimkan data_manual_list ke HTML agar bisa dirender jadi tabel
    return render_template('index.html', manual_data=data_manual_list)

@app.route('/api/kirim-data', methods=['POST'])
def terima_data():
    global data_kandang
    payload = request.get_json()
    data_kandang['suhu'] = payload.get('suhu', 0.0)
    data_kandang['kelembaban'] = payload.get('kelembaban', 0.0)
    data_kandang['cahaya'] = payload.get('cahaya', 0)
    return jsonify({"status": "success"})

@app.route('/api/data-terbaru', methods=['GET'])
def kirim_ke_frontend():
    return jsonify(data_kandang)

@app.route('/input-manual', methods=['POST'])
def input_manual():
    # Ambil data dari form html
    berat_sampah = float(request.form.get('berat_sampah', 0))
    produksi_maggot = float(request.form.get('produksi_maggot', 0))
    
    # Hitung efisiensi biokonversi otomatis (%)
    efisiensi = round((produksi_maggot / berat_sampah) * 100, 2) if berat_sampah > 0 else 0
    
    # Masukkan ke list riwayat
    data_manual_list.append({
        "id": len(data_manual_list) + 1,
        "sampah": berat_sampah,
        "maggot": produksi_maggot,
        "efisiensi": efisiensi
    })
    
    # KUNCI: Langsung balikkan user ke halaman utama, bukan tampilin text hampa
    return redirect('/')


@app.route('/export-csv')
def export_csv():
    si = StringIO()
    
    # KUNCI UTAMA: Tambahkan delimiter=';' di sini beb!
    cw = csv.writer(si, delimiter=';')
    
    # Tulis Header Kolom
    cw.writerow(['No', 'Berat Sampah Masuk (kg)', 'Total Produksi Maggot (kg)', 'Efisiensi Biokonversi (%)'])
    
    # Tulis isi data dari list harian
    for item in data_manual_list:
        cw.writerow([item['id'], item['sampah'], item['maggot'], f"{item['efisiensi']}%"])
    
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=laporan_smart_maggot.csv"
    output.headers["Content-Type"] = "text/csv"
    return output


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)