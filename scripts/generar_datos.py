
import os
import shutil
import gpxpy
import json
from geopy.distance import geodesic

INPUT_DIR = "public/tracks"
GEOJSON_DIR = "public/geojson"
TS_OUTPUT_FILE = "src/data/tracks.ts"
JSON_OUTFILE_FILE = "temp/data_tracks.json"

if os.path.exists("temp"):
    shutil.rmtree("temp")
os.makedirs("temp", exist_ok=True)
os.makedirs(GEOJSON_DIR, exist_ok=True)

def clasificar_dificultad(km, desnivel):
    if km > 50 or desnivel > 1000:
        return "difícil"
    elif km > 20 or desnivel > 500:
        return "media"
    else:
        return "fácil"

def extract_track_data(filename):
    slug = filename.replace(".gpx", "")
    ruta = os.path.join(INPUT_DIR, filename)
    with open(ruta, "r", encoding="utf-8") as f:
        gpx = gpxpy.parse(f)

    track_name = gpx.tracks[0].name if gpx.tracks and gpx.tracks[0].name else slug.replace("-", " ").title()

    points = []
    total_distance = 0
    total_elevation_gain = 0
    alt_min = float("inf")
    alt_max = float("-inf")
    prev_point = None
    coods_geojson = []

    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                elev = point.elevation
                points.append(elev)
                alt_min = min(alt_min, elev)
                alt_max = max(alt_max, elev)
                coods_geojson.append([point.longitude, point.latitude, elev])
                if prev_point:
                    d = geodesic(
                        (prev_point.latitude, prev_point.longitude),
                        (point.latitude, point.longitude)
                    ).meters
                    total_distance += d
                    delta = elev - prev_point.elevation
                    if delta > 0:
                        total_elevation_gain += delta
                prev_point = point

    if not points:
        print(f"⚠️ No se encontraron puntos en el track {slug}.")
        return None, None

    geojson_data = {
        "type": "FeatureCollection",
        "features": [{
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": coods_geojson
            },
            "properties": {
                "name": track_name
            }
        }]
    }

    with open(os.path.join(GEOJSON_DIR, f"{slug}.geojson"), "w", encoding="utf-8") as f:
        json.dump(geojson_data, f, indent=2)

    km = round(total_distance / 1000, 2)
    return {
        "slug": slug,
        "name": track_name,
        "description": f"Ruta generada automáticamente para {slug}.",
        "km": km,
        "alt_min": round(alt_min),
        "alt_max": round(alt_max),
        "elevation": round(total_elevation_gain),
        "difficulty": clasificar_dificultad(km, total_elevation_gain),
        "points": points,
        "image": f"/profile/{slug}.png"
    }

def main():
    tracks = []
    track_json = {}

    files = [f for f in os.listdir(INPUT_DIR) if f.endswith(".gpx")]
    for archivo in files:
        data = extract_track_data(archivo)
        tracks.append({k: data[k] for k in data if k != "points"})
        track_json[data["slug"]] = data

    with open(TS_OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("export const tracks = ")
        json.dump(tracks, f, indent=2, ensure_ascii=False)
        f.write(";\n")

    with open(JSON_OUTFILE_FILE, "w", encoding="utf-8") as f:
        json.dump(track_json, f, indent=2, ensure_ascii=False)

    print(f"✅ Archivo de datos generado: {TS_OUTPUT_FILE}")
    print(f"✅ Archivo JSON generado: {JSON_OUTFILE_FILE}")

if __name__ == "__main__":
    main()
