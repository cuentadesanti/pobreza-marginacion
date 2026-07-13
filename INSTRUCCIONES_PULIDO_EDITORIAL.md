# Pulido editorial — de "reporte técnico" a manuscrito imprimible

Tres defectos que separan un reporte interno de un paper enviable, cuantificados sobre ambos papers.
Cero cómputo nuevo salvo una figura (barra apilada de Theil, desde CSV existente). Aplica a
`paper1_metodo.md` y `paper2_desigualdad.md`.

## 1. Sacar las referencias a archivos internos del cuerpo (70: 37 en P1, 33 en P2)

A un lector externo no le importa `certeza_canonica.csv` ni `check_captions.py`. Ningún paper cita
CSVs inline. Hacer:
- **Borrar del cuerpo, captions y tablas** todo `(fuente: xxx.csv)`, nombre de script en backticks y
  ruta interna. Quitar también la nota de pie que lista los outputs y la que menciona
  `check_dag_conteos.py`/`check_captions.py`.
- **Crear al final una sección "Disponibilidad de datos y código"**: un párrafo — todo el código y los
  datos derivados están en el repositorio público [URL / DOI Zenodo al depositar] — y **una tabla
  suplementaria** figura/tabla → script generador. Ahí vive la reproducibilidad en un paper, no en el
  texto.
- **Preservar `check_captions.py` sin ensuciar el PDF:** mover cada binding a un **comentario HTML
  invisible** junto al número — `41.9%<!-- src: certeza_canonica.csv -->`. Pandoc no lo renderiza; la
  guarda lo sigue leyendo. Verificar que las 48 bindings siguen en verde tras la migración.

## 2. Bautizar la jerga de sesión con nombre propio

Un revisor no entiende "peldaño 3". Reemplazos (globales, cuerpo + captions + tablas):

| Jerga interna | Reemplazo |
|---|---|
| "peldaño 1/2/3/4", "rung" | **Especificación S1–S4** con etiqueta: S1 (GLLVM base) · S2 (+covariables de composición) · S3 (+efectos estatales) · S4 (+espacial BYM2). Definir la escalera una vez en §4 y usar "S3" en adelante. |
| "M−γ / M+γ" | Definir el símbolo una vez ("modelo marginalizado sin/con efectos estatales, M−γ / M+γ") y usar la **frase** en prosa; los códigos solo en encabezados de tabla. |
| "Vista D" | "bloque de covariables de composición (demografía, mezcla sectorial, remesas)" en la 1ª aparición; "las covariables de composición" después. |
| "veta" (5×) | eliminar — es palabra de trabajo. "El análisis de …". |
| "eje 3" a secas | usar el nombre sustantivo ya definido: "el eje de contraste vivienda-ingreso vs. servicios de red". Nunca un número de eje desnudo. |
| "canónico" (ejes) | **se queda** — término estándar. |

Regla general: el lector nunca debe encontrar un token que solo tenga sentido dentro de nuestra sesión.

## 3. Menos mapas, más figuras analíticas (sobre todo Paper 2)

Paper 1 está bien (3 figuras, ninguna es un mapa: DAG, descomposición de varianza, anatomía del método).
**Paper 2 abusa:** su Figura 1 son 6 minimapas (media+sd × 3 ejes) y la Fig 5 otro mapa. Un mapa muestra *dónde*; el paper trata de *relaciones*. Hacer:
- **Paper 2 Fig 1:** reducir a los mapas que contesten una pregunta espacial real (p. ej. solo las 3
  medias, o solo el eje material); mover el resto al suplemento.
- **Nueva figura de Theil (Paper 2 §3):** hoy las "dos escalas" son solo prosa+tabla. Añadir una
  **barra apilada entre-estados / intra-estados** por indicador y por eje canónico, desde
  `desigualdad_theil.csv` (ya existe; usa `plotstyle.py` y `apply_figure_style()`). Es la figura que
  *muestra* la tesis central sin un mapa.
- **Alternar con analíticas ya generadas y sin usar:** `fig_escalera_metricas`, `fig_gamma_estados`
  (P1); `fig_dimensionalidad` (justifica K=3). Criterio: cada mapa que quede debe contestar una
  pregunta espacial; si solo decora, se reemplaza.

## Orden y salvaguardas
1. (2) renombrado global primero — es el que más toca texto. 2. (1) migrar refs a comentarios HTML +
sección de disponibilidad. 3. (3) figuras. 4. Regenerar PDFs e **inspeccionar página por página**
(la deriva de conteos ya se escondió una vez dentro de un PNG — revisar que ninguna figura nueva
reintroduzca jerga o números viejos en sus píxeles). 5. `check_captions.py` y `check_dag_conteos.py`
en verde.

**Salvaguardas de siempre:** ningún número sin su binding (ahora en comentario HTML); no tocar
`outputs/`/`idata_*.nc`; `manuscrito.md` intacto. Target confirmado: **Paper 1 → Social Indicators
Research**; Paper 2 → World Development. Al terminar, ambos deben leerse como si nunca hubieran existido
un CSV ni una sesión de trabajo — solo el argumento.

---

## 4. Correcciones conceptuales de una segunda revisión (verificadas donde aplica)

