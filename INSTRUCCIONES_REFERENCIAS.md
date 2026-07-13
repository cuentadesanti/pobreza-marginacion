# Integración de la literatura sustantiva mexicana (cierra la nota de placeholder)

El aparato metodológico está completo con DOI verificado. Falta solo la literatura sustantiva mexicana,
hoy mencionada por nombre en §2 sin cita formal, y anunciada en una nota entre paréntesis en ambas
bibliografías. Esto la cierra. **Cero cómputo** — es tejido de citas + entradas de bibliografía.
Todos los DOIs abajo fueron resueltos en Crossref (2026-07-13).

Después de aplicar: borrar de ambos papers la nota "(… se completará con DOI verificado al preparar la
versión de envío)". El placeholder `[URL / DOI Zenodo al depositar]` NO se toca — ese depende de
depositar el repo y es un paso de publicación aparte.

---

## Entradas nuevas de bibliografía (verificadas en Crossref)

Añadir a la sección **Referencias** de AMBOS papers las que apliquen (ver mapeo por paper abajo):

- Boltvinik, J. (2012). Treinta años de medición de la pobreza en México. *Estudios Sociológicos*
  30(núm. extra): 79–110. doi:10.24201/es.2012v30nextra.186
- Székely, M. (2017 [orig. 2005]). Pobreza y desigualdad en México entre 1950 y 2004. *El Trimestre
  Económico*. doi:10.20430/ete.v72i288.566 — **Crossref porta 2017** (reedición); citar el año que se
  use consistentemente. Se quitaron páginas 913–931 (no confirmadas en Crossref).
- Lustig, N. & Székely, M. (1997). *México: evolución económica, pobreza y desigualdad*. Banco
  Interamericano de Desarrollo. doi:10.18235/0009827
- Lustig, N. (ed.) (2018). *Commitment to Equity Handbook: Estimating the Impact of Fiscal Policy on
  Inequality and Poverty*, vol. 1. Brookings/CEQ Institute. doi:10.5040/9780815753834
- Cortés, F., Ochoa León, S. & Vargas Chanes, D. (2023). Desigualdad en la distribución del ingreso:
  México 2016 a 2020. En *Los derroteros del desarrollo*, UNAM-PUED. doi:10.22201/pued.9786073078337e.2023.c9
- Peláez Herreros, Ó. (2022). El Índice de Marginación del Conapo transformado en indicador cardinal.
  *EconoQuantum* 20(1). doi:10.18381/eq.v20i1.7294

**Nota de fijación de edición (verificar al citar):** Székely (El Trimestre Económico) tiene reediciones
posteriores sobre un original ~2005 — fijar el año de la que se use. El *CEQ Handbook* tiene vol. 1
(2018), vol. 1 (2023) y vol. 2 (2023) — citar la edición efectivamente consultada.

---

## Paper 1 — dónde y cómo mencionarlas (borrador literal)

El §2 ya dice: *"El debate Boltvinik–CONEVAL sobre umbrales y agregación… y la tradición de series
comparables bajo cambio de instrumento (Székely y coautores), son el trasfondo sustantivo…"*.
Convertir esos dos name-drops en citas y añadir Peláez como antecedente de la crítica al DP2.

**Edición 1 (crítica al índice, junto a Cortés-Vargas).** Donde dice
*"la crítica canónica al índice de marginación es la de Cortés & Vargas (2011)…"*, añadir tras esa
oración:
> Peláez Herreros (2022) profundiza esta línea al recardinalizar el índice para hacer comparables sus
> niveles, evidencia adicional de que la agregación DP2 mezcla constructo y escala de medición — la
> distinción que nuestro modelo hace explícita.

**Edición 2 (trasfondo sustantivo, con cita).** Reemplazar
*"El debate Boltvinik–CONEVAL sobre umbrales… (Székely y coautores)…"* por:
> El debate de larga data sobre umbrales y agregación de la pobreza multidimensional (Boltvinik 2012) y
> la tradición de series comparables de pobreza y desigualdad bajo cambio de instrumento (Székely 2017)
> son el trasfondo sustantivo: dos mediciones oficiales del mismo fenómeno con maquinarias en disputa.

(Usar el mismo año de Székely en prosa y bibliografía — Crossref porta 2017 para ese DOI.)

→ Bibliografía Paper 1: añadir **Boltvinik 2012, Székely 2005, Peláez 2022**.

---

## Paper 2 — dónde y cómo mencionarlas (borrador literal)

El §2 ya dice: *"la agenda de convergencia regional estancada tras la apertura comercial es el trasfondo
macro"* (sin cita) y §6 discute incidencia fiscal del Ramo 33 (sin ancla en la literatura de incidencia).

**Edición 1 (desigualdad del ingreso, ancla la tesis de dos escalas).** Donde §2 habla de la partición
condicional de la desigualdad, añadir:
> Que la desigualdad del ingreso en México se sostiene predominantemente *dentro* de las entidades y no
> entre ellas es un hallazgo recurrente de la literatura distributiva nacional (Cortés, Ochoa León &
> Vargas Chanes 2023); nuestra contribución es mostrar que esa escala se invierte al pasar del nivel
> bruto al residuo condicional.

**Edición 2 (incidencia fiscal, ancla §6 "dos varas y dinero").** En §6, al interpretar la brecha de
Ramo 33 entre regímenes, añadir:
> El análisis de incidencia de la política fiscal sobre la desigualdad tiene marco establecido (Lustig
> 2018); nuestro hallazgo es que la *fórmula de asignación misma* —al heredar la vara de medición—
> introduce una brecha distributiva antes de cualquier análisis de incidencia del gasto.

**Edición 3 (opcional, tradición sustantiva en §2).** Una frase que sitúe el trabajo en la línea larga:
> …en la tradición de medición de pobreza y desigualdad en México (Lustig & Székely 1997; Boltvinik 2012).

→ Bibliografía Paper 2: añadir **Cortés et al. 2023, Lustig 2018**, y (si se usa la Edición 3)
**Lustig & Székely 1997, Boltvinik 2012**.

---

## Cierre y verificación

1. Borrar la nota de placeholder entre paréntesis en ambas bibliografías.
2. Ordenar alfabéticamente las Referencias tras insertar.
3. Regenerar PDFs; inspeccionar que las citas nuevas rendericen y que la bibliografía quede alfabética.
4. `check_captions.py` y `check_dag_conteos.py` en verde (estas ediciones no tocan números, no deberían
   afectar bindings).
5. `manuscrito.md` intacto.

**No inventar páginas/volúmenes que no estén arriba.** Donde falte un dato bibliográfico (p. ej. páginas
exactas de Székely), dejar lo que Crossref porta y no rellenar de memoria.