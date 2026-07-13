# Auditoría de fuentes — Vista G (gobernanza criminal y violencia organizada)

**Regla de la casa (steer maestro):** no se descarga ni se modela antes de auditar; presencia
documentada ≠ control territorial; toda fuente abierta observa `O = R × D` (realidad ×
detección); la ausencia de registro no se codifica como ausencia real. Inventario completo con
27 campos por fuente en `outputs/g_fuentes_crimen.csv` (11 fuentes). Fecha: 2026-07-12.

## Veredictos de la primera pasada

| Fuente | Decisión | Estado de verificación |
|---|---|---|
| **OCVED 2.0** (Osorio) | **core_municipal** | ✅ **Descarga real verificada** (GitHub, xlsx 4 MB): 64,895 eventos **diario-municipales 2000–2018**, columnas `state, mun` (clave municipal), `actor_main/actor_sub` (10 org, ~200 células), lat/lon. ⚠ El sitio anuncia 2019; el archivo llega a 2018-12-31. Metodología Eventus ID, κ=0.70 |
| **ACLED agregado ADMIN1** (export del usuario, en `data/raw`) | **state_context** verificado: semana×estado×tipo, 2018–2026-06, 32/32 estados mapeados; SIN municipio/actores → capa contemporánea nivel 2 |
| **ACLED eventos (municipal)** | core_municipal *pendiente* | Cobertura 2018–presente; codebook y metodología MX/gang públicos; **requiere cuenta gratuita/API key** — pedir al usuario o export manual. ⚠ 2018 es su primer año (ramp-up); verificar universo de violencia criminal cubierto y precisión de localidad ANTES de agregarlo a municipios |
| **BACRIM-2020** (PPD-CIDE) | **state_context** | Presencia/tipología/alianzas/rivalidades de ~150 grupos **por estado** (regla: estatal hasta que el archivo demuestre lo contrario; PPData es plataforma JS — descarga por navegar). Usos: nivel 2 jerárquico, fragmentación estatal, interacciones. NO replicar a municipios |
| **Trejo & Ley (HPCV)** | **political_coercion** | ✅ **DESCARGADO y usado (G5)**: `data/raw/trejo_ley/` (`doi:10.7910/DVN/VIXNNE`). Codebook leído: unidad municipio-año (clave INEGI), panel 2007–2012, 2,018 municipios, CAPAM 311 ataques. Entra rezagado (histórico → outcomes 2020); resultados en `g5_coercion.csv` |
| **CIDE-PPD 2006–2011** | **historical_exposure** | Página oficial verificada + paper JCR 2019 (DOI 10.1177/0022002718817093) que la documenta (agresiones/enfrentamientos/ejecuciones + subbase de combates). Descarga en plataforma por verificar. ⚠ procedencia: disco anónimo con registros oficiales — declararlo siempre |
| **INEGI homicidios** | validation_only | Ya en el repo (2018–2022, ocurrencia+residencia, EB). **Homicidio ≠ crimen organizado**: sin atribución de actor |
| **Gutiérrez-Romero & Iturbe (PAIAMEX)** | candidate_unverified | Publicado (Electoral Studies 2024; arXiv 2407.06733); base 2000–2021 georreferenciada **descrita pero no localizada** en repositorio público → pedir a autoras |
| **MCO (Signoret/Sobrino et al.)** | candidate_unverified | Proyecto de 6 autores (~2,500 municipios anual, 2000–2018 afirmado); plataforma prometida **en futuro desde 2019**, descarga no localizada → email a autores |
| **Panel DDSS-Osorio 1990–2020** | candidate_unverified | El 403 de Princeton corresponde al panel **en construcción** de Osorio (extensión de OCVED); usar OCVED 2.0 publicado mientras tanto |
| **Alcocer (Guanajuato)** | candidate_unverified | Datos finos monopolio-vs-competencia pero de **un solo estado**; JMP + JCR 2026. Rol posible: validación conceptual, no fuente nacional |
| **Data Cívica (violencia político-electoral)** | candidate_unverified | Por auditar producto/codebook/años; no mezclar violencia política con atribución OC confirmada |
| **Narcoblogs (genérico)** | validation_only | Solo con diccionario de actores + desambiguación + réplica; nunca fuente principal |

## Implicaciones para el diseño (antes de escribir pipeline)

1. **La ventana pre-2020 limpia (2018–2019) queda partida**: OCVED cubre 2018 (termina ahí);
   ACLED cubre 2018–2019 pero con ramp-up de primer año y requiere cuenta. Diseño honesto:
   exposición histórica larga (OCVED 2000–2018 + CIDE-PPD 2006–2011, correlacionables entre
   sí como validación cruzada) + exposición contemporánea ACLED (2018–2022) con proxies de
   cobertura SIEMPRE al lado.
2. **Competencia municipal medible ya**: con OCVED, `N_i` = actores distintos por municipio
   (actor_main/sub), `C_i = 1(N_i≥2)`, fragmentación F_i con pesos de eventos — para la
   ventana histórica. Para 2020 contemporáneo, hasta tener ACLED.
3. **BACRIM entra solo como nivel estatal** (fragmentación, rivalidades) en el modelo
   jerárquico 7.2 del steer — jamás como efecto principal junto a FE estatales.
4. **Bloqueo actual**: ACLED necesita credencial (`ACLED_EMAIL`/`ACLED_KEY`) — pedir al
   usuario; PPData requiere navegación manual o headless para BACRIM y CIDE-PPD.

## Próximo paso (Fase 1 mínima, según steer)

Con lo YA verificado y descargable sin credenciales: OCVED municipal (hecho el download de
auditoría) + BACRIM estatal (pendiente PPData) + homicidios existentes + proxies de cobertura
(log_pob, urbano, internet — pendiente ITER/censo, distancia a capital estatal — calculable).
No se promueve nada a la tabla maestra hasta pasar sensibilidad de cobertura, temporalidad y
especificación espacial.
