from datetime import datetime, timedelta
from threading import Timer
from tkinter import messagebox, ttk
import tkinter as tk
import webbrowser
import folium
from collections import defaultdict
from pelengkap import buka_json, clear
from visualisasi_map import visualisasi_map
from manajemen_barang import muat_data_produk
from mst_gui import tampilkan_peta as gui_peta
from manajemen_barang import pilih_kurir
import json

jarak_desa = {}
data_desa = None
data_jarak = None

def muat_data():
    global data_desa, data_jarak
    data_desa = buka_json('data_kec&desa.json')
    data_jarak = buka_json('jarak_desa_lengkap.json')
    parse_jarak(data_jarak)

def parse_jarak(data_jarak):
    global jarak_desa
    jarak_desa = {}
    for key, value in data_jarak["jarak"].items():
        try:
            bagian1, bagian2 = key.split(" -> ")
            kec1, desa1 = bagian1.split(" - (")
            kec2, desa2 = bagian2.split(" - (")
            desa1 = desa1.rstrip(")")
            desa2 = desa2.rstrip(")")
            k1 = (kec1.strip(), desa1.strip())
            k2 = (kec2.strip(), desa2.strip())
            jarak = float(value)
            jarak_desa[(k1, k2)] = jarak
            jarak_desa[(k2, k1)] = jarak  
        except Exception as e:
            print(f"Gagal parsing: {key} | Error: {e}")
    return jarak_desa

def mst_kruskal(simpul, sisi):
    if not sisi or not simpul:
        return [], 0
    parent = {node: node for node in simpul}
    rank = {node: 0 for node in simpul}
    def find(u):
        if parent[u] != u:
            parent[u] = find(parent[u])
        return parent[u]
    def union(u, v):
        root_u = find(u)
        root_v = find(v)
        if root_u != root_v:
            if rank[root_u] > rank[root_v]:
                parent[root_v] = root_u
            else:
                parent[root_u] = root_v
                if rank[root_u] == rank[root_v]:
                    rank[root_v] += 1
    n = len(sisi)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if sisi[j][0] < sisi[min_idx][0]:
                min_idx = j
        sisi[i], sisi[min_idx] = sisi[min_idx], sisi[i]
    mst = []
    total_jarak = 0
    for weight, u, v in sisi:
        if find(u) != find(v):
            union(u, v)
            mst.append((u, v, weight))
            total_jarak += weight
    return mst, total_jarak

def mst_prim(simpul, sisi):
    if not sisi or not simpul:
        return [], 0
    mst = []
    total_jarak = 0
    visited = set([simpul[0]])
    while len(visited) < len(simpul):
        min_weight = float('inf')
        min_edge = None
        for weight, u, v in sisi:
            if (u in visited and v not in visited) or (v in visited and u not in visited):
                if weight < min_weight:
                    min_weight = weight
                    min_edge = (u, v)
        if min_edge:
            u, v = min_edge
            mst.append((u, v, min_weight))
            total_jarak += min_weight
            visited.add(u)
            visited.add(v)
    return mst, total_jarak

