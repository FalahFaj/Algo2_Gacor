import json
import os
from rich.console import Console
from rich.table import Table

console = Console()
file_path = "data_kurir.json"
data_kurir = {"kurir": []}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_data_kurir():
    global data_kurir
    try:
        with open(file_path, "r") as file:
            data_kurir = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        console.print("[yellow]Data tidak ditemukan atau rusak. Membuat data baru...[/yellow]")
        data_kurir = {"kurir": []}

def save_data():
    try:
        with open(file_path, "w") as file:
            json.dump(data_kurir, file, indent=2)
    except Exception as e:
        console.print(f"[red]Gagal menyimpan data: {e}[/red]")


def tampilkan_daftar_kurir():
    if not data_kurir["kurir"]:
        console.print("\n[yellow]Belum ada data kurir.[/yellow]")
        return

    table = Table(title="Daftar Kurir")
    table.add_column("ID", style="cyan", justify="center")
    table.add_column("Nama", style="bold yellow", justify="left")
    table.add_column("Kendaraan", style="magenta", justify="center")
    table.add_column("Kapasitas", style="bright_blue", justify="center")
    table.add_column("Status", style="bold red", justify="center")

    for k in data_kurir["kurir"]:
        warna_status = "green" if k['status'] == "aktif" else "red"
        table.add_row(
            str(k["id"]),
            k["nama_kurir"],
            k["type_kendaraan"],
            f"{k['kapasitas']} kg",
            f"[{warna_status}]{k['status']}[/{warna_status}]"
        )
    console.print(table)

def rekrut_kurir():
    nama = input("Nama Kurir: ").strip()
    kendaraan = input("Jenis Kendaraan (motor/mobil): ").strip().lower()

    if kendaraan not in ["motor", "mobil"]:
        console.print("[red]Kendaraan harus 'motor' atau 'mobil'[/red]")
        return

    kapasitas = 60 if kendaraan == "motor" else 200
    new_id = 1

    if data_kurir["kurir"]:
        new_id = max(k["id"] for k in data_kurir["kurir"]) + 1

    data_kurir["kurir"].append({
        "id": new_id,
        "nama_kurir": nama,
        "type_kendaraan": kendaraan,
        "kapasitas": kapasitas,
        "status": "kosong"
    })

    console.print(f"\n[green]Kurir '{nama}' berhasil direkrut dengan ID {new_id}.[/green]")
    save_data()

def pecat_kurir():
    tampilkan_daftar_kurir()
    try:
        id_hapus = int(input("Masukkan ID kurir yang ingin dipecat: "))
    except ValueError:
        console.print("[red]ID harus berupa angka![/red]")
        return

    for i, k in enumerate(data_kurir["kurir"]):
        if k["id"] == id_hapus:
            nama = k["nama_kurir"]
            konfirmasi = input(f"Yakin hapus kurir '{nama}'? (y/n): ").strip().lower()
            if konfirmasi == 'y':
                del data_kurir["kurir"][i]
                console.print(f"[green]Kurir {nama} berhasil dihapus.[/green]")
                atur_id()
                save_data()
            break
    else:
        console.print("[red]ID kurir tidak ditemukan.[/red]")

def atur_id():
    for idx, item in enumerate(data_kurir["kurir"], start=1):
        item["id"] = idx

def cari_kurir(id_yang_dicari):  
    load_data_kurir()
    daftar_kurir = data_kurir.get("kurir", [])
    
    low = 0
    high = len(daftar_kurir) - 1

    while low <= high:
        mid = (low + high) // 2
        current_id = daftar_kurir[mid]["id"]

        if current_id == id_yang_dicari:
            return daftar_kurir[mid]
        elif current_id < id_yang_dicari:
            low = mid + 1
        else:
            high = mid - 1

    console.print("[yellow]Kurir tidak ditemukan.[/yellow]")
    return None