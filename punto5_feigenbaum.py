"""
punto5_feigenbaum.py

Punto 5: Estimacion numerica de la constante de Feigenbaum a partir de una
busqueda de bifurcacion (bisection) sobre el mapa logistico.
"""
import os
import numpy as np
import matplotlib.pyplot as plt

DELTA_TEORICO = 4.669201609


def periodo_en_r(r, x0=0.5, transitorio=4000, tol=1e-6, periodo_max=128):
    """
    Determina el periodo del atractor del mapa logistico para un valor de r dado,
    comparando el estado tras el transitorio contra estados futuros.

    Se prueban periodos candidatos 1, 2, 4, 8, ..., periodo_max (potencias de 2,
    que es la unica cascada relevante para esta cascada de duplicacion).
    """
    x = x0
    for _ in range(transitorio):
        x = r * x * (1 - x)

    x_ref = x
    p = 1
    while p <= periodo_max:
        xp = x_ref
        for _ in range(p):
            xp = r * xp * (1 - xp)
        if abs(xp - x_ref) < tol:
            return p
        p *= 2
    return None  # no periodico (probablemente caotico) dentro del rango probado


def encontrar_bifurcacion(r_bajo, r_alto, periodo_bajo, transitorio=3000, tol_r=1e-10,
                            max_pasos=100):
    """
    Bisection: en r_bajo el periodo es periodo_bajo; en r_alto ya cambio
    (es 2*periodo_bajo o mayor). Se busca el punto de transicion.
    """
    for _ in range(max_pasos):
        r_mid = (r_bajo + r_alto) / 2
        p_mid = periodo_en_r(r_mid, transitorio=transitorio)
        if p_mid is not None and p_mid <= periodo_bajo:
            r_bajo = r_mid
        else:
            r_alto = r_mid
        if (r_alto - r_bajo) < tol_r:
            break
    return (r_bajo + r_alto) / 2


if __name__ == "__main__":
    os.makedirs("figuras", exist_ok=True)
    # brackets de busqueda: [r_donde_periodo_es_2^(k-1), r_donde_ya_es_2^k]
    # basados en inspeccion del diagrama de bifurcacion (busqueda progresiva)
    brackets = [
        (1, 2.98, 3.02),        # r1: nace periodo 2
        (2, 3.440, 3.455),      # r2: nace periodo 4
        (4, 3.5425, 3.547),     # r3: nace periodo 8
        (8, 3.5625, 3.5655),    # r4: nace periodo 16
        (16, 3.5680, 3.5690),   # r5: nace periodo 32
        (32, 3.5695, 3.5698),   # r6: nace periodo 64 (limite de precision esperado)
    ]

    r_n = {}
    print(f"{'n':<4}{'Periodo':<10}{'r_n estimado':<16}")
    for n, r_bajo, r_alto in brackets:
        try:
            r_est = encontrar_bifurcacion(r_bajo, r_alto, periodo_bajo=n,
                                            transitorio=4000, tol_r=1e-9)
            r_n[n] = r_est
            print(f"{n:<4}{n*2:<10}{r_est:<16.9f}")
        except Exception as e:
            print(f"{n:<4}{n*2:<10}FALLO: {e}")

    # --- calcular deltas ---
    periodos = sorted(r_n.keys())
    print(f"\n{'n':<4}{'r_n - r_(n-1)':<18}{'delta_n':<14}{'Error %':<10}")
    deltas = []
    for i in range(1, len(periodos) - 1):
        p_prev, p_cur, p_next = periodos[i - 1], periodos[i], periodos[i + 1]
        num = r_n[p_cur] - r_n[p_prev]
        den = r_n[p_next] - r_n[p_cur]
        if abs(den) < 1e-14:
            print(f"{i:<4}denominador ~0 (precision de punto flotante agotada)")
            continue
        delta = num / den
        error_pct = abs(delta - DELTA_TEORICO) / DELTA_TEORICO * 100
        deltas.append((i, delta, error_pct))
        print(f"{i:<4}{num:<18.3e}{delta:<14.6f}{error_pct:<10.3f}")

    # --- grafica delta_n vs n ---
    if deltas:
        ns = [d[0] for d in deltas]
        vals = [d[1] for d in deltas]
        fig, ax = plt.subplots(figsize=(8, 5.5))
        ax.plot(ns, vals, 'o-', color='#2563eb', label=r'$\delta_n$ estimado')
        ax.axhline(DELTA_TEORICO, color='tab:red', linestyle='--',
                   label=f'delta teorico = {DELTA_TEORICO}')
        ax.set_xlabel('n')
        ax.set_ylabel(r'$\delta_n$')
        ax.set_title('Convergencia de delta_n hacia la constante de Feigenbaum')
        ax.legend()
        fig.tight_layout()
        fig.savefig("figuras/feigenbaum_convergencia.png", dpi=150)
        print("\nGuardado: figuras/feigenbaum_convergencia.png")
