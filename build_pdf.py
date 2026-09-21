# -*- coding: utf-8 -*-
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak,
    Table, TableStyle, HRFlowable
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT

FIG = "figuras"
OUT = "Taller_Caos_Mandelbrot_Feigenbaum.pdf"

styles = getSampleStyleSheet()

title_style = ParagraphStyle('TitleCustom', parent=styles['Title'], fontSize=18,
                              spaceAfter=6, textColor=colors.HexColor('#1a1a2e'))
subtitle_style = ParagraphStyle('Subtitle', parent=styles['Normal'], fontSize=11.5,
                                 alignment=TA_CENTER, textColor=colors.HexColor('#555555'),
                                 spaceAfter=4)
h1 = ParagraphStyle('H1Custom', parent=styles['Heading1'], fontSize=14,
                     spaceBefore=14, spaceAfter=6, textColor=colors.HexColor('#16213e'))
h2 = ParagraphStyle('H2Custom', parent=styles['Heading2'], fontSize=11.3,
                     spaceBefore=9, spaceAfter=4, textColor=colors.HexColor('#0f3460'))
body = ParagraphStyle('BodyCustom', parent=styles['Normal'], fontSize=9.7,
                       leading=13.6, alignment=TA_LEFT, spaceAfter=6)
bullet = ParagraphStyle('BulletCustom', parent=body, leftIndent=13, bulletIndent=4,
                         spaceAfter=4)
caption = ParagraphStyle('Caption', parent=styles['Normal'], fontSize=8.3,
                          alignment=TA_CENTER, textColor=colors.HexColor('#666666'),
                          spaceBefore=3, spaceAfter=10, fontName='Helvetica-Oblique')
qa = ParagraphStyle('QA', parent=body, leftIndent=10, spaceAfter=7)

story = []

story.append(Spacer(1, 0.4 * inch))
story.append(Paragraph("Taller Computacional: Caos, Conjunto de Mandelbrot y "
                        "Universalidad de Feigenbaum", title_style))
story.append(Paragraph("Sistemas Complejos", subtitle_style))
story.append(Spacer(1, 0.15 * inch))
story.append(HRFlowable(width="55%", thickness=1, color=colors.HexColor('#0f3460'),
                         hAlign='CENTER'))
story.append(Spacer(1, 0.15 * inch))
story.append(Paragraph("Santiago Céspedes — Universidad Sergio Arboleda", subtitle_style))
story.append(Spacer(1, 0.2 * inch))

story.append(Paragraph("Punto 1 — Exploración de órbitas complejas", h1))
story.append(Paragraph(
    "Se implementó la iteración z<sub>n+1</sub> = z<sub>n</sub><super>2</super> + c desde z<sub>0</sub> = 0, "
    "registrando si la órbita escapa, en qué iteración, el máximo módulo alcanzado, y "
    "los primeros valores de la sucesión (100 iteraciones, radio de escape 2).", body))

t1 = Table([
    ["c", "¿Escapa?", "Iter. escape", "Máx |z_n|", "Comportamiento observado"],
    ["0", "No", "—", "0.0000", "Converge al punto fijo z=0"],
    ["−1", "No", "—", "1.0000", "Oscila entre 0 y −1 (periodo 2)"],
    ["1", "Sí", "3", "5.0000", "Diverge rápidamente"],
    ["−0.75+0.1i", "Sí", "33", "2.7044", "Diverge lento (cerca de la frontera)"],
    ["−0.1+0.65i", "Sí", "75", "3.0023", "Diverge muy lento (muy cerca de la frontera)"],
], colWidths=[1.0*inch, 0.7*inch, 0.85*inch, 0.75*inch, 2.4*inch])
t1.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f3460')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,-1), 8.2),
    ('ALIGN', (0,0), (3,-1), 'CENTER'),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cccccc')),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f4f4f4')]),
    ('TOPPADDING', (0,0), (-1,-1), 5), ('BOTTOMPADDING', (0,0), (-1,-1), 5),
]))
story.append(t1)
story.append(Spacer(1, 8))

