
import os
import gpxpy
import matplotlib.pyplot as plt
from geopy.distance import geodesic

INPUT_DIR = "public/tracks"
OUTPUT_DIR = "public/profile"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def procesar_gpx(nombre_archivo):
    ruta = os.path.join(INPUT_DIR, nombre_archivo)
    with open(ruta, "r", encoding="utf-8") as f:
        gpx = gpxpy.parse(f)

    elevaciones = []
    distancias = []
    total_distancia = 0
    desnivel_pos = 0
    desnivel_neg = 0
    prev_point = None

    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                elevaciones.append(point.elevation)
                if prev_point:
                    d = geodesic(
                        (prev_point.latitude, prev_point.longitude),
                        (point.latitude, point.longitude)
                    ).meters
                    total_distancia += d
                    delta = point.elevation - prev_point.elevation
                    if delta > 0:
                        desnivel_pos += delta
                    else:
                        desnivel_neg += abs(delta)
                distancias.append(total_distancia / 1000)
                prev_point = point

    distancia_km = round(total_distancia / 1000, 2)
    desnivel_pos = round(desnivel_pos)
    desnivel_neg = round(desnivel_neg)

    plt.figure(figsize=(12, 5))
    plt.plot(distancias, elevaciones, color='crimson', linewidth=2)
    plt.fill_between(distancias, elevaciones, color='lightgrey', alpha=0.6)
    plt.title(f"Perfil de altitud - {nombre_archivo}", fontsize=14)
    plt.xlabel("Distancia (km)")
    plt.ylabel("Altitud (m)")
    plt.grid(True)

    resumen = f"Distancia total: {distancia_km} km | Desnivel +: {desnivel_pos} m | Desnivel -: {desnivel_neg} m"
    plt.figtext(0.5, -0.05, resumen, ha="center", fontsize=12, color="black")
    plt.tight_layout()

    salida = os.path.join(OUTPUT_DIR, nombre_archivo.replace(".gpx", ".png"))
    plt.savefig(salida, bbox_inches='tight')
    plt.close()
    print(f"✅ Imagen generada: {salida}")

def main():
    archivos = [f for f in os.listdir(INPUT_DIR) if f.endswith(".gpx")]
    for archivo in archivos:
        procesar_gpx(archivo)

if __name__ == "__main__":
    main()