def pilih_desa():
    muat_data()
    if not data_desa or "data_desa" not in data_desa:
        print(" Data desa belum dimuat.")
        return []
    semua_pilihan = []
    titik_awal = ("Rambipuji", "Rambipuji") 
    while True:
        clear()
        print("\n=== DAFTAR KECAMATAN ===")
        daftar_kecamatan = [item['kecamatan'] for item in data_desa.get('data_desa', [])]
        for idx, kec in enumerate(daftar_kecamatan, 1):
            print(f"[{idx}] {kec}")
        print("[0] Selesai")
        try:
            pilihan_kec = input("Pilih kecamatan (masukkan nomor): ").strip()
            if pilihan_kec == "0":
                break  

            idx_kec = int(pilihan_kec) - 1
            if not (0 <= idx_kec < len(daftar_kecamatan)):
                raise ValueError("Nomor kecamatan tidak valid.")
            kecamatan_terpilih = daftar_kecamatan[idx_kec]
        except Exception as e:
            print(f"Pilihan tidak valid. Error: {e}")
            input("Tekan Enter untuk lanjut...")
            continue
        desa_dalam_kec = None
        for item in data_desa.get("data_desa", []):
            if item["kecamatan"] == kecamatan_terpilih:
                desa_dalam_kec = item["desa"]
                break
        if not desa_dalam_kec:
            print("Tidak ada desa dalam kecamatan ini.")
            input("Tekan Enter untuk lanjut...")
            continue

        while True:
            clear()
            print(f"\n=== DESA DI KECAMATAN {kecamatan_terpilih} ===")
            for i, desa in enumerate(desa_dalam_kec, 1):
                print(f"{i}. {desa['nama']}")
            print("\n[0] Kembali ke Daftar Kecamatan")
            pilihan_des = input("Pilih nomor desa (atau 'ex' untuk kembali): ").strip()
            if pilihan_des.lower() == "ex" or pilihan_des == "0":
                break  
            try:
                indeks = int(pilihan_des) - 1
                if 0 <= indeks < len(desa_dalam_kec):
                    nama_desa = desa_dalam_kec[indeks]['nama']
                    entry = (kecamatan_terpilih, nama_desa)

                    if entry in semua_pilihan:
                        print(" Desa sudah dipilih sebelumnya.")
                    else:
                        semua_pilihan.append(entry)
                        print(f"Desa '{nama_desa}' ditambahkan!")
                else:
                    print("Nomor desa tidak valid.")
            except ValueError:
                print("Input tidak valid.")

            lanjut = input("Ingin tambah desa lain di kecamatan ini? (y/n): ").strip().lower()
            if lanjut != "y":
                break
        tambah_lagi = input("Mau pilih desa dari kecamatan lain? (y/n): ").strip().lower()
        if tambah_lagi != "y":
            if titik_awal not in semua_pilihan:
                semua_pilihan.insert(0, titik_awal)
                print(f"Titik awal pengiriman ditambahkan: {titik_awal[1]}, Kecamatan {titik_awal[0]}")
    if semua_pilihan:
        print("\nDesa yang Dipilih:")
        for kec, desa in semua_pilihan:
            print(f"- {desa}, Kecamatan {kec}")
    else:
        print(" Belum ada desa yang dipilih.")
    return semua_pilihan

def hitung_estimasi(jarak_total_km, kecepatan_kmh=40):
    if jarak_total_km <= 0 or kecepatan_kmh <= 0:
        return 0
    return (jarak_total_km / kecepatan_kmh) * 60 

def cek_status_pengiriman(file_paket='barang_dikirim.json', kecepatan_kmh=40):
    try:
        with open(file_paket, 'r') as f:
            data = json.load(f)

        perubahan = False
        for paket in data.get("paket", []):
            if paket.get("dikirim") is True:
                continue

            tgl_pengiriman = datetime.strptime(paket["tanggal_pengiriman"], "%Y-%m-%d %H:%M")
            estimasi_menit = hitung_estimasi(paket["jarak_total_km"], kecepatan_kmh)
            waktu_selesai = tgl_pengiriman + timedelta(minutes=estimasi_menit)

            if datetime.now() >= waktu_selesai:
                paket["status"] = "selesai"
                paket["dikirim"] = True
                perubahan = True
                print(f" Paket {paket['id_paket']} telah selesai.")

                try:
                    with open('data_kurir.json', 'r') as fk:
                        data_kurir = json.load(fk)

                    id_kurir = str(paket["kurir"]["id_kurir"])
                    for kurir in data_kurir.get("kurir", []):
                        if str(kurir.get("id")) == id_kurir:
                            kurir["status"] = "kosong"
                            break

                    with open('data_kurir.json', 'w') as fk:
                        json.dump(data_kurir, fk, indent=2)

                except Exception as e:
                    print(f"Gagal update status kurir: {e}")

        if perubahan:
            with open(file_paket, 'w') as f:
                json.dump(data, f, indent=2)

    except Exception as e:
        print(f"[ERROR] Gagal memperbarui status pengiriman: {e}")


def tandai_sudah_dikirim(id_paket):
    def update_status():
        try:
            with open('barang_dikirim.json', 'r+') as f:
                data = json.load(f)

            for paket in data.get("paket", []):
                if paket["id_paket"] == id_paket:
                    paket["status"] = "selesai"
                    paket["dikirim"] = True
                    break

            with open('barang_dikirim.json', 'w') as f:
                json.dump(data, f, indent=2)

            print(f"Paket {id_paket} ditandai sebagai selesai.")
        except Exception as e:
            print(f"Gagal update status: {e}")

    try:
        with open('barang_dikirim.json', 'r') as f:
            data = json.load(f)
        for paket in data.get("paket", []):
            if paket["id_paket"] == id_paket:
                estimasi_menit = paket.get("estimasi_waktu_menit", 15)
                Timer(estimasi_menit * 60, update_status).start()
                break
    except Exception as e:
        print(f"Gagal baca file: {e}")


