# Estrategia de avance metodológico y separación de manuscritos

**Fecha:** 2026-07-12 · **Estado del repo:** 36 commits, manuscrito v1 (`paper/manuscrito.md`,
245 líneas, todo en uno), 14 reportes, 24 figuras, Vista G cerrada con resultado negativo
documentado, GLLVM marginalizado convergido (R̂ ΛΛᵀ 1.003).

Este documento hace dos cosas: (A) ordena el avance metodológico pendiente por
impacto/esfuerzo/riesgo, y (B) propone cómo partir el material en manuscritos separados con su
índice cada uno. El diagnóstico de fondo: **el v1 mete cuatro rutas + método + DAG + cinco
validaciones en un solo paper**. Es demasiado para un artículo y demasiado poco para el potencial
del material. Hay al menos tres papers aquí, con audiencias distintas.

---

## A. Estrategia de avance metodológico

Ordeno por relación impacto/esfuerzo, marcando riesgo y dependencia de datos.

### A1. Consolidación (cero cómputo nuevo, alta prioridad)
Lo que ya está y solo requiere ensamblaje/verificación, no análisis nuevo:
- **Congelar el DAG y la identificación ΛΛᵀ como la contribución técnica citable.** Es lo más
  novedoso del proyecto y ya está convergido y documentado. No necesita nada más que redacción.
- **Sincronizar el manifiesto de figuras** (24 PNG vs. las filas registradas) y cerrar la deuda de
  las figuras sin script (mapa material, DAG pesado, DAG suplementaria — las 3 de esta sesión;
  las 4 de sprints 1–3 solo se recuperan regenerándolas).
- **Fila de certeza 42/54/14 → CSV reproducible.** Hoy vive solo en una figura; para el paper
  necesita su tabla fuente (pendiente detectado en la sesión anterior).

### A2. Quick wins con dato (medio día c/u, riesgo bajo)
- **Composición indígena a Vista D** (ITER, variable de habla indígena) — pendiente declarado de la
  "capa de oportunidades"; **verificar el nombre exacto de columna en el ITER antes de prometer
  tiempo** (no confirmado aún).
- **PIBE exacto vía INEGI_TOKEN** — reemplaza el flag `pibe_aprox`; quick win *si* el token
  resuelve (dio problemas de alcance antes; no garantizado).
- **Trejo-Ley (coerción política)** — la única fuente de crimen con DOI resuelto en Dataverse
  (`10.7910/DVN/VIXNNE`, verificado en `auditoria_fuentes_crimen.md`); cierra el criterio 5 de la
  Vista G. Cobertura 1995–2012 (histórica): entra como exposición rezagada, no contemporánea.

### A3. Robustez que un referee va a pedir (1–2 sesiones, riesgo medio)
- **Post-procesamiento rotacional de los scores** — el ΛΛᵀ está identificado, pero si el paper
  reporta *ejes individuales* (material/educativo/monetario) conviene fijar la orientación con
  varimax/target sobre E[ΛΛᵀ] y propagarla por draw, para que las cargas por eje sean estables y
  no dependan de la convención de signo documentada.
- **SE del SAE de CONEVAL como capa de error de medición** — hoy la verosimilitud gaussiana en
  logit trata los 4 indicadores SAE como observados con varianza homogénea; incorporar su error
  publicado es la extensión que la literatura de áreas pequeñas (Rao-Molina) pide y que blinda el
  hallazgo 4.4 (firma SAE) contra la crítica de circularidad.
- **Modelo de sesgo de cobertura para la Vista G** — si el crimen entra al paper (aunque sea como
  validación negativa), el `O = R × D` necesita los proxies de observabilidad en la especificación,
  ya anotados pero no todos construidos (log_pob, urbano, internet, distancia a capital).

### A4. Extensiones que son otro paper (ver sección B)
FAIS longitudinal, serie 2010–2020, réplica del SAE, multi-escala del corte B. No son robustez del
paper 1; son contribuciones propias. No bloquean nada.

**Ruta recomendada:** A1 completo → A2 (Trejo-Ley + indígena) → A3 solo lo que el target exija.
A3 se decide *después* de fijar target, porque una revista de métodos pedirá el post-procesamiento
rotacional y el SE-SAE; una de desarrollo no.

---

## B. Separación de manuscritos

El material soporta **tres papers** con audiencias, contribuciones y riesgos distintos. El v1
actual es el germen del Paper 1 pero con secciones que pertenecen a los otros dos.

