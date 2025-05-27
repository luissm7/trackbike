
import os
import json
import matplotlib.pyplot as plt

INPUT_JSON = "temp/data_tracks.json"
OUTPUT_DIR = "public/profile"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def draw_profile(slug, data):
    points = data["points"]
    if not points:
        print(f"⚠️ No hay puntos para el track {slug}.")
        return

    distances = [i * (data["km"] / (len(points) - 1)) for i in range(len(points))]

    plt.figure(figsize=(12, 5))
    plt.plot(distances, points, color='crimson', linewidth=2)
    plt.fill_between(distances, points, color='lightgrey', alpha=0.6)
    plt.title(f"Perfil de altitud - {data['name']}", fontsize=14)
    plt.xlabel("Distancia (km)")
    plt.ylabel("Altitud (m)")
    plt.grid(True)

    summary = (
        f"Distancia total: {data['km']} km | "
        f"Desnivel positivo: {data['elevation']} m | "
        f"Alt. máx: {data['alt_max']} m | "
        f"Alt. min: {data['alt_min']} m | "
    )
    plt.figtext(0.5, -0.05, summary, ha="center", fontsize=12, color="black")
    plt.tight_layout()

    output = os.path.join(OUTPUT_DIR, f"{slug}.png")
    plt.savefig(output, bbox_inches='tight')
    plt.close()
    print(f"✅ Imagen generada: {output}")

def main():
    if not os.path.exists(INPUT_JSON):
        print(f"⚠️ No se encontró el archivo {INPUT_JSON}.")
        return

    with open(INPUT_JSON, "r", encoding="utf-8") as f:
        tracks = json.load(f)
    
    for slug, data in tracks.items():
        if "points" not in data:
            print(f"⚠️ No hay puntos para el track {slug}.")
            continue
        draw_profile(slug, data)

if __name__ == "__main__":
    main()
