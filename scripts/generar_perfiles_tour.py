import os
import json
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

INPUT_JSON = "temp/data_tracks.json"
OUTPUT_DIR = "public/profile_beautiful"
os.makedirs(OUTPUT_DIR, exist_ok=True)

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 11,
    "axes.edgecolor": "white",
    "axes.labelcolor": "white",
    "xtick.color": "white",
    "ytick.color": "white",
    "text.color": "white",
})

def dibujar_perfil(slug, data):
    points = data["points"]
    if not points:
        print(f"⚠️  No hay points para {slug}, se omite el perfil.")
        return

    distancias = np.linspace(0, data["km"], num=len(points))

    fig, ax = plt.subplots(figsize=(14, 5), dpi=100)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    ax.plot(distancias, points, color="black", linewidth=2.5, zorder=2)
    ax.fill_between(distancias, points, min(points), color="#d21e26", alpha=0.7, zorder=1)

    for i in range(10, int(data["km"]) + 1, 10):
        ax.axvline(i, color='gray', linestyle='--', linewidth=0.5, zorder=0)

    ax.set_title(f"{data['name'].upper()} — PERFIL DE ETAPA", fontsize=16, weight="bold", pad=20, loc="left")

    ax.set_yticks([])
    ax.set_xticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    resumen = (
        f"{data['km']} km | Alt. máx: {data['alt_max']} m | Alt. mín: {data['alt_min']} m | "
        f"+{data['elevation']} m"
    )
    fig.text(0.5, 0.02, resumen, ha="center", fontsize=12, weight="bold", color="#333333")

    plt.tight_layout()
    output_path = os.path.join(OUTPUT_DIR, f"{slug}_estilo_tour.png")
    plt.savefig(output_path, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close()
    print(f"✅ Imagen generada: {output_path}")

def main():
    if not os.path.exists(INPUT_JSON):
        print(f"❌ No se encontró el archivo: {INPUT_JSON}")
        return

    with open(INPUT_JSON, "r", encoding="utf-8") as f:
        rutas = json.load(f)

    for slug, data in rutas.items():
        dibujar_perfil(slug, data)

if __name__ == "__main__":
    main()