# Revisión de referee + estrategia de publicación — Paper 2 (`paper2_desigualdad.md` v3)

**Dictamen:** revisión menor de contenido, más una decisión de target que conviene reconsiderar. La
reescritura por preguntas funciona, la voz es de artículo (no de reporte), y las tres correcciones
conceptuales de las auditorías (Theil≠varianza, ortogonalidad por construcción, lenguaje de
circunstancias) están bien incorporadas. Los 58 bindings en verde. Lo de abajo es afinación, no
reestructura.

## Mayor — una sola, pero importante

**R1. El titular del resumen usa justo la comparación que el propio paper declara no comparable.**
El resumen contrasta "31%–59% del índice de Theil" (indicadores observados) contra "76–87% de la
varianza" (dimensiones residuales). Son **dos funcionales distintos** — Theil vs. cociente de varianza
— y el paper con toda razón advierte en §3/caption/Tabla 1 que no se comparan. Pero entonces el resumen
socava su propia nota de honestidad: hace del contraste no comparable la frase-gancho.

La solución es que el paper **ya tiene el contraste limpio** y no lo está usando como espina dorsal: en
la Tabla 1, "factor material (sin condicionar) = 50.8%" y "dimensión material (residual) = 23.6%" son
**el mismo funcional** (varianza entre/dentro), uno sin condicionar y otro condicionado. Ese es el
contraste válido de dos escalas, sin asterisco. Recomendación: reescribir la primera frase-resultado
del resumen y el arranque de §3 alrededor de **50.8% → 23.6% (misma medida de varianza)**, y dejar los
Theil por-indicador como textura descriptiva ("entre 31% y 59% según el indicador"), no como la mitad
del contraste central. Con eso la tesis de dos escalas queda blindada contra el reflejo #1 del referee.

**R1b (corolario de lenguaje):** con el mismo funcional, 50.8% → 23.6% es una **caída a menos de la
mitad**, no una "inversión". §3 dice "el cuadro se invierte"; suavizar a "el peso interestatal cae
marcadamente" o "se reduce a la mitad". "Invierte" sugiere que el residual pasa a ser mayoritariamente
interestatal, y no lo es — sigue siendo intraestatal, solo que más.

## Medianas

**R2. Sensibilidad del §4 a la tercera dimensión (14% de certeza).** El resultado de "solapamiento
débil" usa las tres dimensiones, pero la tercera (vivienda-ingreso vs. redes) solo es firme en 14% de
los municipios (declarado en §2 y §10). Un referee preguntará cuánto del bajo solapamiento depende de
esa dimensión ruidosa. Sugerencia barata: una línea en el apéndice B con la razón obs/esp calculada
solo sobre las dos dimensiones firmes (42% y 55%); si sobrevive, blinda el resultado; si no, se acota
honestamente. Es re-cómputo pequeño sobre outputs existentes.

**R3. Generalización internacional — el gancho que World Development pedirá.** El paper es
íntegramente México. Los tres hallazgos son transferibles y conviene decirlo en una o dos frases de la
conclusión: (i) el patrón de dos escalas y objetos distributivos aplica a cualquier país con medición
en áreas pequeñas calibrada a unidades administrativas; (ii) el desacople luz-bienestar es un método
replicable donde haya luces + medición social; (iii) el sesgo de fórmula fiscal heredado del
instrumento de medición es el hallazgo más general y el más citable fuera de México. Sin esto, el
riesgo de "estudio descriptivo de un solo país" es real en WD.

**R4. El hallazgo fiscal (§7.3) está subvendido.** "La fórmula de asignación misma, al heredar el
instrumento de medición, introduce una diferencia distributiva antes de la incidencia del gasto" es
probablemente el resultado más novedoso y general del paper — un mecanismo de reproducción de
desigualdad que precede al análisis fiscal estándar. Está enterrado como tercer sub-punto de las
validaciones. Considerar elevarlo: mencionarlo en el resumen y hacerlo protagonista de las
implicaciones §8.

