"""
punto3_ampliaciones.py

Punto 3: Tres ampliaciones sucesivas cerca de la frontera del conjunto de Mandelbrot.
Region inicial: -0.80 <= Re(c) <= -0.70, 0.05 <= Im(c) <= 0.15  (valle de "seahorse").
"""
import time
import matplotlib.pyplot as plt
from mandelbrot_core import mandelbrot_grid, graficar_mandelbrot

RESOLUCION = 800
RADIO_ESCAPE = 2.0

# cada ampliacion hace zoom hacia una sub-region interesante de la anterior
AMPLIACIONES = [
    {"re_min": -0.80, "re_max": -0.70, "im_min": 0.05, "im_max": 0.15, "n_max": 200},
    {"re_min": -0.77, "re_max": -0.74, "im_min": 0.08, "im_max": 0.11, "n_max": 400},
    {"re_min": -0.7570, "re_max": -0.7450, "im_min": 0.0920, "im_max": 0.1040, "n_max": 800},
]

if __name__ == "__main__":
    fig, axes = plt.subplots(1, 3, figsize=(18, 6.5))
    registro = []

    for i, (ax, region) in enumerate(zip(axes, AMPLIACIONES), start=1):
        n_max = region["n_max"]
        t0 = time.time()
        tiempo_escape, extent = mandelbrot_grid(
            region["re_min"], region["re_max"], region["im_min"], region["im_max"],
            resolucion=RESOLUCION, n_max=n_max, radio_escape=RADIO_ESCAPE
        )
        dt = time.time() - t0
        graficar_mandelbrot(tiempo_escape, extent, n_max,
                             titulo=f"Ampliacion {i} (Nmax={n_max})", ax=ax, cmap="inferno")
        registro.append({
            "ampliacion": i,
            "re": (region["re_min"], region["re_max"]),
            "im": (region["im_min"], region["im_max"]),
            "resolucion": f"{RESOLUCION}x{RESOLUCION}",
            "n_max": n_max,
            "tiempo_s": round(dt, 3),
        })

    fig.suptitle("Ampliaciones sucesivas cerca de la frontera del conjunto de Mandelbrot",
                 fontsize=13)
    fig.tight_layout()
    fig.savefig("/home/claude/taller_caos/figuras/mandelbrot_ampliaciones.png", dpi=140)
    print("Guardado: figuras/mandelbrot_ampliaciones.png\n")

    print(f"{'Ampl.':<7}{'Re(c)':<24}{'Im(c)':<24}{'Resolucion':<13}{'Nmax':<7}{'Tiempo (s)'}")
    for r in registro:
        re_str = f"[{r['re'][0]}, {r['re'][1]}]"
        im_str = f"[{r['im'][0]}, {r['im'][1]}]"
        print(f"{r['ampliacion']:<7}{re_str:<24}{im_str:<24}{r['resolucion']:<13}{r['n_max']:<7}{r['tiempo_s']}")
