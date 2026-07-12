# Mapa de literatura: dónde se para este proyecto

**Tesis del mapeo.** La economía de la desigualdad mexicana es fuerte en *medición e incidencia*
(qué tanto, para quién, con qué error) y la ciencia social computacional es fuerte en *estructura*
(escalamiento, redes, geografía). Casi nadie trabaja la intersección específica de este repo:
**modelar la maquinaria de medición misma** — dos burocracias estadísticas midiendo el mismo
territorio con instrumentos distintos — como problema de variables latentes con estructura
espacial. Eso es un nicho real, no un hueco por irrelevante.

---

## 1. Economía de la desigualdad (medición)

| Investigador | Núcleo | Qué le importa a este proyecto |
|---|---|---|
| **Miguel Székely** | Series largas de pobreza/desigualdad (desde 1950), capital humano; ex-subsecretario, ex-CEEY | El estándar de cómo construir series comparables cuando el instrumento cambia — el problema de este repo en el eje temporal (DP2 2020 vs ACP 2010; extensión natural de la escalera) |
| **Fernando Cortés** (COLMEX) | El sociólogo cuantitativo de la distribución del ingreso; ENIGH; medición de pobreza | **La crítica canónica al índice de CONAPO es suya**: Cortés y Vargas (2011), "Marginación en México a través del tiempo, a propósito del índice de Conapo" — argumenta que el índice no es comparable intertemporalmente y confunde constructo con método. El GLLVM de este repo es, en cierto sentido, la respuesta formal a esa crítica: separa constructo (z), método (m) y ruido (s) |
| **Julio Boltvinik** (COLMEX) | Método de Medición Integrada de la Pobreza (MMIP); crítica frontal a la metodología CONEVAL | El antecedente conceptual de "dos mediciones del mismo fenómeno": su debate con CONEVAL sobre umbrales y agregación es el trasfondo político de la discordancia que aquí se modela |
| **Nora Lustig** (Tulane, CEQ Institute) | Incidencia fiscal: impuestos y transferencias sobre la distribución | El punto de contacto es la Vista E fiscal: CEQ hace a nivel persona lo que la descomposición de γ_s intenta a nivel estado (¿el gasto público mueve la privación?) |
| **Raymundo Campos-Vázquez** (COLMEX) | Mercado laboral, salarios, informalidad | Su trabajo valida (o cuestiona) el proxy `empleo_precario_pct` de la Vista D; ojo con su literatura sobre ingreso censal subreportado — pega directo a `ing_2sm` |
| **Gerardo Esquivel** (COLMEX/Banxico) | Desigualdad regional, concentración | Su agenda de convergencia regional estancada post-TLCAN es la lectura macro del factor espacial: si ρ (BYM2) es alto, la privación es un fenómeno de *regiones*, no de municipios |
| **Rolando Cordera** (UNAM) | Desarrollo, Estado de bienestar, desigualdad estructural | Marco interpretativo, no metodológico |

## 2. Movilidad social

- **CEEY** (Roberto Vélez-Grajales, Graciela Teruel; antes Monroy-Gómez-Franco): ESRU-EMOVI 2023,
  movilidad intergeneracional por regiones ("A Land of Unequal Chances": la movilidad es mucho
  menor en el sur). Conexión concreta: sus índices regionales de movilidad son un **candidato de
  validación externa** para los scores latentes — ¿predice `z_material` la inmovilidad
  intergeneracional mejor que el IM o la pobreza oficiales por separado? Teruel además co-dirige
  EQUIDE (UIA), que mantiene la ENSANUT/EQUIDE de bienestar — otra fuente de validación.

## 3. Ciencia social computacional / complejidad

