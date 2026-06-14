from flask import Flask, render_template, request, jsonify, redirect, make_response, session, flash, url_for
import csv
from io import StringIO
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.secret_key = 'super_secret_key_maggot'

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
data_manual_list = [] # Menyimpan riwayat input harian sampah & maggot

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        password = request.form['password']
        location = request.form['location']
        
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
    return render_template('index.html', manual_data=data_manual_list, user_name=session.get('user_name'))

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
@login_required
def input_manual():
    berat_sampah = float(request.form.get('berat_sampah', 0))
    produksi_maggot = float(request.form.get('produksi_maggot', 0))
    
    efisiensi = round((produksi_maggot / berat_sampah) * 100, 2) if berat_sampah > 0 else 0
    
    data_manual_list.append({
        "id": len(data_manual_list) + 1,
        "sampah": berat_sampah,
        "maggot": produksi_maggot,
        "efisiensi": efisiensi
    })
    
    return redirect('/')

@app.route('/export-csv')
@login_required
def export_csv():
    si = StringIO()
    cw = csv.writer(si, delimiter=';')
    cw.writerow(['No', 'Trash Weight (kg)', 'Maggot Production (kg)', 'Bioconversion Efficiency (%)'])
    for item in data_manual_list:
        cw.writerow([item['id'], item['sampah'], item['maggot'], f"{item['efisiensi']}%"])
    
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=smart_maggot_report.csv"
    output.headers["Content-Type"] = "text/csv"
    return output

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)