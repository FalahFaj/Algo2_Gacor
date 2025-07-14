import json
import os
from datetime import datetime
import random
from pelengkap import clear

produk_list = []
file_produk = 'data_produk.json'
file_pengiriman = 'barang_dikirim.json'


def muat_data_produk():
    global produk_list
    try:
        with open(file_produk, 'r') as f:
            data = json.load(f)
        produk_list = data.get("produk", [])
        
        for p in produk_list:
            p["id"] = int(p.get("id", 0))
            if "berat" not in p:
                p["berat"] = "0"
            if "nama_produk" not in p:
                p["nama_produk"] = "Tidak Diketahui"
            if "alamat_pengiriman" not in p:
                p["alamat_pengiriman"] = "Tidak Diketahui"
            
    except FileNotFoundError:
        print(" File produk tidak ditemukan. Membuat data baru...")
        produk_list = []
    except json.JSONDecodeError:
        print("File produk rusak atau kosong.")
        produk_list = []
    except Exception as e:
        print(f"Gagal memuat data: {e}")
        produk_list = []

def simpan_data_produk():
    try:
        with open(file_produk, 'w') as f:
            json.dump({"produk": produk_list}, f, indent=2)
        print("Data produk berhasil disimpan.")
    except Exception as e:
        print(f"Gagal menyimpan data produk: {e}")

def tampilkan_daftar_produk():
    if not produk_list:
        return False

    print("{:<5} {:<25} {:<12} {:<35}".format("ID", "Nama Produk", "Berat (kg)", "Alamat Pengiriman"))
    print("-" * 80)
    for p in produk_list:
        id_produk = p.get('id', '?')
        nama = p.get('nama_produk', 'Tidak Diketahui')[:24]  
        berat = p.get('berat', 'N/A')
        alamat = p.get('alamat_pengiriman', 'Tidak Diketahui')[:34]  
        print("{:<5} {:<25} {:<12} {:<35}".format(id_produk, nama, berat, alamat))
    return True

def lihat_produk():
    muat_data_produk()
    clear()
    print("=== DAFTAR PRODUK ===")
    if not tampilkan_daftar_produk():
        print("Belum ada produk tersedia.")
    input("Tekan Enter untuk kembali...")

def tambah_produk():
    while True:
        muat_data_produk()
        clear()
        print("=== TAMBAH PRODUK ===")
        while True:
            nama = input("Masukkan nama produk: ").strip()
            if nama:
                break
            print("Nama produk tidak boleh kosong.")
        while True:
            try:
                berat_input = input("Masukkan berat (kg): ").strip()
                berat = float(berat_input)
                if berat < 0:
                    print("Berat tidak boleh negatif.")
                    continue
                break
            except ValueError:
                print("Berat harus berupa angka.")

        try:
            with open('data_kec&desa.json', 'r') as f:
                data_alamat = json.load(f)
            daftar_alamat = []
            for item in data_alamat.get("data_desa", []):
                kecamatan = item.get("kecamatan", "")
                for desa in item.get("desa", []):
                    nama_desa = desa.get("nama", "")
                    status = desa.get("status", "")
                    full_status = "Kelurahan" if status == "kelurahan" else "Desa"
                    alamat = f"{full_status} {nama_desa}, Kecamatan {kecamatan}"
                    daftar_alamat.append(alamat)
            if not daftar_alamat:
                alamat_pengiriman = "Alamat tidak tersedia"
            else:
                alamat_pengiriman = random.choice(daftar_alamat)
        except FileNotFoundError:
            alamat_pengiriman = "File data_kec&desa.json tidak ditemukan."
        except json.JSONDecodeError:
            alamat_pengiriman = "Format JSON salah atau file rusak."
        except Exception as e:
            alamat_pengiriman = f"Error saat baca alamat: {e}"

        new_id = max([p.get('id', 0) for p in produk_list], default=0) + 1
        produk_baru = {
            "id": new_id,
            "nama_produk": nama,
            "berat": str(berat),
            "alamat_pengiriman": alamat_pengiriman
        }
        produk_list.append(produk_baru)
        simpan_data_produk()
        print(f"Produk berhasil ditambahkan dengan alamat: {alamat_pengiriman}")

        lanjut = input("Apakah Anda ingin menambah produk lagi? (y/n): ").strip().lower()
        if lanjut not in ['y', 'yes', 'ya']:
            break

