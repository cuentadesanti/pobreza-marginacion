# Revisión de referee — Paper 1 (`paper1_metodo.md`)

**Dictamen:** revisión menor. Artículo real, bien construido, honestidad metodológica notable
(reporta R̂ 2.16/2.05 intermedios, distingue tres veredictos de convergencia, hedge correcto en cada
claim fuerte). Aparato completo: 5 figuras, 3 tablas ancladas a CSV, métodos reproducibles, apéndice.
Lo de abajo es precisión y presentación, no fondo. Todos los puntos son cero-cómputo salvo M5 (un
output nuevo pequeño).

## Mayores

**M1 — El "1.53" hace doble función.** En §4.4 paso 2 es el R̂ tras fijar el método como contraste
*con anclas todavía puestas*; en Tabla 1 la fila "marginalizado sin γ_s (p2)" también dice 1.530. Son
dos corridas conceptualmente distintas con el mismo número — un referee se detiene. Aclarar en §4.4
que ese R̂ es "aún con anclas, antes de liberarlas" y, si de verdad coincide con la fila p2, señalar
que es accidente numérico (o reformular para que no confunda).

**M2 — Nomenclatura de escalera solapada.** "peldaño 1–4" (escalera con scores muestreados) coexiste
con "p2/p3" (marginalizado sin/con γ_s). "p3" evoca "peldaño 3", pero el "p3 canónico" marginalizado
NO es el "peldaño 3" muestreado. Renombrar el eje marginalizado (p. ej. "M−γ / M+γ") para reservar
"peldaño" a la escalera muestreada.

**M3 — Reconciliación de N (2,469 → 2,455) de pasada.** §3.1 lo menciona entre paréntesis. Un referee
de medición querrá saber qué 14 municipios se caen y si el descarte es informativo (¿los muy pequeños,
los sin remesas?). Una nota de una línea sobre la naturaleza del descarte blinda contra sospecha de
selección.

## Puntos de anclaje verificados en disco (esta revisión)

**M4 — Puntero de fuente equivocado en el apéndice C.** Los eigenvalores p2=(1.80, 0.63, 0.37, 0.087)
y p3=(1.23, 0.50, 0.34) son CORRECTOS (viven en `reporte_gllvm_escalera.md` L176, L211), pero el
apéndice C los atribuye a `comparacion_marginal_2v3.csv`, que no los contiene (ese CSV es σ/share por
indicador, 17 filas, sin eigenestructura). Corregir la cita de fuente, o exportar la eigenestructura a
un CSV propio y apuntar ahí (mejor, para que `check_captions.py` la cubra).

**M5 — La afirmación de nulidad de §5 no tiene output reproducible.** "22.6% … sin correlación con
composición" (firma SAE ⊥ composición) no está respaldada por ningún CSV en `outputs/` (revisados los
tres `desacuerdo_*`/`gamma_*`). O se genera el output que da esa correlación (con su magnitud) y se
cita, o se suaviza la afirmación. Las afirmaciones de nulidad son las que un referee pide sustanciar.

## Menores

**m1 — Hook antropomórfico en §8.** "el modelo sabe más del campo que de la ciudad, y lo declara"
reaparece en discusión tras haberse movido del cuerpo (B4). Está bien como cierre retórico; solo
confirmar que es deliberado.

**m2 — Consistencia de decimal en γ-PC1.** §7 dice "41.8%" y "+0.42"; resumen dice "42%". Unificar:
valor exacto en tabla, redondeo consistente en prosa.

**m3 — Literatura mexicana anunciada, no integrada.** La nota de referencias difiere Cortés/Boltvinik/
etc. "a la versión de envío". Para SIR/JoEI debe cerrarse antes de mandar — último pedazo de C1.

## No tocar (está muy bien)
- La secuencia de identificación de tres pasos con diagnóstico en cada uno — es la contribución, bien
  contada; no ocultar el 2.05/2.16 intermedios es lo que da credibilidad.
- El manejo del ΔELPD +5,410: en los dos lugares dice que es descriptivo y que un modelo comparado no
  está identificado. Hedge correcto.
- Figura 3 (anatomía del método) como figura central.
- El encuadre del header (aplicada-metodológica, no teoría general; simulación como extensión declarada).

## Veredicto
Con M1–M5 resueltos (horas de reescritura + un output pequeño para M5) y m3 (integrar literatura
mexicana), listo para envío a Social Indicators Research. El target solo mueve el énfasis de §2/§8; la
calidad del objeto no depende de él.

*Nota de método: M1–M3 y los puntos "no tocar" salen de lectura directa del paper; M4 y M5 se
verificaron contra `outputs/` y los reportes en esta revisión — M4 confirmó que los eigenvalores son
correctos pero mal citados, M5 confirmó que el output de respaldo no existe.*