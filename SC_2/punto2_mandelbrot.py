"""
punto2_mandelbrot.py

Punto 2: Construccion del conjunto de Mandelbrot sobre
-2.0 <= Re(c) <= 1.0, -1.5 <= Im(c) <= 1.5, resolucion 800x800,
para Nmax en {50, 100, 200, 500}.
"""
import time
import matplotlib.pyplot as plt
from mandelbrot_core import mandelbrot_grid, graficar_mandelbrot

REGION = dict(re_min=-2.0, re_max=1.0, im_min=-1.5, im_max=1.5)
RESOLUCION = 800
RADIO_ESCAPE = 2.0
VALORES_NMAX = [50, 100, 200, 500]

if __name__ == "__main__":
    fig, axes = plt.subplots(2, 2, figsize=(13, 13))
    tiempos = {}

    for ax, n_max in zip(axes.flat, VALORES_NMAX):
        t0 = time.time()
        tiempo_escape, extent = mandelbrot_grid(**REGION, resolucion=RESOLUCION, n_max=n_max,
                                                  radio_escape=RADIO_ESCAPE)
        dt = time.time() - t0
        tiempos[n_max] = dt
        graficar_mandelbrot(tiempo_escape, extent, n_max,
                             titulo=f"Nmax = {n_max}  (t = {dt:.2f}s)", ax=ax)
        print(f"Nmax={n_max:<5} tiempo={dt:.2f}s")

    fig.suptitle(f"Conjunto de Mandelbrot, resolucion {RESOLUCION}x{RESOLUCION}, "
                 f"radio de escape={RADIO_ESCAPE}", fontsize=13)
    fig.tight_layout()
    fig.savefig("/home/claude/taller_caos/figuras/mandelbrot_nmax_comparacion.png", dpi=140)
    print("\nGuardado: figuras/mandelbrot_nmax_comparacion.png")

    # figura individual grande para Nmax=100 (la version "principal" pedida)
    tiempo_escape, extent = mandelbrot_grid(**REGION, resolucion=RESOLUCION, n_max=100,
                                              radio_escape=RADIO_ESCAPE)
    fig2, ax2 = graficar_mandelbrot(tiempo_escape, extent, 100,
                                      titulo="Conjunto de Mandelbrot (Nmax=100, 800x800)")
    fig2.savefig("/home/claude/taller_caos/figuras/mandelbrot_principal.png", dpi=150)
    print("Guardado: figuras/mandelbrot_principal.png")