def proses_pengiriman():
    muat_data()
    if not data_desa or "data_desa" not in data_desa:
        print("Data desa tidak tersedia.")
        return

    print(f"=== PEMILIHAN DESA ===")
    desa_terpilih = pilih_desa()
    
    if not desa_terpilih or len(desa_terpilih) < 1:
        print(" Minimal 1 desa harus dipilih.")
        return

    koordinat_desa = {}
    for item in data_desa.get('data_desa', []):
        kec = item.get('kecamatan', '')
        for d in item.get('desa', []):
            kunci = f"{kec} - ({d.get('nama', '')})"
            lat = d.get('latitude')
            lng = d.get('longitude')
            if lat is not None and lng is not None:
                koordinat_desa[kunci] = (float(lat), float(lng))

    sisi = []
    for i in range(len(desa_terpilih)):
        for j in range(i + 1, len(desa_terpilih)):
            d1 = desa_terpilih[i]
            d2 = desa_terpilih[j]

            weight = jarak_desa.get((d1, d2)) or jarak_desa.get((d2, d1))

            if weight is not None:
                sisi.append((weight, d1, d2))
            else:
                print(f"Tidak ada data jarak untuk: {d1[1]} <-> {d2[1]}")

    if not sisi and len(desa_terpilih) > 1:
        print("Tidak ada sisi yang terbentuk. Pastikan data jarak lengkap.")
        return

    if len(desa_terpilih) == 1:
        print("\n Pengiriman hanya ke satu lokasi:")
        print(f"- {desa_terpilih[0][1]}, Kecamatan {desa_terpilih[0][0]}")
        print("Tidak perlu jalur MST karena hanya satu tujuan.")
        return

    jalur_mst_prim, total_prim = mst_prim(desa_terpilih, sisi)
    jalur_mst_kruskal, total_kruskal = mst_kruskal(desa_terpilih, sisi)
    map_prim = visualisasi_map(desa_terpilih, jalur_mst_prim, koordinat_desa, sisi)
    if not map_prim:
        print(" Gagal membuat peta.")
        return

    map_file = 'mst_map.html'
    map_prim.save(map_file)
    estimasi_menit = (total_prim / 40) * 60  
    jam = int(estimasi_menit // 60)
    menit = round(estimasi_menit % 60, 2)

    kurir_terpilih = pilih_kurir()
    if not kurir_terpilih:
        print(" Tidak ada kurir yang dipilih. Proses pengiriman dibatalkan.")
        return
    try:
        with open('data_kurir.json', 'r') as f:
            data_kurir = json.load(f)

        for k in data_kurir.get("kurir", []):
            if k["id"] == kurir_terpilih["id"]:
                k["status"] = "aktif"
                kurir_terpilih["status"] = "aktif"
                break

        with open('data_kurir.json', 'w') as f:
            json.dump(data_kurir, f, indent=2)

    except Exception as e:
        print(f"Gagal mengupdate status kurir: {e}")
        return


    try:
        with open('barang_dikirim.json', 'r') as f:
            data_pengiriman = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data_pengiriman = {"paket": []}

    id_paket_baru = str(len(data_pengiriman['paket']) + 1).zfill(4)
    paket_baru = {
        "id_paket": id_paket_baru,
        "items": [f"{d[1]}, {d[0]}" for d in desa_terpilih],  
        "jarak_total_km": total_prim,
        "estimasi_waktu_menit": estimasi_menit,
        "tanggal_pengiriman": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "status": "dalam_pengiriman",
        "dikirim": False,
        "kurir": {
            "id_kurir": kurir_terpilih["id"],
            "nama_kurir": kurir_terpilih["nama_kurir"],
            "type_kendaraan": kurir_terpilih["type_kendaraan"],
            "kapasitas_kg": float(kurir_terpilih["kapasitas"]),
            "status_kurir": kurir_terpilih["status"]
        }
    }

    data_pengiriman["paket"].append(paket_baru)

    with open('barang_dikirim.json', 'w') as f:
        json.dump(data_pengiriman, f, indent=2)

    print(f"Estimasi waktu pengiriman: {jam} jam {menit} menit")
    print(f"Paket disimpan dengan ID '{id_paket_baru}' dan dikirim oleh {kurir_terpilih['nama_kurir']}.")

    try:
        from mst_gui import tampilkan_peta
        tampilkan_peta(
            file_path='mst_map.html',
            html=map_prim,
            jalur_mst=jalur_mst_prim,
            jalur_mst_kruskal=jalur_mst_kruskal,
            total_jarak=total_prim,
            total_jarak_kruskal=total_kruskal,
            estimasi_waktu_pengiriman=estimasi_menit
        )
    except Exception as e:
        print(f"Gagal menjalankan GUI: {e}")