### Paper 1 — "La maquinaria de medición" (METODOLÓGICO, el primero a enviar)
**Tesis:** dos burocracias miden el mismo territorio con instrumentos distintos; modelamos la
maquinaria, no proponemos otro índice. La discordancia fundacional está mediada por el método (SAE).
**Contribución central:** el GLLVM marginalizado + identificación de ΛΛᵀ + DAG de medición.
**Target:** Social Indicators Research / Journal of Economic Inequality.
**Índice:**
1. Introducción — dos mediciones, una pregunta de estructura
2. El proceso generador como DAG de medición (56 nodos, 97 aristas; cinco dependencias mecánicas; circularidad FAIS)
3. Método — GLLVM marginalizado; identificación de ΛΛᵀ; método como contraste inter-agencia
4. **Resultado fundacional — la discordancia es de método (la anatomía del método, veta 1).**
   La firma SAE-EBPH del ingreso es el componente de método dominante (carga 0.58) y parte los
   regímenes LISA limpiamente (AA −0.325 vs BB +0.339); en educación las agencias casi acuerdan
   (0.012); el desacuerdo de vivienda es estatal (0.135→0.029 al condicionar en γ_s). La
   discordancia "más pobre que marginado" que originó el proyecto tiene nombre, y es de método.
   Fuente: `desacuerdo_agencias.csv`, `fig_desacuerdo_agencias.png`.
5. Identificación del subespacio de rango 3 e incertidumbre municipal (42/54/14) — incluye la
   **geografía de la ignorancia (veta 2)**: la incertidumbre posterior es mayor en municipios
   grandes/urbanos (eje1 β log_pob +0.322); el modelo sabe más del campo que de la ciudad.
   Fuente: `veta_ignorancia.csv`.
6. Qué hace γ_estado — **federalismo sectorial (veta 3)**: solo 42% de los efectos estatales es un
   gradiente común de capacidad (PC1, +0.42 con PIBE pc); el 58% restante es específico por dominio
   de política. Fuente: `veta_gamma_pca.csv`. + INSABI como legibilidad del componente estatal.
7. Discusión — qué significa modelar la maquinaria; límites de identificación

### Paper 2 — "Desigualdad territorial en dos escalas" (SUSTANTIVO, desarrollo)
**Tesis:** la desigualdad opera en dos escalas; las geografías de privación rara vez se superponen;
la actividad visible no implica inclusión local (brecha de apropiación).
**Contribución central:** los resultados 4.1, 4.2, 4.3 del v1 + las validaciones externas.
**Target:** World Development / Journal of Development Economics.
**Índice:**
1. Introducción — más allá de "cuál índice": la estructura de la desigualdad
2. Datos y espacio latente (resumen del método; remite al Paper 1 para el detalle)
3. Dos escalas: Theil entre/dentro; el residual intraestatal
4. Geografías disjuntas: acumulación en el bruto, no en el residuo. **Los 48 triple-severos con
   nombre (veta 4)** — el rostro humano del resultado: 24/48 en Oaxaca, mediana 5,430 hab, remesas
   17 vs 92 USD del promedio, 27% con presencia criminal documentada vs 48%, y 44/48 invisibles al
   LISA. Los olvidados de los olvidados. Fuente: `veta_48_triple.csv`.
5. Brecha de apropiación: satélite vs. privación social; precariedad y remesas
6. Validaciones convergentes: homicidios, luces, crimen, fiscal
7. Implicaciones de política: focalización, la vara que paga, ninguna lente única

### Paper 3 — "Cuando la medición asigna el dinero" (IDENTIFICACIÓN, mediano plazo)
**Tesis:** la fórmula FAIS asigna recursos usando la propia medición de pobreza (circularidad);
+15.8% al perfil de marginación a igual privación. El DAG temporalizado es el marco.
**Contribución central:** el hallazgo fiscal (Ramo 33) convertido en diseño de identificación con
montos FISM anuales 2016–2020.
**Target:** economía pública / federalismo fiscal.
**Estado:** requiere dato nuevo (montos FISM municipales anuales — Transparencia Presupuestaria,
scraping serio). Es el segundo paper en el tiempo, no el segundo en prioridad.
**Índice (tentativo):**
1. La circularidad medición→asignación→fenómeno
2. El DAG temporalizado como marco de identificación
3. Montos FISM 2016–2020 por municipio
4. El efecto de la vara: masa carencial heredada vs. pobreza vigente
5. Implicaciones para el diseño de fórmulas de transferencia

### Qué NO es paper propio (queda como capítulo/apéndice o repositorio)
- **Corte B (luz→desarrollo)** — es una subsección del Paper 2 (validación satelital), no un paper;
  su hallazgo (la log-lineal de Jean no es estable a escala municipal) es fuerte pero necesitaría el
  multi-escala para ser paper independiente, y eso es extensión declarada.
- **Vista G (crimen)** — resultado principalmente negativo; entra como validación en el Paper 2
  (una ruta más que converge), con su hallazgo propio (competencia>monopolio para violencia) como
  nota. No sostiene un paper solo.

