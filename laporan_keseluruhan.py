from datetime import datetime
import json
from pelengkap import clear

def laporan_keseluruhan():
    try:
        with open('barang_dikirim.json', 'r') as f:
            data = json.load(f)
            paket_list = data.get("paket", [])

            if not paket_list:
                print("\nTidak ada data pengiriman.")
                return
            n = len(paket_list)
            for i in range(n):
                min_idx = i
                for j in range(i + 1, n):
                    waktu_j = paket_list[j].get('estimasi_waktu_menit', float('inf'))
                    waktu_min = paket_list[min_idx].get('estimasi_waktu_menit', float('inf'))

                    if waktu_j < waktu_min:
                        min_idx = j

                paket_list[i], paket_list[min_idx] = paket_list[min_idx], paket_list[i]
            print("\n=========== LAPORAN KESELURUHAN PENGIRIMAN ===========")
            for paket in paket_list:
                print(f"\nPaket ID      : {paket['id_paket']}")
                print(f"Tanggal Kirim : {paket['tanggal_pengiriman']}")
                print(f"Estimasi Waktu: {paket.get('estimasi_waktu_menit', 0)} menit")     

                if "jarak_total_km" in paket:
                    print(f"Jarak Total   : {paket.get('jarak_total_km', 0)} km")
                elif "total_berat_kg" in paket:
                    print(f"Total Berat   : {paket.get('total_berat_kg', 0)} kg")
                tujuan = paket.get("items", [])
                print("Tujuan        :")
                for t in tujuan:
                    if type(t) == dict:
                        print(f"   - {t.get('nama_produk', '')} ke {t.get('alamat_pengiriman', '')}")
                    else:
                        print(f"   - {t}")
                kurir = paket.get("kurir")
                if kurir:
                    print(f"Kurir         : {kurir.get('nama_kurir', '-')}")
                    print(f"   Kendaraan     : {kurir.get('type_kendaraan', '-')} ({kurir.get('kapasitas_kg', '?')} kg)")
                dikirim = paket.get("dikirim", False)
                status_label = "Selesai" if dikirim else "Dalam pengiriman"
                print(f"Status        : {status_label}")
                print("------------------------------------------------")
    except Exception as e:
        print(f" Gagal memuat laporan: {e}")
    input("\nTekan Enter untuk kembali ke menu...")
