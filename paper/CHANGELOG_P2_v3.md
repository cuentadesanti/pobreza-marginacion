# Changelog editorial — Paper 2 v3 (reescritura integral, 2026-07-13)

Steer aplicado: reescritura de voz, jerarquía y traducción de resultados; el contenido
estadístico no cambió (58 bindings prosa↔CSV en verde antes y después).

## Estructura

- Nuevo orden por preguntas: Introducción → Datos → ¿Dónde vive la desigualdad? →
  ¿Se solapan las dimensiones? → Actividad visible y bienestar → Predictores territoriales →
  Validaciones agrupadas por pregunta (violencia / visibilidad / instituciones-fiscal) →
  Implicaciones para la focalización → **Limitaciones (sección nueva)** → Apéndice.
- Resumen reescrito desde cero: problema → pregunta → método (una frase) → tres resultados →
  implicación. Fuera del abstract: homicidios, crimen, INSABI, fiscalidad, Jaccard,
  ortogonalidad, advertencia Theil-vs-varianza.
- Cada sección abre con la intuición sustantiva; el método llega después. La advertencia de
  ortogonalidad pasó de primera frase de §5 a **nota metodológica** al final de §4 (y a
  Limitaciones). La advertencia de funcionales no comparables pasó del arranque de §4 al
  caption de la Figura 1 y a la columna "Método" de la Tabla 1.
- Los cinco análisis externos dejaron de ser bullets numéricos: ahora son mini-secciones
  completas (pregunta → fuente → medida → modelo → resultado → interpretación → límite)
  agrupadas en 7.1 violencia (homicidios + crimen + coerción), 7.2 visibilidad satelital,
  7.3 instituciones y fiscalidad.
- La "escalera incremental" es ahora "Predictores territoriales de la privación", con tabla
  bloque→variables→R²cv y prosa sin deltas numéricos encadenados.
- Los 48 municipios bajaron a un párrafo en §4 + apéndice F (antes párrafo largo + resumen).
- Tabla 1: eliminada la columna "% dentro" (redundante); añadida columna "Método"; un solo
  cuadro con separación visual por objeto.
- Títulos y palabras clave sobrios (keywords: desigualdad espacial; pobreza municipal;
  privación multidimensional; federalismo fiscal; luces nocturnas; México).

## Figuras (5 regeneradas; píxeles inspeccionados en el PDF)

- **Fig 1 (Theil):** takeaway sustantivo arriba; subtítulos "Desigualdad observada" /
  "Heterogeneidad residual"; método discreto en los ejes; etiquetas internas
  ("bruto"/"condicional") → "sin condicionar"/"residual".
- **Fig 2 (mapa de coincidencia):** el título ahora dice en píxeles "la coincidencia en las
  tres dimensiones es cercana a la esperada bajo independencia".
- **Fig 3 (desacople):** ejes en lenguaje común ("privación observada (estandarizada)" /
  "predicha por luces y geografía"); rojo/azul explicados en el propio panel.
- **Fig 4 (homicidios):** nomenclatura de pipeline eliminada de los píxeles — "z peldaño 1",
  "Vista D", "z peldaño 3 + discordancia" → "factores brutos", "características municipales",
  "factores residuales", "modelo combinado"; título con takeaway. (Redibujada desde el CSV:
  los microdatos crudos de defunciones no están en el repo, así que el recomputo completo no
  era posible; el script queda corregido para el próximo rerun con crudos.)
- **Fig 5 (fiscal):** "La vara vale dinero" / "Dos varas, dos Méxicos" / AA / BB eliminados;
  etiquetas "perfil marginación > pobreza" / "perfil pobreza > marginación"; caja explicativa
  reducida a dos líneas; sin la cifra de millones/año no respaldada.

## Términos internos eliminados del texto y de los píxeles

peldaño · rung · Vista D/F/G · AA/BB · "la vara" (vieja/que paga/vale dinero) · "lente(s)"
como sujeto ("la luz no ve", "el índice no ve", "ninguna lente única") · "firma" sin definir
(ahora "huella de método", con remisión al paper compañero) · "objeto distributivo" como
apertura (se define en §2 antes de usarse) · "bruto/residual" desnudos (ahora "nivel
observado" / "heterogeneidad residual", definidos en §2) · "discordancia" sin definir ·
"brecha de apropiación" antes de definir el objeto (ahora "desacople", y la interpretación se
nombra después) · "escalera incremental" · "el municipio peor en todo" · "los olvidados de
los olvidados" · "la actividad existe y brilla" · "la respuesta: apenas" · "advertencia
algebraica" (ahora nota metodológica) · "funcionales no comparables" como apertura ·
z peldaño 1/3 (píxeles) · GLLVM peldaño 1 (ejes de figura).

Se conservan, definidos en primera aparición: "nivel observado", "heterogeneidad residual",
"desacople", "brecha de apropiación territorial" (como interpretación nombrada tras definir
el objeto), "exposición documentada".

## No cambió

Ningún número, tabla de valores, binding ni resultado. `manuscrito.md` y el Paper 1 intactos.