story.append(Paragraph("<b>a) ¿Qué diferencia existe entre una órbita acotada, una periódica y una divergente?</b>", body))
story.append(Paragraph(
    "Una órbita <b>acotada</b> permanece siempre dentro de un radio finito sin necesariamente "
    "repetirse (puede ser cuasi-periódica o incluso caótica pero limitada). Una órbita "
    "<b>periódica</b> es un caso particular de acotada donde los valores se repiten "
    "exactamente cada cierto número de pasos (ej. c=−1 alterna 0→−1→0→−1...). Una órbita "
    "<b>divergente</b> no está acotada: su módulo crece sin límite (en la práctica, una vez "
    "|z|&gt;2 para este mapa, crece muy rápido hacia infinito).", qa))

story.append(Paragraph("<b>b) ¿Por qué superar un módulo de 2 permite detener la iteración?</b>", body))
story.append(Paragraph(
    "Se puede demostrar que si |z<sub>n</sub>| &gt; 2 y |c| ≤ 2, entonces "
    "|z<sub>n+1</sub>| = |z<sub>n</sub><super>2</super> + c| ≥ |z<sub>n</sub>|<super>2</super> − |c| &gt; |z<sub>n</sub>|<super>2</super> − 2 "
    "&gt; |z<sub>n</sub>|(|z<sub>n</sub>|−2)+ ... crece geométricamente sin cota: una vez "
    "cruzado ese umbral, la sucesión ya no puede regresar a la región acotada. Por eso 2 es "
    "un radio de escape seguro y suficiente para todo el dominio relevante de c "
    "(el conjunto de Mandelbrot está contenido en el disco |c|≤2).", qa))

story.append(Paragraph("<b>c) ¿Es posible asegurar computacionalmente que un punto pertenece al conjunto con un número finito de iteraciones?</b>", body))
story.append(Paragraph(
    "No de forma definitiva. Un número finito de iteraciones solo permite confirmar que un "
    "punto <b>no</b> pertenece al conjunto (si escapa). Si tras N iteraciones no ha escapado, "
    "solo se puede afirmar que \"no escapó en las primeras N iteraciones\" — podría escapar en "
    "la iteración N+1, o nunca. La pertenencia exacta al conjunto (garantía de que la órbita "
    "jamás escapará) requeriría, en general, infinitas iteraciones; por eso las imágenes "
    "computacionales son siempre una aproximación que mejora con Nmax.", qa))

story.append(PageBreak())

story.append(Paragraph("Punto 2 — Construcción del conjunto de Mandelbrot", h1))
story.append(Image(f"{FIG}/mandelbrot_principal.png", width=4.3*inch, height=4.3*inch))
story.append(Paragraph("Figura 1. Conjunto de Mandelbrot, región [−2.0,1.0]×[−1.5,1.5], "
                        "800×800, Nmax=100, radio de escape=2.", caption))

story.append(Image(f"{FIG}/mandelbrot_nmax_comparacion.png", width=6.3*inch,
                    height=6.3*inch*(1200/1200)))
story.append(Paragraph("Figura 2. Comparación para Nmax ∈ {50, 100, 200, 500}, misma región "
                        "y resolución.", caption))