def hapus_produk():
    while True:
        muat_data_produk()
        clear()
        print("=== HAPUS PRODUK ===")
        if not produk_list:
            print("Belum ada produk tersedia.")
            input("Tekan Enter untuk kembali...")
            return
        tampilkan_daftar_produk()

        while True:
            try:
                id_hapus_str = input("Masukkan ID produk yang ingin dihapus (atau 0 untuk batal): ").strip()
                if id_hapus_str == "0":
                    print("Operasi dibatalkan.")
                    input("Tekan Enter untuk kembali...")
                    return
                if not id_hapus_str:
                    print("ID tidak boleh kosong.")
                    continue
                id_hapus = int(id_hapus_str)
                break
            except ValueError:
                print("ID harus berupa angka.")

        produk_ditemukan = None
        for i, p in enumerate(produk_list):
            if p["id"] == id_hapus:
                produk_ditemukan = (i, p)
                break

        if produk_ditemukan:
            index, produk = produk_ditemukan
            print(f"\nProduk yang akan dihapus:")
            print(f"  ID: {produk['id']}")
            print(f"  Nama: {produk['nama_produk']}")
            print(f"  Berat: {produk['berat']} kg")
            print(f"  Alamat: {produk['alamat_pengiriman']}")
            konfirmasi = input("\nApakah Anda yakin ingin menghapus? (y/n): ").strip().lower()
            if konfirmasi in ['y', 'yes', 'ya']:
                produk_list.pop(index)
                simpan_data_produk()
                print(f"Produk dengan ID {id_hapus} berhasil dihapus.")
            else:
                print("Penghapusan dibatalkan.")
        else:
            print("ID produk tidak ditemukan.")

        lanjut = input("\nApakah Anda ingin menghapus produk lagi? (y/n): ").strip().lower()
        if lanjut not in ['y', 'yes', 'ya']:
            break

def pilih_produk_untuk_pengiriman():
    while True:
        muat_data_produk()
        clear()
        print("=== PILIH PRODUK UNTUK DIKIRIM ===")
        if not produk_list:
            print("Belum ada produk tersedia untuk dikirim.")
            input("Tekan Enter untuk kembali...")
            return

        barang_akan_dikirim = []
        total_berat = 0.0

        while True:
            clear()
            print("Keranjang Pengiriman:")
            if barang_akan_dikirim:
                for item in barang_akan_dikirim:
                    print(f"  - {item['nama_produk']} ({item['berat']} kg)")
                print(f"  Total Berat: {total_berat:.2f} kg")
            else:
                print("  (Kosong)")

            print("\nDaftar Produk Tersedia:")
            if not tampilkan_daftar_produk():
                print("Tidak ada produk tersedia.")
                break

            try:
                id_pilih_str = input("\nMasukkan ID produk yang ingin dikirim (0 untuk selesai, -1 untuk batal): ").strip()
                if id_pilih_str == "":
                    continue
                id_pilih = int(id_pilih_str)
                if id_pilih == 0:
                    break
                elif id_pilih == -1:
                    print("Pengiriman dibatalkan.")
                    input("Tekan Enter...")
                    return

                ketemu = False
                for p in produk_list:
                    if p["id"] == id_pilih:
                        ketemu = True
                        if any(item["id"] == id_pilih for item in barang_akan_dikirim):
                            print(" Produk sudah dipilih sebelumnya.")
                        else:
                            try:
                                berat = float(p["berat"])
                            except (ValueError, TypeError):
                                print(f"Berat produk '{p['nama_produk']}' tidak valid. Menggunakan berat 0.")
                                berat = 0.0
                            barang_akan_dikirim.append(p.copy())
                            total_berat += berat
                            print(f"'{p['nama_produk']}' ditambahkan ke daftar pengiriman.")
                        break
                if not ketemu:
                    print("ID produk tidak ditemukan.")
                input("Tekan Enter untuk lanjut...")
            except ValueError:
                print("Masukkan ID yang valid (angka).")
                input("Tekan Enter...")

        if not barang_akan_dikirim:
            print("\nTidak ada produk yang dipilih. Proses dibatalkan.")
            input("Tekan Enter untuk kembali...")
            return

        if simpan_ke_pengiriman(barang_akan_dikirim, total_berat):
            id_barang_dikirim = {item['id'] for item in barang_akan_dikirim}
            produk_list[:] = [p for p in produk_list if p['id'] not in id_barang_dikirim]
            simpan_data_produk()
            print("\nBarang berhasil dijadwalkan untuk pengiriman.")
        else:
            print("\nGagal menyimpan data pengiriman. Produk tidak dipindahkan.")
        input("Tekan Enter untuk kembali...")

def simpan_ke_pengiriman(daftar_produk, total_berat):
    try:
        try:
            with open(file_pengiriman, 'r') as f:
                data_pengiriman = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data_pengiriman = {"paket": []}

        if "paket" not in data_pengiriman:
            data_pengiriman["paket"] = []

        id_paket_baru = str(len(data_pengiriman['paket']) + 1)
        tanggal_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M")
        paket_baru = {
            "id_paket": id_paket_baru,
            "items": daftar_produk,
            "total_berat_kg": round(total_berat, 2),
            "status": "dalam_pengiriman",
            "tanggal_pengiriman": tanggal_sekarang
        }

        data_pengiriman["paket"].append(paket_baru)

        with open(file_pengiriman, 'w') as f:
            json.dump(data_pengiriman, f, indent=2)
        print(f"Produk berhasil disimpan ke '{file_pengiriman}' dengan ID Paket: {id_paket_baru}")
        return True
    except Exception as e:
        print(f"Gagal menyimpan ke file pengiriman: {e}")
        return False
