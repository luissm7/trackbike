
import os
import gpxpy
import json
from geopy.distance import geodesic

INPUT_DIR = "public/tracks"
OUTPUT_FILE = "src/data/tracks.ts"

def clasificar_dificultad(km, desnivel):
    if km > 50 or desnivel > 1000:
        return "difícil"
    elif km > 20 or desnivel > 500:
        return "media"
    else:
        return "fácil"

def extraer_datos(nombre_archivo):
    slug = nombre_archivo.replace(".gpx", "")
    ruta = os.path.join(INPUT_DIR, nombre_archivo)
    with open(ruta, "r", encoding="utf-8") as f:
        gpx = gpxpy.parse(f)

    elevaciones = []
    total_distancia = 0
    desnivel_pos = 0
    alt_min = float("inf")
    alt_max = float("-inf")
    prev_point = None

    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                elev = point.elevation
                elevaciones.append(elev)
                alt_min = min(alt_min, elev)
                alt_max = max(alt_max, elev)
                if prev_point:
                    d = geodesic(
                        (prev_point.latitude, prev_point.longitude),
                        (point.latitude, point.longitude)
                    ).meters
                    total_distancia += d
                    delta = elev - prev_point.elevation
                    if delta > 0:
                        desnivel_pos += delta
                prev_point = point

    km = round(total_distancia / 1000, 2)
    return {
        "slug": slug,
        "nombre": slug.replace("-", " ").title(),
        "descripcion": f"Ruta generada automáticamente para {slug}.",
        "km": km,
        "alt_min": round(alt_min),
        "alt_max": round(alt_max),
        "desnivel": round(desnivel_pos),
        "dificultad": clasificar_dificultad(km, desnivel_pos),
        "imagen": f"/perfiles/{slug}.png"
    }

def main():
    rutas = []
    archivos = [f for f in os.listdir(INPUT_DIR) if f.endswith(".gpx")]
    for archivo in archivos:
        rutas.append(extraer_datos(archivo))

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("export const rutas = ")
        json.dump(rutas, f, indent=2, ensure_ascii=False)
        f.write(";\n")
    print(f"✅ Archivo de datos generado: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
