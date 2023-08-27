from flask import Flask, jsonify, request, render_template
from flask_restful import Resource, Api
from flask_cors import CORS
import os
from db import init, checkBarang
from models import Admin

app = Flask(__name__)
CORS(app)


mysql = init(app)

@app.route("/")
def index():
  return "Masjid Nurul Islam API &copy; 2023"

@app.route('/login', methods=['POST'])
def login():
    # Di sini Anda dapat melakukan validasi dan autentikasi sesuai dengan kebutuhan Anda.
    # Contoh sederhana: Cek apakah username dan password sesuai.
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM admin WHERE username = %s AND password = %s", (username, password))
    result = cur.fetchone()
    cur.close()

    if result:
        return jsonify({"success": True})
    else:
        return jsonify({"success": False}), 401

@app.route('/barang',methods=['GET'])
def barang():
    try:
        return jsonify(checkBarang(mysql))
    except Exception as e:
        err = jsonify(msg=f'{e}',),500
        return err
    
@app.route('/tambah_barang', methods=['POST'])
def tambah_barang():
    try:
        data = request.get_json()
        nama_barang = data.get('nama_barang')
        jumlah_barang = data.get('jumlah_barang')
        keterangan = data.get('keterangan')

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO barang (nama_barang, jumlah_barang, keterangan) VALUES (%s, %s, %s)",
                    (nama_barang, jumlah_barang, keterangan))
        mysql.connection.commit()
        cur.close()

        return jsonify({"success": True})
    except Exception as e:
        err = jsonify(msg=f'{e}'), 500
        return err
    
@app.route('/hapus_barang/<int:barang_id>', methods=['DELETE'])
def hapus_barang(barang_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM barang WHERE no_barang = %s", (barang_id,))
        mysql.connection.commit()
        cur.close()
        return jsonify({"message": "Barang berhasil dihapus."})
    except Exception as e:
        err = jsonify(msg=f'{e}',), 500
        return err
    
@app.route('/edit_barang/<string:no_barang>', methods=['PUT'])
def edit_barang(no_barang):
    print(no_barang)
    try:
        if request.headers['Content-Type'] != 'application/json':
            return "Unsupported Media Type: Did not attempt to load JSON data because the request Content-Type was not 'application/json'.", 415
        data = request.get_json()
        print(data["keterangan"])
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE barang SET jumlah_barang = %s, keterangan = %s WHERE no_barang = %s",
                       (data["jumlah_barang"], data["keterangan"], no_barang))
        mysql.connection.commit()
        cursor.close()
        return "Barang berhasil diupdate", 200
    except KeyError:
        return "Data yang diberikan tidak lengkap", 400
    except Exception as e:
        return f"Terjadi kesalahan: {str(e)}", 500



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8081)))