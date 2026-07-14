#!/usr/bin/env python
"""
Nivel 1 (Bloque 1, revisión Paper 1) — error de medición oficial de los indicadores SAE.

HALLAZGO DE ADQUISICIÓN (2026-07-13, documentado con evidencia de búsqueda):
CONEVAL NO publica el error estándar / CV continuo por municipio para la medición
municipal 2020. Lo publicado oficialmente es:
  (a) el anexo estadístico municipal (Concentrado_indicadores_de_pobreza_2020.zip):
      SOLO estimaciones puntuales;
  (b) el paquete de réplica MunEBPH_2020 (Pobreza_municipal_2020_VCOMPL.rar): programas
      Stata/R + insumos, con datos/salidas VACÍO — el ECM se obtiene re-corriendo el EBPH
      completo (100 simulaciones Monte Carlo sobre la muestra ampliada del Censo);
  (c) "Pobreza por grupos poblacionales a escala municipal 2010-2020" (oct. 2022,
      Indicadores_pobreza_grupos_municipal.zip): BANDAS OFICIALES de precisión por
      municipio x indicador x año, basadas en el CV del ECM del propio EBPH:
        con precisión (CV <= 15%), precisión aceptable (15% < CV <= 25%),
        sin precisión (CV > 25%),
      publicadas para 9 subgrupos poblacionales, entre ellos la PARTICIÓN rural/urbano.

Este script construye el se municipal continuo desde (c): CV representativo por banda
(punto medio: 0.10 / 0.20 / 0.35 para la banda abierta), se por subgrupo = CV * p_g,
y combinación a total municipal con pesos de población w_g = N_g/N (independencia entre
subpoblaciones disjuntas): se_pct = sqrt(w_r^2 se_r^2 + w_u^2 se_u^2).

Dos salvaguardas documentadas:
  1. CAP DE FACTIBILIDAD: se_g <= min(p_g, 100-p_g)/1.96. El CV oficial se define sobre
     p-hat, así que en municipios con p ~ 99% la banda es trivialmente poco informativa y
     CV*p implicaría IC fuera de [0,100] (p.ej. Chiapas, lp_ingreso ~ 99%, se "9.9 pp").
     Ningún error estándar compatible con el espacio del parámetro puede exceder ese cap.
  2. IMPUTACIÓN: municipios con banda ❌ y puntual del subgrupo NO publicado (46 casos en
     lp_ingreso, típicamente <3,000 hab.) o ausentes del anexo: CV = 0.35 sobre el puntual
     municipal oficial del Concentrado, con el mismo cap; flag_imputado_<ind> = True.

lp_ingreso_ext no tiene banda propia publicada; se le aplica el CV implícito combinado de
lp_ingreso (mismo modelo EBPH de ingreso; conservador a la baja porque el CV de la línea
extrema es típicamente mayor). Se marca con flag_ext_imputado.

Propagación a la escala del modelo (gllvm_Y = logit estandarizado), delta method:
  Y_j = (logit(p_adj) - m_j) / s_j,  p_adj = (pct + 0.5) / 101   [c = 0.5 verificado]
  dY/dpct = (1/101) / (p_adj (1 - p_adj)) / s_j
  se_Y = se_pct * dY/dpct
donde m_j, s_j = media y sd (ddof=1) del logit sobre los 2,466 municipios CONEVAL-completos
(reconstrucción verificada exacta contra gllvm_Y.parquet, diff = 0.0).

Crudo (FUERA del repo): ~/Downloads/coneval_municipal_2020/
  - Indicadores_pobreza_grupos_municipal.zip
    https://www.coneval.org.mx/Medicion/Documents/Pobreza_municipal/2020/gpos_pob/Indicadores_pobreza_grupos_municipal.zip
  - Concentrado_indicadores_de_pobreza_2020.zip (verificación de puntuales)
    https://www.coneval.org.mx/Medicion/Documents/Pobreza_municipal/2020/Concentrado_indicadores_de_pobreza_2020.zip

Salida: data/processed/sae_se_municipal.parquet (cvegeo 5 dígitos + se_<ind> en escala
gllvm_Y + sepct_<ind> en puntos porcentuales + bandas crudas por subgrupo).

Uso: python scripts/build_sae_se.py [--raw ~/Downloads/coneval_municipal_2020]
"""
import os, argparse
import numpy as np, pandas as pd
import openpyxl

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC = os.path.join(HERE, "data", "processed")