Estas van más allá del pulido de forma: tocan claims. Ordenadas por gravedad.

### Paper 2 — dos auditorías matemáticas (hacer ANTES de circular; son cómputo pequeño, no veta nueva)

**4a. Comparabilidad Theil vs. varianza en la tabla de "dos escalas" (VERIFICADO).** La tabla mezcla
dos funcionales bajo un mismo encabezado "% entre": `desigualdad_theil.csv` tiene `tipo=theil_indicador`
(53.1%, 58.8%…) para indicadores y `tipo=var_eje_canonico` (23.6%, 13.8%…) para ejes — **Theil ≠
cociente de varianza between/total**. El texto los lee como la misma clase de cantidad y no lo son.
Arreglar con una de: (i) **dos paneles separados**, sin comparar niveles porcentuales entre ellos; o
(ii) aplicar varianza-entre/dentro a **ambos** objetos (funcional común). Mínimo: cambiar el encabezado
y el texto para que no invite a comparar 50.8 con 23.6 como el mismo número. La tesis de dos escalas
sobrevive; la presentación actual no.

**4b. "Geografías disjuntas" está parcialmente inducido por la ortogonalización.** Los ejes canónicos
son la eigendescomposición de E[ΛΛᵀ] → **ortogonales por construcción** → sus extremos se solapan poco
por álgebra, no solo por geografía; y la razón obs/esperado roza 1 en todos los umbrales
(`desigualdad_robustez.csv`). El claim "la acumulación vive en el nivel, no en el residuo" es demasiado
fuerte. Dos salidas: (i) **retitular** la sección a "las severidades de los ejes residuales se solapan
débilmente" y bajar el tono del claim a "poco solapamiento extremo adicional al esperado bajo
independencia"; y/o (ii) un null más exigente — solapamiento sobre **familias de indicadores residuales**
(no ejes ortogonales) o permutaciones que preserven autocorrelación espacial. Los **48 municipios** bajan
de caso central de política a viñeta descriptiva (ya declarados sensibles a umbral y eje 3); quitar
"invisibles a todas las lentes usuales" con tanta fuerza.

### Paper 2 — ajustes de lenguaje (cero cómputo)

**4c. "Circunstancias que ningún municipio elige"** incluye inserción productiva y precariedad, que son
outcomes históricos/institucionales, no circunstancias predeterminadas. Suavizar. Y el "+0.042 → la
desventaja indígena está estructuralmente incorporada": ese incremento **depende del orden de entrada**
de los bloques; sin Shapley R²/permutación de órdenes no sostiene "incorporada". Reformular a: "la
composición indígena aporta poca señal predictiva incremental una vez incluidas geografía, demografía e
inserción — compatible con una fuerte superposición entre dimensiones".

**4d. Brecha de apropiación:** nombrar primero el objeto formal ("brecha entre privación observada y
predicha por lentes espaciales"), la interpretación ("apropiación territorial") después; declarar
unidades de β (¿estandarizadas?); notar que el modelo base ya incluye luz+geografía (no es luz-vs-
bienestar puro); idealmente propagar incertidumbre OOF, no una predicción puntual.

**4e. INSABI:** "el componente estatal captura política real, no solo ruido de medición" →
"…contiene señal compatible con política institucional real, no únicamente con calibración". La corr
0.61 es sugestiva, no identificación.

### Paper 1 — ajustes finos (cero cómputo, salvo simulación que NO se hace ahora)

**4f. DAG comprimido (refuerza el punto 3 de arriba).** La Figura 1 completa (56 nodos) es artefacto de
reproducibilidad, no figura narrativa: el texto es ilegible a tamaño de página. Hacer una **versión
reducida de 15–20 nodos conceptuales** para el cuerpo y mandar el DAG completo al suplemento.

**4g. "La multimodalidad no era de los scores" → "no provenía únicamente de los scores municipales".**
Tras marginalizar la multimodalidad persiste, así que el experimento muestra que no era *únicamente* de
los scores — no excluye toda contribución de la parametrización de z.

**4h. El contraste de líneas de ingreso NO es interagencia** (ambas líneas son CONEVAL; el contraste es
con el factor monetario, ya reconocido entre paréntesis). Renombrar el paraguas: **"direcciones de
dependencia metodológica predefinidas"**, y dentro de ellas: educación y vivienda = contrastes
interagencia; ingreso = bloque intragencia SAE compartido. Hoy "método como contraste interagencia"
suena como si describiera los tres bloques.

**4i. Simulación: NO en este sprint.** El header ya la declara como extensión; el propio revisor dice
que no bloquea el envío a SIR. Anticiparla como "probable petición de referee" en la discusión, sin
ejecutarla.

**Nota de alcance:** 4a, 4b (variante null), 4c (Shapley) y 4d (propagación OOF) son cómputo pequeño
sobre outputs existentes — NO vetas nuevas. Si 4a y 4b sobreviven la auditoría, Paper 2 gana mucha
fuerza; si no, no muere — se reestructura alrededor de los dos objetos distributivos, la brecha de
predictibilidad, la desigualdad intraestatal y los límites de la focalización unidimensional. No abrir
más análisis fuera de estos.