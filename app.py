from flask import Flask, render_template, request, jsonify, redirect, make_response, session, flash, url_for
import csv
from io import StringIO
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import time

app = Flask(__name__)
app.secret_key = 'super_secret_key_maggot'

last_db_write_time = 0

# Database Setup
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            location TEXT NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS sensor_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            suhu REAL,
            kelembaban REAL,
            cahaya INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS production_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            berat_sampah REAL,
            produksi_maggot REAL,
            efisiensi REAL,
            user_id INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Decorator for requiring login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Koleksi penampung data di RAM
data_kandang = {"suhu": 0.0, "kelembaban": 0.0, "cahaya": 0}

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        password = request.form['password']
        location = request.form['location']
        school_code = request.form.get('school_code', '')
        
        if school_code != 'ALAMCIBINONG26':
            flash('Pendaftaran Gagal: Kode Akses Sekolah tidak valid!', 'danger')
            return redirect(url_for('register'))
            
        hashed_password = generate_password_hash(password)
        
        try:
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            c.execute('INSERT INTO users (fullname, email, password, location) VALUES (?, ?, ?, ?)',
                      (fullname, email, hashed_password, location))
            conn.commit()
            conn.close()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Email address already exists.', 'danger')
            
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = c.fetchone()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['user_name'] = user['fullname']
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password', 'danger')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def home():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM production_logs ORDER BY id DESC')
    manual_data = c.fetchall()
    conn.close()
    return render_template('index.html', manual_data=manual_data, user_name=session.get('user_name'))

@app.route('/api/kirim-data', methods=['POST'])
def terima_data():
    global data_kandang, last_db_write_time
    payload = request.get_json()
    suhu = payload.get('suhu', 0.0)
    kelembaban = payload.get('kelembaban', 0.0)
    cahaya = payload.get('cahaya', 0)
    
    data_kandang['suhu'] = suhu
    data_kandang['kelembaban'] = kelembaban
    data_kandang['cahaya'] = cahaya
    
    current_time = time.time()
    # Simpan ke database setiap 5 menit (300 detik)
    if current_time - last_db_write_time > 300:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('INSERT INTO sensor_history (suhu, kelembaban, cahaya) VALUES (?, ?, ?)', (suhu, kelembaban, cahaya))
        conn.commit()
        conn.close()
        last_db_write_time = current_time
        
    return jsonify({"status": "success"})

@app.route('/api/data-terbaru', methods=['GET'])
def kirim_ke_frontend():
    return jsonify(data_kandang)

@app.route('/api/sensor-history', methods=['GET'])
def get_sensor_history():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT suhu, kelembaban, cahaya, datetime(timestamp, "localtime") as ts FROM sensor_history ORDER BY id DESC LIMIT 20')
    rows = c.fetchall()
    conn.close()
    
    # Reverse agar data terurut dari lama ke baru
    history = [dict(row) for row in reversed(rows)]
    return jsonify(history)

@app.route('/input-manual', methods=['POST'])
@login_required
def input_manual():
    berat_sampah = float(request.form.get('berat_sampah', 0))
    produksi_maggot = float(request.form.get('produksi_maggot', 0))
    
    efisiensi = round((produksi_maggot / berat_sampah) * 100, 2) if berat_sampah > 0 else 0
    user_id = session.get('user_id')
    
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('INSERT INTO production_logs (berat_sampah, produksi_maggot, efisiensi, user_id) VALUES (?, ?, ?, ?)',
              (berat_sampah, produksi_maggot, efisiensi, user_id))
    conn.commit()
    conn.close()
    
    return redirect('/')

@app.route('/export-csv')
@login_required
def export_csv():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM production_logs ORDER BY id ASC')
    logs = c.fetchall()
    conn.close()

    si = StringIO()
    si.write('\ufeff') # UTF-8 BOM
    cw = csv.writer(si, delimiter=';')
    cw.writerow(['No', 'Trash Weight (kg)', 'Maggot Production (kg)', 'Bioconversion Efficiency (%)'])
    for item in logs:
        cw.writerow([item['id'], item['berat_sampah'], item['produksi_maggot'], f"{item['efisiensi']}%"])
    
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=smart_maggot_report.csv"
    output.headers["Content-Type"] = "text/csv; charset=utf-8-sig"
    return output

@app.route('/profile')
@login_required
def profile():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],))
    user = c.fetchone()
    conn.close()
    return render_template('profile.html', user=user, user_name=session.get('user_name'))

@app.route('/change-password', methods=['POST'])
@login_required
def change_password():
    old_password = request.form['old_password']
    new_password = request.form['new_password']
    school_code = request.form.get('school_code', '')
    
    if school_code != 'ALAMCIBINONG26':
        flash('Kode Akses Sekolah salah!', 'danger')
        return redirect(url_for('profile'))
        
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],))
    user = c.fetchone()
    
    if user and check_password_hash(user['password'], old_password):
        hashed_new = generate_password_hash(new_password)
        c.execute('UPDATE users SET password = ? WHERE id = ?', (hashed_new, session['user_id']))
        conn.commit()
        flash('Password berhasil diperbarui!', 'success')
    else:
        flash('Password lama salah!', 'danger')
        
    conn.close()
    return redirect(url_for('profile'))

@app.route('/edukasi')
@login_required
def edukasi():
    return render_template('edukasi.html', user_name=session.get('user_name'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)