"""
mandelbrot_core.py

Motor vectorizado (NumPy) para construir el conjunto de Mandelbrot.
Usado por punto2_mandelbrot.py y punto3_ampliaciones.py.
"""
import numpy as np
import matplotlib.pyplot as plt


def mandelbrot_grid(re_min, re_max, im_min, im_max, resolucion, n_max, radio_escape=2.0):
    """
    Calcula el tiempo de escape para cada punto c de una grilla resolucion x resolucion
    sobre la region [re_min,re_max] x [im_min,im_max].

    Implementacion vectorizada: se itera z = z^2 + c sobre TODO el arreglo a la vez,
    y se guarda en que iteracion escapo cada punto (los que nunca escapan quedan con
    valor n_max, que es como se pintan como "dentro" del conjunto).
    """
    re = np.linspace(re_min, re_max, resolucion)
    im = np.linspace(im_min, im_max, resolucion)
    C = re[np.newaxis, :] + 1j * im[:, np.newaxis]

    Z = np.zeros_like(C)
    tiempo_escape = np.full(C.shape, n_max, dtype=int)
    activos = np.ones(C.shape, dtype=bool)  # puntos que aun no han escapado

    for n in range(1, n_max + 1):
        Z[activos] = Z[activos] ** 2 + C[activos]
        escaparon_ahora = activos & (np.abs(Z) > radio_escape)
        tiempo_escape[escaparon_ahora] = n
        activos &= ~escaparon_ahora
        if not activos.any():
            break

    return tiempo_escape, (re_min, re_max, im_min, im_max)


def graficar_mandelbrot(tiempo_escape, extent, n_max, titulo=None, ax=None, cmap="magma"):
    if ax is None:
        fig, ax = plt.subplots(figsize=(7, 7))
    else:
        fig = ax.figure

    im = ax.imshow(tiempo_escape, extent=extent, origin="lower", cmap=cmap,
                    interpolation="bilinear")
    ax.set_xlabel("Re(c)")
    ax.set_ylabel("Im(c)")
    ax.set_aspect("equal")
    ax.set_title(titulo or f"Conjunto de Mandelbrot (Nmax={n_max})")
    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("Iteraciones hasta escape")
    return fig, ax
