import tkinter as tk
import webbrowser
from tkinter import messagebox, ttk
import json
import folium

def tampilkan_peta(file_path, html, jalur_mst, jalur_mst_kruskal, total_jarak, total_jarak_kruskal, estimasi_waktu_pengiriman):
    with open(file_path, 'w') as f:
        f.write(html._repr_html_())
        def open_map():
            webbrowser.open_new_tab(file_path)

        root = tk.Tk()
        root.title("Visualisasi MST Desa")

        frame = ttk.Frame(root, padding=20)
        frame.grid(row=0, column=0, sticky="nsew")

        label = ttk.Label(frame, text="Visualisasi Minimum Spanning Tree (MST) Desa", font=("Arial", 14))
        label.grid(row=0, column=0, columnspan=2, pady=(0, 10))

        btn_open_map = ttk.Button(frame, text="Buka Peta MST", command=open_map)
        btn_open_map.grid(row=1, column=0, pady=10, sticky="ew")

        def estimasi_waktu():
            if estimasi_waktu_pengiriman >= 60:
                jam = int(estimasi_waktu_pengiriman // 60)
                menit = estimasi_waktu_pengiriman % 60
                return f"{jam} jam {menit:.2f} menit"
            else:
                return f"{estimasi_waktu_pengiriman:.2f} menit"

        def show_mst():
            mst_text = "\n".join([f"{desa1} <--> {desa2} : {jarak}" for desa1, desa2, jarak in jalur_mst])
            messagebox.showinfo("Jalur MST (Prim)", f"{mst_text}\nTotal jarak minimum\t: {total_jarak}\nEstimasi waktu pengiriman\t: {estimasi_waktu()}")

        btn_show_mst = ttk.Button(frame, text="Tampilkan Jalur MST (Prim)", command=show_mst)
        btn_show_mst.grid(row=2, column=0, pady=10, sticky="ew")

        def show_mst_kruskal():
            mst_text = "\n".join([f"{desa1} <--> {desa2} : {jarak}" for desa1, desa2, jarak in jalur_mst_kruskal])
            messagebox.showinfo("Jalur MST (Kruskal)", f"{mst_text}\nTotal jarak minimum\t: {total_jarak_kruskal}\nEstimasi waktu pengiriman\t: {estimasi_waktu()}")

        btn_show_mst_kruskal = ttk.Button(frame, text="Tampilkan Jalur MST (Kruskal)", command=show_mst_kruskal)
        btn_show_mst_kruskal.grid(row=3, column=0, pady=10, sticky="ew")

        btn_exit = ttk.Button(frame, text="Keluar", command=root.destroy)
        btn_exit.grid(row=4, column=0, pady=10, sticky="ew")
        root.mainloop()
        