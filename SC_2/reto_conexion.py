"""
reto_conexion.py

Reto: conexion entre el conjunto de Mandelbrot (eje real) y las bifurcaciones
del mapa logistico, via la transformacion c = (r/2)*(1 - r/2).
"""
import numpy as np
import matplotlib.pyplot as plt
from mandelbrot_core import mandelbrot_grid

# valores de r encontrados en el punto 5 (nacimiento de cada periodo)
R_BIFURCACION = {
    1: 2.997401405,
    2: 3.448504316,
    4: 3.543695727,
    8: 3.564251178,
    16: 3.568698510,
    32: 3.569668324,
}


def r_a_c(r):
    return (r / 2) * (1 - r / 2)


def periodo_mandelbrot_real(c, transitorio=4000, tol=1e-5, periodo_max=128):
    """
    Analogo de periodo_en_r pero iterando z_{n+1}=z_n^2+c sobre el eje real
    (z, c reales), para comparar contra el periodo del mapa logistico.
    """
    z = 0.0
    for _ in range(transitorio):
        z = z**2 + c
        if abs(z) > 1e6:
            return None  # diverge, no aplica nocion de periodo
    z_ref = z
    p = 1
    while p <= periodo_max:
        zp = z_ref
        for _ in range(p):
            zp = zp**2 + c
        if abs(zp - z_ref) < tol:
            return p
        p *= 2
    return None


if __name__ == "__main__":
    # se usan valores de r ligeramente DENTRO de cada ventana periodica (no
    # exactamente en el punto de bifurcacion, donde el periodo es ambiguo por
    # definicion -- ahi ocurre "critical slowing down" y la convergencia al
    # atractor se vuelve arbitrariamente lenta).
    r_ventanas = sorted(R_BIFURCACION.items())
    r_demo = {}
    for i, (periodo_log, r_n) in enumerate(r_ventanas):
        if i + 1 < len(r_ventanas):
            r_siguiente = r_ventanas[i + 1][1]
            r_demo[periodo_log] = r_n + 0.3 * (r_siguiente - r_n)
        else:
            r_demo[periodo_log] = r_n + 0.3 * (3.57 - r_n)

    print(f"{'periodo (logistico)':<22}{'r (dentro de la ventana)':<26}{'c=r/2*(1-r/2)':<18}{'periodo (Mandelbrot)'}")
    filas = []
    for periodo_anterior, r in r_demo.items():
        periodo_real_logistico = 2 * periodo_anterior  # el periodo YA ocurrio la transicion
        c = r_a_c(r)
        periodo_mb = periodo_mandelbrot_real(c, transitorio=4000)
        filas.append((periodo_real_logistico, r, c, periodo_mb))
        print(f"{periodo_real_logistico:<22}{r:<26.6f}{c:<18.6f}{periodo_mb}")

    coincide = all(p_log == p_mb for p_log, _, _, p_mb in filas if p_mb is not None)
    print(f"\n¿Coinciden todos los periodos? {coincide}")

    # --- grafica: eje real del Mandelbrot con marcas en los c encontrados ---
    tiempo_escape, extent = mandelbrot_grid(-2.0, 0.4, -0.05, 0.05, resolucion=1200,
                                              n_max=300)
    fig, ax = plt.subplots(figsize=(11, 3.2))
    ax.imshow(tiempo_escape, extent=extent, origin='lower', cmap='magma', aspect='auto')
    for periodo_log, r, c, periodo_mb in filas:
        ax.axvline(c, color='cyan', lw=1, alpha=0.8)
        ax.text(c, 0.03, f'p={periodo_log}', color='cyan', fontsize=8,
                ha='center', rotation=90)
    ax.set_xlabel('Re(c)')
    ax.set_ylabel('Im(c)')
    ax.set_title('Eje real del conjunto de Mandelbrot con los puntos de bifurcacion '
                 'del mapa logistico transformados (c = r/2 (1-r/2))')
    fig.tight_layout()
    fig.savefig("/home/claude/taller_caos/figuras/reto_conexion.png", dpi=150)
    print("\nGuardado: figuras/reto_conexion.png")