def sortir_produk():
    muat_data_produk()
    clear()
    print("\n=== SORTIR PRODUK ===")
    
    if not produk_list:
        print("Belum ada produk tersedia untuk disortir.")
        input("Tekan Enter untuk kembali...")
        return

    print("[1] Sortir berdasarkan berat (rendah → tinggi)")
    print("[2] Sortir berdasarkan alamat pengiriman (A-Z)")
    print("[3] Sortir berdasarkan ID produk (kecil → besar)")
    print("[0] Kembali")
    
    pilihan = input("Pilih opsi: ").strip()
    
    if pilihan == '1':
        n = len(produk_list)
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                try:
                    berat_j = float(produk_list[j]['berat'])
                    berat_min = float(produk_list[min_idx]['berat'])
                    if berat_j < berat_min:
                        min_idx = j
                except:
                    continue
            if min_idx != i:
                produk_list[i], produk_list[min_idx] = produk_list[min_idx], produk_list[i]
        print("Diurutkan berdasarkan berat.")

    elif pilihan == '2':
        n = len(produk_list)
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                alamat_j = str(produk_list[j].get('alamat_pengiriman', '')).lower()
                alamat_min = str(produk_list[min_idx].get('alamat_pengiriman', '')).lower()
                if alamat_j < alamat_min:
                    min_idx = j
            if min_idx != i:
                produk_list[i], produk_list[min_idx] = produk_list[min_idx], produk_list[i]
        print("Diurutkan berdasarkan alamat pengiriman.")

    elif pilihan == '3':
        n = len(produk_list)
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                try:
                    id_j = int(produk_list[j]['id'])
                    id_min = int(produk_list[min_idx]['id'])
                    if id_j < id_min:
                        min_idx = j
                except:
                    continue
            if min_idx != i:
                produk_list[i], produk_list[min_idx] = produk_list[min_idx], produk_list[i]
        print("Diurutkan berdasarkan ID produk.")
    elif pilihan == '0':
        return
    else:
        print("Pilihan tidak valid.")
        input("Tekan Enter...")
        return
    simpan_data_produk()
    clear()
    print("\n=== HASIL SORTIR ===")
    tampilkan_daftar_produk()
    input("\nTekan Enter untuk kembali...")

def total_berat_dari_file(file=file_pengiriman):
    try:
        with open(file, 'r') as f:
            data = json.load(f)
            paket = data.get("paket", [])
            if not paket:
                return 0.0
            return paket[-1].get("total_berat_kg", 0.0)
    except:
        return 0.0

def pilih_kurir():
    try:
        with open('data_kurir.json', 'r') as f:
            data = json.load(f)
        daftar_kurir = data.get("kurir", [])
        if not daftar_kurir:
            print("Tidak ada data kurir ditemukan.")
            return None
        kurir_tersedia = [k for k in daftar_kurir if k.get("status", "").lower() in ["kosong", "tersedia"]]
        if not kurir_tersedia:
            print("Semua kurir sedang dalam pengiriman. Silakan tunggu hingga ada yang tersedia.")
            return None
        print("\n=== PILIH KURIR YANG TERSEDIA ===")
        for idx, k in enumerate(kurir_tersedia, 1):
            print(f"{idx}. {k['nama_kurir']} | Kendaraan: {k['type_kendaraan']} | Kapasitas: {k['kapasitas']} kg")
        while True:
            try:
                pilihan = int(input("Pilih nomor kurir: "))
                if 1 <= pilihan <= len(kurir_tersedia):
                    kurir_terpilih = kurir_tersedia[pilihan - 1]
                    total_berat = total_berat_dari_file()
                    if float(kurir_terpilih["kapasitas"]) >= total_berat:
                        print(f"Pengiriman akan dilakukan oleh: {kurir_terpilih['nama_kurir']}")
                        return kurir_terpilih
                    else:
                        print(f"Kurir '{kurir_terpilih['nama_kurir']}' tidak cukup kapasitas.")
                        print(f"   Total berat: {total_berat} kg > {kurir_terpilih['kapasitas']} kg")
                else:
                    print("Nomor kurir tidak valid.")
            except ValueError:
                print("Masukkan angka yang sesuai.")
    except Exception as e:
        print(f" Gagal memilih kurir: {e}")
        return None
