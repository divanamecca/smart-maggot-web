from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Data sementara disimpan di memori (Array) dulu biar gak ribet set up MySQL malam ini!
data_kandang = {"suhu": 0.0, "kelembaban": 0.0, "cahaya": 0}
data_manual_list = []

@app.route('/')
def home():
    # Langsung lempar file index.html yang tadi
    return render_template('index.html')

@app.route('/api/kirim-data', methods=['POST'])
def terima_data():
    global data_kandang
    # Tempat ESP32 kamu nembak data lewat internet harian
    payload = request.get_json()
    data_kandang['suhu'] = payload.get('suhu')
    data_kandang['kelembaban'] = payload.get('kelembaban')
    data_kandang['cahaya'] = payload.get('cahaya')
    return jsonify({"status": "success", "message": "Data masuk, beb!"})

@app.route('/api/data-terbaru', methods=['GET'])
def kirim_ke_frontend():
    # Tempat JavaScript di HTML mengambil data setiap 2 detik
    return jsonify(data_kandang)

@app.route('/input-manual', methods=['POST'])
def input_manual():
    # Menangkap form berat sampah harian
    berat_sampah = request.form.get('berat_sampah')
    produksi_maggot = request.form.get('produksi_maggot')
    data_manual_list.append({"sampah": berat_sampah, "maggot": produksi_maggot})
    return "Data manual berhasil disimpan! <a href='/'>Kembali</a>"

if __name__ == '__main__':
    # Jalankan di IP 0.0.0.0 agar bisa ditembak oleh ESP32 dari hotspot HP
    app.run(host='0.0.0.0', port=5000, debug=True)
