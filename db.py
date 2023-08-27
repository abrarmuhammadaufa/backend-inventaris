from flask import request, jsonify
from flask_mysqldb import MySQL
from models import Barang

mysql = MySQL()
def init(app):
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_PORT'] = 3306
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = ''
    app.config['MYSQL_DB'] = 'inventaris_masjid'
    return MySQL(app)

def checkBarang(mysql):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM barang")
    result = cursor.fetchall()
    cursor.close()
    barang_list = []
    for row in result:
        barang = Barang(no_barang=row[0], nama_barang=row[1], jumlah_barang=row[2], keterangan=row[3])
        barang_dict = barang.to_dict()
        barang_list.append(barang_dict)
    return barang_list



