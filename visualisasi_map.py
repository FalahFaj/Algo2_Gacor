import folium

def visualisasi_map(simpul, jalur_mst, koordinat_desa,sisi):
    m = folium.Map(location=(-8.1706, 113.7004), zoom_start=11)

    for kec, desa in simpul:
        key = f"{kec} - ({desa})"
        if key in koordinat_desa:
            lat, lng = koordinat_desa[key]
            folium.Marker([lat, lng], popup=key).add_to(m)

    for u, v, jarak in jalur_mst:
        loc1 = koordinat_desa.get(f"{u[0]} - ({u[1]})")
        loc2 = koordinat_desa.get(f"{v[0]} - ({v[1]})")
        if loc1 and loc2:
            folium.PolyLine([loc1, loc2], color="blue", popup=f"{jarak:.2f} km").add_to(m)

    return m