for q, a in [
    ("¿Qué cambia cuando aumenta el número máximo de iteraciones?",
     "La silueta general del conjunto (el interior grande, ya bien definido desde Nmax=50) "
     "casi no cambia; lo que cambia es el <b>detalle en la frontera</b>: con más iteraciones se "
     "revelan filamentos y estructuras cada vez más finas que antes se clasificaban "
     "erróneamente como \"dentro\" del conjunto por escapar demasiado lento para ser detectadas "
     "con pocas iteraciones."),
    ("¿En qué regiones se presenta el mayor detalle?",
     "Exclusivamente en la <b>frontera</b> del conjunto (los filamentos, antenas y la unión "
     "entre bulbos). El interior (siempre acotado) y el exterior lejano (escapa casi de "
     "inmediato) se ven prácticamente idénticos sin importar Nmax."),
    ("¿Por qué la frontera parece tener una complejidad mayor que el interior?",
     "Porque la frontera es, literalmente, un <b>fractal</b>: contiene estructura a todas las "
     "escalas (Punto 3). El interior es una región de estabilidad donde las órbitas convergen "
     "de forma predecible; la frontera es donde el comportamiento pasa de \"acotado\" a "
     "\"divergente\" de forma arbitrariamente sensible al valor exacto de c."),
    ("¿La imagen obtenida es exactamente el conjunto matemático? Justifique.",
     "No. Es una <b>aproximación</b> en dos sentidos: (1) resolución finita — cada píxel "
     "representa un solo valor de c, no un área continua; y (2) Nmax finito — como se discutió "
     "en 1(c), puntos que tardan más de Nmax iteraciones en escapar se clasifican erróneamente "
     "como parte del conjunto. El conjunto matemático real es el límite cuando resolución→∞ y "
     "Nmax→∞."),
]:
    story.append(Paragraph(f"<b>{q}</b>", body))
    story.append(Paragraph(a, qa))

story.append(PageBreak())

story.append(Paragraph("Punto 3 — Ampliación de una región fractal", h1))
story.append(Image(f"{FIG}/mandelbrot_ampliaciones.png", width=6.5*inch,
                    height=6.5*inch*(650/1800)))
story.append(Paragraph("Figura 3. Tres ampliaciones sucesivas en el valle \"seahorse\" "
                        "(cerca de Re(c)≈−0.75).", caption))

t3 = Table([
    ["Ampliación", "Límites (Re, Im)", "Resolución", "Nmax", "Tiempo (s)"],
    ["1", "[−0.80,−0.70] × [0.05,0.15]", "800×800", "200", "1.11"],
    ["2", "[−0.77,−0.74] × [0.08,0.11]", "800×800", "400", "1.76"],
    ["3", "[−0.757,−0.745] × [0.092,0.104]", "800×800", "800", "2.51"],
], colWidths=[0.8*inch, 2.6*inch, 1.0*inch, 0.6*inch, 0.9*inch])
t3.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f3460')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,-1), 8.3),
    ('ALIGN', (0,0), (0,-1), 'CENTER'), ('ALIGN', (2,0), (-1,-1), 'CENTER'),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cccccc')),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f4f4f4')]),
    ('TOPPADDING', (0,0), (-1,-1), 5), ('BOTTOMPADDING', (0,0), (-1,-1), 5),
]))
story.append(t3)
story.append(Spacer(1, 8))

for q, a in [
    ("¿Se observan estructuras semejantes a diferentes escalas?",
     "Sí: en las tres ampliaciones aparecen espirales y \"mini-Mandelbrots\" con la misma "
     "forma general (cuerpo cardioide + bulbos) que el conjunto completo, cada vez más "
     "amplificados."),
    ("¿Las estructuras son copias exactas o aproximadas?",
     "Son <b>aproximadas</b>, no copias exactas (autosimilitud cuasi-, no estricta). El "
     "conjunto de Mandelbrot no es estrictamente autosimilar como un fractal generado por "
     "un IFS (p. ej. el triángulo de Sierpinski): cada \"mini-Mandelbrot\" tiene decoraciones "
     "y proporciones ligeramente distintas."),
    ("¿Qué relación existe entre resolución, número de iteraciones y tiempo de ejecución?",
     "El tiempo escala aproximadamente de forma lineal con el número de píxeles "
     "(resolución<super>2</super>) y con Nmax en el peor caso (todos los puntos usan todas las "
     "iteraciones); en la práctica es menor porque muchos puntos escapan pronto. Al hacer "
     "zoom, casi todos los puntos quedan cerca de la frontera (escapan lento o no escapan), "
     "por lo que el costo efectivo se acerca al peor caso — de ahí que la Ampliación 3 "
     "(Nmax=800) tome más del doble que la Ampliación 1 (Nmax=200)."),
    ("¿Por qué el conjunto constituye un ejemplo de complejidad emergente?",
     "Porque una regla local extremadamente simple (una sola multiplicación y una suma "
     "compleja, iterada) genera, sin ninguna instrucción explícita para hacerlo, estructura "
     "geométrica infinitamente detallada e imposible de anticipar por inspección de la "
     "fórmula — la complejidad no está \"programada\", emerge de la iteración."),
]:
    story.append(Paragraph(f"<b>{q}</b>", body))
    story.append(Paragraph(a, qa))