| Investigador | Núcleo | Conexión |
|---|---|---|
| **Rafael Prieto-Curiel** (Complexity Science Hub Viena; ex-C5 CDMX) | Escalamiento urbano, violencia, movilidad; premio Falling Walls 2024 | El más cercano en agenda. Dos piezas directamente relevantes: (a) *Urban mobility enables deprivation bubble breaking in Indian and Mexican cities* (arXiv:2603.29782) — privación medida por satélite + movilidad celular en 64 ciudades; su noción de "burbuja de privación" es la versión intra-urbana del régimen LISA AA de este repo; (b) *Scaling and Population Loss in Mexican Urban Centres* (2025). Además su trabajo sobre sprawl y acceso a agua/saneamiento toca `sin_agua`/`car_servbas` desde morfología urbana |
| **Carlos Gershenson** (UNAM/IIMAS, ahora Binghamton) | Sistemas complejos, autoorganización, redes | Metodología más que desigualdad; el puente institucional es el C3/LNCC |
| **José Lobo** (ASU) | Urban scaling (con Bettencourt/West), productividad urbana | La literatura de scaling predice que los indicadores per cápita escalan con tamaño de ciudad — el cofactor `log_pob` de la Vista D es exactamente el control que esa literatura exige; una lectura scaling de las cargas (¿qué indicadores son superlineales en población?) sería novedosa aquí |
| **CentroGeo / C3 UNAM** | Geocomputación, análisis espacial | Comunidad natural para el componente ICAR/LISA |

## 4. La maquinaria oficial (con quién se dialoga de verdad)

- **CONEVAL**: la metodología municipal 2020 la firmaron investigadores académicos (John Scott,
  Guillermo Cejudo, Salomón Nahmad, Cárdenas Elizalde, Bartra, Maldonado). El equipo técnico
  publica bases y programas de réplica — el contraste directo-vs-modelado del reporte DGP es
  publicable como auditoría constructiva de su SAE.
- **CONAPO**: la nota 2020 cita a Somarriba/Pena/Zarzosa (escuela española del DP2). La crítica
  académica al DP2 mexicano existe (Gutiérrez-Pulido y Gama-Hernández 2010, "Limitantes de los
  índices de marginación") pero es pre-DP2; el análisis de este repo la actualiza.
- **John Scott** (CIDE) merece mención doble: consejero CONEVAL *y* autor CEQ sobre incidencia
  del gasto — la persona que conecta la medición con la Vista E fiscal.

## 5. El hueco que este proyecto ocupa

1. **Nadie modela conjuntamente marginación y pobreza municipal** como vistas ruidosas de un
   latente común con efectos de método explícitos. Existen comparaciones descriptivas
   (correlaciones, mapas); no existe el modelo generativo.
2. **La incertidumbre municipal es invisible en ambas mediciones oficiales** (CONEVAL publica
   intervalos, CONAPO no publica ninguno; nadie los propaga a la comparación). El `z_i ± sd` de
   la escalera es la primera cuantificación de *qué tan seguro se puede estar de que un municipio
   es más pobre que marginado*.
3. **La circularidad FAIS** (pobreza medida → dinero → indicadores futuros) está documentada en
   evaluaciones de CONEVAL pero no incorporada como restricción de identificación en ningún
   modelo estadístico del tema.
4. El formato — DGP explícito + escalera de especificaciones + descomposición de varianza — es
   exportable a la comparación IRS (CONEVAL) vs IM (CONAPO), y al eje temporal 2010–2020.

## Fuentes

- [Cortés y Vargas (2011), Estudios Sociológicos](http://www.scielo.org.mx/scielo.php?script=sci_arttext&pid=S0301-70362007000200006) · [CEEY](https://ceey.org.mx/) · [Informe de movilidad social 2025](https://ceey.org.mx/informe-de-movilidad-social-en-mexico-2025/) · [A Land of Unequal Chances](https://ceey.org.mx/a-land-of-unequal-chances-social-mobility-across-mexican-regions/comment-page-1/)
- [CEQ Institute](https://commitmentoequity.org/) · [Publicaciones México](https://commitmentoequity.org/publications-mexico/) · [Nora Lustig](https://noralustig.tulane.edu/)
- [Prieto-Curiel — CSH](https://csh.ac.at/rafael-prieto-curiel/) · [Deprivation bubble breaking (arXiv:2603.29782)](https://arxiv.org/abs/2603.29782) · [Scaling and Population Loss in Mexican Urban Centres](https://arxiv.org/pdf/2509.16110)
- [Campos-Vázquez — RePEc](https://ideas.repec.org/f/pca931.html) · [Gershenson](https://gershenson.mx/) · [C3 UNAM](https://www.c3.unam.mx/)
- CONEVAL, metodología municipal 2020 (consejo académico y equipo técnico en el propio PDF).
