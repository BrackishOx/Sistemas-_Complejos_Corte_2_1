"""
punto4_bifurcacion.py

Punto 4: Diagrama de bifurcacion del mapa logistico x_{n+1} = r*x_n*(1-x_n).
"""
import os
import numpy as np
import matplotlib.pyplot as plt


def diagrama_bifurcacion(r_min, r_max, n_r=5000, x0=0.5, n_iter=1500, transitorio=1000,
                           n_mostrar=500):
    """
    Para cada valor de r en [r_min, r_max] (n_r valores), itera el mapa logistico
    n_iter veces desde x0, descarta el transitorio, y retorna los n_mostrar valores
    finales de x (los que ya estan en el atractor).

    Vectorizado sobre r: se itera un vector de r's simultaneamente.
    """
    r_vals = np.linspace(r_min, r_max, n_r)
    x = np.full(n_r, x0)

    for _ in range(transitorio):
        x = r_vals * x * (1 - x)

    r_plot = np.repeat(r_vals, n_mostrar)
    x_plot = np.empty((n_mostrar, n_r))
    for i in range(n_mostrar):
        x = r_vals * x * (1 - x)
        x_plot[i] = x

    return r_plot, x_plot.T.flatten()


if __name__ == "__main__":
    os.makedirs("figuras", exist_ok=True)
    # --- diagrama completo ---
    r_full, x_full = diagrama_bifurcacion(2.5, 4.0, n_r=6000)

    fig, ax = plt.subplots(figsize=(11, 7))
    ax.plot(r_full, x_full, ',k', alpha=0.35)
    ax.set_xlabel("r")
    ax.set_ylabel("x (atractor)")
    ax.set_title("Diagrama de bifurcacion del mapa logistico (2.5 <= r <= 4.0)")
    ax.axvline(3.0, color='tab:blue', ls='--', lw=0.8, alpha=0.6)
    ax.axvline(3.44949, color='tab:green', ls='--', lw=0.8, alpha=0.6)
    ax.axvline(3.569946, color='tab:red', ls='--', lw=0.8, alpha=0.6)
    fig.tight_layout()
    fig.savefig("figuras/bifurcacion_completo.png", dpi=150)
    print("Guardado: figuras/bifurcacion_completo.png")

    # --- ampliacion 3.4 <= r <= 3.6 ---
    r_zoom, x_zoom = diagrama_bifurcacion(3.4, 3.6, n_r=6000)
    fig2, ax2 = plt.subplots(figsize=(11, 7))
    ax2.plot(r_zoom, x_zoom, ',k', alpha=0.35)
    ax2.set_xlabel("r")
    ax2.set_ylabel("x (atractor)")
    ax2.set_title("Diagrama de bifurcacion, ampliacion 3.4 <= r <= 3.6")
    fig2.tight_layout()
    fig2.savefig("figuras/bifurcacion_zoom.png", dpi=150)
    print("Guardado: figuras/bifurcacion_zoom.png")

    # --- ventana periodica dentro del caos (periodo 3 cerca de r=3.83) ---
    r_v3, x_v3 = diagrama_bifurcacion(3.7, 3.9, n_r=4000)
    fig3, ax3 = plt.subplots(figsize=(11, 6))
    ax3.plot(r_v3, x_v3, ',k', alpha=0.35)
    ax3.axvspan(3.8284, 3.8415, color='tab:orange', alpha=0.15, label='ventana periodo-3')
    ax3.set_xlabel("r")
    ax3.set_ylabel("x (atractor)")
    ax3.set_title("Region catica 3.7-3.9: ventana periodica (periodo 3) resaltada")
    ax3.legend()
    fig3.tight_layout()
    fig3.savefig("figuras/bifurcacion_ventana_periodica.png", dpi=150)
    print("Guardado: figuras/bifurcacion_ventana_periodica.png")