# CV representativo por banda oficial (punto medio; 0.35 para la banda abierta CV>0.25)
CV_BANDA = {"✔": 0.10, "⚠": 0.20, "❌": 0.35}

# orden de bloques en las hojas del anexo de grupos poblacionales (6 cols por indicador:
# pct/flag x 2010/2015/2020, a partir de la col 7). Nombres = columnas de gllvm_Y.
BLOQUES = ["pobreza", "lp_ingreso", "rezago_educ", "car_salud",
           "car_segsoc", "car_vivienda", "car_servbas", "car_alim"]
# los 4 modelados por áreas pequeñas (dict/diccionario_indicadores.csv: MODELADA ENIGH+SAE /
# EBPH-SAE); el resto de CONEVAL es estimación directa de la muestra ampliada censal
SAE = ["car_segsoc", "car_alim", "lp_ingreso", "lp_ingreso_ext"]


def leer_hoja(path_xlsx, hoja):
    """Extrae cvegeo, pob 2020 y (pct2020, banda2020) por bloque de una hoja del anexo."""
    wb = openpyxl.load_workbook(path_xlsx, read_only=True)
    ws = wb[hoja]
    rows = []
    for row in ws.iter_rows(min_row=9, values_only=True):
        cve = row[2]
        if cve is None or not str(cve).strip().isdigit():
            continue
        rec = {"cvegeo": str(cve).zfill(5)}
        pob = row[6]
        rec["pob2020"] = float(pob) if isinstance(pob, (int, float)) else np.nan
        for k, b in enumerate(BLOQUES):
            base = 7 + 6 * k
            pct, flag = row[base + 4], row[base + 5]
            rec[f"{b}_pct"] = float(pct) if isinstance(pct, (int, float)) else np.nan
            rec[f"{b}_flag"] = str(flag) if flag is not None else None
        rows.append(rec)
    wb.close()
    return pd.DataFrame(rows).set_index("cvegeo")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", default=os.path.expanduser("~/Downloads/coneval_municipal_2020"))
    a = ap.parse_args()
    xlsx = os.path.join(a.raw, "Indicadores_pobreza_grupos_municipal.xlsx")
    print("leyendo", xlsx)
    rur, urb = leer_hoja(xlsx, "rural"), leer_hoja(xlsx, "urbano")
    print(f"rural: {len(rur)} municipios | urbano: {len(urb)} municipios")

    # universo: 2,466 CONEVAL-completos (mismo del modelo); puntuales oficiales del repo
    mc = pd.read_parquet(os.path.join(PROC, "municipal_components_2020.parquet"))
    mc["cvegeo"] = mc["cvegeo"].astype(str).str.zfill(5)
    mc = mc[mc["coneval_completo"] == True].set_index("cvegeo")

    idx = mc.index
    out = pd.DataFrame(index=idx)
    diag_pct = {}
    cap = lambda p: np.minimum(p, 100.0 - p) / 1.96      # cap de factibilidad (pp)
    for b in BLOQUES:
        if b == "pobreza":
            continue
        se2 = pd.Series(0.0, index=idx)   # suma de w_g^2 se_g^2
        wtot = pd.Series(0.0, index=idx)  # suma de pesos con dato
        ptot = pd.Series(0.0, index=idx)  # reconstrucción del puntual (verificación)
        for sub in (rur, urb):
            s = sub.reindex(idx)
            cv = s[f"{b}_flag"].map(CV_BANDA)
            ok = s["pob2020"].notna() & s[f"{b}_pct"].notna() & cv.notna()
            w = s["pob2020"].where(ok, 0.0)
            se_g = np.minimum(cv * s[f"{b}_pct"], cap(s[f"{b}_pct"])).where(ok, 0.0)
            se2 = se2 + (w ** 2) * (se_g ** 2)
            wtot = wtot + w
            ptot = ptot + w * s[f"{b}_pct"].where(ok, 0.0)
        valid = wtot > 0
        sepct = pd.Series(np.nan, index=idx)
        sepct[valid] = np.sqrt(se2[valid]) / wtot[valid]
        # imputación: sin banda utilizable en ningún subgrupo -> CV 0.35 sobre el
        # puntual municipal oficial, con el mismo cap
        pofi = mc[f"{b}_pct"].astype(float)
        out[f"flag_imputado_{b}"] = ~valid
        sepct[~valid] = np.minimum(0.35 * pofi[~valid], cap(pofi[~valid]))
        out[f"sepct_{b}"] = sepct
        diag_pct[b] = (ptot[valid] / wtot[valid])
        # bandas crudas para trazabilidad
        out[f"banda_rural_{b}"] = rur.reindex(idx)[f"{b}_flag"]
        out[f"banda_urbano_{b}"] = urb.reindex(idx)[f"{b}_flag"]

    # verificación: el total reconstruido rural+urbano ~ puntual oficial del Concentrado
    for b in ["lp_ingreso", "car_segsoc", "car_alim"]:
        rec = diag_pct[b]
        ofi = mc[f"{b}_pct"].reindex(rec.index)
        r = np.corrcoef(rec.dropna(), ofi[rec.notna()])[0, 1]
        md = float((rec - ofi).abs().median())
        print(f"verificación {b}: corr(reconstruido, oficial) = {r:.4f} | "
              f"mediana |diff| = {md:.2f} pp")

    # lp_ingreso_ext: CV implícito de lp_ingreso aplicado al puntual de la línea extrema
    cv_imp = out["sepct_lp_ingreso"] / mc["lp_ingreso_pct"].replace(0, np.nan)
    p_ext = mc["lp_ingreso_ext_pct"].astype(float)
    out["sepct_lp_ingreso_ext"] = np.minimum(cv_imp * p_ext, cap(p_ext))
    out["flag_ext_imputado"] = True

    # propagación a la escala del modelo: constantes de estandarización EXACTAS
    c = 0.5
    logit = lambda pct: np.log(((pct + c) / (100 + 2 * c)) /
                               (1 - (pct + c) / (100 + 2 * c)))
    inds = [b for b in BLOQUES if b != "pobreza"] + ["lp_ingreso_ext"]
    for b in inds:
        l_full = logit(mc[f"{b}_pct"].astype(float))
        m_j, s_j = l_full.mean(), l_full.std(ddof=1)      # sobre los 2,466 (verificado)
        p_adj = (mc[f"{b}_pct"].astype(float) + c) / (100 + 2 * c)
        dY_dpct = (1.0 / (100 + 2 * c)) / (p_adj * (1 - p_adj)) / s_j
        out[f"se_{b}"] = out[f"sepct_{b}"] * dY_dpct

    out = out.reset_index().rename(columns={"index": "cvegeo"})
    dest = os.path.join(PROC, "sae_se_municipal.parquet")
    out.to_parquet(dest, index=False)

    # resumen
    Ycols = pd.read_parquet(os.path.join(PROC, "gllvm_Y.parquet")).columns
    cov = pd.read_parquet(os.path.join(PROC, "gllvm_covars.parquet"))
    cvs = cov["cvegeo"].astype(str).str.zfill(5)
    sub = out.set_index("cvegeo").reindex(cvs)
    print(f"\n{dest}: {out.shape}")
    print("cobertura y magnitud sobre los 2,455 municipios del modelo "
          "(se en unidades de gllvm_Y, que tiene sd=1):")
    for b in inds:
        s = sub[f"se_{b}"]
        print(f"  se_{b:<15} n_falta={int(s.isna().sum()):>3} | media={s.mean():.3f} | "
              f"p50={s.median():.3f} | p90={s.quantile(.9):.3f} | max={s.max():.3f}")
    lp = np.log10(cov.set_index(cvs)["pob_conapo"]) if "pob_conapo" in cov else None
    if lp is None:
        lp = cov.set_index(cvs)["log_pob"]
    for b in SAE:
        m = sub[f"se_{b}"].notna()
        r = np.corrcoef(sub[f"se_{b}"][m], lp[m])[0, 1]
        print(f"  corr(se_{b}, log_pob) = {r:+.3f}")


if __name__ == "__main__":
    main()