story.append(PageBreak())

story.append(Paragraph("Punto 4 — Diagrama de bifurcación del mapa logístico", h1))
story.append(Image(f"{FIG}/bifurcacion_completo.png", width=6.5*inch,
                    height=6.5*inch*(870/1400)))
story.append(Paragraph("Figura 4. Diagrama completo, 2.5≤r≤4.0, 6000 valores de r, "
                        "1500 iteraciones (1000 de transitorio descartado), últimos 500 "
                        "valores graficados por r. Líneas verticales: r=3.0 (azul, nace "
                        "periodo 2), r≈3.449 (verde, nace periodo 4), r≈3.570 (rojo, "
                        "inicio del caos).", caption))

story.append(Image(f"{FIG}/bifurcacion_zoom.png", width=6.2*inch,
                    height=6.2*inch*(870/1400)))
story.append(Paragraph("Figura 5. Ampliación 3.4≤r≤3.6: se distinguen los ciclos de "
                        "periodo 2, 4, 8, 16 y el inicio del caos.", caption))

story.append(Image(f"{FIG}/bifurcacion_ventana_periodica.png", width=6.2*inch,
                    height=6.2*inch*(700/1400)))
story.append(Paragraph("Figura 6. Región caótica 3.7≤r≤3.9 con la ventana periódica "
                        "(periodo 3) resaltada cerca de r≈3.83.", caption))

story.append(Paragraph("Identificación de regímenes:", h2))
for txt in [
    "<b>Punto fijo:</b> 2.5 ≤ r &lt; 3.0 — una sola rama.",
    "<b>Periodo 2:</b> 3.0 ≤ r &lt; 3.449 — la rama se bifurca en dos.",
    "<b>Periodo 4:</b> 3.449 ≤ r &lt; 3.544.",
    "<b>Periodo 8:</b> 3.544 ≤ r &lt; 3.564.",
    "<b>Periodo 16:</b> 3.564 ≤ r &lt; 3.569 (ver Punto 5 para valores precisos).",
    "<b>Inicio del caos:</b> r ≈ 3.5699 (punto de Feigenbaum), donde se acumulan infinitas "
    "duplicaciones de periodo en un intervalo finito de r.",
    "<b>Ventana periódica dentro del caos:</b> periodo 3 visible cerca de r≈3.83-3.84 "
    "(Fig. 6) — una \"isla\" de orden dentro de la región caótica.",
]:
    story.append(Paragraph("• " + txt, bullet))

story.append(Paragraph("<b>¿Por qué deben descartarse las primeras iteraciones?</b>", body))
story.append(Paragraph(
    "Las primeras iteraciones corresponden al <b>transitorio</b>: la trayectoria partiendo de "
    "x<sub>0</sub>=0.5 aún no ha convergido al atractor (el conjunto de valores que el sistema visita a "
    "largo plazo). Graficar estas iteraciones mezclaría el camino de aproximación —que "
    "depende de la condición inicial arbitraria— con el comportamiento asintótico real del "
    "sistema, que es lo que el diagrama busca mostrar y que no depende de x<sub>0</sub>.", qa))

