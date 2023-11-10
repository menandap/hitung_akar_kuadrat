import pymysql
import dbm
from flask import Flask, render_template, request, jsonify
import time
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
        cursor.execute("SELECT input, hasil, waktu, jenis FROM logs ORDER BY id DESC") #filter dari data terbaru
        data = cursor.fetchall()
        cursor.close()

        # Convert data
        logs = [{'input': row[0], 'hasil': row[1], 'waktu': row[2], 'jenis': row[3]} for row in data]

        # Passing data ke template
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

     # Your code to calculate the square root
        tebakan = angka / 2
        epsilon = 0.00001

        # Catat waktu mulai perhitungan
        start_time = time.perf_counter()  # Waktu dalam detik dengan presisi yang lebih tinggi

        while True:
            akar_tebakan = 0.5 * (tebakan + angka / tebakan)
            error = abs(akar_tebakan - tebakan)

            if error < epsilon:
                break

            tebakan = akar_tebakan

        # Hitung waktu selesai perhitungan
        end_time = time.perf_counter()  # Waktu dalam detik dengan presisi yang lebih tinggi
        waktu_penghitungan = (end_time - start_time)  # Dalam detik

        # Format the time result to match PHP
        waktu_penghitungan = round(waktu_penghitungan, 9)  # Round to 9 decimal places

        # Simpan hasil perhitungan ke database MySQL
        cursor = db.cursor()
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Insert data ke tabel
        cursor.execute("INSERT INTO logs (input, hasil, waktu, jenis, created_at, updated_at) VALUES (%s, %s, %s, %s, NOW(), NOW())",
        (angka, akar_tebakan, waktu_penghitungan, jenis))
        db.commit()

        return jsonify({'input_angka': angka, 'hasil': akar_tebakan, 'waktu_penghitungan': waktu_penghitungan}), 200
    
    except Exception as e:
        if cursor:
            db.rollback()  # rollback jika ada error
            cursor.close()
        print(f"Database error: {str(e)}")
        return jsonify({'error': 'Terjadi kesalahan'}), 500

# Menggunakan Stored Procedure 
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

        # Mengambil ID terbaru dari tabel 
        cursor.execute("SELECT LAST_INSERT_ID()")
        result = cursor.fetchone()
        newest_id = result[0]

        # memanggil hasil dari db
        cursor.execute("SELECT input, hasil, waktu FROM logs WHERE id = %s", (newest_id,))
        data = cursor.fetchall()
        cursor.close()

        # convert data
        logs = [{'input': row[0],'hasil': row[1], 'waktu-penghitungan': row[2]} for row in data]
        formatted_data = {
        "input_angka": logs[0]['input'],  
        "hasil": logs[0]['hasil'],  
        "waktu_penghitungan": logs[0]['waktu-penghitungan'] 
        }

        return jsonify(formatted_data)


        # Mengembalikan hasil dalam bentuk ID terbaru
        # return jsonify({'id_terbaru': newest_id}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5010, debug=True)

