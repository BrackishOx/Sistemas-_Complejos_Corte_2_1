# Taller Computacional: Caos, Conjunto de Mandelbrot y Universalidad de Feigenbaum

Sistemas Complejos — Universidad Sergio Arboleda

## Integrantes

- Juan Pablo Beltrán Santana
- Santiago Alejandro Céspedes Daza
- Jhonatan David Valdés González

## Descripción

Este taller explora cómo reglas iterativas simples pueden producir estructuras
fractales y comportamiento caótico, mediante dos experimentos computacionales
conectados entre sí:

1. **Construcción y exploración del conjunto de Mandelbrot**, incluyendo el
   análisis de órbitas complejas individuales y ampliaciones sucesivas de su
   frontera fractal.
2. **Estimación numérica de la constante universal de Feigenbaum** a partir
   del diagrama de bifurcación del mapa logístico.

El informe completo (`Taller_Caos_Mandelbrot_Feigenbaum.pdf`) documenta la
metodología, los resultados y el análisis de los 5 puntos del taller, el reto
de conexión Mandelbrot–logístico, y la pregunta integradora.

## Contenido del repositorio

| Archivo | Contenido |
|---|---|
| `Taller_Caos_Mandelbrot_Feigenbaum.pdf` | Informe completo con resultados, tablas y análisis |
| `mandelbrot_core.py` | Motor vectorizado (NumPy) para calcular el conjunto de Mandelbrot |
| `punto1_orbitas.py` | Exploración de órbitas complejas individuales |
| `punto2_mandelbrot.py` | Construcción del conjunto de Mandelbrot con distintos Nmax |
| `punto3_ampliaciones.py` | Ampliaciones sucesivas de una región fractal |
| `punto4_bifurcacion.py` | Diagrama de bifurcación del mapa logístico |
| `punto5_feigenbaum.py` | Estimación numérica de la constante de Feigenbaum |
| `reto_conexion.py` | Verificación de la conexión Mandelbrot–mapa logístico |
| `build_pdf.py` | Genera el informe PDF a partir de las figuras |
| `figuras/` | Todas las gráficas generadas (PNG) |
| `requirements.txt` | Dependencias necesarias |

## Cómo ejecutar

Requisitos: Python 3.10+.

```bash
pip install -r requirements.txt
```

Cada script se ejecuta de forma independiente y guarda sus figuras en `figuras/`
(la carpeta se crea automáticamente si no existe):

```bash
python punto1_orbitas.py
python punto2_mandelbrot.py
python punto3_ampliaciones.py
python punto4_bifurcacion.py
python punto5_feigenbaum.py
python reto_conexion.py
```

Para regenerar el informe en PDF a partir de las figuras ya generadas:

```bash
python build_pdf.py
```

## Resumen de resultados

- **Órbitas complejas**: c=0 y c=−1 permanecen acotadas (punto fijo y periodo 2
  respectivamente); c=1 diverge en 3 iteraciones; los puntos cercanos a la
  frontera del conjunto escapan de forma cada vez más lenta.
- **Conjunto de Mandelbrot**: construido sobre una grilla 800×800, comparando
  Nmax ∈ {50, 100, 200, 500} y con tres ampliaciones sucesivas que muestran
  autosimilitud aproximada en la frontera fractal.
- **Constante de Feigenbaum**: estimada mediante búsqueda progresiva con
  bisección sobre los puntos de bifurcación del mapa logístico, obteniendo
  δ ≈ 4.59–4.74 (error entre 0.8% y 1.8% respecto al valor teórico
  4.669201609).
- **Reto**: se verificó numéricamente que la transformación c=(r/2)(1−r/2)
  hace coincidir exactamente los periodos del mapa logístico con los del
  conjunto de Mandelbrot sobre el eje real (6/6 casos verificados).

## Declaración de uso de herramientas

El desarrollo de los scripts, la depuración numérica y la redacción del
informe se apoyaron en Claude (Anthropic) como asistente de programación y
escritura. El equipo revisó y comprende el código entregado.
