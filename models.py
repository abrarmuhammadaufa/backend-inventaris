class Barang:
    def __init__(self, no_barang, nama_barang, jumlah_barang, keterangan):
        self.no_barang = no_barang
        self.nama_barang = nama_barang
        self.jumlah_barang = jumlah_barang
        self.keterangan = keterangan

    def to_dict(self):
        return {
            "no_barang": self.no_barang,
            "nama_barang": self.nama_barang,
            "jumlah_barang": self.jumlah_barang,
            "keterangan": self.keterangan
        }


class Admin:
    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
        }