story.append(PageBreak())

story.append(Paragraph("Punto 5 — Estimación de la constante universal de Feigenbaum", h1))
story.append(Paragraph(
    "Se implementó un procedimiento numérico de <b>búsqueda progresiva con bisección</b>: "
    "para cada r se determina el periodo del atractor comparando el estado tras un "
    "transitorio (4000 iteraciones) contra su valor futuro para periodos candidatos "
    "1,2,4,8,...,128; luego se hace bisección sobre r entre un punto donde el periodo es "
    "2<super>k-1</super> y otro donde ya es mayor, para ubicar la transición con precisión ~10<super>-9</super>.", body))

t5 = Table([
    ["n", "Periodo", "r_n estimado", "r_n − r_(n-1)", "δ_n", "Error %"],
    ["1", "2", "2.997401405", "—", "—", "—"],
    ["2", "4", "3.448504316", "4.511e-01", "4.7389", "1.49%"],
    ["3", "8", "3.543695727", "9.519e-02", "4.6310", "0.82%"],
    ["4", "16", "3.564251178", "2.056e-02", "4.6220", "1.01%"],
    ["5", "32", "3.568698510", "4.447e-03", "4.5858", "1.79%"],
    ["6", "64", "3.569668324", "9.698e-04", "—", "límite de precisión"],
], colWidths=[0.4*inch, 0.65*inch, 1.15*inch, 1.05*inch, 0.75*inch, 1.1*inch])
t5.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f3460')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,-1), 8.2),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cccccc')),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f4f4f4')]),
    ('TOPPADDING', (0,0), (-1,-1), 5), ('BOTTOMPADDING', (0,0), (-1,-1), 5),
]))
story.append(t5)
story.append(Paragraph("δ teórico = 4.669201609. Error % = |δ_n − δ_teórico| / δ_teórico × 100.",
                        caption))

story.append(Image(f"{FIG}/feigenbaum_convergencia.png", width=4.6*inch, height=4.6*inch*(750/1050)))
story.append(Paragraph("Figura 7. δ_n estimado vs. n, con la constante teórica como referencia.",
                        caption))

for q, a in [
    ("¿Las estimaciones convergen hacia el valor teórico?",
     "Sí, de forma aproximada: los cuatro valores de δ_n obtenidos (4.74, 4.63, 4.62, 4.59) "
     "oscilan alrededor de 4.669 con errores entre 0.8% y 1.8%, cruzando el valor teórico "
     "entre n=1 y n=2. No se observa una convergencia monótona perfecta porque las "
     "estimaciones de orden alto (n≥4) dependen de diferencias r_n−r_(n-1) extremadamente "
     "pequeñas (~10<super>-3</super>), sensibles al error numérico."),
    ("¿Por qué las primeras razones están relativamente alejadas de la constante?",
     "Porque δ=4.669 es un límite asintótico (n→∞); para n pequeño, las correcciones de "
     "orden superior en la teoría de renormalización de Feigenbaum todavía tienen peso "
     "significativo. La convergencia es geométrica pero no instantánea."),
    ("¿Qué dificultades numéricas aparecen al identificar periodos altos?",
     "Las ventanas de r donde vive cada periodo se encogen geométricamente (factor ≈1/δ "
     "cada vez): la ventana de periodo 64 mide apenas ~10<super>-4</super> en r. Además, el fenómeno de "
     "<b>desaceleración crítica</b> (\"critical slowing down\") hace que, cerca de cada "
     "bifurcación, el sistema tarde arbitrariamente más iteraciones en converger a su "
     "atractor verdadero, por lo que el transitorio descartado deja de ser suficiente y el "
     "algoritmo de detección de periodo puede confundirse (como se observó al depurar "
     "el punto de bifurcación exacto, donde el periodo es ambiguo por definición)."),
    ("¿Cómo influyen la resolución de r, el número de iteraciones y el descarte del transitorio?",
     "Una resolución de r insuficiente puede saltarse por completo ventanas de periodo alto "
     "(demasiado angostas). Muy pocas iteraciones tras el transitorio no permiten distinguir "
     "un periodo alto de una órbita aún no convergida. Un transitorio corto es "
     "particularmente problemático cerca de las bifurcaciones, donde la convergencia al "
     "atractor se vuelve arbitrariamente lenta."),
    ("¿Los resultados constituyen una demostración matemática o evidencia experimental?",
     "Son <b>evidencia experimental/numérica</b>, no una demostración matemática. Muestran "
     "que, dentro del error numérico esperado, los datos son consistentes con δ≈4.669, pero "
     "no prueban que el límite exacto sea ese valor — eso requiere un argumento analítico "
     "(teoría de grupo de renormalización), que es como Feigenbaum y otros demostraron "
     "formalmente la universalidad."),
    ("¿Qué significa que esta constante sea universal?",
     "Que δ no depende de los detalles del mapa logístico en particular: <b>cualquier</b> "
     "familia de mapas unidimensionales con un único máximo cuadrático (no solo "
     "rx(1−x)) exhibe la misma cascada de duplicación de periodo con la misma razón "
     "límite δ≈4.669. Es una propiedad de la clase de universalidad del sistema, no del "
     "mapa específico — análogo a cómo distintos sistemas físicos comparten exponentes "
     "críticos cerca de una transición de fase."),
]:
    story.append(Paragraph(f"<b>{q}</b>", body))
    story.append(Paragraph(a, qa))

