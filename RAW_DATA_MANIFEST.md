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

### Finanzas públicas 2020 (Vista E — cofactores fiscales)
- EFIPEM estatal (CSV abiertos): https://www.inegi.org.mx/contenidos/programas/finanzas/datosabiertos/efipem_estatal_csv.zip
- EFIPEM municipal (109 MB): https://www.inegi.org.mx/contenidos/programas/finanzas/datosabiertos/efipem_municipal_csv.zip
  - Cobertura 2020: 2,250/2,469 municipios (91%). El faltante NO es aleatorio: se concentra por
    estado (Puebla 139, Chiapas 33, Oaxaca 24, las 16 alcaldías de CDMX). CDMX tampoco reportó
    el nivel estatal 2020 (gasto NaN en `estatales_2020.csv`).
- PIBE 2020 preliminar (base 2013): boletín INEGI dic. 2021
  https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2021/pibe/PIBEntFed2020.pdf
  (11 entidades con monto exacto; resto reconstruido de la estructura porcentual, flag `pibe_aprox`).
- Constructor: `scripts/build_finanzas_2020.py <dir_con_zips_extraidos>` → `estatales_2020.csv`,
  `finanzas_mun_2020.parquet`.
- **Advertencia de circularidad**: las aportaciones municipales contienen FAIS, asignado por la
  fórmula del art. 34 LCF sobre pobreza extrema CONEVAL → NO usar como cofactor del latente
  (ver `reports/reporte_dgp_dag.md`, dependencia 5).

### Defunciones registradas 2019–2021 (validación externa: homicidios)
- Espejo abierto (CSV por año, 160–240 MB): `https://repodatos.atdt.gob.mx/all_data/secretaria_salud/6fecbbb3-afd9-44a1-8665-679a80ce4a15/defunciones_registradas_{2019,2020,2021}.csv`
  (los zips de inegi.org.mx/programas/edr rechazan descargas no-navegador).
- Homicidio: `PRESUNTO == 2` (≡ ICD-10 X85–Y09 al 99.99%); municipio de OCURRENCIA
  (`ENT_OCURR`+`MUN_OCURR`, excluyendo claves ≥900). Totales validados contra boletines INEGI.
- Constructor: `scripts/validacion_homicidios.py <dir>` → `homicidios_mun_2019_2021.parquet`.

## Tooling para ampliar indicadores
- `~/code/inegi-client` (repo local): cliente de la API de Indicadores INEGI/BISE, DENUE y Marco
  Geoestadístico, con backfill a DuckDB. Requiere `INEGI_TOKEN` (env var). Pendientes naturales:
  PIBE exacto por entidad (reemplaza la reconstrucción porcentual de `estatales_2020.csv`),
  densidad de amenidades DENUE (cofactor municipal, Vista F), geojson para mapas de scores.

## Nota de reproducibilidad
- CVEGEO = clave de 5 dígitos (2 entidad + 3 municipio). Llave de cruce validada: CONAPO ∩ CONEVAL = 2,469 municipios, 0 huérfanos.
- Indicadores en porcentaje transformados con logit tras corrección de continuidad: `p = (y + c)/(100 + 2c)`.

### Vista F — lentes satelitales (2026-07-12)
- NTL: NPP-VIIRS-like v2 anual 2020, 500 m (Chen et al.), Harvard Dataverse doi:10.7910/DVN/YGIVCD,
  archivo `2020_Version2.zip` (id 13295279; EOG VNL v2.1 requiere OAuth — por eso el espejo).
  Recortado a bbox MX antes de zonal stats (global = 10 GB).
- DEM: GMTED2010 media 30 arcseg, tiles USGS `10N120W`, `10N090W`, `30N120W`
  (⚠ el nombre del tile es la esquina INFERIOR-izquierda). TRI (Riley 1999) calculado en
  `scripts/build_vistaF.py`.
- Accesibilidad: distancia (EPSG:6372) del centroide municipal a la localidad ≥50k más cercana,
  232 ciudades del ITER 2020 local (lat/lon DMS parseadas). Upgrade opcional: raster Malaria Atlas.
- ⚠ BUG DE CLAVE: `cvegeo` se lee como int64 desde los zscores CSV (pierde el cero inicial);
  SIEMPRE `astype(str).str.zfill(5)` antes de cualquier join (asserts en los scripts).

### Vista G — crimen organizado (Fase 1, 2026-07-12)
- OCVED 2.0 (Osorio): https://github.com/javierosorio/OCVED_2.0 (OCVED_2.0.xlsx, 4 MB).
  64,895 eventos diario-municipales 2000–2018 (⚠ el sitio anuncia 2019; el archivo termina
  2018-12-31), actor_main/actor_sub, lat/lon, clave municipal (match 100% con la base).
  Metodología Eventus ID (κ=0.70). Constructor: `scripts/build_vistaG.py <scratch>`.
- ⚠ O = R × D: eventos documentados, NO censo ni control territorial; sin-registro ≠ ausencia.
  Proxies de observabilidad en la misma tabla (internet_pct del ITER, dist_capital_km, etc.).
- ACLED (2018+): REQUIERE cuenta gratuita — variables `ACLED_EMAIL`/`ACLED_KEY` pendientes.
- Auditoría completa de 12 fuentes: `reports/auditoria_fuentes_crimen.md` + `outputs/g_fuentes_crimen.csv`.
- ACLED agregado ADMIN1 (export de usuario 2026-06-27): `data/raw/acled_agregado_admin1_lac.xlsx`
  → `scripts/build_vistaG_estatal.py` → `vistaG_crimen_estatal.parquet` (estado-año 2018-2026,
  violencia política, fatalidades, batallas). ESTATAL: no sustituye el export de eventos.
