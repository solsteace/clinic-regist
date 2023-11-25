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
        pass


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

    def __init__(self, name):
        self.name = name
        self.nomor_antrean = -1;
        self.nomor_rekor_medis = -1;
        self.waktu_pengobatan = -1;
        self.klinik_perawatan = None;
        Pasien.tambah_pasien(self)

    def get_waktu_antrian(self):
        if(self.klinik_perawatan != None):
            return "Silakan tunggu " \
                f"{self.klinik_perawatan._get_waktu_antrian(self.nomor_antrean)} menit lagi"
        return "Anda tidak terdaftar di klinik manapun!"

    def get_daftar_pasien(self):
        pass

# Initial condition (Usahakan nama disini sinkron sama client.py)
NAMA_KLINIK = ["Nusa Harapan", "Do'a Ibu", "Pasti Bugar" ]
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
    pasien = Pasien.get_pasien(idxPasien)
    return pasien.get_waktu_antrian()

def daftar(idxPasien, klinik):
    """
    Mendaftarkan pasien di klinik tertentu
    Parameter:
    pasien: Pasien
    klinik: Klinik
    """
    pass

    
def cek_antrian_klinik(klinik):
    """ 
    Mengembalikan string berisi info tentang daftar pasien yang mengantre di klinik tersebut
    Parameter:
    klinik: Klinik
    """ 
    pass

def buat_pasien(nama):
    """ 
    Client-side awalnya 'tidak punya' akun pasien jadi tidak bisa daftar di klinik manapun
    (handle di client-side). Fungsi ini mengembalikan indeks dari pasien untuk digunakan 
    oleh client sebagai identifier.
    """
    return Pasien.tambah_pasien(Pasien(nama))
    
if __name__ == "__main__":
    # server settings
    PORT = 6969;
    ADDRESS = "127.0.0.1"

    # Contoh pemakaian
    p1 = buat_pasien("Sumarno")
    p2 = buat_pasien("Budiono")
    p3 = buat_pasien("Sujono")

    KLINIK[1].register(Pasien.get_pasien(p1));
    KLINIK[1].register(Pasien.get_pasien(p2));
    KLINIK[1].register(Pasien.get_pasien(p3));

    print(cek_daftar_klinik())
    print(Pasien.get_pasien(p1).get_waktu_antrian())
    print(Pasien.get_pasien(p2).get_waktu_antrian())
    print(Pasien.get_pasien(p3).get_waktu_antrian())
