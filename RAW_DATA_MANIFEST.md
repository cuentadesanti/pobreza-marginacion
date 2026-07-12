# Manifiesto de datos crudos

Los insumos grandes NO se versionan en el repo (tamaño). Descárgalos a `data/raw/` con estas URLs.

## Incluidos en el repo (`data/raw/`)
- `iter_2020.zip` (36.6 MB) — INEGI Censo 2020, Iterador (ITER) nacional.
  https://www.inegi.org.mx/contenidos/programas/ccpv/2020/datosabiertos/iter/iter_00_cpv2020_csv.zip
- `banxico_ce166.xls` (105 KB) — export directo del cuadro CE166 (solo trimestres recientes; los datos 2020 se bajaron vía API SIE).

## NO incluidos (grandes — descargar aparte)

### Censo 2020 — Cuestionario ampliado (microdatos)
- Archivo: `Censo2020_CA_eum_csv.zip` (486 MB, compresión **Deflate64** — usar `unzip`/`ditto` del sistema, no zipfile de Python).
- URL: https://www.inegi.org.mx/contenidos/programas/ccpv/2020/microdatos/Censo2020_CA_eum_csv.zip
- Uso: `Personas00.CSV` (3.3 GB, 15 M registros). Columnas usadas (por posición): 1=ENT, 2=MUN, 9=FACTOR (expansión), 61=CONACT, 62=OCUPACION_C, 63=SITTRA, 71=INGTRMEN, 73=ACTIVIDADES_C (SCIAN 4 díg).
- Derivados → `vistaD_v1.parquet`: mezcla sectorial ponderada (primario/secundario/terciario) y `empleo_precario_pct` (proxy de informalidad).

### Remesas municipales 2020 (Banxico SIE API)
- Cuadro CE166, ~2,456 series municipales (formato `SE#####`), 2020 completo (4 trimestres, millones USD, flujo).
- Endpoint: `https://www.banxico.org.mx/SieAPIRest/service/v1/series/{IDs}/datos/2020-01-01/2020-12-31`
- Requiere token SIE gratuito en header `Bmx-Token` (obtener en el portal de Banxico; NO se incluye en el repo).
- Crosswalk serie↔CVEGEO ya resuelto en `data/processed/crosswalk_banxico_cvegeo.csv`.
- Validación: suma municipal 2020 = 41,676 MUSD = 103% del total nacional oficial.

### Geometrías municipales
- Marco Geoestadístico INEGI 2020 (usado para el grafo de contigüidad Queen → `spatial/icar_edges.npz`).

## Nota de reproducibilidad
- CVEGEO = clave de 5 dígitos (2 entidad + 3 municipio). Llave de cruce validada: CONAPO ∩ CONEVAL = 2,469 municipios, 0 huérfanos.
- Indicadores en porcentaje transformados con logit tras corrección de continuidad: `p = (y + c)/(100 + 2c)`.
