"""
punto1_orbitas.py

Punto 1: Exploracion de orbitas complejas bajo z_{n+1} = z_n^2 + c.
"""
import numpy as np


def explorar_orbita(c, max_iter=100, radio_escape=2.0, n_guardar=12):
    """
    Itera z_{n+1} = z_n^2 + c desde z_0 = 0.

    Retorna un diccionario con:
      escapo: bool
      iter_escape: int o None
      orbita: lista de los primeros n_guardar valores de z
      max_modulo: maximo |z_n| alcanzado en toda la iteracion
    """
    z = complex(0, 0)
    orbita = [z]
    max_modulo = abs(z)
    escapo = False
    iter_escape = None

    for n in range(1, max_iter + 1):
        z = z**2 + c
        modulo = abs(z)
        max_modulo = max(max_modulo, modulo)
        if len(orbita) < n_guardar:
            orbita.append(z)
        if modulo > radio_escape:
            escapo = True
            iter_escape = n
            break

    return {
        "c": c,
        "escapo": escapo,
        "iter_escape": iter_escape,
        "orbita": orbita,
        "max_modulo": max_modulo,
    }


def clasificar_comportamiento(resultado, tol=1e-3):
    """Clasificacion cualitativa simple para la columna 'comportamiento observado'."""
    if resultado["escapo"]:
        return f"Diverge (escapa en n={resultado['iter_escape']})"

    orbita = resultado["orbita"]
    ultimos = orbita[-6:]
    # punto fijo: los ultimos valores casi no cambian
    diffs = [abs(ultimos[i + 1] - ultimos[i]) for i in range(len(ultimos) - 1)]
    if all(d < tol for d in diffs):
        return f"Converge a punto fijo ~{ultimos[-1]:.4f}"

    # periodicidad simple: compara z_n con z_{n-2}
    if len(orbita) >= 4 and abs(orbita[-1] - orbita[-3]) < tol:
        return "Oscila (periodo 2 aparente)"

    return "Acotada, sin convergencia clara a punto fijo (posible cuasi-periodica)"


if __name__ == "__main__":
    valores_c = {
        "c1 = 0": complex(0, 0),
        "c2 = -1": complex(-1, 0),
        "c3 = 1": complex(1, 0),
        "c4 = -0.75+0.1i": complex(-0.75, 0.1),
        "c5 = -0.1+0.65i": complex(-0.1, 0.65),
    }

    print(f"{'c':<18}{'Escapa':<10}{'Iter. escape':<14}{'Max |z_n|':<12}Comportamiento")
    resultados = {}
    for nombre, c in valores_c.items():
        r = explorar_orbita(c, max_iter=100)
        resultados[nombre] = r
        comport = clasificar_comportamiento(r)
        it_esc = r["iter_escape"] if r["iter_escape"] is not None else "-"
        print(f"{nombre:<18}{str(r['escapo']):<10}{str(it_esc):<14}{r['max_modulo']:<12.4f}{comport}")