## Menores
- **m1.** §5: "unas 20 veces (IC95 14–28)" la mediana de remesas — dar el par de medianas crudas de
  los dos grupos de cola (subestimados vs. sobreestimados) entre paréntesis ayuda al lector. Tomar los
  valores de `satelital_remesas_reg.csv` / la fuente del desacople de §5, NO del apéndice F (esos 17/92
  son de los 48 triple-severos, otro análisis).
- **m2.** Consistencia autor: §3 cita "Cortés & Valdés Cruz 2023" y la bibliografía igual — coincide
  con lo que Crossref porta para ese DOI (bien; corregido respecto de mi borrador que decía "Ochoa
  León & Vargas Chanes").
- **m3.** Tabla 3: la fila "+ pertenencia estatal (validación no bloqueada; no comparable) 0.891"
  mezcla un R²cv bloqueado con uno no bloqueado en la misma columna. Mover a nota al pie o sombrear,
  para que no se lea como el siguiente peldaño comparable.
- **m4.** El placeholder `[URL / DOI Zenodo al depositar]` sigue — depósito pendiente (tu paso).

## Lo que está muy bien (no tocar)
- La nota metodológica de ortogonalidad al final de §4 y en §10 — colocación exacta: advierte sin matar
  el resultado.
- §7 agrupado por pregunta con el "no" adelantado en 7.1 — lectura fluida.
- El bloque de límites de §10 es de los más honestos que he visto en un borrador; es un activo, no una
  debilidad, ante un buen referee.

---

# Estrategia de publicación

**El matiz central:** World Development es un tiro ambicioso y **con riesgo real de desk-reject** por
"estudio descriptivo de un solo país sin identificación causal". El paper es asociativo, transversal y
mexicano-específico; WD suele exigir o identificación causal o una contribución de desarrollo global
explícita. R3 y R4 (generalización + elevar el hallazgo fiscal) son exactamente lo que reduce ese
riesgo, pero aun así WD es apuesta alta.

**Mi recomendación de cartera (en orden de envío realista):**

1. **Review of Income and Wealth** — el hogar más natural. Vive de medición de desigualdad/pobreza y
   descomposiciones; "dos objetos distributivos" + partición Theil/varianza + el sesgo de fórmula
   fiscal encajan sin forzar nada. Alta probabilidad de mandarse a revisión. **Primer envío recomendado.**
2. **Journal of Economic Inequality** — segundo natural: descomposición de desigualdad es su núcleo
   (Shorrocks está en sus páginas). Menos apetito por el componente satelital/crimen, que iría más
   comprimido.
3. **World Development** — el tiro ambicioso. Enviar aquí solo tras aplicar R3+R4 y si estás dispuesto
   al riesgo de desk-reject por el ciclo largo. Alternativa de menor fricción del mismo grupo:
   **World Development Perspectives** (más receptivo a estudios de país).
4. **Regional Studies / Journal of Regional Science** — si el eje se reencuadra hacia la *escala
   espacial* de la desigualdad como contribución central (menos sobre medición, más sobre geografía).

**Recomendación firme:** enviar primero a **Review of Income and Wealth**, con World Development como
segunda vuelta si RIW lo rechaza pero con buenos comentarios. RIW maximiza probabilidad de revisión sin
sacrificar prestigio, y es donde el aparato del paper (descomposiciones, dos objetos) es lengua materna.

**Secuencia entre los dos papers:** Paper 1 (SIR) establece el objeto de medición que Paper 2 explota.
Enviar Paper 1 primero o en paralelo, y que Paper 2 cite a Paper 1 como el paper de medición compañero
(ya lo remite). Deben delimitarse mutuamente para no auto-solaparse ante un referee que vea ambos.

**Antes de cualquier envío (no analítico):** depositar el repo en Zenodo (resuelve el placeholder),
traducción profesional al inglés, y 2–3 lectores externos — idealmente uno de medición de pobreza
(para §2–4) y uno de federalismo fiscal (para §7.3–8).