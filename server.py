from xmlrpc.server import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
from time import time 

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ("/RPC2", )

# Buat 'struct' klinik
class Klinik:
    # Variabel statik untuk generate nomor antrean
    # dan nomor rekor medis
    nomor_rekor_medis_sekarang = 999;
    nomor_antrian_sekarang = 0;

    @classmethod # Ini method yang ngakses variabel statik kelas
    def get_nomor_antrian(cls):
        cls.nomor_antrian_sekarang += 1
        return cls.nomor_antrian_sekarang

    @classmethod
    def get_nomor_rekor_medis(cls):
        cls.nomor_rekor_medis_sekarang += 1
        return cls.nomor_rekor_medis_sekarang

    def __init__(self, name):
        self.nama = name
        self.antrean = []

    def register(self, pasien):
        """ 
        Mendaftarkan pasien di klinik 
        Parameter:
        pasien: Pasien
        """
        pasien.nomor_antrean = self.get_nomor_antrian();
        pasien.nomor_rekor_medis = self.get_nomor_rekor_medis();
        pasien.klinik_perawatan = self;
        pasien.waktu_pengobatan = int((time() % 30) + 1); # Random [1, 30]
        self.antrean.append(pasien)
    
    # Satu underscore di awal anggap functionnya private
    def _get_waktu_antrian(self, nomor_antrean):
        """
        Mendapatkan nomor antrian pasien di klinik ini jika ada. Return -1 kalau pasien
        tidak mengantri di klinik ini.
        Parameter
        nomor_antrean: int
        """

        total_waktu_tunggu = 0
        ptr = 0
    
        # Cari pasien dengan nomor antrean tertentu
        while(nomor_antrean != self.antrean[ptr].nomor_antrean
               and ptr < len(self.antrean)
        ):
            total_waktu_tunggu += self.antrean[ptr].waktu_pengobatan
            ptr += 1
        if(ptr < len(self.antrean)):
            return total_waktu_tunggu
        return -1
        

    def get_antrean(self):
        """ Mengembalikan antrean saat ini """
        return self.antrean
    
# Buat 'struct' pasien
class Pasien:
    DAFTAR_PASIEN = []

    @classmethod
    def tambah_pasien(cls, pasien):
        cls.DAFTAR_PASIEN.append(pasien)
        return len(cls.DAFTAR_PASIEN) - 1;

    @classmethod
    def get_pasien(cls, idx):
        return cls.DAFTAR_PASIEN[idx]
    
    def __init__(self, name, tanggal_lahir):
        self.name = name
        self.tanggal_lahir = tanggal_lahir
        self.nomor_antrean = -1;
        self.nomor_rekor_medis = -1;
        self.waktu_pengobatan = -1;
        self.klinik_perawatan = None;

    def get_waktu_antrian(self):
        if(self.klinik_perawatan != None):
            return "silakan tunggu " \
                f"{self.klinik_perawatan._get_waktu_antrian(self.nomor_antrean)} menit lagi"
        return "Anda tidak terdaftar di klinik manapun!"

def pasien_terdaftar(idxPasien):
    return not(idxPasien < 0 or idxPasien >= len(Pasien.DAFTAR_PASIEN))

def klinik_tersedia(idxKlinik):
    return not(idxKlinik >= len(KLINIK) or idxKlinik < 0)

# Initial condition (Usahakan nama disini sinkron sama client.py)
NAMA_KLINIK = ["Telkomedika", "Do'a Ibu", "Mayapada" ]
KLINIK = [Klinik(NAMA_KLINIK[i]) for i in range(3)]

# Fungsi-fungsi yang bisa diakses secara remote. Semua ini fungsi khusus diakses oleh
# client. Fungsi dan kelas sebelumnya hanya diakses oleh server. Kalau mau bikin biar
# bisa akses, tambahin fungsi sendiri buat ngejembatanin.
def cek_daftar_klinik():
    buffer = "\n".join(
        [f"{idx + 1}. {nama_klinik}" for idx, nama_klinik in enumerate(NAMA_KLINIK)]
    )
    return "=== DAFTAR KLINIK === \n" + buffer;

def display_waktu_tunggu_pasien(idxPasien):
    if(not(pasien_terdaftar(idxPasien))):
        return "Anda belum terdaftar sebagai pasien di sistem kami"

    pasien = Pasien.get_pasien(idxPasien)
    return "Pasien "+pasien.name+" "+pasien.get_waktu_antrian()

def daftar(idxPasien, idxKlinik):
    if(not(pasien_terdaftar)):
        return "Anda belum terdaftar sebagai pasien di sistem kami"

    if(not(klinik_tersedia)):
        return "Klinik tidak ada"

    klinik = KLINIK[idxKlinik]
    pasien = Pasien.get_pasien(idxPasien)
    klinik.register(pasien)
    return f"Pasien {pasien.name} berhasil mendaftar di klinik {klinik.nama} dengan idxPasien = {idxPasien}"

def cek_antrian_klinik(idxKlinik):
    if (not(klinik_tersedia)):
        return "Klinik tidak ada"

    antrian = KLINIK[idxKlinik].get_antrean()
    buffer=""
    for i in range(0,len(antrian)):
        pasien = antrian[i]
        buffer += f"{str(i+1)}. {pasien.name} - {pasien.waktu_pengobatan}min\n"

    if buffer == "":
        buffer += "Tidak ada antrian\n"
    return f"Daftar antrian klinik {KLINIK[idxKlinik].nama}:\n{buffer}"

def buat_pasien(nama, tanggal_lahir):
    """ 
    Client-side awalnya 'tidak punya' akun pasien jadi tidak bisa daftar di klinik manapun
    (handle di client-side). Fungsi ini mengembalikan indeks dari pasien untuk digunakan 
    oleh client sebagai identifier.
    """
    return Pasien.tambah_pasien(Pasien(nama, tanggal_lahir))
    
if __name__ == "__main__":
    # server settings
    PORT = 6969;
    ADDRESS = "localhost"

    with SimpleXMLRPCServer((ADDRESS,PORT),requestHandler=RequestHandler, allow_none=True) as server:
        server.register_introspection_functions()
        
        # Register the methods of the ServerVoting class with the server
        server.register_function(cek_daftar_klinik)
        server.register_function(display_waktu_tunggu_pasien)
        server.register_function(daftar)
        server.register_function(cek_antrian_klinik)
        server.register_function(buat_pasien)

        print(f"Server sedang berjalan di {ADDRESS}:{PORT}")
        server.serve_forever()
