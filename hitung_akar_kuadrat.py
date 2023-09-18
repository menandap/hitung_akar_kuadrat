import pymysql
import dbm
from flask import Flask, render_template, request, jsonify
import datetime
import hashlib

# Membuat server Flask
app = Flask(__name__)


# Koneksi ke database MySQL
db = pymysql.connect(
	host="localhost",
	user="root",
	passwd="",
	database="db-square-root"
)

@app.route('/')
def index():
    try:
        cursor = db.cursor()
        cursor.execute("SELECT input, hasil, waktu, jenis FROM logs")
        data = cursor.fetchall()
        cursor.close()

        # convert data
        logs = [{'input': row[0], 'hasil': row[1], 'waktu': row[2], 'jenis': row[3]} if all(row) else None for row in data]

        # passing data ke template
        return render_template('index.html', logs=logs)

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/ambil-akar-kuadrat', methods=['GET'])
def ambil_akar_kuadrat():
    try:
        cursor = db.cursor()
        cursor.execute("SELECT input, hasil, waktu, jenis FROM logs")
        data = cursor.fetchall()

        cursor.close()

        # convert data
        logs = [{'input': row[0], 'hasil': row[1], 'waktu': row[2], 'jenis': row[3]} for row in data]
        
        # passing data json
        return jsonify({'logs': logs}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Menggunakan API
@app.route('/api/hitung-akar-kuadrat-api', methods=['POST'])
def hitung_akar_kuadrat_api():
    cursor = None  
    try:
        jenis ='API'
        data = request.get_json()
        angka = data.get('angka')  # Use get() to safely access the 'angka' key

        if angka is None:
            return jsonify({'error': 'Masukkan angka'}), 400

        if angka < 0:
            return jsonify({'error': 'Angka harus positif atau nol'}), 400

        # Inisialisasi tebakan awal
        tebakan = angka / 2

        epsilon = 1e-6  # Toleransi error yang cukup kecil

        # Catat waktu mulai perhitungan
        start_time = datetime.datetime.now()

        while True:
            akar_tebakan = 0.5 * (tebakan + angka / tebakan)
            error = abs(akar_tebakan - tebakan)

            if error < epsilon:
                break

            tebakan = akar_tebakan

        # Hitung waktu selesai perhitungan
        end_time = datetime.datetime.now()
        waktu_penghitungan = (end_time - start_time).total_seconds() * 1000  # Dalam milidetik

        # Simpan hasil perhitungan ke database MySQL
        cursor = db.cursor()
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Insert data ke tabel
        cursor.execute("INSERT INTO logs (input, hasil, waktu, jenis, created_at, updated_at) VALUES (%s, %s, %s, %s, NOW(), NOW())",
        (angka, akar_tebakan, waktu_penghitungan, jenis))
        db.commit()

        return jsonify({'hasil': akar_tebakan, 'waktu_penghitungan': waktu_penghitungan}), 200
    
    except Exception as e:
        if cursor:
            db.rollback()  # rollback jika ada error
            cursor.close()
        print(f"Database error: {str(e)}")
        return jsonify({'error': 'Terjadi kesalahan'}), 500
    finally:
        if cursor:
            cursor.close()  # menutup cursor jika kosong

# Menggunakan Stored Procedure (error)
@app.route('/api/hitung-akar-kuadrat-plsql', methods=['POST'])
def hitung_akar_kuadrat_plsql():
    try:
        jenis = 'SP-SQL'
        data = request.get_json()
        angka = data['angka']

        if angka is None:
            return jsonify({'error': 'Masukkan angka'}), 400

        if angka < 0:
            return jsonify({'error': 'Angka harus positif atau nol'}), 400

        # Menggunakan stored procedure SQL
        cursor = db.cursor()
        cursor.callproc('square_root', (angka, 0, 0))  # Memanggil stored procedure dengan parameter input, output output, dan output timeoutput
        db.commit()

        # memanggil hasil dari db
        cursor.execute("SELECT hasil, waktu FROM logs WHERE input = %s", (angka,))
        data = cursor.fetchall()
        cursor.close()

        # convert data
        logs = [{'hasil': row[0], 'waktu-penghitungan': row[1]} for row in data]
        formatted_data = {
        "hasil": logs[0]['hasil'],  # Replace with the correct key you want
        "waktu_penghitungan": logs[0]['waktu-penghitungan']  # Replace with the correct key you want
        }

        return jsonify(formatted_data)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5010, debug=True)