story.append(PageBreak())

story.append(Paragraph("Reto — Conexión entre Mandelbrot y las bifurcaciones", h1))
story.append(Paragraph(
    "Usando la transformación c = (r/2)(1−r/2), se llevaron los valores de r donde nace "
    "cada periodo (Punto 5) al plano complejo, y se verificó el periodo de la órbita de "
    "z<sub>n+1</sub>=z<sub>n</sub><super>2</super>+c sobre el eje real de Mandelbrot para un r tomado "
    "ligeramente <i>dentro</i> de cada ventana periódica (no exactamente en la bifurcación, "
    "donde el periodo es ambiguo por definición).", body))

t6 = Table([
    ["Periodo (mapa logístico)", "r usado", "c = r/2·(1−r/2)", "Periodo (Mandelbrot, eje real)"],
    ["2", "3.132732", "−0.887137", "2"],
    ["4", "3.477062", "−1.283959", "4"],
    ["8", "3.549862", "−1.375450", "8"],
    ["16", "3.565585", "−1.395557", "16"],
    ["32", "3.568989", "−1.399927", "32"],
    ["64", "3.569768", "−1.400927", "64"],
], colWidths=[1.5*inch, 1.0*inch, 1.15*inch, 1.9*inch])
t6.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f3460')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,-1), 8.3),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cccccc')),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f4f4f4')]),
    ('TOPPADDING', (0,0), (-1,-1), 5), ('BOTTOMPADDING', (0,0), (-1,-1), 5),
]))
story.append(t6)
story.append(Paragraph("Coincidencia exacta de periodo en los 6 casos verificados.", caption))

story.append(Image(f"{FIG}/reto_conexion.png", width=6.5*inch, height=6.5*inch*(320/1600)))
story.append(Paragraph("Figura 8. Eje real del conjunto de Mandelbrot con los valores de c "
                        "transformados marcados; cada uno cae exactamente en la unión entre "
                        "un bulbo y el siguiente.", caption))

