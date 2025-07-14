from manajemen_barang import lihat_produk, tambah_produk, hapus_produk, sortir_produk, pilih_produk_untuk_pengiriman
from manajemen_kurir import tampilkan_daftar_kurir, rekrut_kurir, pecat_kurir, cari_kurir,load_data_kurir
from buat_pengiriman import proses_pengiriman, cek_status_pengiriman
from laporan_jadwal import laporan_jadwal_pengiriman
from laporan_keseluruhan import laporan_keseluruhan
from pelengkap import clear
import json

def menu_manajemen_barang():
    while True:
        clear()
        print(f"========================================")
        print(f"|      SUB MENU MANAJEMEN BARANG     |")
        print(f"========================================")
        print(f"| 1. Lihat Daftar Produk               |")
        print(f"| 2. Tambah Produk                     |")
        print(f"| 3. Hapus Produk                      |")
        print(f"| 4. Sortir Produk                     |")
        print(f"| 5. Pilih Barang untuk Dikirim        |")
        print(f"| 0. Kembali ke Menu Utama             |")
        print(f"========================================")

        pilihan = input("Pilih menu (0-5): ").strip()
        
        if pilihan == '1':
            lihat_produk()
        elif pilihan == '2':
            tambah_produk()
        elif pilihan == '3':
            hapus_produk()
        elif pilihan == '4':
            sortir_produk()
        elif pilihan == '5':
            pilih_produk_untuk_pengiriman()
        elif pilihan == '0':
            break
        else:
            print(f"Pilihan tidak valid.")
            input(f"Tekan Enter untuk melanjutkan...")

def menu_kurir():
    load_data_kurir()
    while True:
        clear()
        print(f"========================================")
        print(f"|      SUB MENU MANAJEMEN KURIR      |")
        print(f"========================================")
        print(f"| 1. Lihat Daftar Kurir                |")
        print(f"| 2. Rekrut Kurir                      |")
        print(f"| 3. Pecat Kurir                       |")
        print(f"| 4. Cari Kurir                        |")
        print(f"| 0. Kembali ke Menu Utama             |")
        print(f"========================================")
        pilihan = input("Pilih menu (0-4): ").strip()

        if pilihan == '1':
            tampilkan_daftar_kurir()
            input("\nTekan Enter untuk kembali...")
        elif pilihan == '2':
            rekrut_kurir()
            input("\nTekan Enter untuk kembali...")
        elif pilihan == '3':
            pecat_kurir()
            input("\nTekan Enter untuk kembali...")
        elif pilihan == '4':
            try:
                id_cari = int(input("Masukkan ID kurir yang dicari: "))
                hasil = cari_kurir(id_cari)  # Pastikan fungsi ini menerima target_id
                if hasil:
                    print("\nKurir Ditemukan:")
                    print(json.dumps(hasil, indent=2, ensure_ascii=False))
                else:
                    print("\nKurir tidak ditemukan.")
            except ValueError:
                print("[red]ID harus berupa angka![/red]")
            input("Tekan Enter untuk kembali...")
        elif pilihan == '0':
            break
        else:
            print(f"Pilihan tidak valid.")
            input(f"Tekan Enter untuk melanjutkan...")

def menu_pengiriman_barang():
    while True:
        clear()
        print(f"==========================================")
        print(f"|    SUB MENU BUAT PENGIRIMAN BARANG   |")
        print(f"==========================================")
        print(f"| 1. Buat Rute Pengiriman Optimal      |")
        print(f"| 0. Kembali ke Menu Utama             |")
        print(f"==========================================")

        pilihan = input("Pilih menu (0-1): ").strip()

        if pilihan == '1':
            proses_pengiriman()
        elif pilihan == '0':
            break
        else:
            print(f"Pilihan tidak valid.")
            input(f"Tekan Enter untuk melanjutkan...")

def tampilkan_menu():
    """
    Fungsi utama untuk menjalankan loop menu aplikasi.
    """
    while True:
        cek_status_pengiriman() 
        clear()
        
        print(f"========================================")
        print(f"|        DASHBOARD PENGIRIMAN        |")
        print(f"========================================")
        print(f"| 1. Manajemen Barang                  |")
        print(f"| 2. Manajemen Kurir                   |")
        print(f"| 3. Buat Pengiriman Barang            |")
        print(f"| 4. Laporan Jadwal Selesai            |")
        print(f"| 5. Laporan Keseluruhan (Urut Waktu)  |")
        print(f"| 0. Keluar                            |")
        print(f"========================================")

        pilihan = input("Pilih menu (0-5): ").strip()
        
        if pilihan == '1':
            menu_manajemen_barang()
        elif pilihan == '2':
            menu_kurir()
        elif pilihan == '3':
            menu_pengiriman_barang()
        elif pilihan == '4':
            laporan_jadwal_pengiriman()
        elif pilihan == '5':
            laporan_keseluruhan()
        elif pilihan == '0':
            print(f"Terima kasih telah menggunakan aplikasi ini. Sampai jumpa!")
            break
        else:
            print(f"Pilihan tidak valid.")
            input(f"Tekan Enter untuk melanjutkan...")
