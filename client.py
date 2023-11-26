from xmlrpc.client import ServerProxy

client = ServerProxy('http://localhost:6969')

idxKlinik = -1
idxPasien = -1

print("Selamat Datang di Antrean Registrasi Medis")

while True:
    print("============ Menu ============")
    print("1. Lihat daftar klinik buka")
    print("2. Registrasi ke klinik")
    print("3. Lihat daftar antrean suatu klinik")
    print("4. Lihat waktu tunggu")
    print("0. Keluar")

    print("------------------------------")
    menu = int(input("Pilih Menu : "))
    print("------------------------------")

    if (menu == 1):
        print(client.cek_daftar_klinik())
        print("------------------------------")
    elif (menu == 2):
        print(client.cek_daftar_klinik())
        print("------------------------------")
        idxKlinik = int(input("Pilih nomor klinik tujuan registrasi: ")) - 1
        nama_pasien = input("Masukkan nama Anda: ")
        tgl_lahir_pasien = input("Masukkan tanggal lahir anda (dd-mm-yyyy): ")
        idxPasien = client.buat_pasien(nama_pasien, tgl_lahir_pasien)
        result = client.daftar(idxPasien, idxKlinik)
        print("------------------------------")
        print(result)
        print("------------------------------")
    elif (menu == 3):
        print(client.cek_daftar_klinik())
        print("------------------------------")
        idxKlinik = int(input("Pilih nomor klinik yang ingin dicek antriannya: ")) - 1
        print("------------------------------")
        print(client.cek_antrian_klinik(idxKlinik))
        print("------------------------------")
    elif menu == 4:
        print("------------------------------")
        print(client.display_waktu_tunggu_pasien(idxPasien))
        print("------------------------------")
    elif (menu == 0):
        break
    else:
        print("Menu Tidak Tersedia")

    print("")