---

## C. Dependencias y orden de ejecución

```
Paper 1 (método)  ─── listo tras A1 + redacción; NO depende de dato nuevo
Paper 2 (desarrollo) ─ listo tras A1 + A2(indígena) + redacción; comparte método con P1
Paper 3 (fiscal)  ─── BLOQUEADO por dato FISM (scraping) → mediano plazo
```

**Recomendación:** Paper 1 primero (es donde vive la contribución técnica y no depende de dato
nuevo), Paper 2 en paralelo compartiendo la sección de método comprimida, Paper 3 cuando el dato
FISM esté. A3 (robustez) se activa por target, no antes.

**Decisiones abiertas del usuario** (no inferibles del repo): idioma (respondió **español**);
target de cada paper (define el énfasis y qué robustez de A3 se vuelve obligatoria); y si Paper 1 y
Paper 2 se envían como par coordinado (mismo espacio latente, dos lecturas) o secuencial.

---

---

## D. Handoff para Claude Code — tareas concretas

Orden sugerido. Todo aditivo sobre el repo; no reescribir outputs existentes salvo donde se indique.

**D1. Partir el manuscrito v1 en dos (Paper 1 + Paper 2).**
`paper/manuscrito.md` (245 líneas, todo en uno) es el germen. Crear:
- `paper/paper1_metodo.md` — secciones 1–3 del v1 (intro, DAG, método) + resultado 4.4 (firma SAE)
  como resultado *fundacional*, no como validación. Absorbe vetas 1, 2, 3 según el índice de arriba.
- `paper/paper2_desigualdad.md` — resultados 4.1–4.3 del v1 + las 5 validaciones convergentes +
  veta 4 (triple-severos). Método comprimido con remisión al Paper 1.
Conservar `paper/manuscrito.md` como versión unificada de referencia (no borrar).

**D2. Antes de nada, arreglar la deriva de conteos del DAG.** Ya corregí a mano manuscrito y
`reporte_dgp_dag.md` a **56 nodos / 97 aristas** (las tablas `dict/dag_nodes.csv` y
`dict/dag_edges.csv` son la verdad). Añadir un check al final del script del DAG que haga
`assert len(nodes)==56 and len(edges)==97` o, mejor, que imprima los conteos leídos de los CSV para
que la prosa nunca vuelva a desincronizarse. Barrer el resto de reportes por si "51 nodos"/"92
aristas" quedó en otro lado.

**D3. Cerrar la fila de certeza 42/54/14 con su CSV fuente.** Hoy vive solo en una figura; generar
el CSV reproducible que la respalda (el reparto de certeza por eje canónico) para que el Paper 1
pueda citarla desde un output, no desde un PNG.

**D4. Quick win con dato — Trejo-Ley (criterio 5 de la Vista G).** DOI verificado
`10.7910/DVN/VIXNNE` (Dataverse, con codebook). Bajar, confirmar unidad municipal en el codebook,
y correr la línea de coerción política × fragmentación × γ_s. Es exposición histórica (1995–2012):
entra **rezagada**, no contemporánea.

**D5. Quick win con dato — composición indígena a Vista D.** ITER 2020, variable de habla indígena.
**Verificar primero el nombre exacto de la columna en el archivo** (no asumir `P3YM_HLI`); si es la
correcta, agregarla a Vista D como capa de oportunidades.

**Salvaguardas (las de siempre):** no filtrar el token Banxico ni INEGI en ningún commit; presencia
criminal documentada ≠ control territorial (mantener el encuadre `O = R × D` y el modelo de sesgo de
cobertura); toda cifra nueva en prosa debe tener su output/CSV detrás; y las fuentes de crimen no
verificadas de primera mano (OCVED, ACLED cobertura MX) se confirman en la fuente antes de citarse
como resultado.

**Decisiones del usuario que faltan para D1** (no inferibles): target de cada paper (define qué
robustez de A3 se vuelve obligatoria) y si Paper 1/Paper 2 se envían coordinados o en secuencia.
Idioma ya decidido: **español**, traducir al enviar.

---

*Nota de método de este documento: las cifras citadas (R̂ 1.003, ELPD +5,410, Jaccard ≤0.21,
β precariedad +0.23, +15.8% Ramo 33, 42/54/14, DOI Trejo-Ley, y las cuatro vetas: firma SAE 0.58,
LISA −0.325/+0.339, γ-PC1 42%, 48 triple-severos/24 Oaxaca/mediana 5,430 hab/44 ns) provienen de
reportes y outputs verificados en el repo esta sesión. Las que dependen de dato aún no adquirido
(FISM anual, columna indígena del ITER, PIBE vía token) están marcadas como no confirmadas y no
deben citarse como resultados hasta verificarse en la fuente.*