story.append(Paragraph(
    "<b>Conclusión del reto:</b> los bulbos que cuelgan del cardioide principal del conjunto "
    "de Mandelbrot a lo largo del eje real corresponden, uno a uno, a las regiones de periodo "
    "2, 4, 8, 16... del mapa logístico, bajo la transformación c=(r/2)(1−r/2). Esto no es "
    "coincidencia: ambos mapas son <b>topológicamente conjugados</b> sobre el eje real "
    "(existe un cambio de variable que convierte uno en el otro exactamente). Por eso las "
    "bifurcaciones por duplicación de periodo del mapa logístico son, literalmente, la misma "
    "secuencia de bifurcaciones que uno atraviesa al recorrer el eje real del conjunto de "
    "Mandelbrot de derecha a izquierda: el punto de acumulación r≈3.5699 corresponde "
    "exactamente al extremo izquierdo del cardioide principal, c≈−1.401 — el \"punto de "
    "Feigenbaum\" del conjunto de Mandelbrot.", body))

story.append(PageBreak())

story.append(Paragraph("Pregunta integradora", h1))
story.append(Paragraph(
    "<b>¿Cómo puede una regla determinista, sencilla y completamente conocida producir "
    "estructuras de gran complejidad y comportamientos difíciles de predecir?</b>", h2))
story.append(Paragraph(
    "Tanto z<sub>n+1</sub>=z<sub>n</sub><super>2</super>+c como x<sub>n+1</sub>=rx<sub>n</sub>(1−x<sub>n</sub>) "
    "son reglas de una sola línea, sin ningún elemento aleatorio. La complejidad no proviene "
    "de la regla en sí, sino de su <b>iteración</b> repetida combinada con la "
    "<b>no linealidad</b> del término cuadrático: cada aplicación de la regla no solo mueve "
    "el estado, sino que <i>amplifica o comprime</i> diferencias entre estados cercanos de "
    "forma distinta según en qué región del espacio se encuentren.", body))
story.append(Paragraph(
    "Esa no linealidad produce <b>sensibilidad a los parámetros</b>: al variar r o c de forma "
    "continua, el comportamiento asintótico del sistema no cambia de forma continua sino que "
    "atraviesa <b>bifurcaciones</b> — umbrales precisos donde un punto fijo estable se vuelve "
    "inestable y da lugar a una órbita de periodo doble. Repetir este proceso genera una "
    "<b>cascada de duplicación de periodo</b> que se acumula en un intervalo finito de "
    "parámetro y desemboca en <b>caos</b>: órbitas acotadas (no divergen) pero aperiódicas y "
    "exponencialmente sensibles a la condición inicial, de modo que aunque la regla es "
    "perfectamente conocida, predecir el estado a largo plazo requiere una precisión inicial "
    "infinita —inalcanzable en la práctica—.", body))
story.append(Paragraph(
    "En el plano complejo, esa misma cascada de bifurcaciones, vista simultáneamente para "
    "todos los valores de c, dibuja una frontera con <b>estructura fractal</b>: autosimilar a "
    "todas las escalas, como se observó en las ampliaciones del Punto 3. Y —lo más "
    "sorprendente— la <b>razón geométrica</b> con la que se acumulan esas bifurcaciones (la "
    "constante δ≈4.669) no depende de los detalles de la regla particular, sino solo de que "
    "tenga un máximo cuadrático: es <b>universal</b>, apareciendo en sistemas físicos, "
    "biológicos y económicos completamente distintos que comparten esa misma no linealidad "
    "esencial. La lección central de este taller es, entonces, que determinismo y "
    "predictibilidad no son lo mismo: una regla simple y determinista puede generar, por "
    "simple iteración no lineal, tanto estructura infinitamente rica (el fractal) como "
    "comportamiento efectivamente impredecible (el caos) — y ambos fenómenos están "
    "gobernados por las mismas matemáticas universales.", body))

doc = SimpleDocTemplate(OUT, pagesize=letter,
                         topMargin=0.6*inch, bottomMargin=0.6*inch,
                         leftMargin=0.7*inch, rightMargin=0.7*inch,
                         title="Taller Caos - Mandelbrot y Feigenbaum")
doc.build(story)
print("PDF generado en", OUT)
