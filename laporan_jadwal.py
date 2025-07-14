import json
from datetime import datetime

def laporan_jadwal_pengiriman():
    try:
        with open('barang_dikirim.json', 'r') as f:
            data = json.load(f)

        paket_terkirim = [p for p in data.get("paket", []) if p.get("dikirim") is True]
        
        print("Laporan Jadwal Pengiriman yang Telah Selesai")
        print("=" * 60)
        
        if not paket_terkirim:
            print("Belum ada pengiriman yang selesai.")
        else:
            for p in paket_terkirim:
                try:
                    tgl = datetime.strptime(p['tanggal_pengiriman'], "%Y-%m-%d %H:%M")
                    tgl_str = tgl.strftime("%d %B %Y, %H:%M WIB")
                except ValueError:
                    tgl_str = p['tanggal_pengiriman'] 

                print(f"Paket ID: {p['id_paket']}")
                print(f" Tanggal Kirim : {tgl_str}")
                print(f" Tujuan        :")
                
                for tujuan in p["items"]:
                    if isinstance(tujuan, dict):
                        alamat = tujuan.get("alamat_pengiriman", "Tidak diketahui")
                        nama_produk = tujuan.get("nama_produk", "Produk tidak dikenali")
                        print(f"   - {nama_produk} → {alamat}")
                    else:
                        print(f"   - {tujuan}")

                print(f"  Estimasi     : {p['estimasi_waktu_menit']:.2f} menit")

                kurir = p.get("kurir", {})
                if kurir:
                    nama_kurir = kurir.get("nama_kurir", "-")
                    kendaraan = kurir.get("type_kendaraan", "-")
                    print(f" Kurir         : {nama_kurir} ({kendaraan})")
                else:
                    print(" Kurir         : Tidak tersedia")

                print("-" * 60)

    except FileNotFoundError:
        print("[red]File 'barang_dikirim.json' tidak ditemukan.[/red]")
    except json.JSONDecodeError:
        print("[red]File 'barang_dikirim.json' rusak atau bukan format JSON valid.[/red]")
    except Exception as e:
        print(f"[red]Terjadi kesalahan saat memuat laporan: {e}[/red]")

    input("Tekan Enter untuk kembali ke menu...")